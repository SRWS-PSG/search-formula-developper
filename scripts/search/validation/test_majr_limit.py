#!/usr/bin/env python3
"""Majr限定テスト - シンプル版"""
import requests
import time
import xml.etree.ElementTree as ET
import os

api_key = os.environ.get('NCBI_API_KEY')
base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'

def get_count(query):
    params = {'db': 'pubmed', 'term': query, 'retmode': 'xml', 'retmax': 0}
    if api_key:
        params['api_key'] = api_key
    time.sleep(0.4)
    try:
        r = requests.get(base_url, params=params, timeout=30)
        root = ET.fromstring(r.content)
        count = root.find('.//Count')
        return int(count.text) if count is not None else 0
    except Exception as e:
        print(f"Error: {e}")
        return -1

# 検索式
block1_mesh = '"Faculty, Medical"[Mesh] OR medical faculty[tiab] OR clinical educator*[tiab] OR clinician educator*[tiab] OR medical educator*[tiab] OR clinical teacher*[tiab] OR clinical teaching[tiab]'
block1_majr = '"Faculty, Medical"[Majr] OR medical faculty[tiab] OR clinical educator*[tiab] OR clinician educator*[tiab] OR medical educator*[tiab] OR clinical teacher*[tiab] OR clinical teaching[tiab]'
block2 = '"Staff Development"[Mesh] OR faculty development*[tiab] OR professional development*[tiab] OR teaching skill*[tiab] OR "program design"[tiab]'
seeds = ['35173512', '19811202', '21821215', '38442199', '21869655']

print("=" * 60)
print("Majr限定テスト")
print("=" * 60)

# #1比較
print("\n#1単独:")
c1_mesh = get_count(block1_mesh)
print(f"  [Mesh]: {c1_mesh:,}")
c1_majr = get_count(block1_majr)
print(f"  [Majr]: {c1_majr:,}")
if c1_mesh > 0:
    print(f"  削減: {c1_mesh - c1_majr:,} ({(c1_mesh - c1_majr)/c1_mesh*100:.1f}%)")

# #3比較
print("\n#3 (AND結合):")
c3_mesh = get_count(f"({block1_mesh}) AND ({block2})")
print(f"  [Mesh]: {c3_mesh:,}")
c3_majr = get_count(f"({block1_majr}) AND ({block2})")
print(f"  [Majr]: {c3_majr:,}")
if c3_mesh > 0:
    print(f"  削減: {c3_mesh - c3_majr:,} ({(c3_mesh - c3_majr)/c3_mesh*100:.1f}%)")

# シード論文チェック
print("\nシード論文チェック (Majr版):")
all_ok = True
for pmid in seeds:
    c = get_count(f'({block1_majr}) AND ({block2}) AND {pmid}[pmid]')
    status = "✓" if c > 0 else "✗"
    if c == 0:
        all_ok = False
    print(f"  {pmid}: {status}")

print("\n" + "=" * 60)
print("結果: " + ("100%捕捉 ✓" if all_ok else "取りこぼしあり ✗"))
