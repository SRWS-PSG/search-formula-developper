#!/usr/bin/env python3
"""検索式の各タームを個別に検証"""

import requests
import time

def get_count(term):
    """PubMedで検索件数を取得"""
    response = requests.get(
        'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi',
        params={'db': 'pubmed', 'term': term, 'retmode': 'json'}
    )
    return int(response.json()['esearchresult']['count'])

# HFNC関連タームs
hfnc_terms = [
    '"high flow nasal cannula"[tiab]',
    '"high flow oxygen therapy"[tiab]',
    '"nasal high flow therapy"[tiab]',
    'hfnc[tiab]',
    'hfno[tiab]',
    '"heated humidified high flow"[tiab]',
    '"Precision Flow"[tiab]',
    '"HVT"[tiab]',
    'ProSoft[tiab]',
    'Optiflow[tiab]',
    'AIRVO[tiab]',
]

# 呼吸不全関連ターム
respiratory_terms = [
    '"Respiratory Insufficiency"[Mesh]',
    '"Respiratory Failure"[tiab]',
    '"Acute respiratory failure"[tiab]',
    'hypercapnia[Mesh]',
    'hypercapnia[tiab]',
    'hypercapnic[tiab]',
]

results = []
results.append("=== HFNC関連ターム ===")
for term in hfnc_terms:
    count = get_count(term)
    status = " ⚠️ 0件!" if count == 0 else ""
    results.append(f"{count:>8} : {term}{status}")
    time.sleep(0.35)

results.append("")
results.append("=== 呼吸不全関連ターム ===")
for term in respiratory_terms:
    count = get_count(term)
    status = " ⚠️ 0件!" if count == 0 else ""
    results.append(f"{count:>8} : {term}{status}")
    time.sleep(0.35)

output = "\n".join(results)
print(output)

# ファイルにも保存
with open("projects/nppv vs hfnc/term_counts.txt", "w", encoding="utf-8") as f:
    f.write(output)
