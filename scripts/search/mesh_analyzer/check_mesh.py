import requests
import time
from typing import List, Dict

def check_mesh_term(term: str) -> Dict:
    """
    PubMed E-utilities APIを使用してMeSH用語の存在を確認する
    
    Args:
        term: 確認するMeSH用語（例: "Leukemia, Myeloid, Acute"）
        
    Returns:
        Dict: {
            'exists': bool,
            'term': str,
            'count': int,  # その用語を含む文献数
            'message': str  # エラーメッセージなど
        }
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    # MeSH用語の検索
    search_url = f"{base_url}/esearch.fcgi"
    params = {
        'db': 'mesh',
        'term': term,
        'retmode': 'json'
    }
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        count = int(data['esearchresult'].get('count', 0))
        exists = count > 0
        
        # PubMedでの文献数も確認
        pubmed_params = {
            'db': 'pubmed',
            'term': f'{term}[Mesh]',
            'retmode': 'json'
        }
        pubmed_response = requests.get(search_url, params=pubmed_params)
        pubmed_response.raise_for_status()
        pubmed_data = pubmed_response.json()
        pubmed_count = int(pubmed_data['esearchresult'].get('count', 0))
        
        return {
            'exists': exists,
            'term': term,
            'mesh_count': count,
            'pubmed_count': pubmed_count,
            'message': 'Success'
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'exists': False,
            'term': term,
            'mesh_count': 0,
            'pubmed_count': 0,
            'message': f'Error: {str(e)}'
        }

def main():
    # 確認するMeSH用語のリスト
    mesh_terms = [
        "Leukemia, Myeloid, Acute",
        "Myelodysplastic Syndromes",
        "Induction Chemotherapy",
        "Remission Induction",
        "Immunocompromised Host",
        "Agranulocytosis"
    ]
    
    print("MeSH用語の確認を開始します...\n")
    
    for term in mesh_terms:
        # APIの制限を考慮して少し待機
        time.sleep(1)
        
        result = check_mesh_term(term)
        
        print(f"用語: {result['term']}")
        print(f"存在: {'はい' if result['exists'] else 'いいえ'}")
        print(f"MeSHデータベースでの出現数: {result['mesh_count']}")
        print(f"PubMedでの文献数: {result['pubmed_count']}")
        if result['message'] != 'Success':
            print(f"メッセージ: {result['message']}")
        print("-" * 50)

if __name__ == "__main__":
    main()
