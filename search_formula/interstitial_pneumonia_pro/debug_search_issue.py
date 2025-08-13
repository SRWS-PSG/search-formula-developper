import requests
import time

def test_pubmed_query(query):
    """Test a PubMed query and return hit count"""
    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi'
    params = {
        'db': 'pubmed',
        'term': query,
        'retmax': 0,
        'retmode': 'json'
    }
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return int(data['esearchresult']['count'])
        return -1
    except Exception as e:
        print(f"Error: {e}")
        return -1

def test_pmid_in_query(pmid, query):
    """Test if a specific PMID is captured by a query"""
    combined_query = f"({query}) AND {pmid}[PMID]"
    return test_pubmed_query(combined_query)

simple_query = '("Lung Diseases, Interstitial"[Mesh] OR "ILD"[tiab] OR "interstitial lung disease"[tiab]) AND ("Quality of Life"[Mesh] OR "quality of life"[tiab] OR "patient reported"[tiab])'

print("=== Testing Simple Search Formula ===")
simple_count = test_pubmed_query(simple_query)
print(f"Simple search hits: {simple_count}")

seed_pmids = ['38648021', '35964592', '34559419', '36701677', '38536110', 
              '28213592', '36179385', '39129185', '28487307', '16817954']

print("\n=== Testing Seed PMIDs against Simple Search ===")
captured_pmids = []
for pmid in seed_pmids:
    result = test_pmid_in_query(pmid, simple_query)
    status = "✓" if result > 0 else "✗"
    print(f"PMID {pmid}: {status} ({result})")
    if result > 0:
        captured_pmids.append(pmid)
    time.sleep(0.5)

print(f"\nCaptured {len(captured_pmids)}/{len(seed_pmids)} seed PMIDs")
print(f"Captured PMIDs: {captured_pmids}")

broad_query = '"Lung Diseases, Interstitial"[Mesh] OR "ILD"[tiab] OR "interstitial lung disease"[tiab]'
print(f"\n=== Testing Broader ILD-only Search ===")
broad_count = test_pubmed_query(broad_query)
print(f"Broad ILD search hits: {broad_count}")

print("\n=== Testing Seed PMIDs against ILD-only Search ===")
for pmid in seed_pmids:
    result = test_pmid_in_query(pmid, broad_query)
    status = "✓" if result > 0 else "✗"
    print(f"PMID {pmid}: {status} ({result})")
    time.sleep(0.5)
