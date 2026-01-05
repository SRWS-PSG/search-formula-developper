#!/usr/bin/env python3
"""Pantazopoulos論文がなぜヒットしないか調査"""

import requests

# Pantazopoulos論文の詳細を取得
pmid = '39111544'

# 論文のタイトル・抄録を取得
response = requests.get(
    'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi',
    params={'db': 'pubmed', 'id': pmid, 'rettype': 'abstract', 'retmode': 'text'}
)
print("=== 論文情報 ===")
print(response.text[:2000])

# 各ブロックで個別にヒットするか確認
print("\n=== 各ブロックでの検索確認 ===")

blocks = {
    "HFNC block": '("high flow nasal cannula"[tiab] OR "high flow oxygen therapy"[tiab] OR "nasal high flow therapy"[tiab] OR hfnc[tiab] OR hfno[tiab] OR "heated humidified high flow"[tiab] OR "Precision Flow"[tiab] OR "HVT"[tiab] OR ProSoft[tiab] OR Optiflow[tiab] OR AIRVO[tiab])',
    "呼吸不全 block": '("Respiratory Insufficiency"[Mesh] OR "Respiratory Failure"[tiab] OR "Acute respiratory failure"[tiab] OR hypercapnia[Mesh] OR hypercapnia[tiab] OR hypercapnic[tiab])',
    "RCT filter": '((randomized controlled trial[pt] OR controlled clinical trial[pt] OR randomized[tiab] OR placebo[tiab] OR drug therapy[sh] OR randomly[tiab] OR trial[tiab] OR groups[tiab]) NOT (animals[mh] NOT humans[mh]))',
}

for name, block in blocks.items():
    query = f'{pmid}[uid] AND {block}'
    r = requests.get(
        'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi',
        params={'db': 'pubmed', 'term': query, 'retmode': 'json'}
    )
    count = int(r.json()['esearchresult']['count'])
    status = "✅" if count > 0 else "❌"
    print(f"{status} {name}: {count}件")
