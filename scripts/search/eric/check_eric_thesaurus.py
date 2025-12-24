#!/usr/bin/env python3
"""
ERIC Thesaurus CLI Script

ERICシソーラス用語の情報をコマンドラインから取得するスクリプト。

Usage:
    # 単一用語の情報取得
    python scripts/search/eric/check_eric_thesaurus.py -t "Medical School Faculty"
    
    # 関連語を含む検索式を生成
    python scripts/search/eric/check_eric_thesaurus.py -t "Faculty Development" --build-query
    
    # 複数用語を確認
    python scripts/search/eric/check_eric_thesaurus.py --file terms.txt
"""

import argparse
import sys
import os
import time
from datetime import datetime

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(script_dir))))

try:
    from scripts.search.eric.eric_thesaurus import (
        get_thesaurus_info,
        check_term_exists,
        get_related_terms,
        format_thesaurus_info,
        build_search_query_with_related,
        HAS_BS4
    )
except ImportError:
    # Fallback for direct execution
    from eric_thesaurus import (
        get_thesaurus_info,
        check_term_exists,
        get_related_terms,
        format_thesaurus_info,
        build_search_query_with_related,
        HAS_BS4
    )


def main():
    parser = argparse.ArgumentParser(
        description="ERICシソーラス用語の情報を取得します。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  単一用語:    python check_eric_thesaurus.py -t "Medical School Faculty"
  検索式生成:  python check_eric_thesaurus.py -t "Faculty Development" --build-query
  ファイル入力: python check_eric_thesaurus.py --file terms.txt --output results.md
        """
    )
    
    parser.add_argument(
        "-t", "--term",
        type=str,
        help="検索するシソーラス用語"
    )
    
    parser.add_argument(
        "--file",
        type=str,
        help="用語リストファイル (1行1用語)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="結果を保存するファイルパス (.md)"
    )
    
    parser.add_argument(
        "--build-query",
        action="store_true",
        help="関連語を含むERIC検索クエリを生成"
    )
    
    parser.add_argument(
        "--show-related",
        action="store_true",
        help="関連語のみを表示"
    )
    
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="用語の存在確認のみ (簡易出力)"
    )
    
    args = parser.parse_args()
    
    # Check beautifulsoup4
    if not HAS_BS4:
        print("[ERROR] beautifulsoup4 がインストールされていません。")
        print("以下のコマンドでインストールしてください:")
        print("  pip install beautifulsoup4")
        return 1
    
    # Validate arguments
    if not args.term and not args.file:
        parser.error("--term または --file を指定してください")
    
    print(f"\n{'='*60}")
    print(f"ERIC Thesaurus Lookup")
    print(f"{'='*60}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # Get terms to process
    terms = []
    if args.term:
        terms = [args.term]
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            terms = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    results = []
    
    for i, term in enumerate(terms, 1):
        if len(terms) > 1:
            print(f"[{i}/{len(terms)}] Looking up: {term}")
        else:
            print(f"Looking up: {term}")
        
        info = get_thesaurus_info(term)
        results.append(info)
        
        # Check only mode
        if args.check_only:
            status = "✓ EXISTS" if info.exists else "✗ NOT FOUND"
            print(f"  {status}")
            if len(terms) > 1:
                time.sleep(0.5)
            continue
        
        # Show related only
        if args.show_related:
            if info.exists and info.related_terms:
                print(f"  Related Terms ({len(info.related_terms)}):")
                for rt in info.related_terms:
                    print(f"    - {rt}")
            else:
                print("  No related terms found")
            if len(terms) > 1:
                time.sleep(0.5)
            continue
        
        # Build query mode
        if args.build_query:
            print(f"\n  Exists: {'Yes' if info.exists else 'No'}")
            if info.exists:
                query = build_search_query_with_related(term)
                print(f"\n  Generated Query:")
                print(f"  {query}")
            if len(terms) > 1:
                time.sleep(0.5)
            continue
        
        # Full info display
        print()
        print(format_thesaurus_info(info))
        print()
        
        if len(terms) > 1:
            time.sleep(0.5)
    
    # Summary
    if len(terms) > 1:
        found_count = sum(1 for r in results if r.exists)
        print(f"\n{'='*60}")
        print(f"Summary: {found_count}/{len(terms)} terms found in thesaurus")
    
    # Save to file
    if args.output and results:
        _save_results_to_markdown(results, args.output, args)
        print(f"\n[OK] Results saved to: {args.output}")
    
    return 0


def _save_results_to_markdown(results, output_path, args):
    """結果をMarkdownファイルに保存"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# ERIC Thesaurus Lookup Results\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Summary table
        f.write("## Summary\n\n")
        f.write("| Term | Status | Related Terms |\n")
        f.write("|------|--------|---------------|\n")
        
        for info in results:
            status = "✓" if info.exists else "✗"
            related_count = len(info.related_terms) if info.exists else 0
            f.write(f"| {info.term} | {status} | {related_count} |\n")
        
        # Detailed info
        f.write("\n## Details\n\n")
        
        for info in results:
            f.write(f"### {info.term}\n\n")
            
            if not info.exists:
                f.write("**Status**: Not found in thesaurus\n\n")
                continue
            
            f.write("**Status**: Found\n\n")
            
            if info.category:
                f.write(f"**Category**: {info.category}\n\n")
            
            if info.related_terms:
                f.write("**Related Terms**:\n")
                for rt in info.related_terms:
                    f.write(f"- {rt}\n")
                f.write("\n")
            
            if info.used_for:
                f.write(f"**Former Terms**: {', '.join(info.used_for)}\n\n")
            
            # Build query if requested
            if args.build_query:
                query = build_search_query_with_related(info.term)
                f.write(f"**Generated Query**:\n```\n{query}\n```\n\n")


if __name__ == "__main__":
    sys.exit(main())
