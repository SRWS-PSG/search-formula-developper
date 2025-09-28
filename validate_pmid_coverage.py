#!/usr/bin/env python3

import sys
import os
import requests
import time
from typing import Dict, List, Set

sys.path.append('/home/ubuntu/repos/search-formula-developper')

def get_pubmed_results(query: str, retmax: int = 10000) -> Dict:
    """
    PubMed E-utilities APIを使用して検索結果のPMIDリストを取得する
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        'db': 'pubmed',
        'term': query,
        'retmode': 'json',
        'retmax': retmax,
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

def validate_pmid_coverage():
    """
    検索式が指定されたPMIDをすべて含むかを検証する
    """
    pubmed_query = '("Helicobacter"[Mesh] OR "Helicobacter Infections"[Mesh] OR (helicobacter OR campylobacter)[tiab] OR (pylori OR pyloridis OR HP)[tiab]) AND ("Anti-Inflammatory Agents, Non-Steroidal"[Mesh] OR nsaid*[tiab] OR "non steroidal anti inflammatory"[tiab] OR "non steroid anti inflammatory"[tiab] OR "nonsteroidal anti inflammatory"[tiab] OR "nonsteroid anti inflammatory"[tiab]) AND ((("stomach"[Mesh] OR stomach[tiab] OR gastr*[tiab] OR "duodenum"[Mesh] OR duoden*[tiab]) AND (peptic*[tiab] OR "peptic ulcer"[Mesh])) OR "peptic ulcer"[tiab] OR "stomach ulcer"[tiab] OR "duodenal ulcer"[tiab] OR "gastroduodenal ulcer"[tiab])'
    
    target_pmids = {
        "1882793", "1415095", "9576450", "10452677", "10520889", "10573377", 
        "10792126", "10912481", "10914775", "11736717", "11275883", "12741450", 
        "15165261", "15940620", "15962366", "15962375", "16501856", "17932759", 
        "20074147", "21424697", "22732269", "24834225", "22126650", "25532720", 
        "31037448", "37223285", "38111504", "38292123"
    }
    
    print("=== PMID Coverage Validation ===\n")
    print(f"Target PMIDs: {len(target_pmids)}")
    print(f"PubMed Query: {pubmed_query}\n")
    
    print("Executing PubMed search...")
    result = get_pubmed_results(pubmed_query, retmax=10000)
    search_pmids = set(result['ids'])
    
    print(f"Search returned {result['count']} results")
    print(f"Retrieved {len(search_pmids)} PMIDs\n")
    
    covered_pmids = target_pmids.intersection(search_pmids)
    missing_pmids = target_pmids - search_pmids
    
    print("=== Coverage Analysis ===")
    print(f"Covered PMIDs: {len(covered_pmids)}/{len(target_pmids)}")
    print(f"Coverage rate: {len(covered_pmids)/len(target_pmids)*100:.1f}%")
    
    if covered_pmids:
        print(f"\nCovered PMIDs: {sorted(covered_pmids)}")
    
    if missing_pmids:
        print(f"\nMissing PMIDs: {sorted(missing_pmids)}")
        
        print("\n=== Individual PMID Analysis ===")
        for pmid in sorted(missing_pmids):
            time.sleep(0.5)  # API制限を考慮
            
            pmid_exists = get_pubmed_results(f"{pmid}[uid]")
            if pmid_exists['count'] == 0:
                print(f"PMID {pmid}: Does not exist in PubMed")
                continue
                
            blocks = [
                '("Helicobacter"[Mesh] OR "Helicobacter Infections"[Mesh] OR (helicobacter OR campylobacter)[tiab] OR (pylori OR pyloridis OR HP)[tiab])',
                '("Anti-Inflammatory Agents, Non-Steroidal"[Mesh] OR nsaid*[tiab] OR "non steroidal anti inflammatory"[tiab] OR "non steroid anti inflammatory"[tiab] OR "nonsteroidal anti inflammatory"[tiab] OR "nonsteroid anti inflammatory"[tiab])',
                '((("stomach"[Mesh] OR stomach[tiab] OR gastr*[tiab] OR "duodenum"[Mesh] OR duoden*[tiab]) AND (peptic*[tiab] OR "peptic ulcer"[Mesh])) OR "peptic ulcer"[tiab] OR "stomach ulcer"[tiab] OR "duodenal ulcer"[tiab] OR "gastroduodenal ulcer"[tiab])'
            ]
            
            block_names = ["Helicobacter", "NSAIDs", "Peptic Ulcer"]
            
            print(f"\nPMID {pmid} analysis:")
            for i, (block, name) in enumerate(zip(blocks, block_names)):
                block_query = f"({block}) AND {pmid}[uid]"
                block_result = get_pubmed_results(block_query)
                matches = block_result['count'] > 0
                print(f"  {name} block: {'✓' if matches else '✗'}")
                time.sleep(0.3)
    
    return len(missing_pmids) == 0, covered_pmids, missing_pmids

def main():
    success, covered, missing = validate_pmid_coverage()
    
    print("\n" + "="*60)
    if success:
        print("✅ SUCCESS: All target PMIDs are covered by the search formula!")
    else:
        print(f"❌ FAILURE: {len(missing)} PMIDs are missing from the search results")
        print("The search formula needs to be modified to include all target PMIDs.")
    
    return success

if __name__ == "__main__":
    main()
