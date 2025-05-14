import re
import os
import sys
import requests
import time
import argparse
from datetime import datetime

def get_pubmed_count(query: str) -> dict:
    """
    PubMed E-utilities APIを使用して検索クエリの結果件数を取得する
    
    Args:
        query: PubMed検索クエリ
        
    Returns:
        Dict: {
            'count': int,
            'query': str,
            'message': str
        }
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    search_url = f"{base_url}/esearch.fcgi"
    
    params = {
        'db': 'pubmed',
        'term': query,
        'retmode': 'json'
    }
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        return {
            'count': int(data['esearchresult'].get('count', 0)),
            'query': query,
            'message': 'Success'
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'count': 0,
            'query': query,
            'message': f'Error: {str(e)}'
        }

def parse_search_formula(text: str) -> dict:
    """
    検索式のテキストを解析して、ブロックごとに分割する
    
    Args:
        text: 検索式のテキスト
        
    Returns:
        Dict: {
            'blocks': [
                {
                    'name': str,
                    'lines': [str, str, ...],
                },
                ...
            ],
            'final': str
        }
    """
    # 行に分割
    lines = text.strip().split('\n')
    
    # ブロック構造の初期化
    blocks = []
    current_block = None
    current_lines = []
    final_query = None
    
    # 各行を処理
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # ブロック開始の検出 (#1, #2, #3 etc.)
        block_match = re.match(r'#(\d+)\s+(.*?)$', line)
        if block_match:
            # 前のブロックがあれば保存
            if current_block is not None and current_lines:
                blocks.append({
                    'name': current_block,
                    'lines': current_lines
                })
            
            # 新しいブロックを開始
            block_num = block_match.group(1)
            block_name = block_match.group(2)
            current_block = f"#{block_num} {block_name}"
            current_lines = []
            
            # 最終検索式の検出
            if "最終" in block_name or "final" in block_name.lower():
                final_query = line
                current_block = None
                
        elif current_block is not None:
            # ブロック内の行を追加
            line = line.strip()
            if line:
                # ORやANDなどの演算子だけの行は前の行に結合
                if line in ['OR', 'AND', 'NOT'] and current_lines:
                    current_lines[-1] += f" {line}"
                else:
                    current_lines.append(line)
    
    # 最後のブロックを保存
    if current_block is not None and current_lines:
        blocks.append({
            'name': current_block,
            'lines': current_lines
        })
    
    return {
        'blocks': blocks,
        'final': final_query
    }

def create_structured_markdown(formula_dict: dict, counts_results: dict) -> str:
    """
    解析した検索式と検索結果件数からMarkdownファイルを生成する
    
    Args:
        formula_dict: 解析された検索式の辞書
        counts_results: 検索結果件数の辞書
        
    Returns:
        str: Markdownフォーマットのテキスト
    """
    blocks = formula_dict['blocks']
    final_query = formula_dict['final']
    
    md_text = "# 検索式の構造化分析\n\n"
    md_text += f"分析日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    # 各ブロックの詳細
    for block in blocks:
        block_name = block['name']
        lines = block['lines']
        
        md_text += f"## {block_name}\n\n"
        md_text += "| 検索語 | 文献数 |\n"
        md_text += "|---------|--------|\n"
        
        for line in lines:
            # 行の検索結果件数を取得
            if line in counts_results:
                count = counts_results[line]['count']
                md_text += f"| `{line}` | {count:,} |\n"
            else:
                md_text += f"| `{line}` | - |\n"
        
        md_text += "\n"
        
        # ブロック全体の検索結果件数
        if block_name in counts_results:
            block_count = counts_results[block_name]['count']
            md_text += f"**ブロック全体の文献数**: {block_count:,}\n\n"
    
    # 最終検索式の結果
    if final_query and 'combined_query' in counts_results:
        md_text += "## 最終検索式\n\n"
        md_text += f"検索式: `{final_query}`\n\n"
        md_text += f"**検索結果**: {counts_results['combined_query']['count']:,} 件\n\n"
    
    return md_text

def main():
    parser = argparse.ArgumentParser(description='検索式を構造化して各行のヒット数を確認するツール')
    parser.add_argument('input', nargs='?', help='検索式のテキストファイル（指定がなければ標準入力から読み込み）')
    parser.add_argument('--project', '-p', default=None, help='プロジェクト名（search_formula/配下のディレクトリ名）')
    parser.add_argument('--output', '-o', default=None, help='出力ファイル名（デフォルト: structured_search.md）')
    args = parser.parse_args()

    # テキスト入力の取得
    if args.input:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"ファイルの読み込みに失敗しました: {str(e)}")
            return
    else:
        print("検索式を入力してください（終了するには Ctrl+D または Ctrl+Z を押してください）:")
        text = sys.stdin.read()
    
    # プロジェクトディレクトリを決定
    if args.project:
        project_name = args.project
    else:
        # プロジェクト名未指定時はタイムスタンプを使用
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        project_name = f"project_{timestamp}"
    
    project_dir = os.path.join("search_formula", project_name)
    
    # ディレクトリが存在しなければ作成
    os.makedirs(project_dir, exist_ok=True)
    os.makedirs(os.path.join(project_dir, "log"), exist_ok=True)
    
    # 出力ファイル名を決定
    if args.output:
        output_file = os.path.join(project_dir, args.output)
    else:
        output_file = os.path.join(project_dir, "structured_search.md")
    
    print(f"プロジェクトディレクトリ: {project_dir}")
    
    # 検索式を解析
    print("検索式を解析中...")
    formula_dict = parse_search_formula(text)
    
    # 各行の検索結果件数を取得
    print("PubMedで検索結果件数を取得中...")
    counts_results = {}
    
    # 各ブロック内の行の検索結果件数
    for block in formula_dict['blocks']:
        block_name = block['name']
        lines = block['lines']
        
        print(f"\n{block_name} のヒット件数を確認中...")
        
        # 各行の検索結果件数
        for line in lines:
            if line.strip() and not (line.strip() in ['OR', 'AND', 'NOT']):
                print(f"  検索中: {line}")
                result = get_pubmed_count(line)
                counts_results[line] = result
                print(f"  ヒット数: {result['count']:,}")
                time.sleep(1)  # API制限を考慮
        
        # ブロック全体の検索結果件数（OR結合）
        if lines:
            block_query = " OR ".join([f"({line})" for line in lines if line.strip() and not (line.strip() in ['OR', 'AND', 'NOT'])])
            print(f"  ブロック全体: {block_name}")
            block_result = get_pubmed_count(block_query)
            counts_results[block_name] = block_result
            print(f"  ブロック全体のヒット数: {block_result['count']:,}")
            time.sleep(1)  # API制限を考慮
    
    # 最終検索式の検索結果件数
    if formula_dict['blocks']:
        # 各ブロックを結合して最終検索式を作成
        blocks_queries = []
        for block in formula_dict['blocks']:
            block_query = " OR ".join([f"({line})" for line in block['lines'] if line.strip() and not (line.strip() in ['OR', 'AND', 'NOT'])])
            if block_query:
                blocks_queries.append(f"({block_query})")
        
        if blocks_queries:
            combined_query = " AND ".join(blocks_queries)
            print(f"\n最終検索式のヒット件数を確認中...")
            combined_result = get_pubmed_count(combined_query)
            counts_results['combined_query'] = combined_result
            print(f"最終検索式のヒット数: {combined_result['count']:,}")
    
    # 結果をMarkdownに変換
    md_text = create_structured_markdown(formula_dict, counts_results)
    
    # 構造化された検索式をMarkdownファイルとして出力
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_text)
    
    # 元の検索式も保存
    raw_file = os.path.join(project_dir, "original_search.txt")
    with open(raw_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"\n処理が完了しました。")
    print(f"構造化された検索式と結果: {output_file}")
    print(f"元の検索式: {raw_file}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n処理が中断されました。")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
