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

queries = [
    ('Block 8 (ILD)', '"Lung Diseases, Interstitial"[Mesh] OR ("Interstitial"[tiab] AND ("lung"[tiab] OR "lungs"[tiab] OR "pulmonary"[tiab] OR "pneumonia"[tiab] OR "pneumonitis"[tiab])) OR "ILD"[tiab]'),
    ('Block 13 (Progression)', '"Disease Progression"[Mesh] OR ("acute"[tiab] AND ("exacerbation"[tiab] OR "exacerbations"[tiab]))'),
    ('Block 20 (Symptoms)', '"Dyspnea"[Mesh] OR "dyspnea"[tiab] OR "Cough"[Mesh] OR "cough"[tiab] OR "Fatigue"[Mesh] OR "fatigue"[tiab]'),
    ('Block 26 (PRO)', '"Patient Reported Outcome Measures"[Mesh] OR "Quality of Life"[Mesh] OR "quality of life"[tiab]'),
    ('ILD + PRO', '("Lung Diseases, Interstitial"[Mesh] OR "ILD"[tiab]) AND ("Quality of Life"[Mesh] OR "quality of life"[tiab])'),
    ('ILD + Symptoms', '("Lung Diseases, Interstitial"[Mesh] OR "ILD"[tiab]) AND ("Dyspnea"[Mesh] OR "dyspnea"[tiab] OR "Cough"[Mesh] OR "cough"[tiab])'),
]

print("=== Testing Individual Search Blocks ===")
for name, query in queries:
    count = test_pubmed_query(query)
    print(f'{name}: {count} hits')
    time.sleep(0.5)

print("\n=== Testing Seed PMID Coverage ===")
seed_pmids = ['38648021', '35964592', '34559419', '36701677', '38536110', 
              '28213592', '36179385', '39129185', '28487307', '16817954']

for pmid in seed_pmids:
    ild_query = f'("Lung Diseases, Interstitial"[Mesh] OR "ILD"[tiab] OR "interstitial lung disease"[tiab]) AND {pmid}[PMID]'
    ild_count = test_pubmed_query(ild_query)
    
    pro_query = f'("Quality of Life"[Mesh] OR "quality of life"[tiab] OR "patient reported"[tiab]) AND {pmid}[PMID]'
    pro_count = test_pubmed_query(pro_query)
    
    print(f'PMID {pmid}: ILD={ild_count}, PRO={pro_count}')
    time.sleep(0.5)
