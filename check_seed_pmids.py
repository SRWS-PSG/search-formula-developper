import sys
sys.path.append('scripts/search/mesh_analyzer')
from check_mesh import get_pmid_details

pmids = ['31342903', '35161852', '36519748', '38900745']
for pmid in pmids:
    print(f'=== PMID {pmid} ===')
    try:
        details = get_pmid_details(pmid)
        print(f'Title: {details.get("title", "N/A")}')
        print(f'Abstract: {details.get("abstract", "N/A")[:200]}...')
        print(f'MeSH Terms: {details.get("mesh_terms", [])}')
        print()
    except Exception as e:
        print(f'Error retrieving details: {e}')
        print()
