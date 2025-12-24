import requests
import time

pmids = ['35173512', '19811202', '21821215', '38442199', '21869655']

# #2ブロックの各用語
block2_terms = [
    '"Staff Development"[Mesh]',
    '"Program Development"[Mesh]',
    'teaching[MeSH]',
    'faculty development*[tiab]',
    'academic development*[tiab]',
    'faculty training*[tiab]',
    'teacher training*[tiab]',
    'professional development*[tiab]',
    'teaching program*[tiab]',
    'educational program*[tiab]',
    'educator training[tiab]',
    'educator development[tiab]',
    'teacher development[tiab]',
    'teaching workshop*[tiab]',
    'educational workshop*[tiab]',
    'teaching seminar*[tiab]',
    'longitudinal program*[tiab]',
    'peer learning[tiab]',
    'educator competenc*[tiab]',
    'teaching competenc*[tiab]',
    'educational competenc*[tiab]',
    'teaching skill*[tiab]',
    'assessment strateg*[tiab]',
    '"program design"[tiab]',
    '"program evaluation"[tiab]',
    '"program goal*"[tiab]',
    '"program content"[tiab]',
    '"delivery method*"[tiab]',
    '"evaluation approach*"[tiab]'
]

print('# シード論文の#2ブロック用語マッチング分析')
print()

# 各用語の件数とシード論文マッチを分析
results = []
for term in block2_terms:
    time.sleep(0.3)
    # 用語の総件数
    url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&rettype=count&term={requests.utils.quote(term)}'
    resp = requests.get(url)
    import re
    count_match = re.search(r'<Count>(\d+)</Count>', resp.text)
    count = int(count_match.group(1)) if count_match else 0
    
    # シード論文とのマッチ
    matching_pmids = []
    for pmid in pmids:
        time.sleep(0.2)
        test_query = f'{term} AND {pmid}[PMID]'
        url = f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&rettype=count&term={requests.utils.quote(test_query)}'
        resp = requests.get(url)
        if '<Count>1</Count>' in resp.text:
            matching_pmids.append(pmid)
    
    results.append({
        'term': term,
        'count': count,
        'matches': len(matching_pmids),
        'pmids': matching_pmids
    })
    
    short_term = term[:30] + '...' if len(term) > 30 else term
    print(f'{short_term}: {count:,}件, {len(matching_pmids)}論文マッチ')

print()
print('## 削除候補（シード論文にマッチしない用語）')
for r in results:
    if r['matches'] == 0:
        print(f"- `{r['term']}` ({r['count']:,}件)")

print()
print('## 必須用語（シード論文にマッチする用語）')
for r in results:
    if r['matches'] > 0:
        print(f"- `{r['term']}` ({r['count']:,}件) - {r['matches']}論文: {r['pmids']}")
