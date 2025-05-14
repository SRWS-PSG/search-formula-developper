#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import re
import requests
import time
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional

def parse_search_formula(file_path: str) -> Dict[str, List[str]]:
    """
    検索式ファイル（MD形式）からMeSH用語とキーワードを抽出する
    
    Args:
        file_path: 検索式ファイルのパス
        
    Returns:
        Dict: {
            'mesh_p': [MeSH用語（P）のリスト],
            'mesh_i': [MeSH用語（I）のリスト],
            'keyword_p': [キーワード（P）のリスト],
            'keyword_i': [キーワード（I）のリスト],
        }
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 結果を格納する辞書
    terms = {
        'mesh_p': [],
        'mesh_i': [],
        'keyword_p': [],
        'keyword_i': []
    }
    
    # MeSH用語（P）の抽出
    mesh_p_match = re.search(r'統制語\s*\(P.*?\).*?\[(MeSH|mh)\].*?\((.*?)\)', content, re.DOTALL)
    if mesh_p_match:
        mesh_p_block = mesh_p_match.group(2)
        # 各MeSH用語を抽出
        mesh_p_terms = re.findall(r'\(\s*"([^"]+)"\s*\[\s*(?:MeSH|mh)\s*\]\s*\)', mesh_p_block)
        terms['mesh_p'] = mesh_p_terms
    
    # フリーワード（P）の抽出
    keyword_p_match = re.search(r'フリーワード\s*\(P.*?\).*?\[tiab\](.*?)\((?:\(|"統制語|$)', content, re.DOTALL)
    if keyword_p_match:
        keyword_p_block = keyword_p_match.group(1)
        # 各キーワードを抽出
        keyword_p_terms = re.findall(r'\(\s*"([^"]+)"\s*\[\s*tiab\s*\]\s*\)', keyword_p_block)
        terms['keyword_p'] = keyword_p_terms
    
    # MeSH用語（I）の抽出
    mesh_i_match = re.search(r'統制語\s*\(\s*I.*?\).*?\[(MeSH|mh)\].*?\((.*?)\)', content, re.DOTALL)
    if mesh_i_match:
        mesh_i_block = mesh_i_match.group(2)
        # 各MeSH用語を抽出
        mesh_i_terms = re.findall(r'\(\s*"([^"]+)"\s*\[\s*(?:MeSH|mh)\s*\]\s*\)', mesh_i_block)
        terms['mesh_i'] = mesh_i_terms
    
    # フリーワード（I）の抽出
    keyword_i_match = re.search(r'フリーワード\s*\(\s*I.*?\).*?\[tiab\](.*?)(?:\Z|\(#|\n#)', content, re.DOTALL)
    if keyword_i_match:
        keyword_i_block = keyword_i_match.group(1)
        # 各キーワードを抽出
        keyword_i_terms = re.findall(r'\(\s*"([^"]+)"\s*\[\s*tiab\s*\]\s*\)', keyword_i_block)
        terms['keyword_i'] = keyword_i_terms
    
    return terms

def extract_pmids_from_file(file_path: str) -> List[str]:
    """
    ファイルから組入論文のPMIDを抽出する
    
    Args:
        file_path: ファイルパス
    
    Returns:
        List[str]: PMIDのリスト
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # PMID抽出（PMID: 数字形式）
    pmids = re.findall(r'PMID:\s*(\d+)', content)
    
    return pmids

def check_pubmed_term(term: str, field: str) -> Dict:
    """
    PubMed E-utilities APIを使用して検索用語の検索結果件数を取得する
    
    Args:
        term: 検索用語
        field: フィールドタグ（例: [Mesh], [tiab]）
        
    Returns:
        Dict: {
            'term': str,
            'field': str,
            'count': int,
            'message': str
        }
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    search_url = f"{base_url}/esearch.fcgi"
    
    # 検索クエリの構築
    query = f'"{term}"{field}'
    
    params = {
        'db': 'pubmed',
        'term': query,
        'retmode': 'json'
    }
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        count = int(data['esearchresult'].get('count', 0))
        
        return {
            'term': term,
            'field': field,
            'count': count,
            'query': query,
            'message': 'Success'
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'term': term,
            'field': field,
            'count': 0,
            'query': query,
            'message': f'Error: {str(e)}'
        }

def check_pmid_with_term(pmid: str, term: str, field: str) -> Dict:
    """
    指定されたPMIDの論文が特定の検索用語にマッチするか確認する
    
    Args:
        pmid: PMID
        term: 検索用語
        field: フィールドタグ（例: [Mesh], [tiab]）
    
    Returns:
        Dict: {
            'pmid': str,
            'term': str,
            'field': str,
            'matches': bool,
            'message': str
        }
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    search_url = f"{base_url}/esearch.fcgi"
    
    # 検索クエリの構築
    query = f'{pmid}[uid] AND "{term}"{field}'
    
    params = {
        'db': 'pubmed',
        'term': query,
        'retmode': 'json'
    }
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        count = int(data['esearchresult'].get('count', 0))
        matches = count > 0
        
        return {
            'pmid': pmid,
            'term': term,
            'field': field,
            'matches': matches,
            'query': query,
            'message': 'Success'
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'pmid': pmid,
            'term': term,
            'field': field,
            'matches': False,
            'query': query,
            'message': f'Error: {str(e)}'
        }

def ensure_directory_exists(path: str) -> None:
    """
    ディレクトリが存在しない場合は作成する
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description='検索用語の検索件数を確認するスクリプト')
    parser.add_argument('--input', required=True, help='検索式ファイルのパス')
    parser.add_argument('--output', help='出力ファイルのパス（指定しない場合はlogs/validation/に保存）')
    
    args = parser.parse_args()
    input_file = args.input
    
    if args.output:
        output_file = args.output
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"logs/validation/term_check_{timestamp}.log"
    
    # 出力ディレクトリの確保
    ensure_directory_exists(output_file)
    
    # 検索式の解析
    terms = parse_search_formula(input_file)
    
    # 組入論文のPMID抽出
    pmids = extract_pmids_from_file(input_file)
    
    # 結果を格納するリスト
    results = {
        'mesh_p': [],
        'mesh_i': [],
        'keyword_p': [],
        'keyword_i': [],
        'pmid_analysis': {}
    }
    
    # MeSH用語（P）の検索件数確認
    print("\n=== Population MeSH用語の検索件数確認中... ===")
    for term in terms['mesh_p']:
        print(f"\n用語: {term}[Mesh]")
        time.sleep(1)  # API制限を考慮
        result = check_pubmed_term(term, "[Mesh]")
        print(f"検索結果: {result['count']:,}件")
        results['mesh_p'].append(result)
    
    # MeSH用語（I）の検索件数確認
    print("\n=== Intervention MeSH用語の検索件数確認中... ===")
    for term in terms['mesh_i']:
        print(f"\n用語: {term}[Mesh]")
        time.sleep(1)
        result = check_pubmed_term(term, "[Mesh]")
        print(f"検索結果: {result['count']:,}件")
        results['mesh_i'].append(result)
    
    # キーワード（P）の検索件数確認
    print("\n=== Population キーワードの検索件数確認中... ===")
    for term in terms['keyword_p']:
        print(f"\n用語: {term}[tiab]")
        time.sleep(1)
        result = check_pubmed_term(term, "[tiab]")
        print(f"検索結果: {result['count']:,}件")
        results['keyword_p'].append(result)
    
    # キーワード（I）の検索件数確認
    print("\n=== Intervention キーワードの検索件数確認中... ===")
    for term in terms['keyword_i']:
        print(f"\n用語: {term}[tiab]")
        time.sleep(1)
        result = check_pubmed_term(term, "[tiab]")
        print(f"検索結果: {result['count']:,}件")
        results['keyword_i'].append(result)
    
    # 組入論文と検索用語のマッチング分析
    if pmids:
        print("\n=== 組入論文と検索用語のマッチング分析... ===")
        
        for pmid in pmids:
            print(f"\nPMID: {pmid}の分析")
            results['pmid_analysis'][pmid] = {
                'mesh_p': [],
                'mesh_i': [],
                'keyword_p': [],
                'keyword_i': []
            }
            
            # MeSH用語（P）とのマッチング
            for term in terms['mesh_p']:
                time.sleep(1)
                result = check_pmid_with_term(pmid, term, "[Mesh]")
                match_status = "○" if result['matches'] else "×"
                print(f"{match_status} {term}[Mesh]")
                results['pmid_analysis'][pmid]['mesh_p'].append(result)
            
            # MeSH用語（I）とのマッチング
            for term in terms['mesh_i']:
                time.sleep(1)
                result = check_pmid_with_term(pmid, term, "[Mesh]")
                match_status = "○" if result['matches'] else "×"
                print(f"{match_status} {term}[Mesh]")
                results['pmid_analysis'][pmid]['mesh_i'].append(result)
            
            # キーワード（P）とのマッチング
            for term in terms['keyword_p']:
                time.sleep(1)
                result = check_pmid_with_term(pmid, term, "[tiab]")
                match_status = "○" if result['matches'] else "×"
                print(f"{match_status} {term}[tiab]")
                results['pmid_analysis'][pmid]['keyword_p'].append(result)
            
            # キーワード（I）とのマッチング
            for term in terms['keyword_i']:
                time.sleep(1)
                result = check_pmid_with_term(pmid, term, "[tiab]")
                match_status = "○" if result['matches'] else "×"
                print(f"{match_status} {term}[tiab]")
                results['pmid_analysis'][pmid]['keyword_i'].append(result)
    
    # 結果のログファイル生成
    with open(output_file, 'w', encoding='utf-8') as f:
        # ヘッダー
        f.write(f"# 検索用語検証レポート\n")
        f.write(f"日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"入力ファイル: {input_file}\n\n")
        
        # Population MeSH用語
        f.write("## Population MeSH用語の検索件数\n\n")
        for result in results['mesh_p']:
            f.write(f"- 用語: {result['term']}[Mesh]\n")
            f.write(f"  - 検索結果: {result['count']:,}件\n")
            f.write(f"  - クエリ: {result['query']}\n")
        
        # Intervention MeSH用語
        f.write("\n## Intervention MeSH用語の検索件数\n\n")
        for result in results['mesh_i']:
            f.write(f"- 用語: {result['term']}[Mesh]\n")
            f.write(f"  - 検索結果: {result['count']:,}件\n")
            f.write(f"  - クエリ: {result['query']}\n")
        
        # Population キーワード
        f.write("\n## Population キーワードの検索件数\n\n")
        for result in results['keyword_p']:
            f.write(f"- 用語: {result['term']}[tiab]\n")
            f.write(f"  - 検索結果: {result['count']:,}件\n")
            f.write(f"  - クエリ: {result['query']}\n")
        
        # Intervention キーワード
        f.write("\n## Intervention キーワードの検索件数\n\n")
        for result in results['keyword_i']:
            f.write(f"- 用語: {result['term']}[tiab]\n")
            f.write(f"  - 検索結果: {result['count']:,}件\n")
            f.write(f"  - クエリ: {result['query']}\n")
        
        # 組入論文と検索用語のマッチング分析
        if pmids:
            f.write("\n## 組入論文と検索用語のマッチング分析\n\n")
            
            for pmid, analysis in results['pmid_analysis'].items():
                f.write(f"### PMID: {pmid}\n\n")
                
                # Population MeSH用語
                f.write("#### Population MeSH用語とのマッチング\n\n")
                for result in analysis['mesh_p']:
                    match_status = "○" if result['matches'] else "×"
                    f.write(f"- {match_status} {result['term']}[Mesh]\n")
                
                # Intervention MeSH用語
                f.write("\n#### Intervention MeSH用語とのマッチング\n\n")
                for result in analysis['mesh_i']:
                    match_status = "○" if result['matches'] else "×"
                    f.write(f"- {match_status} {result['term']}[Mesh]\n")
                
                # Population キーワード
                f.write("\n#### Population キーワードとのマッチング\n\n")
                for result in analysis['keyword_p']:
                    match_status = "○" if result['matches'] else "×"
                    f.write(f"- {match_status} {result['term']}[tiab]\n")
                
                # Intervention キーワード
                f.write("\n#### Intervention キーワードとのマッチング\n\n")
                for result in analysis['keyword_i']:
                    match_status = "○" if result['matches'] else "×"
                    f.write(f"- {match_status} {result['term']}[tiab]\n")
        
        # 要約
        f.write("\n## 検索結果要約\n\n")
        
        # 検索件数が0または少ない（<10）用語のリスト
        low_count_terms = []
        for category, results_list in [
            ("Population MeSH", results['mesh_p']),
            ("Intervention MeSH", results['mesh_i']),
            ("Population キーワード", results['keyword_p']),
            ("Intervention キーワード", results['keyword_i'])
        ]:
            for result in results_list:
                if result['count'] == 0:
                    low_count_terms.append((category, result['term'], result['count'], "検索結果なし"))
                elif result['count'] < 10:
                    low_count_terms.append((category, result['term'], result['count'], "検索結果が少ない"))
        
        if low_count_terms:
            f.write("### 注意が必要な検索用語\n\n")
            for category, term, count, note in low_count_terms:
                f.write(f"- [{category}] {term}: {count:,}件 - {note}\n")
        
        # 組入論文のマッチング状況
        if pmids:
            f.write("\n### 組入論文のマッチング状況\n\n")
            
            for pmid, analysis in results['pmid_analysis'].items():
                # 各カテゴリでのマッチ数をカウント
                match_counts = {
                    'mesh_p': sum(1 for r in analysis['mesh_p'] if r['matches']),
                    'mesh_i': sum(1 for r in analysis['mesh_i'] if r['matches']),
                    'keyword_p': sum(1 for r in analysis['keyword_p'] if r['matches']),
                    'keyword_i': sum(1 for r in analysis['keyword_i'] if r['matches'])
                }
                
                total_matches = sum(match_counts.values())
                
                if total_matches == 0:
                    status = "⚠️ マッチする用語がありません（検索式で捕捉できない可能性）"
                elif match_counts['mesh_p'] == 0 and match_counts['keyword_p'] == 0:
                    status = "⚠️ Population条件にマッチしません"
                elif match_counts['mesh_i'] == 0 and match_counts['keyword_i'] == 0:
                    status = "⚠️ Intervention条件にマッチしません"
                else:
                    status = "✅ 検索式でカバーされる可能性あり"
                
                f.write(f"- PMID: {pmid}\n")
                f.write(f"  - Population MeSH: {match_counts['mesh_p']}/{len(analysis['mesh_p'])}個マッチ\n")
                f.write(f"  - Intervention MeSH: {match_counts['mesh_i']}/{len(analysis['mesh_i'])}個マッチ\n")
                f.write(f"  - Population キーワード: {match_counts['keyword_p']}/{len(analysis['keyword_p'])}個マッチ\n")
                f.write(f"  - Intervention キーワード: {match_counts['keyword_i']}/{len(analysis['keyword_i'])}個マッチ\n")
                f.write(f"  - 状態: {status}\n")
    
    print(f"\n検証結果を {output_file} に保存しました。")

if __name__ == "__main__":
    main()
