#!/usr/bin/env python3
"""更新した検索式でseed trialsがヒットするか確認"""

import requests

# 更新後の最終検索式
query = '''(("high flow nasal cannula"[tiab] OR "high flow oxygen therapy"[tiab] OR "nasal high flow therapy"[tiab] OR "nasal high flow"[tiab] OR hfnc[tiab] OR hfno[tiab] OR "heated humidified high flow"[tiab] OR "Precision Flow"[tiab] OR "HVT"[tiab] OR ProSoft[tiab] OR Optiflow[tiab] OR AIRVO[tiab]) AND ("Respiratory Insufficiency"[Mesh] OR "Respiratory Failure"[tiab] OR "Acute respiratory failure"[tiab] OR hypercapnia[Mesh] OR hypercapnia[tiab] OR hypercapnic[tiab])) AND ((randomized controlled trial[pt] OR controlled clinical trial[pt] OR randomized[tiab] OR placebo[tiab] OR drug therapy[sh] OR randomly[tiab] OR trial[tiab] OR groups[tiab]) NOT (animals[mh] NOT humans[mh]))'''

# 検索実行
response = requests.get(
    'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi',
    params={'db': 'pubmed', 'term': query, 'retmax': 2000, 'retmode': 'json'}
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
output.append(f"検索件数: {count}")
output.append("")
output.append("=== Seed trials確認 ===")
all_found = True
for pmid, name in seed_pmids.items():
    found = pmid in pmids
    if not found:
        all_found = False
    status = "✅ ヒット" if found else "❌ 未ヒット"
    output.append(f"{status}: {name} (PMID: {pmid})")

output.append("")
if all_found:
    output.append("🎉 全てのseed trialsがヒットしました！")
else:
    output.append("⚠️ 一部のseed trialsがヒットしていません")

result_text = "\n".join(output)
print(result_text)

with open("projects/nppv vs hfnc/search_result.txt", "w", encoding="utf-8") as f:
    f.write(result_text)
