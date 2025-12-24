#!/usr/bin/env python3
"""
Test ERIC search with 10-year filter (2015-2025)
"""
import sys
sys.path.insert(0, '.')
from scripts.search.eric.eric_api import get_eric_record_count

block1 = '(subject:"Medical School Faculty" OR subject:"College Faculty" OR title:"medical faculty" OR title:"clinical educator" OR title:"clinician educator" OR title:"medical educator" OR title:"clinical teacher" OR title:"clinical teaching")'

block2 = '(subject:"Faculty Development" OR subject:"Professional Development" OR subject:"Staff Development" OR subject:"Program Development" OR subject:"Program Design" OR title:"faculty development" OR title:"professional development" OR title:"teaching skill" OR title:"program design")'

combined = f'{block1} AND {block2}'

# Test different date filter syntaxes
print("=" * 60)
print("ERIC 10-Year Filter Test (2015-2025)")
print("=" * 60)

print(f"\nCombined (all years): {get_eric_record_count(combined):,}")

# Try different date filter formats
date_filters = [
    'publicationdateyear:[2015 TO 2025]',
    'publicationdateyear:2015-2025',
    'publicationdateyear:[2015 TO *]',
]

for df in date_filters:
    query = f'{combined} AND {df}'
    count = get_eric_record_count(query)
    print(f"With {df}: {count:,}")

print("\n" + "=" * 60)
