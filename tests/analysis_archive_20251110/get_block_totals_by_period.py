#!/usr/bin/env python3
"""
#2各ブロックの総ヒット数を期間別（全期間／5年／3年）で取得し、集計ファイルを出力する。
"""

import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../scripts/search/term_validator"))
from check_block_overlap import get_pubmed_count  # noqa: E402

DATE_FILTERS = {
    "all": None,
    "5y": '("2021"[Date - Publication] : "3000"[Date - Publication])',
    "3y": '("2023"[Date - Publication] : "3000"[Date - Publication])',
}

BLOCKS = [
    (
        "#2A MeSH Terms",
        '''
(("Physicians"[Mesh] OR physician*[tiab]) AND "Personal Satisfaction"[Mesh]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "Job Satisfaction"[Mesh]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "Motivation"[Mesh]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "Work Engagement"[Mesh])
''',
    ),
    (
        "#2B Meaningful Work",
        '''
(("Physicians"[Mesh] OR physician*[tiab]) AND "meaningful work"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "work meaningfulness"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "meaningfulness of work"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "meaning in work"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "work meaning"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "sense of meaning"[tiab])
''',
    ),
    (
        "#2C Work Engagement",
        '''
(("Physicians"[Mesh] OR physician*[tiab]) AND "work engagement"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND vigor[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND dedication[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND absorption[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "engaged at work"[tiab])
''',
    ),
    (
        "#2D Calling/Vocation",
        '''
(("Physicians"[Mesh] OR physician*[tiab]) AND calling[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "career calling"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "vocational calling"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND vocation*[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "calling orientation"[tiab])
''',
    ),
    (
        "#2E Motivation",
        '''
(("Physicians"[Mesh] OR physician*[tiab]) AND "prosocial motivation"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "intrinsic motivation"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "work motivation"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND (motivat*[tiab] AND (work*[tiab] OR job*[tiab] OR career*[tiab] OR professional*[tiab] OR workplace[tiab])))
''',
    ),
    (
        "#2F Satisfaction",
        '''
(("Physicians"[Mesh] OR physician*[tiab]) AND "job satisfaction"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "career satisfaction"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "professional satisfaction"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "work satisfaction"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "workplace satisfaction"[tiab])
''',
    ),
    (
        "#2G Professional Fulfillment",
        '''
(("Physicians"[Mesh] OR physician*[tiab]) AND "professional fulfillment"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "career fulfillment"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND fulfillment[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "professional well-being"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "professional wellbeing"[tiab])
''',
    ),
    (
        "#2H Japanese Concepts",
        '''
(("Physicians"[Mesh] OR physician*[tiab]) AND ikigai[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "iki-gai"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND yarigai[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "yari-gai"[tiab])
''',
    ),
    (
        "#2I Psychological Needs",
        '''
(("Physicians"[Mesh] OR physician*[tiab]) AND (autonomy[tiab] AND work*[tiab])) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND (competence[tiab] AND work*[tiab])) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND (relatedness[tiab] AND work*[tiab])) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "self-determination"[tiab])
''',
    ),
    (
        "#2J Task Significance",
        '''
(("Physicians"[Mesh] OR physician*[tiab]) AND "task significance"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "work significance"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "job significance"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "meaningful work"[tiab])
''',
    ),
]


def build_query(base: str, filter_clause: str | None) -> str:
    base_clean = base.strip()
    if not base_clean.startswith("("):
        base_clean = f"({base_clean})"
    if filter_clause:
        return f"{base_clean} AND {filter_clause}"
    return base_clean


def main():
    results = []
    for block_name, query in BLOCKS:
        block_entry = {"block": block_name, "queries": {}}
        for label, filter_clause in DATE_FILTERS.items():
            actual_query = build_query(query, filter_clause)
            res = get_pubmed_count(actual_query)
            if not res.get("success"):
                raise RuntimeError(f"{block_name} {label} failed: {res['message']}")
            block_entry["queries"][label] = res["count"]
        results.append(block_entry)

    payload = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data": results,
    }

    json_path = "tests/block_totals_by_period.json"
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(payload, jf, ensure_ascii=False, indent=2)

    md_path = "tests/block_totals_by_period.md"
    with open(md_path, "w", encoding="utf-8") as mf:
        mf.write("# #2 ブロック別 総ヒット数 (期間比較)\n\n")
        mf.write(f"**取得日**: {payload['generated_at']}\n\n")
        mf.write("| Block | All-time | 5y (2021+) | 3y (2023+) |\n")
        mf.write("|-------|----------|-------------|------------|\n")
        for block_entry in results:
            q = block_entry["queries"]
            mf.write(
                f"| {block_entry['block']} | {q['all']:,} | {q['5y']:,} | {q['3y']:,} |\n"
            )

    print("✓ block totals saved:", json_path, md_path)


if __name__ == "__main__":
    main()
