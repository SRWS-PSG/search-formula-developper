import requests
import time

pmids = ['35173512', '38442199']

print('=== NG論文のMeSH詳細確認 ===')
print()

for pmid in pmids:
    time.sleep(0.4)
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&rettype=medline&retmode=text'
    resp = requests.get(url)
    text = resp.text
    
    # タイトルを抽出
    title = ''
    for line in text.split('\n'):
        if line.startswith('TI  - '):
            title = line[6:]
            break
    
    # MeSH termsを抽出
    mesh_terms = []
    for line in text.split('\n'):
        if line.startswith('MH  - '):
            mesh_terms.append(line[6:])
    
    print(f'PMID: {pmid}')
    print(f'Title: {title}')
    print(f'MeSH Terms ({len(mesh_terms)}):')
    for term in mesh_terms:
        print(f'  - {term}')
    print()
