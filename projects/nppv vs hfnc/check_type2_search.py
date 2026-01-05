#!/usr/bin/env python3
"""2型呼吸不全に絞った検索式でseed trialsがヒットするか確認"""

import requests

# HFNC block (そのまま)
hfnc_block = '''("high flow nasal cannula"[tiab] OR "high flow oxygen therapy"[tiab] OR "nasal high flow therapy"[tiab] OR hfnc[tiab] OR hfno[tiab] OR "heated humidified high flow"[tiab] OR "Precision Flow"[tiab] OR "HVT"[tiab] OR ProSoft[tiab] OR Optiflow[tiab] OR AIRVO[tiab])'''

# 2型呼吸不全のみ (hypercapnia関連のみ)
type2_block = '''(hypercapnia[Mesh] OR hypercapnia[tiab] OR hypercapnic[tiab])'''

# 完全な検索式
query = f'{hfnc_block} AND {type2_block}'

# 検索実行
response = requests.get(
    'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi',
    params={'db': 'pubmed', 'term': query, 'retmax': 1000, 'retmode': 'json'}
)
result = response.json()['esearchresult']
count = int(result['count'])
pmids = result.get('idlist', [])

# seed.txtからPMIDを読み込み
seed_pmids = {
    '39657981': 'JAMA 2025 - BRIC-NET',
    '39111544': 'Respir Med 2024 - Pantazopoulos'
}

output = []
output.append("=== 検索式 ===")
output.append(query)
output.append("")
output.append(f"検索件数: {count}")
output.append("")
output.append("=== Seed trials確認 ===")
for pmid, name in seed_pmids.items():
    found = "✅ ヒット" if pmid in pmids else "❌ 未ヒット"
    output.append(f"{found}: {name} (PMID: {pmid})")

result_text = "\n".join(output)
print(result_text)

with open("projects/nppv vs hfnc/search_result.txt", "w", encoding="utf-8") as f:
    f.write(result_text)
