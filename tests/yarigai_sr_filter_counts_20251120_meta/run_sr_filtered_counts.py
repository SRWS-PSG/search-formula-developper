#!/usr/bin/env python3
"""
#2 Concept Block（医師×やりがい関連語）の統合クエリに
HSLS systematic reviewフィルター（Ovid Medline guide掲載）をANDで適用した
PubMedヒット数（全期間・5年・3年）を取得するスクリプト。

実行例:
    python tests/yarigai_sr_filter_counts_20251120_meta/run_sr_filtered_counts.py
"""

import os
import sys
import time
from typing import Optional

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SCRIPT_PATH = os.path.join(REPO_ROOT, "scripts", "search", "term_validator")

if SCRIPT_PATH not in sys.path:
    sys.path.insert(0, SCRIPT_PATH)

from check_block_overlap import get_pubmed_count  # noqa: E402

# #2 Concept Block全体のクエリ（#2A-#2J のOR結合）
FULL_CONCEPT_QUERY = '''(
    (("Physicians"[Mesh] OR physician*[tiab]) AND "Personal Satisfaction"[Mesh]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "Job Satisfaction"[Mesh]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "Motivation"[Mesh]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "Work Engagement"[Mesh]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "meaningful work"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "work meaningfulness"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "meaningfulness of work"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "meaning in work"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "work meaning"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "sense of meaning"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "work engagement"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND vigor[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND dedication[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND absorption[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "engaged at work"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND calling[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "career calling"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "vocational calling"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND vocation*[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "calling orientation"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "prosocial motivation"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "intrinsic motivation"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "work motivation"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND (motivat*[tiab] AND (work*[tiab] OR job*[tiab] OR career*[tiab] OR professional*[tiab] OR workplace[tiab]))) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "job satisfaction"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "career satisfaction"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "professional satisfaction"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "work satisfaction"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "workplace satisfaction"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "professional fulfillment"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "career fulfillment"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND fulfillment[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "professional well-being"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "professional wellbeing"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND ikigai[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "iki-gai"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND yarigai[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "yari-gai"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND (autonomy[tiab] AND work*[tiab])) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND (competence[tiab] AND work*[tiab])) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND (relatedness[tiab] AND work*[tiab])) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "self-determination"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "task significance"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "work significance"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "job significance"[tiab]) OR
    (("Physicians"[Mesh] OR physician*[tiab]) AND "meaningful work"[tiab])
)'''

OUTPUT_PATH = os.path.join(
    REPO_ROOT,
    "tests",
    "yarigai_sr_filter_counts_20251120_meta",
    "sr_filtered_counts_20251120_hsls.md",
)

SR_FILTER_PATH = os.path.join(REPO_ROOT, "templates", "SR_filter.md")


def load_sr_filter_query(path: str) -> str:
    """
    templates/SR_filter.md からSRフィルタークエリ本体だけを抽出する。

    仕様:
        - クエリは最初に "(" で始まる行から開始
        - 以降、空行または "http" で始まる行までをクエリとして取得
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    start_index = None
    for idx, line in enumerate(lines):
        if line.strip().startswith("("):
            start_index = idx
            break

    if start_index is None:
        raise ValueError("SRフィルターの開始行 '(' を検出できませんでした。")

    end_index = len(lines)
    for idx in range(start_index, len(lines)):
        stripped = lines[idx].strip()
        if stripped == "" or stripped.lower().startswith("http"):
            end_index = idx
            break

    query = "".join(lines[start_index:end_index]).strip()
    if not query:
        raise ValueError("SRフィルタークエリが空です。フォーマットを確認してください。")

    return query


def get_count(query: str, label: str) -> Optional[int]:
    """PubMed APIから該当クエリのヒット数を取得してログを整形。"""
    print(f"{label}...")
    result = get_pubmed_count(query)
    if result.get("success"):
        count = result["count"]
        print(f"   ✓ {count:,} hits")
        return count

    print(f"   ✗ Error: {result.get('message', 'Unknown error')}")
    return None


def write_report(all_time: Optional[int], five_year: Optional[int], three_year: Optional[int], combined_query: str, sr_filter_query: str) -> None:
    """実行結果をMarkdownに保存する。"""
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("# SRフィルター適用後の #2 Concept Block ヒット数\n\n")
        f.write(f"**生成日**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("**検索式概要**:\n")
        f.write("- 医師×やりがい概念 (#2A-#2J のOR)\n")
        f.write("- HSLS LibGuides Ovid MEDLINE Systematic Review フィルター\n")
        f.write("- 出典: https://hsls.libguides.com/Ovid-Medline-search-filters/systematic-reviews\n\n")
        f.write("## ヒット数\n\n")
        f.write("| 期間 | ヒット数 |\n")
        f.write("|------|----------|\n")
        f.write(f"| 全期間 | {all_time:,} |\n" if all_time is not None else "| 全期間 | ERROR |\n")
        f.write(f"| 5年限定 (2021+) | {five_year:,} |\n" if five_year is not None else "| 5年限定 (2021+) | ERROR |\n")
        f.write(f"| 3年限定 (2023+) | {three_year:,} |\n" if three_year is not None else "| 3年限定 (2023+) | ERROR |\n")
        f.write("\n## 使用クエリ\n\n")
        f.write("### Systematic Reviewフィルター\n")
        f.write("```\n")
        f.write(sr_filter_query.strip())
        f.write("\n```\n\n")
        f.write("### AND適用済み統合クエリ（抜粋）\n")
        f.write("```\n")
        f.write(f"{combined_query[:1500]}...\n")
        f.write("```\n")
        f.write("\n※ ブロック行ごとの個別テーブルは今回出力していません。\n")


def main() -> None:
    print("=" * 80)
    print("SRフィルター適用済み #2 Concept Block ヒット数取得")
    print("=" * 80)

    sr_filter_query = load_sr_filter_query(SR_FILTER_PATH)
    combined_query = f"({FULL_CONCEPT_QUERY.strip()}) AND ({sr_filter_query})"

    print("\n[1] 全期間")
    all_time = get_count(combined_query, "   PubMed検索中")

    print("\n[2] 5年限定（2021+）")
    five_year_query = f'{combined_query} AND ("2021"[Date - Publication] : "3000"[Date - Publication])'
    five_year = get_count(five_year_query, "   PubMed検索中")

    print("\n[3] 3年限定（2023+）")
    three_year_query = f'{combined_query} AND ("2023"[Date - Publication] : "3000"[Date - Publication])'
    three_year = get_count(three_year_query, "   PubMed検索中")

    print("\n結果をMarkdownに保存中...")
    write_report(all_time, five_year, three_year, combined_query, sr_filter_query)
    print(f"✓ 完了: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
