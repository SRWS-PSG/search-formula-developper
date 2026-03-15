#!/usr/bin/env python3
"""
#2 Concept Block全体（ORで結合）のヒット数を取得

使用方法:
    python3 tests/get_final_concept_block_count.py
"""

import sys
import os
import time

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../scripts/search/term_validator'))

from check_block_overlap import get_pubmed_count

# #2 Concept Block全体のクエリ（すべてのブロック #2A-#2J をORで結合）
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

def get_count(query, label):
    """カウントを取得"""
    print(f"{label}...")
    result = get_pubmed_count(query)

    if result.get('success'):
        count = result['count']
        print(f"  ✓ {count:,} papers")
        return count
    else:
        print(f"  ✗ エラー: {result.get('message', 'Unknown error')}")
        return None

def main():
    print("=" * 80)
    print("#2 Concept Block 全体のヒット数取得")
    print("=" * 80)
    print()

    # 1. 全期間
    print("1. 全期間（All-time）")
    all_time_count = get_count(FULL_CONCEPT_QUERY, "  検索中")
    print()

    # 2. 5年限定（2021年以降）
    print("2. 5年限定（2021年以降）")
    five_year_query = f'{FULL_CONCEPT_QUERY} AND ("2021"[Date - Publication] : "3000"[Date - Publication])'
    five_year_count = get_count(five_year_query, "  検索中")
    print()

    # 3. 3年限定（2023年以降）
    print("3. 3年限定（2023年以降）")
    three_year_query = f'{FULL_CONCEPT_QUERY} AND ("2023"[Date - Publication] : "3000"[Date - Publication])'
    three_year_count = get_count(three_year_query, "  検索中")
    print()

    # 結果をファイルに保存
    output_file = "tests/final_concept_block_count_20251110.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# #2 Concept Block 全体のヒット数\n\n")
        f.write(f"**取得日**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## 結果\n\n")
        f.write("| 期間 | ヒット数 |\n")
        f.write("|------|----------|\n")

        if all_time_count is not None:
            f.write(f"| 全期間 | {all_time_count:,} |\n")
        else:
            f.write(f"| 全期間 | ERROR |\n")

        if five_year_count is not None:
            f.write(f"| 5年限定 (2021+) | {five_year_count:,} |\n")
        else:
            f.write(f"| 5年限定 (2021+) | ERROR |\n")

        if three_year_count is not None:
            f.write(f"| 3年限定 (2023+) | {three_year_count:,} |\n")
        else:
            f.write(f"| 3年限定 (2023+) | ERROR |\n")

        f.write("\n## 内訳\n\n")
        f.write("このクエリは以下のブロックをORで結合したものです：\n\n")
        f.write("- #2A MeSH Terms (4個)\n")
        f.write("- #2B Meaningful Work (6個)\n")
        f.write("- #2C Work Engagement (5個)\n")
        f.write("- #2D Calling/Vocation (5個)\n")
        f.write("- #2E Motivation (4個)\n")
        f.write("- #2F Satisfaction (6個)\n")
        f.write("- #2G Professional Fulfillment (5個)\n")
        f.write("- #2H Japanese Concepts (4個)\n")
        f.write("- #2I Psychological Needs (4個)\n")
        f.write("- #2J Task Significance (4個)\n")
        f.write("\n**合計**: 47個の検索語をORで結合\n")

    print("=" * 80)
    print(f"✓ 完了: {output_file}")
    print("=" * 80)
    print()

    # 結果サマリー
    print("結果サマリー:")
    if all_time_count is not None:
        print(f"  全期間: {all_time_count:,} papers")
    if five_year_count is not None:
        print(f"  5年限定: {five_year_count:,} papers")
    if three_year_count is not None:
        print(f"  3年限定: {three_year_count:,} papers")
    if all_time_count and five_year_count:
        pct5 = (five_year_count / all_time_count) * 100
        print(f"  5年間の割合: {pct5:.1f}%")
    if all_time_count and three_year_count:
        pct3 = (three_year_count / all_time_count) * 100
        print(f"  3年間の割合: {pct3:.1f}%")

if __name__ == "__main__":
    main()
