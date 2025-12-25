#!/usr/bin/env python3
"""ERIC v2検索式の件数確認"""
import sys
sys.path.insert(0, r'c:\Users\youki\codes\search-formula-developper\scripts\search\eric')

from eric_api import get_eric_record_count

# ERIC v2 検索式 (College Faculty を削除)
block1 = '(subject:"Medical School Faculty" OR title:"medical faculty" OR title:"clinical educator" OR title:"clinician educator" OR title:"medical educator" OR title:"clinical teacher" OR title:"clinical teaching")'

block2 = '(subject:"Faculty Development" OR subject:"Professional Development" OR subject:"Staff Development" OR subject:"Program Development" OR subject:"Program Design" OR title:"faculty development" OR title:"professional development" OR title:"teaching skill" OR title:"program design")'

block3 = f'{block1} AND {block2}'

print("ERIC v2 検索式 件数確認")
print("=" * 60)
print("変更点: College Faculty 削除 (医学部focus維持)")
print("=" * 60)

print("\n#1 Target Audience:")
c1 = get_eric_record_count(block1)
print(f"  → {c1:,} hits")

print("\n#2 Intervention:")
c2 = get_eric_record_count(block2)
print(f"  → {c2:,} hits")

print("\n#3 Combined (#1 AND #2):")
c3 = get_eric_record_count(block3)
print(f"  → {c3:,} hits")

# 10年フィルター
block3_10y = f'{block3} AND publicationdateyear:[2015 TO 2025]'
print("\n#4 With 10-Year Filter (2015-2025):")
c4 = get_eric_record_count(block3_10y)
print(f"  → {c4:,} hits")

print("\n" + "=" * 60)
print("サマリー")
print("=" * 60)
print(f"  #3 (all years): {c3:,} hits")
print(f"  #4 (2015-2025): {c4:,} hits")
if c3 > 0:
    print(f"  10年フィルター削減: -{c3 - c4:,} ({(c3 - c4) / c3 * 100:.1f}%)")
