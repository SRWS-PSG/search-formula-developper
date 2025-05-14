import requests
import time
from typing import Dict, List, Tuple, Any
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

def export_to_ris(pmids: List[str], filename: str, output_dir: str) -> None:
    """
    PMIDのリストからRISファイルを作成する
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    
    # 出力ディレクトリが存在しない場合は作成
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filepath = os.path.join(output_dir, filename)

    # PMIDを100件ずつ処理
    batch_size = 100
    with open(filepath, 'w', encoding='utf-8') as f:
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
                
                # MEDLINEフォーマットをRISフォーマットに変換
                entries = medline_data.split('\n\n')
                for entry in entries:
                    if not entry.strip():
                        continue
                    
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
                                abstract.append(line.split('- ')[1])
                            else:
                                abstract.append(line[6:])  # インデントを除去
                            continue
                        
                        # その他のフィールドの処理
                        if line.startswith('PMID-'):
                            f.write(f'ID  - {line.split("- ")[1]}\n')
                        elif line.startswith('TI  -'):
                            f.write(f'T1  - {line.split("- ")[1]}\n')
                        elif line.startswith('AU  -'):
                            f.write(f'A1  - {line.split("- ")[1]}\n')
                        elif line.startswith('JT  -'):
                            f.write(f'JF  - {line.split("- ")[1]}\n')
                        elif line.startswith('DP  -'):
                            f.write(f'Y1  - {line.split("- ")[1]}\n')
                        elif line.startswith('VI  -'):
                            f.write(f'VL  - {line.split("- ")[1]}\n')
                        elif line.startswith('IP  -'):
                            f.write(f'IS  - {line.split("- ")[1]}\n')
                        elif line.startswith('PG  -'):
                            f.write(f'SP  - {line.split("- ")[1]}\n')
                    
                    # エントリの最後でアブストラクトが残っている場合に書き込み
                    if abstract:
                        f.write(f'AB  - {" ".join(abstract)}\n')
                    
                    # RISエントリの終了
                    f.write('ER  -\n\n')
            
            except requests.exceptions.RequestException as e:
                print(f"Error fetching batch {i//batch_size + 1}: {str(e)}")
            
            # API制限を考慮して待機
            time.sleep(0.5)

def parse_search_formula_md(file_path: str) -> Tuple[Dict[str, str], str]:
    """
    search_formula.mdファイルを解析して、各行のクエリと最終クエリを取得する。
    """
    line_queries: Dict[str, str] = {}
    final_query_structure = ""

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line.startswith("#"):
                continue

            match = re.match(r"#(\d+)\s+(.*)", line)
            if match:
                line_num = match.group(1)
                query_part = match.group(2).strip()
                line_queries[line_num] = query_part
            
            if re.match(r"#(\d+)\s+(.*#\d+.*)", line): # 最終行の構造 (例: #5 (#1 OR #2) AND (#3 OR #4))
                final_query_structure = re.match(r"#\d+\s+(.*)", line).group(1).strip()
                
    if not final_query_structure and line_queries: # 最終行の構造が複雑な演算子なしの場合
        # 最後の行番号を取得
        last_line_num = sorted(line_queries.keys(), key=int)[-1]
        # 最終行のクエリが他の行を参照していない場合、それが最終クエリ構造とみなす
        if not re.search(r"#\d+", line_queries[last_line_num]):
             final_query_structure = f"#{last_line_num}"


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

def load_pmids_from_file(file_path: str) -> List[str]:
    """
    テキストファイルからPMIDのリストを読み込む。
    """
    pmids = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"): # コメント行と空行を無視
                pmids.append(line)
    return pmids

def main():
    parser = argparse.ArgumentParser(description="指定された検索式ファイルとPMIDリストファイルに基づき、最終検索式を実行し、シード論文が検索結果に含まれるかを確認します。")
    parser.add_argument(
        "--formula-file",
        type=str,
        required=True,
        help="検索式が記述されたMarkdownファイルのパス (例: search_formula/プロジェクト名/search_formula.md)"
    )
    parser.add_argument(
        "--pmid-file",
        type=str,
        required=True,
        help="シード論文のPMIDが記述されたテキストファイルのパス (例: search_formula/プロジェクト名/seed_pmids.txt)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None, # デフォルトはNoneに変更
        help="生成されるRISファイルなどの出力先ディレクトリ (デフォルト: search_formula/プロジェクト名/)"
    )
    args = parser.parse_args()

    # 出力ディレクトリの決定
    output_dir = args.output_dir
    if output_dir is None:
        # formula_file のパスからプロジェクトディレクトリを推定
        match = re.search(r"(search_formula/[^/]+)/", args.formula_file)
        if match:
            output_dir = match.group(1)
        else:
            # 推定できない場合はデフォルトの logs/search を使用
            output_dir = "logs/search"
            print(f"警告: プロジェクトディレクトリを推定できませんでした。RISファイルは {output_dir} に保存されます。")

    # PMIDリストの読み込み
    pmids_to_check = load_pmids_from_file(args.pmid_file)
    if not pmids_to_check:
        print(f"PMIDファイルに有効なPMIDが見つかりませんでした: {args.pmid_file}")
        return

    # 検索式の解析と構築
    line_queries, final_query_structure = parse_search_formula_md(args.formula_file)
    if not final_query_structure:
        print(f"検索式ファイルから最終検索構造を特定できませんでした: {args.formula_file}")
        return
        
    final_query = build_final_query(final_query_structure, line_queries)

    print(f"\n=== 最終検索式の評価 ===")
    print(f"検索式ファイル: {args.formula_file}")
    print(f"PMIDファイル: {args.pmid_file}")
    print(f"最終検索式: {final_query}")

    # 最終検索式の実行
    result = get_pubmed_results(final_query)
    print(f"検索結果総数: {result['count']:,}件")

    # シード論文の包含確認
    found_ids = set(result['ids'])
    included_pmids = []
    not_found_pmids = []

    for pmid in pmids_to_check:
        if pmid in found_ids:
            included_pmids.append(pmid)
        else:
            not_found_pmids.append(pmid)

    print(f"\n--- シード論文の包含状況 ---")
    print(f"含まれていたPMID ({len(included_pmids)}件): {', '.join(included_pmids) if included_pmids else 'なし'}")
    if not_found_pmids:
        print(f"含まれていなかったPMID ({len(not_found_pmids)}件): {', '.join(not_found_pmids)}")

    # RISファイルの出力
    if result['count'] > 0:
        date = datetime.now().strftime('%Y%m%d')
        # プロジェクト名を取得しようと試みる (output_dirから)
        project_name_match = re.search(r"search_formula/([^/]+)", output_dir)
        project_name_prefix = f"{project_name_match.group(1)}_" if project_name_match else ""
        
        # データベース名とヒット数をファイル名に含める
        ris_filename = f"{project_name_prefix}PubMed_{result['count']}hits_{date}.ris"
        
        print(f"\nRISファイルを出力中: {os.path.join(output_dir, ris_filename)}")
        export_to_ris(result['ids'], ris_filename, output_dir)
        print("RISファイルの出力が完了しました。")
    else:
        print("\n検索結果が0件のため、RISファイルは出力されませんでした。")

if __name__ == "__main__":
    main()
