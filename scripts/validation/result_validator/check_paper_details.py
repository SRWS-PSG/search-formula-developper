import requests
import time
from typing import Dict

def get_paper_details(pmid: str) -> Dict:
    """
    PubMed E-utilities APIを使用して論文の詳細情報を取得する
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    summary_url = f"{base_url}/esummary.fcgi"
    
    params = {
        'db': 'pubmed',
        'id': pmid,
        'retmode': 'json'
    }
    
    try:
        response = requests.get(summary_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        paper_data = data['result'][pmid]
        
        return {
            'title': paper_data.get('title', ''),
            'pubdate': paper_data.get('pubdate', ''),
            'source': paper_data.get('source', ''),
            'authors': [author.get('name', '') for author in paper_data.get('authors', [])],
            'mesh_terms': [mesh.get('name', '') for mesh in paper_data.get('mesh', [])],
            'keywords': paper_data.get('keywords', []),
            'abstract': paper_data.get('abstract', '')
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'error': f'Error: {str(e)}'
        }

def main():
    pmids = ["21258094", "35803707"]
    
    print("論文の詳細情報を取得します...\n")
    
    for pmid in pmids:
        print(f"PMID: {pmid}")
        print("-" * 50)
        
        details = get_paper_details(pmid)
        
        if 'error' in details:
            print(f"エラー: {details['error']}")
            continue
        
        print(f"タイトル: {details['title']}")
        print(f"出版日: {details['pubdate']}")
        print(f"ジャーナル: {details['source']}")
        print("\n著者:")
        for author in details['authors']:
            print(f"- {author}")
        
        print("\nMeSH用語:")
        for term in details['mesh_terms']:
            print(f"- {term}")
        
        if details['keywords']:
            print("\nキーワード:")
            for keyword in details['keywords']:
                print(f"- {keyword}")
        
        print("\n要約:")
        print(details['abstract'])
        print("\n" + "=" * 80 + "\n")
        
        time.sleep(1)  # API制限を考慮

if __name__ == "__main__":
    main()
