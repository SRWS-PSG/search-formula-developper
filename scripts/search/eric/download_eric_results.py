#!/usr/bin/env python3
"""
ERIC検索結果ダウンロードスクリプト

fd_review検索式を実行し、全文献をRIS形式でダウンロードします。
ファイル名は「日付_件数_eric.ris」形式で保存されます。

Usage:
    python scripts/search/eric/download_eric_results.py --output-dir projects/fd_review/eric_results
"""

import sys
import os
from datetime import datetime

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(script_dir))))

from scripts.search.eric.eric_api import (
    search_eric,
    get_eric_record_count,
    export_results_to_ris,
)


# fd_review ERIC検索式 (search_formula.md v2 - 2025-12-25)
ERIC_QUERY_BLOCK1 = (
    '(subject:"Medical School Faculty" OR '
    'title:"medical faculty" OR '
    'title:"clinical educator" OR '
    'title:"clinician educator" OR '
    'title:"medical educator" OR '
    'title:"clinical teacher" OR '
    'title:"clinical teaching")'
)

ERIC_QUERY_BLOCK2 = (
    '(subject:"Faculty Development" OR '
    'subject:"Professional Development" OR '
    'subject:"Staff Development" OR '
    'subject:"Program Development" OR '
    'subject:"Program Design" OR '
    'title:"faculty development" OR '
    'title:"professional development" OR '
    'title:"teaching skill" OR '
    'title:"program design")'
)

# Combined query (#3)
ERIC_FINAL_QUERY = f"{ERIC_QUERY_BLOCK1} AND {ERIC_QUERY_BLOCK2}"


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="ERIC検索結果をRIS形式でダウンロードします。"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="projects/fd_review/eric_results",
        help="RISファイルの出力先ディレクトリ"
    )
    args = parser.parse_args()

    # 出力ディレクトリの確認・作成
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    print(f"\n{'='*60}")
    print("ERIC Search Results Download")
    print(f"{'='*60}")
    print(f"Query Block #1: {ERIC_QUERY_BLOCK1}")
    print(f"Query Block #2: {ERIC_QUERY_BLOCK2}")
    print(f"Final Query: #1 AND #2")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    # 件数を取得
    print("Counting results...")
    total_count = get_eric_record_count(ERIC_FINAL_QUERY)
    print(f"Total results: {total_count:,}")
    
    if total_count == 0:
        print("No results found.")
        return 0
    
    # 全件取得（ERICは最大2000件まで）
    print(f"\nRetrieving all {total_count} records...")
    result = search_eric(
        query=ERIC_FINAL_QUERY,
        format='json',
        start=0,
        rows=min(total_count, 2000)  # ERIC API max is 2000
    )
    
    if "Error" in result.message:
        print(f"Error: {result.message}")
        return 1
    
    print(f"Retrieved {len(result.records)} records")
    
    # ファイル名を生成: 日付_件数_eric.ris
    date_str = datetime.now().strftime('%Y%m%d')
    filename = f"{date_str}_{total_count}_eric.ris"
    filepath = os.path.join(args.output_dir, filename)
    
    # RIS形式でエクスポート
    print(f"\nExporting to RIS format...")
    export_results_to_ris(result.records, filepath)
    
    print(f"\n{'='*60}")
    print(f"✅ Download complete!")
    print(f"   File: {filepath}")
    print(f"   Records: {total_count:,}")
    print(f"{'='*60}")
    
    return 0


if __name__ == "__main__":
    exit(main())
