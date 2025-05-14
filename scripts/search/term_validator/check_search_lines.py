import requests
import time
from typing import Dict, List, Tuple, Any
import argparse
import os
import re

def get_pubmed_count(query: str) -> Dict[str, Any]:
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

def parse_search_formula_md(file_path: str) -> Tuple[Dict[str, str], str, Dict[str, str], Dict[str, List[str]]]:
    """
    search_formula.mdファイルを解析して、各行のクエリと最終クエリを取得する。
    セミコロンはORとして解釈する。
    
    Returns:
        line_queries: 各行の展開後クエリ
        final_query_structure: 最終検索式の構造
        raw_line_queries: 各行の元のクエリ
        individual_terms: 各行のORで分割された個別の検索語のリスト
    """
    line_queries: Dict[str, str] = {}
    raw_line_queries: Dict[str, str] = {} # OR展開前のクエリを保持
    individual_terms: Dict[str, List[str]] = {}  # 各行の個別のキーワードを保持
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
                raw_line_queries[line_num] = query_part
                individual_terms[line_num] = []

                # ";" または " OR " を使用して個別のキーワードを分割
                if ";" in query_part:
                    terms = [term.strip() for term in query_part.split(';')]
                    # 各タームが既に括弧で囲まれていないか、またはMeSHタグを含んでいるか確認
                    processed_terms = []
                    for term in terms:
                        if (term.startswith('(') and term.endswith(')')) or "[mh]" in term.lower() or "[mesh]" in term.lower() or "[tiab]" in term.lower():
                             processed_terms.append(term)
                        else:
                            processed_terms.append(f"({term})")
                    line_queries[line_num] = " OR ".join(processed_terms)
                    individual_terms[line_num] = processed_terms
                elif " OR " in query_part:
                    line_queries[line_num] = query_part # <--- この行を追加して、行全体のクエリを保存
                    # OR演算子で分割して個別のキーワードを取得
                    if query_part.count('(') > query_part.count(')'):
                        # 括弧が閉じていない場合は、全体を1つのキーワードとして扱う
                        individual_terms[line_num] = [query_part]
                    else:
                        try:
                            # 単純なOR条件を分割
                            terms = []
                            # 括弧のネストを考慮した分割が必要
                            term_start = 0
                            bracket_count = 0
                            in_quotes = False
                            for i, char in enumerate(query_part):
                                if char == '"':
                                    in_quotes = not in_quotes
                                elif not in_quotes:
                                    if char == '(':
                                        bracket_count += 1
                                    elif char == ')':
                                        bracket_count -= 1
                                    # " OR "の検出 (前後に空白があるORのみ)
                                    elif (char == 'O' and i + 3 < len(query_part) and 
                                          query_part[i:i+3] == 'OR ' and
                                          i > 0 and query_part[i-1] == ' ' and 
                                          bracket_count == 0):
                                        terms.append(query_part[term_start:i-1].strip())
                                        term_start = i + 3
                            
                            # 最後のタームを追加
                            if term_start < len(query_part):
                                terms.append(query_part[term_start:].strip())
                            
                            individual_terms[line_num] = terms
                        except Exception as e:
                            # 解析エラーの場合は、全体を1つのキーワードとして扱う
                            individual_terms[line_num] = [query_part]
                else:
                    line_queries[line_num] = query_part
                    individual_terms[line_num] = [query_part]
            
            # 最終行の構造を取得 (例: #5 (#1 OR #2) AND (#3 OR #4))
            if re.match(r"#(\d+)\s+(.*#\d+.*)", line):
                line_num = re.match(r"#(\d+)\s+(.*)", line).group(1)
                if line_num not in line_queries or line_num == max(line_queries.keys(), key=int):  # この行番号が最後の行番号または処理されていない場合
                    final_query_structure = re.match(r"#\d+\s+(.*)", line).group(1).strip()

    return line_queries, final_query_structure, raw_line_queries, individual_terms

def expand_references(query: str, line_queries: Dict[str, str], max_depth: int = 10) -> str:
    """
    行番号の参照（#n）を実際の検索クエリに展開する
    
    Args:
        query: 展開する検索クエリ
        line_queries: 行番号と検索クエリのマッピング
        max_depth: 最大再帰深度（循環参照対策）
        
    Returns:
        展開後の検索クエリ
    """
    depth = 0
    expanded = query
    
    while depth < max_depth:
        original = expanded
        # #数字 を対応するクエリで置換
        expanded = re.sub(r"#(\d+)", lambda m: f"({line_queries.get(m.group(1), '')})", expanded)
        
        # 変化がなければ終了
        if original == expanded:
            break
            
        depth += 1
        
    if depth >= max_depth:
        print(f"警告: 最大再帰深度({max_depth})に達しました。循環参照の可能性があります。")
        
    return expanded

def build_final_query(structure: str, line_queries: Dict[str, str]) -> str:
    """
    最終クエリの構造と各行のクエリから最終的な検索式を構築する。
    """
    # 再利用可能な参照展開関数を使用
    return expand_references(structure, line_queries)

def main():
    parser = argparse.ArgumentParser(description="search_formula.mdを読み込み、PubMedの検索語ヒット件数を確認し、結果をMarkdownファイルに出力します。")
    parser.add_argument(
        "-i", "--input-formula",
        type=str,
        required=True,
        help="検索式が記述されたMarkdownファイルのパス (例: search_formula/ujihara/search_formula.md)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        required=True,
        help="結果を保存するMarkdownファイルのパス (例: search_formula/ujihara/search_lines_results.md)"
    )
    args = parser.parse_args()

    # 出力ディレクトリが存在しない場合は作成
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    line_queries, final_query_structure, raw_line_queries, individual_terms = parse_search_formula_md(args.input_formula)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(f"# 検索式ファイル: {args.input_formula}\n\n")
        f.write("=== 各行の検索結果 ===\n")
        f.write("| 行番号 | オリジナル検索クエリ | 個別キーワード/展開後クエリ (OR処理済) | 文献数 |\n")
        f.write("|--------|--------------------|------------------------------------|---------|")

        sorted_line_nums = sorted(raw_line_queries.keys(), key=int)

        for line_num in sorted_line_nums:
            original_query = raw_line_queries[line_num]
            expanded_query = line_queries.get(line_num, original_query)
            
            # 最初の行の出力
            f.write(f"\n| #{line_num} | `{original_query}` | | |")
            
            # 個別キーワードごとの件数を出力
            terms = individual_terms.get(line_num, [])
            
            # 行番号の参照を含むか確認（#1、#2などの形式）
            contains_line_reference = bool(re.search(r"#\d+", original_query))
            
            # 行番号参照を含む場合は、展開してから結果を取得
            if contains_line_reference:
                # 行番号を実際のクエリに展開
                fully_expanded_query = expand_references(original_query, line_queries)
                time.sleep(1)  # API制限を考慮
                expanded_result = get_pubmed_count(fully_expanded_query)
                f.write(f"\n| | | `{fully_expanded_query}` | {expanded_result['count']:,} |")
            # 行番号参照を含まない場合は通常の処理
            elif len(terms) == 1:
                time.sleep(1)  # API制限を考慮
                term_result = get_pubmed_count(terms[0])
                f.write(f"\n| | | `{terms[0]}` | {term_result['count']:,} |")
            # 複数のキーワードがある場合は個別に表示
            elif len(terms) > 1:
                for term in terms:
                    time.sleep(1)  # API制限を考慮
                    term_result = get_pubmed_count(term)
                    f.write(f"\n| | | `{term}` | {term_result['count']:,} |")
                
                # 全体のOR結果
                time.sleep(1)  # API制限を考慮
                result = get_pubmed_count(expanded_query)
                f.write(f"\n| | | **全体OR結果** | **{result['count']:,}** |")
            # 個別キーワードがない場合（通常はあり得ない）
            else:
                time.sleep(1)  # API制限を考慮
                result = get_pubmed_count(expanded_query)
                f.write(f"\n| | | `{expanded_query}` | {result['count']:,} |")

        if final_query_structure:
            f.write("\n\n=== 最終的な組み合わせ検索結果 ===\n")
            final_query = build_final_query(final_query_structure, line_queries)
            time.sleep(1)
            final_result = get_pubmed_count(final_query)
            f.write(f"最終検索構造: `{final_query_structure}`\n\n")
            f.write(f"展開後の最終検索式: `{final_query}`\n\n")
            f.write(f"最終検索結果: **{final_result['count']:,}** 件\n")
        else:
            f.write("\n\n=== 最終的な組み合わせ検索結果 ===\n")
            f.write("最終検索構造が見つかりませんでした。\n")

    print(f"結果を {args.output} に保存しました。")

if __name__ == "__main__":
    main()
