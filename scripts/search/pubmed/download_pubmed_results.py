#!/usr/bin/env python3
"""
PubMed検索結果ダウンロードスクリプト

検索式を実行し、抄録を含む全文献をRIS形式でダウンロードします。
ファイル名は「日付_件数_pubmed.ris」形式で保存されます。

Usage:
    python scripts/search/pubmed/download_pubmed_results.py --formula-file projects/fd_review/search_formula.md --output-dir projects/fd_review/pubmed_results
"""

import requests
import time
import argparse
import os
import re
from datetime import datetime
from typing import Dict, List, Tuple, Any


def get_pubmed_results(query: str, retmax: int = 100000) -> Dict[str, Any]:
    """
    PubMed E-utilities APIを使用して検索クエリの結果件数とPMIDを取得する
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    params = {
        'db': 'pubmed',
        'term': query,
        'retmax': retmax,
        'retmode': 'json',
        'usehistory': 'y'
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        result = data.get('esearchresult', {})
        count = int(result.get('count', 0))
        pmids = result.get('idlist', [])
        webenv = result.get('webenv', '')
        query_key = result.get('querykey', '')
        
        return {
            'count': count,
            'pmids': pmids,
            'webenv': webenv,
            'query_key': query_key
        }
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        return {'count': 0, 'pmids': [], 'webenv': '', 'query_key': ''}


def fetch_pubmed_records(webenv: str, query_key: str, total: int, batch_size: int = 200) -> str:
    """
    WebEnvとQueryKeyを使って全レコードをMEDLINE形式で取得する
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    all_records = []
    
    for start in range(0, total, batch_size):
        print(f"  Fetching records {start + 1} - {min(start + batch_size, total)} of {total}...")
        
        params = {
            'db': 'pubmed',
            'query_key': query_key,
            'WebEnv': webenv,
            'retstart': start,
            'retmax': batch_size,
            'rettype': 'medline',
            'retmode': 'text'
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            all_records.append(response.text)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching batch starting at {start}: {str(e)}")
        
        # API制限を考慮して待機
        time.sleep(0.4)
    
    return '\n'.join(all_records)


def convert_medline_to_ris(medline_data: str) -> str:
    """
    MEDLINEフォーマットをRISフォーマットに変換する（抄録含む）
    """
    ris_output = []
    
    # レコードを分割
    records = re.split(r'\n(?=PMID-)', medline_data)
    
    for record in records:
        if not record.strip():
            continue
        
        ris_entry = ['TY  - JOUR']
        
        # フィールドをパース
        current_field = None
        current_value = []
        
        lines = record.split('\n')
        for line in lines:
            # 新しいフィールドの開始を検出
            if len(line) >= 4 and line[4:6] == '- ':
                # 前のフィールドを処理
                if current_field:
                    value = ' '.join(current_value).strip()
                    ris_line = convert_field_to_ris(current_field, value)
                    if ris_line:
                        ris_entry.extend(ris_line if isinstance(ris_line, list) else [ris_line])
                
                current_field = line[:4].strip()
                current_value = [line[6:]]
            elif line.startswith('      '):
                # 継続行
                current_value.append(line.strip())
            elif line.strip() and current_field:
                current_value.append(line.strip())
        
        # 最後のフィールドを処理
        if current_field:
            value = ' '.join(current_value).strip()
            ris_line = convert_field_to_ris(current_field, value)
            if ris_line:
                ris_entry.extend(ris_line if isinstance(ris_line, list) else [ris_line])
        
        ris_entry.append('ER  -')
        ris_entry.append('')
        
        ris_output.append('\n'.join(ris_entry))
    
    return '\n'.join(ris_output)


def convert_field_to_ris(field: str, value: str) -> List[str] | str | None:
    """
    MEDLINEフィールドをRISフィールドに変換する
    """
    field_mapping = {
        'PMID': 'ID',
        'TI': 'T1',
        'AB': 'AB',   # 抄録
        'AU': 'AU',   # 著者
        'FAU': 'A1',  # フル著者名
        'JT': 'JF',   # ジャーナル名
        'TA': 'JA',   # 略誌名
        'DP': 'Y1',   # 発行日
        'VI': 'VL',   # 巻
        'IP': 'IS',   # 号
        'PG': 'SP',   # ページ
        'LID': 'DO',  # DOI (10.xxx形式のみ)
        'MH': 'KW',   # MeSH用語
        'OT': 'KW',   # その他のキーワード
        'PT': 'M3',   # 出版タイプ
        'LA': 'LA',   # 言語
    }
    
    if field not in field_mapping:
        return None
    
    ris_field = field_mapping[field]
    
    # DOIの場合は10.で始まるもののみ
    if field == 'LID':
        if '[doi]' in value:
            doi = value.replace('[doi]', '').strip()
            return f'{ris_field}  - {doi}'
        return None
    
    # 著者フィールドは複数行になる可能性がある
    if field in ['AU', 'FAU', 'MH', 'OT']:
        return f'{ris_field}  - {value}'
    
    return f'{ris_field}  - {value}'


def parse_search_formula_md(file_path: str) -> Tuple[Dict[str, str], str]:
    """
    search_formula.mdファイルを解析して、各行のクエリと最終クエリを取得する。
    """
    line_queries = {}
    final_query_structure = None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # PubMed/MEDLINEセクションを探す
        pubmed_section = re.search(
            r'## PubMed/MEDLINE.*?```\s*(.*?)```',
            content,
            re.DOTALL | re.IGNORECASE
        )
        
        if pubmed_section:
            formula_block = pubmed_section.group(1).strip()
            
            for line in formula_block.split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                # #1, #2, #3 などの行を検出
                match = re.match(r'^#(\d+)\s+(.+)$', line)
                if match:
                    line_num = match.group(1)
                    query = match.group(2).strip()
                    
                    # #1 AND #2 のような参照のみの行を最終クエリとして扱う
                    if re.match(r'^#\d+(\s+AND\s+#\d+)+$', query):
                        final_query_structure = query
                    else:
                        line_queries[line_num] = query
        
        return line_queries, final_query_structure
        
    except Exception as e:
        print(f"Error parsing search formula: {str(e)}")
        return {}, None


def build_final_query(structure: str, line_queries: Dict[str, str]) -> str:
    """
    最終クエリの構造と各行のクエリから最終的な検索式を構築する。
    """
    def replace_line_num(match):
        line_num = match.group(1)
        return f"({line_queries.get(line_num, '')})"
    
    return re.sub(r'#(\d+)', replace_line_num, structure)


def main():
    parser = argparse.ArgumentParser(
        description="PubMed検索結果をRIS形式でダウンロードします。抄録を含む全文献情報を取得します。"
    )
    parser.add_argument(
        "--formula-file",
        type=str,
        required=True,
        help="検索式が記述されたMarkdownファイルのパス"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="RISファイルの出力先ディレクトリ"
    )
    parser.add_argument(
        "--database-name",
        type=str,
        default="pubmed",
        help="データベース名（ファイル名に使用、デフォルト: pubmed）"
    )
    args = parser.parse_args()

    # 出力ディレクトリの確認・作成
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # 検索式の解析と構築
    print(f"\n{'='*60}")
    print("PubMed Search Results Download")
    print(f"{'='*60}")
    
    line_queries, final_query_structure = parse_search_formula_md(args.formula_file)
    if not final_query_structure:
        print(f"Error: 検索式ファイルから最終検索構造を特定できませんでした: {args.formula_file}")
        return 1
        
    final_query = build_final_query(final_query_structure, line_queries)

    print(f"Formula file: {args.formula_file}")
    print(f"Final query: {final_query}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    # 検索実行
    print("Executing search...")
    result = get_pubmed_results(final_query, retmax=0)
    total_count = result['count']
    
    print(f"Total results: {total_count:,}")
    
    if total_count == 0:
        print("No results found.")
        return 0
    
    # WebEnvを使って再検索（全件取得用）
    print("\nRetrieving all records with abstracts...")
    result = get_pubmed_results(final_query, retmax=total_count)
    
    if not result['webenv']:
        print("Error: Could not obtain WebEnv for batch download.")
        return 1
    
    # 全レコードを取得
    medline_data = fetch_pubmed_records(
        result['webenv'],
        result['query_key'],
        total_count
    )
    
    # RIS形式に変換
    print("\nConverting to RIS format...")
    ris_data = convert_medline_to_ris(medline_data)
    
    # ファイル名を生成: 日付_件数_データベース.ris
    date_str = datetime.now().strftime('%Y%m%d')
    filename = f"{date_str}_{total_count}_{args.database_name}.ris"
    filepath = os.path.join(args.output_dir, filename)
    
    # ファイルに保存
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(ris_data)
    
    print(f"\n{'='*60}")
    print(f"✅ Download complete!")
    print(f"   File: {filepath}")
    print(f"   Records: {total_count:,}")
    print(f"{'='*60}")
    
    return 0


if __name__ == "__main__":
    exit(main())
