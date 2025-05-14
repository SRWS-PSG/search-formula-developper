import requests
import time
from typing import Dict, List

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
            'ids': data['esearchresult'].get('idlist', []),
            'query': query,
            'message': 'Success'
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'count': 0,
            'ids': [],
            'query': query,
            'message': f'Error: {str(e)}'
        }

def check_papers(pmids: List[str], search_query: str) -> None:
    """
    指定されたPMIDの論文が検索結果に含まれるか確認する
    """
    result = get_pubmed_count(search_query)
    found_ids = set(result['ids'])
    
    print(f"\n検索結果: {result['count']:,}件")
    
    for pmid in pmids:
        included = pmid in found_ids
        print(f"\nPMID: {pmid}")
        print(f"検索結果に含まれる: {'はい' if included else 'いいえ'}")

def main():
    # 確認したいPMID
    pmids = ["21258094", "35803707"]
    
    # 修正した検索式
    modified_query = """
    (
        # AML/MDS関連
        "Leukemia, Myeloid, Acute"[Mesh] OR
        "Myelodysplastic Syndromes"[Mesh] OR
        acute myeloid leukemia[tiab] OR
        AML[tiab] OR
        acute leukemia[tiab] OR
        high-risk myelodysplastic syndrome[tiab] OR
        high risk MDS[tiab] OR
        
        # 化学療法関連
        "Remission Induction"[Mesh] OR
        "Antineoplastic Combined Chemotherapy Protocols"[Mesh] OR
        induction therapy[tiab] OR
        intensive chemotherapy[tiab] OR
        remission induction[tiab] OR
        induction chemotherapy[tiab]
    )
    AND
    (
        # 免疫不全・食事関連
        "Immunocompromised Host"[Mesh] OR
        "Agranulocytosis"[Mesh] OR
        "Diet"[Mesh] OR
        "Food"[Mesh] OR
        neutropeni*[tiab] OR
        immunocompromised[tiab] OR
        immunocompromized[tiab] OR
        leukopeni*[tiab] OR
        leucopeni*[tiab] OR
        granulocytopeni*[tiab] OR
        neutropenic diet[tiab] OR
        regular diet[tiab] OR
        dietary restriction*[tiab] OR
        food restriction*[tiab]
    )
    AND
    (
        # RCTフィルター
        randomized controlled trial[pt] OR
        controlled clinical trial[pt] OR
        randomized[tiab] OR
        placebo[tiab] OR
        clinical trials as topic[mesh:noexp] OR
        randomly[tiab] OR
        trial[ti] OR
        "Practice Guidelines as Topic"[Mesh] OR
        guideline[pt] OR
        practice guideline[pt]
    )
    """
    
    print("修正した検索式で論文の包含を確認します...")
    check_papers(pmids, modified_query)

if __name__ == "__main__":
    main()
