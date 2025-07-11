import requests
import time
import xml.etree.ElementTree as ET

def get_detailed_pmid_info(pmid):
    """Get comprehensive information about a specific PMID"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    fetch_url = f"{base_url}/efetch.fcgi"
    params = {
        'db': 'pubmed',
        'id': pmid,
        'retmode': 'xml'
    }
    
    try:
        response = requests.get(fetch_url, params=params)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        
        title_elem = root.find('.//ArticleTitle')
        title = title_elem.text if title_elem is not None else "No title found"
        
        abstract_elem = root.find('.//AbstractText')
        abstract = abstract_elem.text if abstract_elem is not None else "No abstract found"
        
        mesh_terms = []
        mesh_headings = root.findall('.//MeshHeading')
        for heading in mesh_headings:
            descriptor = heading.find('DescriptorName')
            if descriptor is not None:
                mesh_terms.append(descriptor.text)
        
        keywords = []
        keyword_list = root.findall('.//Keyword')
        for kw in keyword_list:
            if kw.text:
                keywords.append(kw.text)
        
        pub_types = []
        pub_type_list = root.findall('.//PublicationType')
        for pt in pub_type_list:
            if pt.text:
                pub_types.append(pt.text)
        
        return {
            'pmid': pmid,
            'title': title,
            'abstract': abstract,
            'mesh_terms': mesh_terms,
            'keywords': keywords,
            'publication_types': pub_types
        }
        
    except Exception as e:
        return {
            'pmid': pmid,
            'title': f"Error retrieving: {e}",
            'abstract': "",
            'mesh_terms': [],
            'keywords': [],
            'publication_types': []
        }

def test_pmid_with_various_terms(pmid, test_terms):
    """Test if a PMID is captured by various search terms"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    results = {}
    for term in test_terms:
        params = {
            'db': 'pubmed',
            'term': term,
            'retmode': 'json',
            'retmax': 1000
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            id_list = data['esearchresult'].get('idlist', [])
            total_count = int(data['esearchresult'].get('count', 0))
            
            results[term] = {
                'found': pmid in id_list,
                'total_hits': total_count
            }
            
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            results[term] = {
                'found': False,
                'total_hits': 0,
                'error': str(e)
            }
    
    return results

missing_pmid = '36519748'

print(f"=== Detailed Analysis of Missing PMID {missing_pmid} ===\n")

details = get_detailed_pmid_info(missing_pmid)

print(f"Title: {details['title']}")
print(f"Abstract: {details['abstract'][:500]}...")
print(f"MeSH Terms: {', '.join(details['mesh_terms'])}")
print(f"Keywords: {', '.join(details['keywords'])}")
print(f"Publication Types: {', '.join(details['publication_types'])}")

print("\n" + "="*80)
print("TESTING VARIOUS SEARCH TERMS FOR THIS PMID")
print("="*80)

test_terms = [
    'Social Isolation[mh]',
    'Loneliness[mh]',
    'Aging[mh]',
    'Aged[mh]',
    'technology[tiab]',
    '"social isolation"[tiab]',
    'Cohort Studies[mh]',
    'United States[mh]',
    'Independent Living[mh]',
    'Surveys and Questionnaires[mh]',
    '"technology"[tiab] AND "social isolation"[tiab]',
    'Aging[mh] AND technology[tiab]',
    '"older adults"[tiab]',
    '"community-dwelling"[tiab]'
]

results = test_pmid_with_various_terms(missing_pmid, test_terms)

for term, result in results.items():
    status = "FOUND" if result['found'] else "NOT FOUND"
    print(f"{term:<50} | {status:<10} | Hits: {result.get('total_hits', 0)}")
