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

def analyze_paper(pmid: str) -> None:
    """
    論文の各検索条件への合致を分析する
    """
    print(f"\nPMID: {pmid}の分析")
    print("-" * 50)
    
    # 各ブロックの検索条件
    blocks = {
        "AML/MDS": [
            '"Leukemia, Myeloid, Acute"[Mesh]',
            '"Myelodysplastic Syndromes"[Mesh]',
            'acute myeloid leukemia[tiab]',
            'AML[tiab]',
            'acute leukemia[tiab]',
            'high-risk myelodysplastic syndrome[tiab]',
            'high risk MDS[tiab]'
        ],
        "化学療法": [
            '"Remission Induction"[Mesh]',
            '"Antineoplastic Combined Chemotherapy Protocols"[Mesh]',
            'induction therapy[tiab]',
            'intensive chemotherapy[tiab]',
            'remission induction[tiab]',
            'induction chemotherapy[tiab]'
        ],
        "免疫不全・食事": [
            '"Immunocompromised Host"[Mesh]',
            '"Agranulocytosis"[Mesh]',
            '"Diet"[Mesh]',
            '"Food"[Mesh]',
            'neutropeni*[tiab]',
            'immunocompromised[tiab]',
            'immunocompromized[tiab]',
            'leukopeni*[tiab]',
            'leucopeni*[tiab]',
            'granulocytopeni*[tiab]',
            'neutropenic diet[tiab]',
            'regular diet[tiab]',
            'dietary restriction*[tiab]',
            'food restriction*[tiab]'
        ],
        "RCT/ガイドライン": [
            'randomized controlled trial[pt]',
            'controlled clinical trial[pt]',
            'randomized[tiab]',
            'placebo[tiab]',
            'clinical trials as topic[mesh:noexp]',
            'randomly[tiab]',
            'trial[ti]',
            '"Practice Guidelines as Topic"[Mesh]',
            'guideline[pt]',
            'practice guideline[pt]'
        ]
    }
    
    # 各条件での検索結果を確認
    for block_name, terms in blocks.items():
        print(f"\n{block_name}ブロック:")
        for term in terms:
            time.sleep(1)  # API制限を考慮
            query = f"{pmid}[uid] AND ({term})"
            result = get_pubmed_count(query)
            match = "○" if result['count'] > 0 else "×"
            print(f"{match} {term}")

def main():
    pmids = ["21258094", "35803707"]
    
    print("論文の詳細な検索条件分析を開始します...")
    for pmid in pmids:
        analyze_paper(pmid)

if __name__ == "__main__":
    main()
