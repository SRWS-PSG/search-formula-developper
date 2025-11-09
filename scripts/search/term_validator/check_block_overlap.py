import argparse
import os
import re
import time
from typing import Any, Dict, List, Tuple

import random
import requests

try:
    from dotenv import load_dotenv
except ImportError:  # Optional dependency
    load_dotenv = None

if load_dotenv:
    load_dotenv()

NCBI_API_KEY = os.getenv("NCBI_API_KEY") or None
NCBI_TOOL = os.getenv("NCBI_TOOL") or None
NCBI_EMAIL = os.getenv("NCBI_EMAIL") or None

def _determine_request_interval(default_interval: float = 5.0) -> float:
    """Return waiting time between API calls derived from env rate limit."""
    raw_rate = os.getenv("NCBI_RATE_LIMIT_RPS")
    if not raw_rate:
        return default_interval
    try:
        rate = float(raw_rate)
        if rate > 0:
            return max(1.0 / rate, 0.1)
    except ValueError:
        pass
    return default_interval

REQUEST_INTERVAL = _determine_request_interval()
REQUEST_TIMEOUT = 30
MAX_RETRIES = 5
RETRY_BACKOFF_SECONDS = 2.0

_LAST_REQUEST_TS = 0.0

COMMON_EUTILS_PARAMS: Dict[str, str] = {}
if NCBI_API_KEY:
    COMMON_EUTILS_PARAMS["api_key"] = NCBI_API_KEY
if NCBI_TOOL:
    COMMON_EUTILS_PARAMS["tool"] = NCBI_TOOL
if NCBI_EMAIL:
    COMMON_EUTILS_PARAMS["email"] = NCBI_EMAIL

def _respect_rate_limit() -> None:
    """Wait until the next API call is allowed based on REQUEST_INTERVAL."""
    global _LAST_REQUEST_TS
    if REQUEST_INTERVAL <= 0:
        return

    now = time.monotonic()
    elapsed = now - _LAST_REQUEST_TS
    if elapsed < REQUEST_INTERVAL:
        time.sleep(REQUEST_INTERVAL - elapsed)
    _LAST_REQUEST_TS = time.monotonic()


def _build_request_params(query: str) -> Dict[str, str]:
    params: Dict[str, str] = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": "0",
    }
    params.update(COMMON_EUTILS_PARAMS)
    return params

def format_count(value: Any) -> str:
    """Return thousands-separated count or NA when unavailable."""
    if isinstance(value, int):
        return f"{value:,}"
    return "NA"


def _format_count_for_log(value: Any) -> str:
    """Lightweight formatter for console logging."""
    return format_count(value)


def get_pubmed_count(query: str) -> Dict[str, Any]:
    """Call PubMed E-utilities and return the hit count with retry logic."""

    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    search_url = f"{base_url}/esearch.fcgi"
    params = _build_request_params(query)
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            _respect_rate_limit()
            response = requests.get(search_url, params=params, timeout=REQUEST_TIMEOUT)
            if response.status_code == 429:
                last_error = "HTTP 429: API rate limit exceeded"
                backoff = RETRY_BACKOFF_SECONDS * (2 ** (attempt - 1))
                time.sleep(backoff + random.uniform(0, 0.5))
                continue

            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict) and data.get("error"):
                last_error = f"API error: {data['error']}"
                backoff = RETRY_BACKOFF_SECONDS * (2 ** (attempt - 1))
                time.sleep(backoff + random.uniform(0, 0.5))
                continue
            result = data.get("esearchresult", {})

            error_list = result.get("errorlist") or {}
            if error_list:
                last_error = f"API error: {error_list}"
                backoff = RETRY_BACKOFF_SECONDS * (2 ** (attempt - 1))
                time.sleep(backoff + random.uniform(0, 0.5))
                continue

            if isinstance(result, dict) and result.get("ERROR"):
                last_error = f"API error: {result['ERROR']}"
                backoff = RETRY_BACKOFF_SECONDS * (2 ** (attempt - 1))
                time.sleep(backoff + random.uniform(0, 0.5))
                continue

            count_str = result.get("count")
            if count_str is None:
                last_error = "API response missing 'count'"
                backoff = RETRY_BACKOFF_SECONDS * (2 ** (attempt - 1))
                time.sleep(backoff + random.uniform(0, 0.5))
                continue

            try:
                count = int(count_str)
            except (TypeError, ValueError):
                last_error = f"Invalid count value: {count_str}"
                backoff = RETRY_BACKOFF_SECONDS * (2 ** (attempt - 1))
                time.sleep(backoff + random.uniform(0, 0.5))
                continue

            return {
                "count": count,
                "query": query,
                "message": "Success",
                "success": True,
            }

        except (requests.exceptions.RequestException, ValueError) as exc:
            last_error = str(exc)
            backoff = RETRY_BACKOFF_SECONDS * (2 ** (attempt - 1))
            time.sleep(backoff + random.uniform(0, 0.5))

    return {
        "count": None,
        "query": query,
        "message": f"Error after {MAX_RETRIES} attempts: {last_error or 'Unknown error'}",
        "success": False,
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
        individual_result = get_pubmed_count(term)
        if not individual_result.get('success'):
            print(f"  [WARN] 個別検索でエラー: {individual_result['message']}")
        individual_count = individual_result['count']

        # 累積クエリを構築
        cumulative_query_parts.append(f"({term})")
        cumulative_query = " OR ".join(cumulative_query_parts)

        # 累積ヒット件数を取得
        cumulative_result = get_pubmed_count(cumulative_query)
        if not cumulative_result.get('success'):
            print(f"  [WARN] 累積検索でエラー: {cumulative_result['message']}")
        previous_cumulative = results[-1]['cumulative_count'] if results else 0
        cumulative_count = cumulative_result['count'] if cumulative_result['count'] is not None else previous_cumulative

        # 追加された件数を計算
        added_count = cumulative_count - previous_cumulative if cumulative_count >= previous_cumulative else 0
        if idx == 1:
            previous_cumulative = 0
            added_count = cumulative_count

        results.append({
            'line': idx,
            'term': term,
            'individual_count': individual_count,
            'cumulative_count': cumulative_count,
            'added_count': added_count,
            'previous_cumulative': previous_cumulative
        })

        individual_display = _format_count_for_log(individual_count)
        print(f"  個別: {individual_display} | 累積: {cumulative_count:,} | 追加: {added_count:,}")

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

        report += f"| {result['line']} | `{term_display}` | {format_count(individual)} | {cumulative:,} | **+{added:,}** | {pct:.1f}% |\n"

    # サマリー
    report += f"\n### Summary\n\n"
    report += f"- **Total unique papers**: {total_count:,}\n"

    # 最も効果的な行
    if results and total_count > 0:
        max_added = max(results, key=lambda x: x['added_count'])
        report += f"- **Most effective term**: Line {max_added['line']} (+{max_added['added_count']:,} papers, {(max_added['added_count']/total_count*100):.1f}% of total)\n"

        # 低効果の行（全体の1%未満）
        low_value_terms = [r for r in results if total_count > 0 and (r['added_count'] / total_count) < 0.01]
        if low_value_terms:
            report += f"- **Low-value terms** (Added < 1% of total): Lines "
            report += ", ".join([str(r['line']) for r in low_value_terms])
            report += "\n"

        # 重複率が高い行（追加件数が個別件数の20%未満）
        high_overlap_terms = [
            r for r in results[1:]
            if isinstance(r['individual_count'], int) and r['individual_count'] > 0
            and (r['added_count'] / r['individual_count']) < 0.2
        ]
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
        # メタデータコメントを追加
        f.write("<!--\n")
        f.write(f"Generated by: scripts/search/term_validator/check_block_overlap.py\n")

        # コマンドを再構築
        cmd_parts = ["python scripts/search/term_validator/check_block_overlap.py"]
        if args.input:
            cmd_parts.append(f"-i {args.input}")
        cmd_parts.append(f"-o {args.output}")
        cmd_parts.append(f'--block-name "{args.block_name}"')
        f.write(f"Command: {' '.join(cmd_parts)}\n")

        if args.input:
            f.write(f"Input data: {args.input}\n")
        else:
            f.write(f"Input data: stdin (manual input)\n")

        f.write(f"Output directory: {output_dir if output_dir else '.'}\n")
        f.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-->\n\n")

        # レポート本体
        f.write(f"# Search Block Overlap Analysis\n\n")
        f.write(f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        if args.input:
            f.write(f"Input File: {args.input}\n\n")
        f.write(report)

    print(f"\n[OK] 分析完了! 結果を {args.output} に保存しました。")
    print(f"\n総ヒット件数: {results[-1]['cumulative_count']:,}")

if __name__ == "__main__":
    main()
