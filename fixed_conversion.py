#!/usr/bin/env python3

import sys
import os
import requests
import time
from typing import Dict

sys.path.append('/home/ubuntu/repos/search-formula-developper')

def get_pubmed_count(query: str) -> Dict:
    """
    PubMed E-utilities APIを使用して検索クエリの結果件数を取得する
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        'db': 'pubmed',
        'term': query,
        'retmode': 'json',
        'retmax': 100000,  # 最大取得件数
        'usehistory': 'y'
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        count = int(data['esearchresult']['count'])
        ids = data['esearchresult']['idlist']
        
        return {
            'count': count,
            'ids': ids,
            'webenv': data['esearchresult'].get('webenv'),
            'querykey': data['esearchresult'].get('querykey')
        }
    except Exception as e:
        print(f"Error querying PubMed: {e}")
        return {'count': 0, 'ids': [], 'webenv': None, 'querykey': None}

def manual_convert_ovid_to_pubmed():
    """
    Manual conversion of the Ovid query to proper PubMed format
    """
    
    part1 = '("Helicobacter"[Mesh] OR "Helicobacter Infections"[Mesh] OR (helicobacter OR campylobacter)[tiab] OR (pylori OR pyloridis OR HP)[tiab])'
    
    part2 = '("Anti-Inflammatory Agents, Non-Steroidal"[Mesh] OR nsaid*[tiab] OR "non steroidal anti inflammatory"[tiab] OR "non steroid anti inflammatory"[tiab] OR "nonsteroidal anti inflammatory"[tiab] OR "nonsteroid anti inflammatory"[tiab])'
    
    part3 = '((("stomach"[Mesh] OR stomach[tiab] OR gastr*[tiab] OR "duodenum"[Mesh] OR duoden*[tiab]) AND (peptic*[tiab] OR "peptic ulcer"[Mesh])) OR "peptic ulcer"[tiab] OR "stomach ulcer"[tiab] OR "duodenal ulcer"[tiab] OR "gastroduodenal ulcer"[tiab])'
    
    pubmed_query = f"{part1} AND {part2} AND {part3}"
    
    return pubmed_query

def test_query_with_pmids():
    """
    Test if the query retrieves the specified PMIDs
    """
    pmids_to_check = [
        "1882793", "1415095", "9576450", "10452677", "10520889", "10573377", 
        "10792126", "10912481", "10914775", "11736717", "11275883", "12741450", 
        "15165261", "15940620", "15962366", "15962375", "16501856", "17932759", 
        "20074147", "21424697", "22732269", "24834225", "22126650", "25532720", 
        "31037448", "37223285", "38111504", "38292123"
    ]
    
    pmid_query = f"({' OR '.join(pmids_to_check)})[uid]"
    
    print("Testing PMID query:")
    print(pmid_query)
    
    try:
        result = get_pubmed_count(pmid_query)
        count = result['count']
        print(f"Found {count} out of {len(pmids_to_check)} PMIDs in PubMed")
        return count == len(pmids_to_check)
    except Exception as e:
        print(f"Error testing PMID query: {e}")
        return False

def main():
    print("=== Manual Ovid to PubMed Conversion ===\n")
    
    pubmed_query = manual_convert_ovid_to_pubmed()
    
    print("Corrected PubMed Query:")
    print(pubmed_query)
    print("\n" + "="*80 + "\n")
    
    try:
        result = get_pubmed_count(pubmed_query)
        count = result['count']
        print(f"Query returns {count} results in PubMed")
    except Exception as e:
        print(f"Error testing query: {e}")
    
    print("\n" + "="*80 + "\n")
    
    pmids_exist = test_query_with_pmids()
    print(f"All target PMIDs exist in PubMed: {pmids_exist}")
    
    return pubmed_query

if __name__ == "__main__":
    main()
