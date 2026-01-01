import requests
import time
from typing import Dict, List, Tuple
import argparse
import os
import re
from datetime import datetime

def get_pubmed_results(query: str, retmax: int = 100000) -> Dict:
    """
    PubMed E-utilities APIを使用して検索クエリの結果件数とPMIDを取得する
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    search_url = f"{base_url}/esearch.fcgi"

    params = {
        'db': 'pubmed',
        'term': query,
        'retmode': 'json',
        'retmax': retmax,
        'usehistory': 'y'
    }

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()

        return {
            'count': int(data['esearchresult'].get('count', 0)),
            'ids': data['esearchresult'].get('idlist', []),
            'query': query,
            'message': 'Success',
            'webenv': data['esearchresult'].get('webenv', ''),
            'querykey': data['esearchresult'].get('querykey', '')
        }

    except requests.exceptions.RequestException as e:
        return {
            'count': 0,
            'ids': [],
            'query': query,
            'message': f'Error: {str(e)}',
            'webenv': '',
            'querykey': ''
        }

def fetch_all_records(pmids: List[str]) -> Tuple[List[Dict], List[Dict], List[str]]:
    """
    PMIDリストから全レコードを取得
    Returns: (all_records, records_with_abstract, records_without_abstract)
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    all_records = []
    records_with_abstract = []
    records_without_abstract = []

    # PMIDを100件ずつ処理
    batch_size = 100
    for i in range(0, len(pmids), batch_size):
        batch_pmids = pmids[i:i + batch_size]
        params = {
            'db': 'pubmed',
            'id': ','.join(batch_pmids),
            'rettype': 'medline',
            'retmode': 'text'
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            medline_data = response.text

            # MEDLINEフォーマットを個別レコードに分割
            entries = medline_data.split('\n\n')
            for entry in entries:
                if not entry.strip():
                    continue

                # PMIDと抄録の有無を確認
                pmid = None
                has_abstract = False
                record_data = {'pmid': None, 'medline': entry}

                for line in entry.split('\n'):
                    if line.startswith('PMID-'):
                        pmid = line.split('- ')[1].strip()
                        record_data['pmid'] = pmid
                    elif line.startswith('AB  -'):
                        has_abstract = True

                if pmid:
                    all_records.append(record_data)
                    if has_abstract:
                        records_with_abstract.append(record_data)
                    else:
                        records_without_abstract.append(record_data)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching batch {i//batch_size + 1}: {str(e)}")

        # API制限を考慮して待機
        time.sleep(0.4)

    return all_records, records_with_abstract, records_without_abstract

def export_to_ris(records: List[Dict], filename: str, output_dir: str) -> None:
    """
    MEDLINEレコードをRISファイルに変換して保存
    """
    # 出力ディレクトリが存在しない場合は作成
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        for record in records:
            entry = record['medline']

            # RISエントリの開始
            f.write('TY  - JOUR\n')

            # アブストラクトを蓄積するための変数
            abstract = []
            current_field = None

            for line in entry.split('\n'):
                if not line.strip():
                    continue

                # フィールドの開始行を検出
                if line[:4].strip():  # 新しいフィールドの開始
                    if current_field == 'AB' and abstract:
                        # アブストラクトの書き込み
                        f.write(f'AB  - {" ".join(abstract)}\n')
                        abstract = []
                    current_field = line[:4].strip()

                # アブストラクトの続きの行を処理
                if current_field == 'AB':
                    if line.startswith('AB  -'):
                        abstract.append(line.split('- ', 1)[1] if '- ' in line else '')
                    else:
                        abstract.append(line[6:])  # インデントを除去
                    continue

                # その他のフィールドの処理
                if line.startswith('PMID-'):
                    f.write(f'ID  - {line.split("- ", 1)[1]}\n')
                elif line.startswith('TI  -'):
                    f.write(f'T1  - {line.split("- ", 1)[1]}\n')
                elif line.startswith('AU  -'):
                    f.write(f'A1  - {line.split("- ", 1)[1]}\n')
                elif line.startswith('JT  -'):
                    f.write(f'JF  - {line.split("- ", 1)[1]}\n')
                elif line.startswith('DP  -'):
                    f.write(f'Y1  - {line.split("- ", 1)[1]}\n')
                elif line.startswith('VI  -'):
                    f.write(f'VL  - {line.split("- ", 1)[1]}\n')
                elif line.startswith('IP  -'):
                    f.write(f'IS  - {line.split("- ", 1)[1]}\n')
                elif line.startswith('PG  -'):
                    f.write(f'SP  - {line.split("- ", 1)[1]}\n')
                elif line.startswith('DOI -'):
                    f.write(f'DO  - {line.split("- ", 1)[1]}\n')

            # エントリの最後でアブストラクトが残っている場合に書き込み
            if abstract:
                f.write(f'AB  - {" ".join(abstract)}\n')

            # RISエントリの終了
            f.write('ER  -\n\n')

def parse_search_formula_md(file_path: str) -> Tuple[Dict[str, str], str]:
    """
    search_formula.mdファイルを解析して、各行のクエリと最終クエリを取得する。
    PubMed/MEDLINE セクションのみを解析
    """
    line_queries: Dict[str, str] = {}
    final_query_structure = ""
    in_pubmed_section = False

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # PubMed/MEDLINEセクションを抽出
    pubmed_match = re.search(r'## 1\. PubMed/MEDLINE.*?(?=## \d+\.|$)', content, re.DOTALL)
    if not pubmed_match:
        return line_queries, final_query_structure

    pubmed_section = pubmed_match.group(0)

    # コードブロック内の検索式を抽出
    code_blocks = re.findall(r'```\n(.*?)\n```', pubmed_section, re.DOTALL)

    for i, block in enumerate(code_blocks, 1):
        # 複数行のORで繋がれた検索式を1つのクエリとして結合
        query_lines = []
        for line in block.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                # 末尾のORを削除
                line = re.sub(r'\s+OR\s*$', '', line)
                query_lines.append(line)

        if query_lines:
            combined_query = ' OR '.join(query_lines)
            line_queries[str(i)] = combined_query

    # 最終クエリは #1 AND #2 の形式を想定
    if len(line_queries) >= 2:
        final_query_structure = "#1 AND #2"

    return line_queries, final_query_structure

def build_final_query(structure: str, line_queries: Dict[str, str]) -> str:
    """
    最終クエリの構造と各行のクエリから最終的な検索式を構築する。
    """
    def replace_line_num(match):
        line_num = match.group(1)
        return f"({line_queries.get(line_num, '')})"

    expanded_query = re.sub(r"#(\d+)", replace_line_num, structure)
    return expanded_query

def main():
    parser = argparse.ArgumentParser(
        description="PubMed検索式を実行し、抄録付きレコードのみをRIS形式でエクスポート"
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
        default=None,
        help="出力先ディレクトリ（デフォルト: formula-fileと同じディレクトリ/log/）"
    )
    args = parser.parse_args()

    # 出力ディレクトリの決定
    if args.output_dir:
        output_dir = args.output_dir
    else:
        # formula_fileと同じディレクトリの log/ フォルダ
        formula_dir = os.path.dirname(os.path.abspath(args.formula_file))
        output_dir = os.path.join(formula_dir, 'log')

    # 検索式の解析
    print(f"\n=== PubMed検索式の実行 ===")
    print(f"検索式ファイル: {args.formula_file}")

    line_queries, final_query_structure = parse_search_formula_md(args.formula_file)

    if not line_queries or not final_query_structure:
        print(f"エラー: 検索式を解析できませんでした")
        return

    final_query = build_final_query(final_query_structure, line_queries)
    print(f"\n最終検索式:")
    print(f"{final_query}\n")

    # 検索実行
    print("検索を実行中...")
    result = get_pubmed_results(final_query, retmax=10000)

    if result['message'] != 'Success':
        print(f"エラー: {result['message']}")
        return

    total_count = result['count']
    pmids = result['ids']

    print(f"検索結果総数: {total_count:,}件")
    print(f"取得PMID数: {len(pmids):,}件")

    # 全レコードを取得（抄録の有無に関わらず）
    print("\n全レコードを取得中...")
    all_records, records_with_abstract, records_without_abstract = fetch_all_records(pmids)

    print(f"\n抄録あり: {len(records_with_abstract):,}件")
    print(f"抄録なし: {len(records_without_abstract):,}件")
    print(f"総レコード数: {len(all_records):,}件")

    # RISファイルにエクスポート
    if all_records:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        ris_filename = f'search_results_all_{timestamp}.ris'

        print(f"\nRISファイルを作成中...")
        export_to_ris(all_records, ris_filename, output_dir)

        output_path = os.path.join(output_dir, ris_filename)
        print(f"[OK] 保存完了: {output_path}")
        print(f"   レコード数: {len(all_records)}件")
    else:
        print("\n[WARNING] レコードが見つかりませんでした")

    # サマリーファイルの作成
    summary_filename = f'search_summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
    summary_path = os.path.join(output_dir, summary_filename)

    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(f"# PubMed検索結果サマリー\n\n")
        f.write(f"<!--\n")
        f.write(f"Generated by: scripts/search/query_executor/export_with_abstracts.py\n")
        f.write(f"Command: python scripts/search/query_executor/export_with_abstracts.py --formula-file {args.formula_file}\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"-->\n\n")
        f.write(f"**検索日時:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**検索式:**\n```\n{final_query}\n```\n\n")
        f.write(f"**結果:**\n")
        f.write(f"- 総ヒット数: {total_count:,}件\n")
        f.write(f"- 取得レコード数: {len(pmids):,}件\n")
        f.write(f"- 抄録あり: {len(records_with_abstract):,}件 ({len(records_with_abstract)/len(all_records)*100:.1f}%)\n")
        f.write(f"- 抄録なし: {len(records_without_abstract):,}件 ({len(records_without_abstract)/len(all_records)*100:.1f}%)\n\n")
        f.write(f"**出力ファイル:**\n")
        f.write(f"- RIS: `{ris_filename}` (全{len(all_records)}件)\n")

    print(f"[OK] サマリー保存完了: {summary_path}")

if __name__ == "__main__":
    main()
