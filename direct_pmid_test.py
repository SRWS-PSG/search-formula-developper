import requests
import time

def test_direct_search_with_pmids(search_query, pmids):
    """Test if specific PMIDs are captured by a search query"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    params = {
        'db': 'pubmed',
        'term': search_query,
        'retmode': 'json',
        'retmax': 10000  # Increase limit to capture more results
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        total_count = int(data['esearchresult'].get('count', 0))
        id_list = data['esearchresult'].get('idlist', [])
        
        print(f"Search Query: {search_query}")
        print(f"Total Hits: {total_count}")
        print(f"Retrieved IDs: {len(id_list)}")
        
        captured_pmids = []
        missing_pmids = []
        
        for pmid in pmids:
            if pmid in id_list:
                captured_pmids.append(pmid)
            else:
                missing_pmids.append(pmid)
        
        print(f"Captured PMIDs: {captured_pmids}")
        print(f"Missing PMIDs: {missing_pmids}")
        print("-" * 80)
        
        return len(captured_pmids) == len(pmids)
        
    except Exception as e:
        print(f"Error: {e}")
        return False

seed_pmids = ['31342903', '35161852', '36519748', '38900745']

test_queries = [
    '(Social Isolation[mh] OR Loneliness[mh]) AND (Smartphone[mh] OR Wearable Electronic Devices[mh] OR Mobile Applications[mh])',
    
    '(Social Isolation[mh] OR Loneliness[mh] OR loneliness[tiab]) AND (Smartphone[mh] OR smartphone*[tiab] OR Wearable Electronic Devices[mh])',
    
    'Social Isolation[mh] AND Smartphone[mh]',
    
    'Loneliness[mh] AND Smartphone[mh]',
    
    'loneliness[tiab] AND smartphone*[tiab]'
]

print("=== Testing Direct Search Queries with Seed PMIDs ===\n")

for i, query in enumerate(test_queries, 1):
    print(f"TEST {i}:")
    time.sleep(1)  # Rate limiting
    success = test_direct_search_with_pmids(query, seed_pmids)
    print(f"All PMIDs captured: {'YES' if success else 'NO'}")
    print()
