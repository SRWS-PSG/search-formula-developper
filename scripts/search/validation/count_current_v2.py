#!/usr/bin/env python3
"""現在の検索式の件数を測定"""
import requests
import time
import xml.etree.ElementTree as ET
import os

api_key = os.environ.get('NCBI_API_KEY')

def get_count(query):
    params = {'db': 'pubmed', 'term': query, 'retmode': 'xml', 'retmax': 0}
    if api_key:
        params['api_key'] = api_key
    time.sleep(0.4)
    r = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi', params=params, timeout=30)
    root = ET.fromstring(r.content)
    count = root.find('.//Count')
    return int(count.text) if count is not None else 0

# 現在の検索式 (v2: Majr + Program Development維持)
block1 = '"Faculty, Medical"[Majr] OR medical faculty[tiab] OR clinical educator*[tiab] OR clinician educator*[tiab] OR medical educator*[tiab] OR clinical teacher*[tiab] OR clinical teaching[tiab]'
block2 = '"Staff Development"[Mesh] OR "Program Development"[Mesh] OR faculty development*[tiab] OR professional development*[tiab] OR teaching skill*[tiab] OR "program design"[tiab]'

print("現在の検索式 (v2) 件数測定")
print("=" * 50)

c3 = get_count(f"({block1}) AND ({block2})")
print(f"#3 (Majr + Program Development): {c3:,} hits")

# シード論文確認
seeds = ['35173512', '19811202', '21821215', '38442199', '21869655']
print("\nシード論文チェック:")
all_ok = True
for pmid in seeds:
    c = get_count(f'({block1}) AND ({block2}) AND {pmid}[pmid]')
    status = "✓" if c > 0 else "✗"
    if c == 0:
        all_ok = False
    print(f"  {pmid}: {status}")

print("\n" + "=" * 50)
print("結果: " + ("100%捕捉 ✓" if all_ok else "取りこぼしあり ✗"))
