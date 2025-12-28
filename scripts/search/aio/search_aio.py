#!/usr/bin/env python3
"""
AIO (Anthropological Index Online) CLI Search Script

Usage:
    # Basic search (quick search)
    python search_aio.py --keyword "autoethnography"
    
    # Count only
    python search_aio.py --keyword "autoethnography" --count-only
    
    # Save RIS output
    python search_aio.py --keyword "autoethnography" --output results.ris
    
    # Specify decades
    python search_aio.py --keyword "autoethnography" --decades recent
"""

import sys
import os
import argparse
from pathlib import Path

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(script_dir))))

from scripts.search.aio.aio_client import AIOClient


def main():
    parser = argparse.ArgumentParser(
        description="Search Anthropological Index Online (AIO)"
    )
    parser.add_argument(
        "--keyword", "-k",
        required=True,
        help="Search keyword"
    )
    parser.add_argument(
        "--decades", "-d",
        nargs="+",
        default=["all"],
        help="Decades filter (e.g., recent, all, 1950, 1960, ...)"
    )
    parser.add_argument(
        "--sort", "-s",
        choices=["year_d", "year_a", "title_a", "title_d"],
        default="year_d",
        help="Sort order (default: year_d)"
    )
    parser.add_argument(
        "--filter", "-f",
        choices=["*", "Article", "Film"],
        default="*",
        help="Filter type (default: *)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path (RIS format)"
    )
    parser.add_argument(
        "--count-only", "-c",
        action="store_true",
        help="Only show result count"
    )
    parser.add_argument(
        "--format",
        choices=["ris", "csv", "html", "endnote"],
        default="ris",
        help="Output format (default: ris)"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Delay between requests in seconds (default: 2.0)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("AIO (Anthropological Index Online) Search")
    print("=" * 60)
    print(f"Keyword: {args.keyword}")
    print(f"Decades: {args.decades}")
    print(f"Sort: {args.sort}")
    print(f"Filter: {args.filter}")
    print("-" * 60)
    
    try:
        client = AIOClient(delay_sec=args.delay)
        
        # Execute search
        print("Executing search...")
        results_id = client.quick_search(
            keyword=args.keyword,
            decades=args.decades,
            sort=args.sort,
            filter_type=args.filter
        )
        print(f"Results ID: {results_id}")
        
        # Download results
        print(f"Downloading results ({args.format})...")
        data = client.download_results(
            results_id=results_id,
            mimetype=args.format
        )
        
        # Get count
        if args.format == "ris":
            count = client.get_result_count_from_ris(data)
            print(f"\nResults: {count:,} records")
        
        # Output
        if args.count_only:
            return 0
        
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(data, encoding="utf-8")
            print(f"\nSaved to: {output_path}")
        else:
            # Show first few lines
            lines = data.split("\n")[:30]
            print("\n--- Preview (first 30 lines) ---")
            for line in lines:
                print(line)
            if len(data.split("\n")) > 30:
                print("...")
        
        print("\n" + "=" * 60)
        print("Search completed successfully")
        return 0
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
