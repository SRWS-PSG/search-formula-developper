import requests
import time
import xml.etree.ElementTree as ET

def get_pmid_details(pmid):
    """Retrieve detailed information about a PMID including title, abstract, and MeSH terms"""
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
        
        return {
            'pmid': pmid,
            'title': title,
            'abstract': abstract,
            'mesh_terms': mesh_terms,
            'keywords': keywords
        }
        
    except Exception as e:
        return {
            'pmid': pmid,
            'title': f"Error retrieving: {e}",
            'abstract': "",
            'mesh_terms': [],
            'keywords': []
        }

seed_pmids = ['31342903', '35161852', '36519748', '38900745']

print("=== Analyzing Seed PMIDs ===\n")

all_mesh_terms = set()
all_keywords = set()
all_titles = []
all_abstracts = []

for pmid in seed_pmids:
    print(f"PMID: {pmid}")
    time.sleep(1)  # Rate limiting
    
    details = get_pmid_details(pmid)
    
    print(f"Title: {details['title']}")
    print(f"Abstract: {details['abstract'][:300]}...")
    print(f"MeSH Terms: {', '.join(details['mesh_terms'])}")
    print(f"Keywords: {', '.join(details['keywords'])}")
    print("-" * 80)
    
    all_mesh_terms.update(details['mesh_terms'])
    all_keywords.update(details['keywords'])
    all_titles.append(details['title'])
    all_abstracts.append(details['abstract'])

print("\n=== SUMMARY ANALYSIS ===")
print(f"Unique MeSH Terms across all papers: {len(all_mesh_terms)}")
print("MeSH Terms:", ', '.join(sorted(all_mesh_terms)))
print(f"\nUnique Keywords across all papers: {len(all_keywords)}")
print("Keywords:", ', '.join(sorted(all_keywords)))

social_terms = [term for term in all_mesh_terms if any(word in term.lower() for word in ['social', 'isolation', 'loneliness', 'lonely'])]
tech_terms = [term for term in all_mesh_terms if any(word in term.lower() for word in ['phone', 'mobile', 'digital', 'internet', 'computer', 'device', 'technology', 'app', 'smartphone'])]

print(f"\nSocial/Isolation related MeSH terms: {social_terms}")
print(f"Technology related MeSH terms: {tech_terms}")
