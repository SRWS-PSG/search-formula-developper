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

def test_individual_pmids_with_original_formula():
    """
    元の変換された検索式で各PMIDを個別にテストする
    """
    target_pmids = [
        "1882793", "1415095", "9576450", "10452677", "10520889", "10573377", 
        "10792126", "10912481", "10914775", "11736717", "11275883", "12741450", 
        "15165261", "15940620", "15962366", "15962375", "16501856", "17932759", 
        "20074147", "21424697", "22732269", "24834225", "22126650", "25532720", 
        "31037448", "37223285", "38111504", "38292123"
    ]
    
    original_formula = '("Helicobacter"[Mesh] OR "Helicobacter Infections"[Mesh] OR (helicobacter OR campylobacter)[tiab] OR (pylori OR pyloridis OR HP)[tiab]) AND ("Anti-Inflammatory Agents, Non-Steroidal"[Mesh] OR nsaid*[tiab] OR "non steroidal anti inflammatory"[tiab] OR "non steroid anti inflammatory"[tiab] OR "nonsteroidal anti inflammatory"[tiab] OR "nonsteroid anti inflammatory"[tiab]) AND ((("stomach"[Mesh] OR stomach[tiab] OR gastr*[tiab] OR "duodenum"[Mesh] OR duoden*[tiab]) AND (peptic*[tiab] OR "peptic ulcer"[Mesh])) OR "peptic ulcer"[tiab] OR "stomach ulcer"[tiab] OR "duodenal ulcer"[tiab] OR "gastroduodenal ulcer"[tiab])'
    
    print("=== Individual PMID Testing with Original Formula ===\n")
    print("Original converted formula:")
    print(original_formula)
    print()
    
    covered_pmids = []
    missing_pmids = []
    
    for pmid in target_pmids:
        time.sleep(0.3)  # API制限を考慮
        
        test_query = f"({original_formula}) AND {pmid}[uid]"
        result = get_pubmed_results(test_query)
        
        if result['count'] > 0:
            covered_pmids.append(pmid)
            print(f"PMID {pmid}: ✓ COVERED")
        else:
            missing_pmids.append(pmid)
            print(f"PMID {pmid}: ✗ MISSING")
    
    print(f"\n=== Original Formula Results ===")
    print(f"Covered: {len(covered_pmids)}/{len(target_pmids)} ({len(covered_pmids)/len(target_pmids)*100:.1f}%)")
    print(f"Missing: {len(missing_pmids)} PMIDs")
    
    if missing_pmids:
        print(f"Missing PMIDs: {missing_pmids}")
    
    return covered_pmids, missing_pmids

def create_final_optimized_formula():
    """
    最適化された最終検索式を作成する
    
    戦略：
    1. H. pylori関連の潰瘍研究（NSAIDs不要）
    2. NSAIDs関連の潰瘍研究（H. pylori不要）  
    3. 両方を含む研究
    """
    
    helicobacter_terms = [
        '"Helicobacter"[Mesh]',
        '"Helicobacter Infections"[Mesh]', 
        '"Helicobacter pylori"[Mesh]',
        'helicobacter[tiab]',
        'campylobacter[tiab]',
        '"H pylori"[tiab]',
        '"H. pylori"[tiab]',
        'pylori[tiab]',
        'pyloridis[tiab]',
        '"HP infection"[tiab]'
    ]
    
    nsaid_terms = [
        '"Anti-Inflammatory Agents, Non-Steroidal"[Mesh]',
        'nsaid*[tiab]',
        '"nonsteroidal anti-inflammatory"[tiab]',
        '"non-steroidal anti-inflammatory"[tiab]',
        '"nonsteroidal antiinflammatory"[tiab]',
        'aspirin[tiab]',
        'ibuprofen[tiab]',
        'diclofenac[tiab]',
        'indomethacin[tiab]',
        'naproxen[tiab]',
        'piroxicam[tiab]',
        'celecoxib[tiab]'
    ]
    
    ulcer_terms = [
        '"Peptic Ulcer"[Mesh]',
        '"Stomach Ulcer"[Mesh]',
        '"Duodenal Ulcer"[Mesh]',
        '"peptic ulcer"[tiab]',
        '"gastric ulcer"[tiab]',
        '"duodenal ulcer"[tiab]',
        '"stomach ulcer"[tiab]',
        '"gastroduodenal ulcer"[tiab]',
        '(peptic*[tiab] AND ulcer*[tiab])',
        '(gastric[tiab] AND ulcer*[tiab])',
        '(duoden*[tiab] AND ulcer*[tiab])',
        '(stomach[tiab] AND ulcer*[tiab])',
        '"ulcer disease"[tiab]',
        '"bleeding ulcer"[tiab]',
        '"idiopathic ulcer"[tiab]'
    ]
    
    h_block = f"({' OR '.join(helicobacter_terms)})"
    n_block = f"({' OR '.join(nsaid_terms)})"  
    u_block = f"({' OR '.join(ulcer_terms)})"
    
    final_formula = f"({h_block} AND {u_block}) OR ({n_block} AND {u_block})"
    
    return final_formula

def validate_final_optimized_formula():
    """
    最適化された検索式を検証する
    """
    target_pmids = [
        "1882793", "1415095", "9576450", "10452677", "10520889", "10573377", 
        "10792126", "10912481", "10914775", "11736717", "11275883", "12741450", 
        "15165261", "15940620", "15962366", "15962375", "16501856", "17932759", 
        "20074147", "21424697", "22732269", "24834225", "22126650", "25532720", 
        "31037448", "37223285", "38111504", "38292123"
    ]
    
    print("\n" + "="*80)
    print("=== Final Optimized Formula Validation ===\n")
    
    final_formula = create_final_optimized_formula()
    print("Final Optimized PubMed Search Formula:")
    print(final_formula)
    print()
    
    print("Testing individual PMIDs...")
    covered_pmids = []
    missing_pmids = []
    
    for pmid in target_pmids:
        time.sleep(0.3)
        
        test_query = f"({final_formula}) AND {pmid}[uid]"
        result = get_pubmed_results(test_query)
        
        if result['count'] > 0:
            covered_pmids.append(pmid)
            print(f"PMID {pmid}: ✓")
        else:
            missing_pmids.append(pmid)
            print(f"PMID {pmid}: ✗")
    
    print(f"\n=== Final Results ===")
    print(f"Covered: {len(covered_pmids)}/{len(target_pmids)} ({len(covered_pmids)/len(target_pmids)*100:.1f}%)")
    
    if missing_pmids:
        print(f"Still missing: {missing_pmids}")
    
    total_result = get_pubmed_results(final_formula)
    print(f"Total search results: {total_result['count']:,}")
    
    success = len(missing_pmids) == 0
    
    print("\n" + "="*60)
    if success:
        print("🎉 SUCCESS: All target PMIDs are covered!")
        print("\n✅ FINAL PUBMED SEARCH FORMULA:")
        print(final_formula)
    else:
        print(f"❌ Still missing {len(missing_pmids)} PMIDs")
    
    return success, final_formula, covered_pmids, missing_pmids

def main():
    print("=== Comprehensive PMID Validation and Final Solution ===\n")
    
    print("Step 1: Testing original converted formula...")
    orig_covered, orig_missing = test_individual_pmids_with_original_formula()
    
    print("\nStep 2: Creating and testing optimized formula...")
    success, final_formula, covered, missing = validate_final_optimized_formula()
    
    return success, final_formula

if __name__ == "__main__":
    main()
