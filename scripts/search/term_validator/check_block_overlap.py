import requests
import time
from typing import Dict, List, Tuple
import argparse
import os
import re

def get_pubmed_count(query: str) -> Dict[str, any]:
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

def parse_block_from_text(block_text: str) -> List[str]:
    """
    ブロックのテキストから検索行を抽出する

    Args:
        block_text: ブロックのテキスト（改行区切り）

    Returns:
        検索クエリのリスト（ORで分割されていないもの）
    """
    lines = []
    for line in block_text.strip().split('\n'):
        line = line.strip()
        # コメント行やヘッダー行をスキップ
        if not line or line.startswith('#') or line.startswith('```'):
            continue
        # ORやAND演算子だけの行をスキップ
        if line in ['OR', 'AND']:
            continue
        # 末尾のORを削除
        line = re.sub(r'\s+OR\s*$', '', line)
        if line:
            lines.append(line)

    return lines

def analyze_block_overlap(search_terms: List[str], block_name: str = "Block") -> Tuple[List[Dict], str]:
    """
    ブロック内の検索行の重複を分析する

    Args:
        search_terms: 検索クエリのリスト
        block_name: ブロック名（出力用）

    Returns:
        結果のリストとMarkdown形式のレポート
    """
    results = []
    cumulative_query_parts = []

    print(f"\n{block_name}の分析を開始します...")
    print(f"検索行数: {len(search_terms)}")

    for idx, term in enumerate(search_terms, 1):
        print(f"\n[{idx}/{len(search_terms)}] 検索中: {term[:60]}...")

        # 個別のヒット件数を取得
        time.sleep(0.4)  # API制限を考慮
        individual_result = get_pubmed_count(term)
        individual_count = individual_result['count']

        # 累積クエリを構築
        cumulative_query_parts.append(f"({term})")
        cumulative_query = " OR ".join(cumulative_query_parts)

        # 累積ヒット件数を取得
        time.sleep(0.4)  # API制限を考慮
        cumulative_result = get_pubmed_count(cumulative_query)
        cumulative_count = cumulative_result['count']

        # 追加された件数を計算
        if idx == 1:
            added_count = individual_count
            previous_cumulative = 0
        else:
            previous_cumulative = results[-1]['cumulative_count']
            added_count = cumulative_count - previous_cumulative

        results.append({
            'line': idx,
            'term': term,
            'individual_count': individual_count,
            'cumulative_count': cumulative_count,
            'added_count': added_count,
            'previous_cumulative': previous_cumulative
        })

        print(f"  個別: {individual_count:,} | 累積: {cumulative_count:,} | 追加: {added_count:,}")

    # Markdownレポートを生成
    report = generate_markdown_report(results, block_name, cumulative_query)

    return results, report

def generate_markdown_report(results: List[Dict], block_name: str, final_query: str) -> str:
    """
    分析結果からMarkdownレポートを生成する
    """
    report = f"## {block_name} - Hit Count Analysis\n\n"

    # テーブルヘッダー
    report += "| Line | Term | Individual Count | Cumulative (OR) | Added | % of Total |\n"
    report += "|------|------|------------------|-----------------|-------|------------|\n"

    total_count = results[-1]['cumulative_count'] if results else 0

    # 各行の結果
    for result in results:
        term_display = result['term'][:80] + "..." if len(result['term']) > 80 else result['term']
        individual = result['individual_count']
        cumulative = result['cumulative_count']
        added = result['added_count']

        # 全体に対する追加分の割合
        if total_count > 0:
            pct = (added / total_count) * 100
        else:
            pct = 0

        report += f"| {result['line']} | `{term_display}` | {individual:,} | {cumulative:,} | **+{added:,}** | {pct:.1f}% |\n"

    # サマリー
    report += f"\n### Summary\n\n"
    report += f"- **Total unique papers**: {total_count:,}\n"

    # 最も効果的な行
    if results:
        max_added = max(results, key=lambda x: x['added_count'])
        report += f"- **Most effective term**: Line {max_added['line']} (+{max_added['added_count']:,} papers, {(max_added['added_count']/total_count*100):.1f}% of total)\n"

        # 低効果の行（全体の1%未満）
        low_value_terms = [r for r in results if total_count > 0 and (r['added_count'] / total_count) < 0.01]
        if low_value_terms:
            report += f"- **Low-value terms** (Added < 1% of total): Lines "
            report += ", ".join([str(r['line']) for r in low_value_terms])
            report += "\n"

        # 重複率が高い行（追加件数が個別件数の20%未満）
        high_overlap_terms = [r for r in results[1:] if r['individual_count'] > 0 and (r['added_count'] / r['individual_count']) < 0.2]
        if high_overlap_terms:
            report += f"- **High overlap terms** (>80% already covered): Lines "
            report += ", ".join([str(r['line']) for r in high_overlap_terms])
            report += "\n"

    # 最終クエリ
    report += f"\n### Final Combined Query\n\n"
    report += f"```\n{final_query}\n```\n"

    return report

def main():
    parser = argparse.ArgumentParser(
        description="検索ブロック内の各行のヒット件数と累積OR結果を分析します。",
        epilog="""
使用例:
  1. テキストファイルから読み込む:
     python check_block_overlap.py -i block.txt -o report.md --block-name "Population"

  2. コマンドラインから直接入力:
     python check_block_overlap.py --block-name "Population" -o report.md
     （その後、複数行の検索式を貼り付けてCtrl+Zで終了）
        """
    )
    parser.add_argument(
        "-i", "--input",
        type=str,
        help="検索ブロックが記述されたテキストファイルのパス"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        required=True,
        help="結果を保存するMarkdownファイルのパス"
    )
    parser.add_argument(
        "-b", "--block-name",
        type=str,
        default="Block #1",
        help="ブロック名（レポート表示用）"
    )

    args = parser.parse_args()

    # 出力ディレクトリが存在しない場合は作成
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 入力の取得
    if args.input:
        # ファイルから読み込み
        with open(args.input, 'r', encoding='utf-8') as f:
            block_text = f.read()
    else:
        # 標準入力から読み込み
        print(f"検索ブロックの内容を入力してください（入力終了はCtrl+Z (Windows) または Ctrl+D (Unix)）:")
        import sys
        block_text = sys.stdin.read()

    # ブロックを解析
    search_terms = parse_block_from_text(block_text)

    if not search_terms:
        print("エラー: 有効な検索行が見つかりませんでした。")
        return

    print(f"\n検出された検索行:")
    for idx, term in enumerate(search_terms, 1):
        print(f"  {idx}. {term}")

    # 分析を実行
    results, report = analyze_block_overlap(search_terms, args.block_name)

    # レポートを保存
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(f"# Search Block Overlap Analysis\n\n")
        f.write(f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        if args.input:
            f.write(f"Input File: {args.input}\n\n")
        f.write(report)

    print(f"\n[OK] 分析完了! 結果を {args.output} に保存しました。")
    print(f"\n総ヒット件数: {results[-1]['cumulative_count']:,}")

if __name__ == "__main__":
    main()
