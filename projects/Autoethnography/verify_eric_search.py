#!/usr/bin/env python3
"""ERIC Autoethnography Search - Test different queries"""
import sys
sys.path.insert(0, r'c:\Users\youki\codes\search-formula-developper\scripts\search\eric')

from eric_api import get_eric_record_count

print("ERIC Autoethnography Query Testing")
print("=" * 60)

# Test different query formats
queries = [
    ("autoethnograph* (truncation)", "autoethnograph*"),
    ("autoethnography (exact)", "autoethnography"),
    ("autoethnographic", "autoethnographic"),
    ("title:autoethnography", "title:autoethnography"),
    ("abstract:autoethnography", "abstract:autoethnography"),
    ("keyword:autoethnography", "autoethnography"),
    ("ethnograph*", "ethnograph*"),
]

for label, query in queries:
    try:
        count = get_eric_record_count(query)
        print(f"{label}: {count:,} hits")
    except Exception as e:
        print(f"{label}: ERROR - {e}")

print("\n" + "=" * 60)
print("Testing combined queries")
print("=" * 60)

# Try simpler combined query
block1 = "autoethnography"
block2 = 'subject:"Medical Education"'
combined = f'{block1} AND {block2}'

print(f"\nautoethnography alone: {get_eric_record_count(block1):,}")
print(f'subject:"Medical Education" alone: {get_eric_record_count(block2):,}')
print(f"Combined: {get_eric_record_count(combined):,}")
