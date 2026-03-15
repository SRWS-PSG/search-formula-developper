#!/usr/bin/env python3
"""
全ブロックの検索行について過去3年 (2023年以降) のPubMed件数を取得するスクリプト

出力:
    - tests/three_year_counts_2023plus.md  : 人間向けサマリー
    - tests/three_year_counts_2023plus.json: プログラム用マッピング
"""

import json
import os
import sys
import time
from datetime import datetime
from typing import Dict, List

# scripts 配下を import path に追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../scripts/search/term_validator"))

from check_block_overlap import get_pubmed_count, parse_block_from_text  # noqa: E402

THREE_YEAR_FILTER = '("2023"[Date - Publication] : "3000"[Date - Publication])'

# recount_all_blocks_unified.py と同じブロック定義
BLOCKS: List[Dict[str, str]] = [
    {
        "name": "#1 Population (Physicians only)",
        "query": '''
"Physicians"[Mesh] OR
physician*[tiab]
''',
    },
    {
        "name": "#2A MeSH Terms",
        "query": '''
(("Physicians"[Mesh] OR physician*[tiab]) AND "Personal Satisfaction"[Mesh]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "Job Satisfaction"[Mesh]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "Motivation"[Mesh]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "Work Engagement"[Mesh])
''',
    },
    {
        "name": "#2B Meaningful Work",
        "query": '''
(("Physicians"[Mesh] OR physician*[tiab]) AND "meaningful work"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "work meaningfulness"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "meaningfulness of work"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "meaning in work"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "work meaning"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "sense of meaning"[tiab])
''',
    },
    {
        "name": "#2C Work Engagement",
        "query": '''
(("Physicians"[Mesh] OR physician*[tiab]) AND "work engagement"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND vigor[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND dedication[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND absorption[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "engaged at work"[tiab])
''',
    },
    {
        "name": "#2D Calling/Vocation",
        "query": '''
(("Physicians"[Mesh] OR physician*[tiab]) AND calling[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "career calling"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "vocational calling"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND vocation*[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "calling orientation"[tiab])
''',
    },
    {
        "name": "#2E Motivation",
        "query": '''
(("Physicians"[Mesh] OR physician*[tiab]) AND "prosocial motivation"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "intrinsic motivation"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "work motivation"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND (motivat*[tiab] AND (work*[tiab] OR job*[tiab] OR career*[tiab] OR professional*[tiab] OR workplace[tiab])))
''',
    },
    {
        "name": "#2F Satisfaction",
        "query": '''
(("Physicians"[Mesh] OR physician*[tiab]) AND "job satisfaction"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "career satisfaction"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "professional satisfaction"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "work satisfaction"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "workplace satisfaction"[tiab])
''',
    },
    {
        "name": "#2G Professional Fulfillment",
        "query": '''
(("Physicians"[Mesh] OR physician*[tiab]) AND "professional fulfillment"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "career fulfillment"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND fulfillment[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "professional well-being"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "professional wellbeing"[tiab])
''',
    },
    {
        "name": "#2H Japanese Concepts",
        "query": '''
(("Physicians"[Mesh] OR physician*[tiab]) AND ikigai[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "iki-gai"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND yarigai[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "yari-gai"[tiab])
''',
    },
    {
        "name": "#2I Psychological Needs",
        "query": '''
(("Physicians"[Mesh] OR physician*[tiab]) AND (autonomy[tiab] AND work*[tiab])) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND (competence[tiab] AND work*[tiab])) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND (relatedness[tiab] AND work*[tiab])) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "self-determination"[tiab])
''',
    },
    {
        "name": "#2J Task Significance",
        "query": '''
(("Physicians"[Mesh] OR physician*[tiab]) AND "task significance"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "work significance"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "job significance"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "meaningful work"[tiab])
''',
    },
]


def simplify_term_display(term: str, block_name: str) -> str:
    """recount_all_blocks_unified.py と同じ簡略化処理"""
    population_patterns = [
        '(("Physicians"[Mesh] OR physician*[tiab]) AND ',
        '("Physicians"[Mesh] OR physician*[tiab]) AND ',
    ]
    simplified = term
    for pattern in population_patterns:
        if pattern in simplified:
            simplified = simplified.replace(pattern, "#1 AND ")
            break
    if simplified.startswith("#1 AND "):
        if simplified.endswith(")"):
            simplified = simplified[:-1]
        if simplified.endswith("))"):
            simplified = simplified[:-1]
    return simplified


def _wrap_query(query: str) -> str:
    stripped = query.strip()
    if stripped.startswith("(") and stripped.endswith(")"):
        return stripped
    return f"({stripped})"


def build_filtered_query(query: str) -> str:
    return f"{_wrap_query(query)} AND {THREE_YEAR_FILTER}"


def main() -> None:
    print("=" * 80)
    print("過去3年 (2023+) の件数取得")
    print("=" * 80)
    print()

    all_results: List[Dict] = []

    for block_idx, block in enumerate(BLOCKS, 1):
        block_name = block["name"]
        terms = parse_block_from_text(block["query"])
        print(f"[{block_idx}/{len(BLOCKS)}] {block_name} - {len(terms)} 行")

        for line_no, term in enumerate(terms, 1):
            display_term = simplify_term_display(term, block_name)
            filtered_query = build_filtered_query(term)
            print(f"  L{line_no}: {display_term[:60]}...")

            result = get_pubmed_count(filtered_query)
            count = result.get("count") if result.get("success") else None

            if count is not None:
                print(f"    ✓ 3年限定: {count:,}")
            else:
                print(f"    ✗ ERROR: {result.get('message', 'Unknown error')}")

            all_results.append(
                {
                    "block": block_name,
                    "line": line_no,
                    "term": term.strip(),
                    "display_term": display_term,
                    "three_year_count": count,
                    "query": filtered_query,
                    "success": bool(count is not None),
                    "error": None if count is not None else result.get("message"),
                }
            )

            # API礼儀上の軽い待機
            time.sleep(0.5)

        print()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # JSON
    json_path = "tests/three_year_counts_2023plus.json"
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump({"generated_at": timestamp, "results": all_results}, jf, ensure_ascii=False, indent=2)

    # Markdown
    md_path = "tests/three_year_counts_2023plus.md"
    with open(md_path, "w", encoding="utf-8") as mf:
        mf.write("# 3年限定 (2023年以降) の検索行別件数\n\n")
        mf.write(f"**取得日**: {timestamp}\n\n")
        mf.write("| Block | Line | Term | 3-year (2023+) |\n")
        mf.write("|-------|------|------|----------------|\n")
        for item in all_results:
            term_disp = item["display_term"]
            count_disp = "ERROR" if item["three_year_count"] is None else f"{item['three_year_count']:,}"
            mf.write(f"| {item['block']} | L{item['line']} | `{term_disp}` | {count_disp} |\n")

    print("=" * 80)
    print(f"✓ JSON : {json_path}")
    print(f"✓ Markdown: {md_path}")
    print("=" * 80)


if __name__ == "__main__":
    main()
