#!/usr/bin/env python3
"""Pantazopoulos論文のHFNC関連用語を確認"""

import requests

pmid = '39111544'

# 論文のタイトル・抄録を取得
response = requests.get(
    'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi',
    params={'db': 'pubmed', 'id': pmid, 'rettype': 'abstract', 'retmode': 'text'}
)
print("=== 論文情報 ===")
print(response.text)

# 追加すべき可能性があるターム候補をテスト
print("\n=== 追加候補タームテスト ===")
terms = [
    '"nasal high flow"[tiab]',
    'NHF[tiab]',
    '"high flow"[tiab]',
]
for term in terms:
    query = f'{pmid}[uid] AND {term}'
    r = requests.get(
        'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi',
        params={'db': 'pubmed', 'term': query, 'retmode': 'json'}
    )
    count = int(r.json()['esearchresult']['count'])
    status = "✅" if count > 0 else "❌"
    print(f"{status} {term}: {count}件")
