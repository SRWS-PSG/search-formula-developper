import requests
import time

def test_pmid_in_search(pmid, search_query):
    """Test if a specific PMID is included in a search query"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    params = {
        'db': 'pubmed',
        'term': search_query,
        'retmode': 'json',
        'retmax': 1000
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        total_count = int(data['esearchresult'].get('count', 0))
        id_list = data['esearchresult'].get('idlist', [])
        
        print(f"Search query: {search_query}")
        print(f"Total hits: {total_count}")
        print(f"PMID {pmid} found: {'Yes' if pmid in id_list else 'No'}")
        
        pmid_params = {
            'db': 'pubmed', 
            'term': f"{pmid}[pmid]",
            'retmode': 'json'
        }
        pmid_response = requests.get(base_url, params=pmid_params)
        pmid_data = pmid_response.json()
        pmid_exists = int(pmid_data['esearchresult'].get('count', 0)) > 0
        print(f"PMID {pmid} exists in PubMed: {'Yes' if pmid_exists else 'No'}")
        print("-" * 50)
        
        return pmid in id_list
        
    except Exception as e:
        print(f"Error testing PMID {pmid}: {e}")
        return False

seed_pmids = ['31342903', '35161852', '36519748', '38900745']

basic_searches = [
    'Social Isolation[mh]',
    'Loneliness[mh]', 
    'loneliness[tiab]',
    'smartphone*[tiab]',
    'Cell Phone[mh]',
    'mhealth[tiab]'
]

print("=== Testing individual PMIDs against basic search terms ===\n")

for pmid in seed_pmids:
    print(f"Testing PMID {pmid}:")
    for search in basic_searches:
        time.sleep(0.5)  # Rate limiting
        test_pmid_in_search(pmid, search)
    print("=" * 60)
