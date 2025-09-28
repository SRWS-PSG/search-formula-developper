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

def create_corrected_pubmed_formula():
    """
    論理構造を修正したPubMed検索式を作成する
    
    原因分析：
    - 欠落PMIDは「特発性潰瘍」や「H. pylori陰性潰瘍」の研究
    - これらはNSAIDsとは無関係だが、H. pyloriと潰瘍の関連を扱っている
    - 元のOvid式のAND論理が過度に制限的
    
    修正方針：
    - H. pylori AND 潰瘍の研究を含める
    - NSAIDs AND 潰瘍の研究も含める  
    - H. pylori AND NSAIDs AND 潰瘍の研究も含める
    """
    
    helicobacter_block = '("Helicobacter"[Mesh] OR "Helicobacter Infections"[Mesh] OR (helicobacter OR campylobacter)[tiab] OR (pylori OR pyloridis OR HP)[tiab])'
    
    nsaid_block = '("Anti-Inflammatory Agents, Non-Steroidal"[Mesh] OR nsaid*[tiab] OR "non steroidal anti inflammatory"[tiab] OR "non steroid anti inflammatory"[tiab] OR "nonsteroidal anti inflammatory"[tiab] OR "nonsteroid anti inflammatory"[tiab] OR aspirin[tiab] OR ibuprofen[tiab] OR diclofenac[tiab] OR indomethacin[tiab] OR naproxen[tiab])'
    
    peptic_ulcer_block = '(("stomach"[Mesh] OR "duodenum"[Mesh] OR "peptic ulcer"[Mesh] OR stomach[tiab] OR gastric[tiab] OR duoden*[tiab] OR peptic*[tiab]) AND (ulcer*[tiab] OR ulceration[tiab] OR bleeding[tiab] OR erosion[tiab]))'
    
    corrected_formula = f'({helicobacter_block} AND {peptic_ulcer_block}) OR ({nsaid_block} AND {peptic_ulcer_block})'
    
    return corrected_formula

def validate_final_formula():
    """
    最終的な検索式を検証する
    """
    target_pmids = {
        "1882793", "1415095", "9576450", "10452677", "10520889", "10573377", 
        "10792126", "10912481", "10914775", "11736717", "11275883", "12741450", 
        "15165261", "15940620", "15962366", "15962375", "16501856", "17932759", 
        "20074147", "21424697", "22732269", "24834225", "22126650", "25532720", 
        "31037448", "37223285", "38111504", "38292123"
    }
    
    print("=== Final Search Formula Validation ===\n")
    
    corrected_formula = create_corrected_pubmed_formula()
    print("Corrected PubMed Search Formula:")
    print(corrected_formula)
    print()
    
    print("Executing search...")
    result = get_pubmed_results(corrected_formula, retmax=20000)
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
        print(f"\nStill missing PMIDs: {sorted(missing_pmids)}")
        
        print("\n=== Analysis of Remaining Missing PMIDs ===")
        for pmid in sorted(missing_pmids):
            time.sleep(0.5)
            
            helicobacter_query = f'("Helicobacter"[Mesh] OR "Helicobacter Infections"[Mesh] OR (helicobacter OR campylobacter)[tiab] OR (pylori OR pyloridis OR HP)[tiab]) AND {pmid}[uid]'
            nsaid_query = f'("Anti-Inflammatory Agents, Non-Steroidal"[Mesh] OR nsaid*[tiab] OR "non steroidal anti inflammatory"[tiab] OR "non steroid anti inflammatory"[tiab] OR "nonsteroidal anti inflammatory"[tiab] OR "nonsteroid anti inflammatory"[tiab] OR aspirin[tiab] OR ibuprofen[tiab] OR diclofenac[tiab] OR indomethacin[tiab] OR naproxen[tiab]) AND {pmid}[uid]'
            peptic_query = f'(("stomach"[Mesh] OR "duodenum"[Mesh] OR "peptic ulcer"[Mesh] OR stomach[tiab] OR gastric[tiab] OR duoden*[tiab] OR peptic*[tiab]) AND (ulcer*[tiab] OR ulceration[tiab] OR bleeding[tiab] OR erosion[tiab])) AND {pmid}[uid]'
            
            h_result = get_pubmed_results(helicobacter_query)
            n_result = get_pubmed_results(nsaid_query)  
            p_result = get_pubmed_results(peptic_query)
            
            print(f"PMID {pmid}: H.pylori={'✓' if h_result['count']>0 else '✗'} NSAIDs={'✓' if n_result['count']>0 else '✗'} Peptic={'✓' if p_result['count']>0 else '✗'}")
            time.sleep(0.3)
    
    success = len(missing_pmids) == 0
    
    print("\n" + "="*60)
    if success:
        print("✅ SUCCESS: All target PMIDs are covered!")
    else:
        print(f"❌ Still missing {len(missing_pmids)} PMIDs")
    
    return success, corrected_formula, covered_pmids, missing_pmids

def main():
    success, formula, covered, missing = validate_final_formula()
    
    if success:
        print("\n🎉 FINAL RESULT:")
        print("The corrected PubMed search formula successfully captures all target PMIDs!")
        print("\nFinal PubMed Search Formula:")
        print(formula)
    else:
        print(f"\n⚠️  Need further refinement - {len(missing)} PMIDs still missing")
    
    return success, formula

if __name__ == "__main__":
    main()
