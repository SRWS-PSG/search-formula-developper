import requests
import time
from typing import Dict

def get_pubmed_count(query: str) -> Dict:
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
            'query': query,
            'message': 'Success'
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'count': 0,
            'query': query,
            'message': f'Error: {str(e)}'
        }

def main():
    # 各ブロックの検索式
    aml_mds = [
        '"Leukemia, Myeloid, Acute"[Mesh]',
        '"Myelodysplastic Syndromes"[Mesh]',
        'acute myeloid leukemia[tiab]',
        'AML[tiab]',
        'high-risk myelodysplastic syndrome[tiab]',
        'high risk MDS[tiab]'
    ]
    
    chemo = [
        '"Remission Induction"[Mesh]',
        'induction therapy[tiab]',
        'intensive chemotherapy[tiab]',
        'remission induction[tiab]'
    ]
    
    immune = [
        '"Immunocompromised Host"[Mesh]',
        '"Agranulocytosis"[Mesh]',
        'neutropeni*[tiab]',
        'immunocompromised[tiab]',
        'immunocompromized[tiab]',
        'leukopeni*[tiab]',
        'leucopeni*[tiab]',
        'granulocytopeni*[tiab]'
    ]
    
    rct = [
        'randomized controlled trial[pt]',
        'controlled clinical trial[pt]',
        'randomized[tiab]',
        'placebo[tiab]',
        'clinical trials as topic[mesh:noexp]',
        'randomly[tiab]',
        'trial[ti]'
    ]
    
    print("=== 段階的な検索結果 ===")
    
    # 1. AML/MDS OR 化学療法
    condition_query = f"({' OR '.join(aml_mds + chemo)})"
    time.sleep(1)
    condition_result = get_pubmed_count(condition_query)
    print(f"1. AML/MDS OR 化学療法: {condition_result['count']:,}件")
    
    # 2. (AML/MDS OR 化学療法) AND 免疫不全
    immune_query = f"{condition_query} AND ({' OR '.join(immune)})"
    time.sleep(1)
    immune_result = get_pubmed_count(immune_query)
    print(f"2. AND 免疫不全: {immune_result['count']:,}件")
    
    # 3. (AML/MDS OR 化学療法) AND 免疫不全 AND RCTフィルター
    final_query = f"{immune_query} AND ({' OR '.join(rct)})"
    time.sleep(1)
    final_result = get_pubmed_count(final_query)
    print(f"3. AND RCTフィルター: {final_result['count']:,}件")

if __name__ == "__main__":
    main()
