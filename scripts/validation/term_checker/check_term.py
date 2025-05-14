import requests
import time

def get_pubmed_count(query: str) -> dict:
    """
    PubMed E-utilities APIを使用して検索クエリの結果件数を取得する
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    search_url = f"{base_url}/esearch.fcgi"
    
    params = {
        'db': 'pubmed',
        'term': query,
        'retmode': 'json'
    }
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        return {
            'count': int(data['esearchresult'].get('count', 0)),
            'query': query
        }
    except requests.exceptions.RequestException as e:
        return {
            'count': 0,
            'query': query,
            'error': str(e)
        }

def check_search_terms():
    """
    PubMed Search History Formatの各要素を検証
    """
    terms = [
        '"Leukemia, Myeloid, Acute"[Mesh]',
        '"Myelodysplastic Syndromes"[Mesh]',
        'acute myeloid leukemia[tiab]',
        'AML[tiab]',
        'high-risk myelodysplastic syndrome[tiab]',
        'high risk MDS[tiab]',
        '"Remission Induction"[Mesh]',
        'induction therapy[tiab]',
        'intensive chemotherapy[tiab]',
        'remission induction[tiab]',
        '"Immunocompromised Host"[Mesh]',
        '"Agranulocytosis"[Mesh]',
        'neutropeni*[tiab]',
        'immunocompromised[tiab]',
        'immunocompromized[tiab]',
        'leukopeni*[tiab]',
        'leucopeni*[tiab]',
        'granulocytopeni*[tiab]',
        'neutropenic diet[tiab]',
        'cooked diet[tiab]',
        'regular diet[tiab]',
        'sterile[tiab]',
        'clean[tiab]',
        'diet*[tiab]',
        'feeding[tiab]',
        'food*[tiab]',
        'nutrition[tiab]',
        'dietary restriction*[tiab]',
        'low bacteria*[tiab]',
        'low microb*[tiab]',
        'minimal bacteria*[tiab]',
        'minimal microb*[tiab]',
        'germ poor[tiab]',
        'reduced bacteria*[tiab]'
    ]
    
    print("各検索用語の検索結果件数を確認します...\n")
    for term in terms:
        time.sleep(1)  # API制限を考慮
        result = get_pubmed_count(term)
        print(f"{term}: {result['count']:,}件")

def main():
    check_search_terms()

if __name__ == "__main__":
    main()
