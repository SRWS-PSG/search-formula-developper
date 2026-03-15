#!/usr/bin/env python3
"""
ERIC API CLI Search Script

ERIC (Education Resources Information Center) データベースを
コマンドラインから検索するスクリプト。

Usage:
    # 基本検索
    python scripts/search/eric/search_eric.py --query "medical education"
    
    # peer-reviewed のみ (フラグ使用)
    python scripts/search/eric/search_eric.py --query "medical education" --peer-reviewed
    
    # 年代指定
    python scripts/search/eric/search_eric.py --query "faculty development" --year-min 2020
    
    # フルテキスト利用可能のみ
    python scripts/search/eric/search_eric.py --query "reading" --fulltext
    
    # IES助成研究のみ
    python scripts/search/eric/search_eric.py --query "reading" --ies-funded
    
    # WWCレビュー済みのみ
    python scripts/search/eric/search_eric.py --query "reading" --wwc-reviewed y
    
    # シソーラス + フリーワード複合検索
    python scripts/search/eric/search_eric.py --query 'subject:"Medical School Faculty" AND burnout'
    
    # RIS出力
    python scripts/search/eric/search_eric.py --query "faculty development" --output results.ris
"""

import argparse
import sys
import os
import json
from datetime import datetime

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(script_dir))))

from scripts.search.eric.eric_api import (
    search_eric,
    get_eric_record_count,
    export_results_to_ris,
    format_record_for_display
)


def main():
    parser = argparse.ArgumentParser(
        description="ERIC (Education Resources Information Center) データベースを検索します。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
検索クエリの例:
  基本検索:           "medical education"
  タイトル検索:       title:"faculty development"
  シソーラス検索:     subject:"Medical School Faculty"
  著者検索:           author:"Smith, John"
  peer-reviewed:      peerreviewed:T
  年指定:             publicationdateyear:2023
  複合検索:           subject:"Medical School Faculty" AND burnout
        """
    )
    
    parser.add_argument(
        "-q", "--query",
        type=str,
        required=True,
        help="検索クエリ"
    )
    
    parser.add_argument(
        "-f", "--format",
        type=str,
        choices=["json", "xml", "csv"],
        default="json",
        help="レスポンス形式 (デフォルト: json)"
    )
    
    parser.add_argument(
        "-s", "--start",
        type=int,
        default=0,
        help="開始レコード番号 (ページネーション用, デフォルト: 0)"
    )
    
    parser.add_argument(
        "-r", "--rows",
        type=int,
        default=20,
        help="取得件数 (1-2000, デフォルト: 20)"
    )
    
    parser.add_argument(
        "--fields",
        type=str,
        default=None,
        help="取得フィールド (カンマ区切り, 例: id,title,author,subject)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="出力ファイルパス (.ris または .json)"
    )
    
    parser.add_argument(
        "--count-only",
        action="store_true",
        help="件数のみ表示"
    )
    
    parser.add_argument(
        "--json-output",
        action="store_true",
        help="結果をJSON形式で出力"
    )
    
    # New filter options
    parser.add_argument(
        "--peer-reviewed",
        action="store_true",
        help="Peer-reviewed論文のみを検索"
    )
    
    parser.add_argument(
        "--fulltext",
        action="store_true",
        help="フルテキスト利用可能な論文のみを検索"
    )
    
    parser.add_argument(
        "--ies-funded",
        action="store_true",
        help="IES助成研究のみを検索"
    )
    
    parser.add_argument(
        "--wwc-reviewed",
        type=str,
        choices=["y", "r", "n"],
        default=None,
        help="WWCレビュー済みを検索 (y=Meets Standards, r=With Reservations, n=Does Not Meet)"
    )
    
    parser.add_argument(
        "--year-min",
        type=int,
        default=None,
        help="最小出版年 (例: 2020)"
    )
    
    parser.add_argument(
        "--year-max",
        type=int,
        default=None,
        help="最大出版年 (例: 2025)"
    )
    
    args = parser.parse_args()
    
    # Parse fields if provided
    fields = None
    if args.fields:
        fields = [f.strip() for f in args.fields.split(',')]
    
    # Build query with filters
    query = args.query
    filters_applied = []
    
    if args.peer_reviewed:
        query = f'({query}) AND peerreviewed:T'
        filters_applied.append('Peer-reviewed')
    
    if args.fulltext:
        query = f'({query}) AND e_fulltextauth:T'
        filters_applied.append('Fulltext')
    
    if args.ies_funded:
        query = f'({query}) AND funded:y'
        filters_applied.append('IES Funded')
    
    if args.wwc_reviewed:
        query = f'({query}) AND wwcr:{args.wwc_reviewed}'
        wwc_labels = {'y': 'Meets Standards', 'r': 'With Reservations', 'n': 'Does Not Meet'}
        filters_applied.append(f'WWC: {wwc_labels[args.wwc_reviewed]}')
    
    # Year filters using publicationdateyear range syntax
    if args.year_min or args.year_max:
        min_val = str(args.year_min) if args.year_min else '*'
        max_val = str(args.year_max) if args.year_max else '*'
        date_filter = f'publicationdateyear:[{min_val} TO {max_val}]'
        query = f'({query}) AND {date_filter}'
        if args.year_min and args.year_max:
            filters_applied.append(f'Year: {args.year_min}-{args.year_max}')
        elif args.year_min:
            filters_applied.append(f'Year >= {args.year_min}')
        else:
            filters_applied.append(f'Year <= {args.year_max}')
    
    print(f"\n{'='*60}")
    print(f"ERIC Search")
    print(f"{'='*60}")
    print(f"Query: {args.query}")
    if filters_applied:
        print(f"Filters: {', '.join(filters_applied)}")
    print(f"Final Query: {query}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # Count only mode
    if args.count_only:
        count = get_eric_record_count(query)
        print(f"Total results: {count:,}")
        return 0
    
    # Execute search
    result = search_eric(
        query=query,
        format=args.format,
        start=args.start,
        rows=args.rows,
        fields=fields
    )
    
    # Check for errors
    if "Error" in result.message:
        print(f"[ERROR] {result.message}")
        return 1
    
    # Display summary
    print(f"Total results: {result.total_count:,}")
    print(f"Showing: {result.start + 1} - {result.start + len(result.records)} of {result.total_count}")
    
    if args.format != 'json':
        # Raw format output
        print(f"\n{result.records[0].get('raw_response', 'No response')}")
        return 0
    
    # JSON output mode
    if args.json_output:
        output_data = {
            "query": result.query,
            "total_count": result.total_count,
            "start": result.start,
            "rows": len(result.records),
            "records": result.records
        }
        print(json.dumps(output_data, indent=2, ensure_ascii=False))
        return 0
    
    # Display records (skip display if output file is specified to avoid encoding errors)
    if not args.output:
        print(f"\n{'-'*60}\n")

        for i, rec in enumerate(result.records, 1):
            try:
                print(f"[{result.start + i}] {format_record_for_display(rec)}")
                print()
            except UnicodeEncodeError:
                print(f"[{result.start + i}] [Record contains special characters - see output file]")
                print()

    # Export to file if requested
    if args.output:
        output_path = args.output
        
        if output_path.endswith('.ris'):
            export_results_to_ris(result.records, output_path)
            print(f"\n[OK] RISファイルを保存しました: {output_path}")
        elif output_path.endswith('.json'):
            output_data = {
                "query": result.query,
                "total_count": result.total_count,
                "start": result.start,
                "rows": len(result.records),
                "records": result.records,
                "exported_at": datetime.now().isoformat()
            }
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            print(f"\n[OK] JSONファイルを保存しました: {output_path}")
        else:
            print(f"\n[WARNING] 未対応の出力形式です。.ris または .json を指定してください。")
    
    # Pagination hint
    if result.total_count > result.start + len(result.records):
        next_start = result.start + args.rows
        print(f"\n[INFO] 次のページを取得するには: --start {next_start}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
