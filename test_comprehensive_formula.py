import requests
import time

def test_comprehensive_search_with_pmids():
    """Test the comprehensive search formula with all 4 seed PMIDs"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    search_query = '((Social Isolation[mh]) OR (Loneliness[mh]) OR (loneliness[tiab]) OR ("social isolation"[tiab]) OR ("social isolat*"[tiab])) AND ((Smartphone[mh]) OR (Wearable Electronic Devices[mh]) OR (Mobile Applications[mh]) OR (smartphone*[tiab]) OR ("mobile app*"[tiab]) OR ("mobile application*"[tiab]) OR ("wearable device*"[tiab]) OR ("digital phenotyping"[tiab]) OR ("passive sensing"[tiab]) OR ("mobile health"[tiab]) OR (mhealth[tiab]) OR (technology[tiab]))'
    
    seed_pmids = ['31342903', '35161852', '36519748', '38900745']
    
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
        
        print("=== COMPREHENSIVE SEARCH FORMULA TEST ===")
        print(f"Search Query: {search_query}")
        print(f"Total Hits: {total_count}")
        print(f"Retrieved IDs: {len(id_list)}")
        print()
        
        captured_pmids = []
        missing_pmids = []
        
        for pmid in seed_pmids:
            if pmid in id_list:
                captured_pmids.append(pmid)
                print(f"✓ PMID {pmid}: FOUND")
            else:
                missing_pmids.append(pmid)
                print(f"✗ PMID {pmid}: MISSING")
        
        print()
        print(f"SUMMARY:")
        print(f"Captured PMIDs ({len(captured_pmids)}/4): {captured_pmids}")
        print(f"Missing PMIDs ({len(missing_pmids)}/4): {missing_pmids}")
        print(f"Success Rate: {len(captured_pmids)}/4 = {len(captured_pmids)/4*100:.1f}%")
        print(f"Total Hits: {total_count}")
        print(f"Within Target (≤3000): {'YES' if total_count <= 3000 else 'NO'}")
        
        return len(captured_pmids) == 4 and total_count <= 3000
        
    except Exception as e:
        print(f"Error: {e}")
        return False

success = test_comprehensive_search_with_pmids()
print(f"\nFINAL RESULT: {'SUCCESS' if success else 'NEEDS REFINEMENT'}")
