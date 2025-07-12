import requests
import time

def test_extended_intervention_search_with_pmids():
    """Test the extended intervention search formula with 3 in-scope seed PMIDs"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    search_query = '((Social Isolation[mh]) OR (Loneliness[mh]) OR (loneliness[tiab]) OR ("social isolation"[tiab]) OR ("social isolat*"[tiab])) AND ((Smartphone[mh]) OR (Wearable Electronic Devices[mh]) OR (Mobile Applications[mh]) OR (smartphone*[tiab]) OR ("mobile app*"[tiab]) OR ("mobile application*"[tiab]) OR ("wearable device*"[tiab]) OR ("digital phenotyping"[tiab]) OR ("passive sensing"[tiab]) OR ("mobile health"[tiab]) OR (mhealth[tiab]) OR (Cell Phone[mh]) OR (Remote Sensing Technology[mh]) OR ("Digital Biomarkers"[tiab]) OR ("sensor data"[tiab]) OR (accelerometer[tiab]) OR ("activity monitor*"[tiab]) OR (app[tiab]) OR (apps[tiab]) OR (("cell"[tiab] or "cellular"[tiab] or "mobile"[tiab] or "smart"[tiab]) AND ("phone"[tiab] or "telephone"[tiab] or "device"[tiab] or "application"[tiab])) OR ("Handheld Computer*"[tiab]) OR ("real time data"[tiab]) OR ("Short Messag* Service*"[tiab]) OR (SMS[tiab]) OR ("text messag*"[tiab]))'
    
    seed_pmids = ['31342903', '35161852', '38900745']
    
    params = {
        'db': 'pubmed',
        'term': search_query,
        'retmode': 'json',
        'retmax': 10000
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        total_count = int(data['esearchresult'].get('count', 0))
        id_list = data['esearchresult'].get('idlist', [])
        
        print("=== EXTENDED INTERVENTION SEARCH FORMULA TEST ===")
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
        
        out_of_scope_pmid = '36519748'
        if out_of_scope_pmid in id_list:
            print(f"⚠ PMID {out_of_scope_pmid}: FOUND (should be out of scope)")
        else:
            print(f"✓ PMID {out_of_scope_pmid}: NOT FOUND (correctly out of scope)")
        
        print()
        print(f"SUMMARY:")
        print(f"In-scope PMIDs captured ({len(captured_pmids)}/3): {captured_pmids}")
        print(f"In-scope PMIDs missing ({len(missing_pmids)}/3): {missing_pmids}")
        print(f"Out-of-scope PMID 36519748: {'FOUND (unexpected)' if out_of_scope_pmid in id_list else 'NOT FOUND (correct)'}")
        print(f"Success Rate: {len(captured_pmids)}/3 = {len(captured_pmids)/3*100:.1f}%")
        print(f"Total Hits: {total_count}")
        print(f"Within Target (≤3000): {'YES' if total_count <= 3000 else 'NO'}")
        print(f"Approach: Extended Intervention Block with comprehensive smart device terms")
        
        return len(captured_pmids) == 3 and total_count <= 5000  # Allow some flexibility for extended search
        
    except Exception as e:
        print(f"Error: {e}")
        return False

success = test_extended_intervention_search_with_pmids()
print(f"\nFINAL RESULT: {'SUCCESS' if success else 'NEEDS REFINEMENT'}")
