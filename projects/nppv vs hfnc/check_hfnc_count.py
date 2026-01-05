#!/usr/bin/env python3
"""HFNCの検索式件数確認"""

import requests

query = '''("high flow nasal cannula"[tiab] OR "high flow oxygen therapy"[tiab] OR "nasal high flow therapy"[tiab] OR hfnc[tiab] OR hfno[tiab] OR "heated humidified high flow"[tiab] OR "Precision Flow"[tiab] OR "HVT"[tiab] OR ProSoft[tiab] OR Optiflow[tiab] OR AIRVO[tiab]) AND ("Respiratory Insufficiency"[Mesh] OR "Respiratory Failure"[tiab] OR "Acute respiratory failure"[tiab] OR hypercapnia[Mesh] OR hypercapnia[tiab] OR hypercapnic[tiab])'''

response = requests.get(
    'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi',
    params={'db': 'pubmed', 'term': query, 'retmode': 'json'}
)

result = response.json()['esearchresult']
print(f"検索件数: {result['count']}")
