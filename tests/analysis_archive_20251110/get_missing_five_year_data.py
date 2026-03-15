#!/usr/bin/env python3
"""
不足している5年限定データを取得

使用方法:
    python3 tests/get_missing_five_year_data.py

取得するクエリ:
    - #2C absorption[tiab]
    - #2E motivat*[tiab] AND (work*[tiab] OR ...)
    - #2F satisfaction[tiab]
    - #2F "workplace satisfaction"[tiab]
    - #2G "career fulfillment"[tiab]
    - #2G fulfillment[tiab]
    - #2G "professional well-being"[tiab]
    - #2G "professional wellbeing"[tiab]
    - #2I (autonomy[tiab] AND work*[tiab])
    - #2I (competence[tiab] AND work*[tiab])
    - #2I (relatedness[tiab] AND work*[tiab])
    - #2I "self-determination"[tiab]
"""

import sys
import os
import time

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../scripts/search/term_validator'))

from check_block_overlap import get_pubmed_count

# 不足しているクエリ（Population条件付き）
MISSING_QUERIES = [
    ('("Physicians"[Mesh] OR physician*[tiab]) AND absorption[tiab]', '#2C L4'),
    ('("Physicians"[Mesh] OR physician*[tiab]) AND (motivat*[tiab] AND (work*[tiab] OR job*[tiab] OR career*[tiab] OR professional*[tiab] OR workplace[tiab]))', '#2E L4'),
    ('("Physicians"[Mesh] OR physician*[tiab]) AND "workplace satisfaction"[tiab]', '#2F L5'),
    ('("Physicians"[Mesh] OR physician*[tiab]) AND "career fulfillment"[tiab]', '#2G L2'),
    ('("Physicians"[Mesh] OR physician*[tiab]) AND fulfillment[tiab]', '#2G L3'),
    ('("Physicians"[Mesh] OR physician*[tiab]) AND "professional well-being"[tiab]', '#2G L4'),
    ('("Physicians"[Mesh] OR physician*[tiab]) AND "professional wellbeing"[tiab]', '#2G L5'),
    ('("Physicians"[Mesh] OR physician*[tiab]) AND (autonomy[tiab] AND work*[tiab])', '#2I L1'),
    ('("Physicians"[Mesh] OR physician*[tiab]) AND (competence[tiab] AND work*[tiab])', '#2I L2'),
    ('("Physicians"[Mesh] OR physician*[tiab]) AND (relatedness[tiab] AND work*[tiab])', '#2I L3'),
    ('("Physicians"[Mesh] OR physician*[tiab]) AND "self-determination"[tiab]', '#2I L4'),
]

def get_five_year_count(query):
    """5年限定（2021年以降）のカウントを取得"""
    # 5年限定フィルターを追加
    query_with_filter = f'({query}) AND ("2021"[Date - Publication] : "3000"[Date - Publication])'

    result = get_pubmed_count(query_with_filter)

    if result.get('success'):
        return result['count']
    else:
        print(f"  [ERROR] {result.get('message', 'Unknown error')}")
        return None

def main():
    print("=" * 80)
    print("不足している5年限定データの取得")
    print("=" * 80)
    print()
    print(f"取得するクエリ数: {len(MISSING_QUERIES)}")
    print()

    results = []

    for i, (query, label) in enumerate(MISSING_QUERIES, 1):
        print(f"[{i}/{len(MISSING_QUERIES)}] {label}")
        print(f"  Query: {query[:80]}...")

        five_year_count = get_five_year_count(query)

        if five_year_count is not None:
            print(f"  ✓ 5年限定: {five_year_count:,} papers")
            results.append({
                'label': label,
                'query': query,
                'five_year_count': five_year_count
            })
        else:
            print(f"  ✗ 取得失敗")

        # API rate limit対策
        if i < len(MISSING_QUERIES):
            print(f"  待機中（1秒）...")
            time.sleep(1)
        print()

    # 結果をファイルに保存
    output_file = "tests/missing_five_year_data_20251110.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 不足していた5年限定データ\n\n")
        f.write(f"**取得日**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("| Label | Query | All-time | 5-year (2021+) |\n")
        f.write("|-------|-------|----------|----------------|\n")

        for r in results:
            # 全期間のデータは統合レポートから取得済み（ここでは省略）
            f.write(f"| {r['label']} | `{r['query'][:60]}...` | - | {r['five_year_count']:,} |\n")

    print()
    print("=" * 80)
    print(f"✓ 完了: {output_file}")
    print("=" * 80)
    print()

    # 結果を表示
    print("取得した5年限定データ:")
    for r in results:
        print(f"  {r['label']}: {r['five_year_count']:,}")

if __name__ == "__main__":
    main()
