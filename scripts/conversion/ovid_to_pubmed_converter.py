#!/usr/bin/env python3
"""
Ovid MEDLINE to PubMed search formula converter with API verification
"""

import re
import requests
import time
import json
import os
import argparse
from xml.etree import ElementTree as ET
from typing import List, Set, Tuple, Dict

def convert_ovid_to_pubmed(ovid_formula: str) -> str:
    """
    Convert Ovid MEDLINE search formula to PubMed format
    
    Args:
        ovid_formula: Original Ovid MEDLINE search formula
        
    Returns:
        str: Converted PubMed search formula
    """
    pubmed_formula = ovid_formula.replace('<http://stomach.tw|stomach.tw>,kw.', 'stomach.tw,kw.')
    
    pubmed_formula = re.sub(r'exp ([^/]+)/', r'"\1"[MeSH Terms]', pubmed_formula)
    
    pubmed_formula = re.sub(r'\.tw,kw\.', '[tiab]', pubmed_formula)
    
    pubmed_formula = re.sub(r'\badj\d+\b', 'AND', pubmed_formula)
    
    pubmed_formula = re.sub(r'\band\b', 'AND', pubmed_formula, flags=re.IGNORECASE)
    pubmed_formula = re.sub(r'\bor\b', 'OR', pubmed_formula, flags=re.IGNORECASE)
    
    pubmed_formula = re.sub(r'\s+', ' ', pubmed_formula).strip()
    
    return pubmed_formula

def create_simplified_pubmed_query() -> str:
    """
    Create simplified PubMed query based on core concepts
    
    Returns:
        str: Simplified PubMed search query
    """
    query = '''(
        ("Helicobacter"[MeSH Terms] OR "Helicobacter Infections"[MeSH Terms] OR 
         helicobacter[tiab] OR pylori[tiab] OR "H pylori"[tiab]) 
        AND 
        ("Anti-Inflammatory Agents, Non-Steroidal"[MeSH Terms] OR nsaid[tiab] OR nsaids[tiab] OR 
         "nonsteroidal anti-inflammatory"[tiab] OR "non-steroidal anti-inflammatory"[tiab])
        AND 
        ("Peptic Ulcer"[MeSH Terms] OR "Duodenal Ulcer"[MeSH Terms] OR "Stomach Ulcer"[MeSH Terms] OR 
         "peptic ulcer"[tiab] OR "duodenal ulcer"[tiab] OR "gastric ulcer"[tiab] OR "stomach ulcer"[tiab])
    )'''
    
    query = re.sub(r'\s+', ' ', query).strip()
    return query

def search_pubmed(query: str, retmax: int = 5000) -> Tuple[List[str], int]:
    """
    Search PubMed using E-utilities API
    
    Args:
        query: PubMed search query
        retmax: Maximum number of results to retrieve
        
    Returns:
        Tuple[List[str], int]: List of PMIDs and total count
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    api_key = os.getenv("NCBI_API_KEY")
    params = {
        'db': 'pubmed',
        'term': query,
        'retmax': retmax,
        'retmode': 'xml'
    }
    if api_key:
        params['api_key'] = api_key
    
    try:
        print(f"Searching PubMed with query: {query[:200]}...")
        response = requests.get(base_url, params=params, timeout=30)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        pmids = [id_elem.text for id_elem in root.findall('.//Id')]
        
        count_elem = root.find('.//Count')
        total_count = int(count_elem.text) if count_elem is not None else len(pmids)
        
        print(f"Found {total_count} total results, retrieved {len(pmids)} PMIDs")
        return pmids, total_count
        
    except Exception as e:
        print(f"Error searching PubMed: {e}")
        return [], 0

def verify_pmids_in_results(target_pmids: List[str], search_results: List[str]) -> Tuple[Set[str], Set[str]]:
    """
    Check which target PMIDs are found in search results
    
    Args:
        target_pmids: List of target PMIDs to verify
        search_results: List of PMIDs from search results
        
    Returns:
        Tuple[Set[str], Set[str]]: Found PMIDs and missing PMIDs
    """
    target_set = set(target_pmids)
    result_set = set(search_results)
    
    found = target_set.intersection(result_set)
    missing = target_set - result_set
    
    return found, missing

def main():
    """Main function to convert and verify Ovid formula"""
    print("=== Ovid MEDLINE to PubMed Converter and Verifier ===\n")
    
    ovid_formula = """(exp Helicobacter/ or exp Helicobacter Infections/ or (helicobacter or campylobacter).tw,kw. or (pylori or pyloridis or HP).tw,kw.) and (exp Anti-Inflammatory Agents, Non-Steroidal/ or nsaid*.tw,kw. or non steroid* anti?inflammator*.tw,kw. or non steroid* anti inflammator*.tw,kw. or non?steroid* anti inflammator*.tw,kw. or non?steroid* anti?inflammator*.tw,kw.) and (((exp stomach/ or <http://stomach.tw|stomach.tw>,kw. or gastr*.tw,kw. or exp duodenum/ or duoden*.tw,kw.) and (peptic*.tw,kw. or exp peptic ulcer/)) or (peptic adj5 ulcer*).tw,kw. or (stomach adj5 ulcer*).tw,kw. or (duoden* adj5 ulcer*).tw,kw. or (gastroduoden* adj5 ulcer*).tw,kw.)"""
    
    print("Original Ovid formula:")
    print(ovid_formula)
    print("\n" + "="*80 + "\n")
    
    target_pmids = [
        "1882793", "1415095", "9576450", "10452677", "10520889", "10573377", 
        "10792126", "10912481", "10914775", "11736717", "11275883", "12741450", 
        "15165261", "15940620", "15962366", "15962375", "16501856", "17932759", 
        "20074147", "21424697", "22732269", "24834225", "22126650", "25532720", 
        "31037448", "37223285", "38111504", "38292123"
    ]
    
    print(f"Target PMIDs to verify: {len(target_pmids)} total")
    print("Target PMIDs:", target_pmids[:5], "... (showing first 5)")
    print("\n" + "="*80 + "\n")
    
    pubmed_formula = convert_ovid_to_pubmed(ovid_formula)
    simplified_query = create_simplified_pubmed_query()
    
    print("Converted PubMed formula:")
    print(pubmed_formula)
    print("\n" + "-"*60 + "\n")
    
    print("Simplified PubMed query:")
    print(simplified_query)
    print("\n" + "="*80 + "\n")
    
    results = {}
    for query_name, query in [("Converted Formula", pubmed_formula), ("Simplified Query", simplified_query)]:
        print(f"Testing {query_name}...")
        
        search_results, total_count = search_pubmed(query, retmax=5000)
        
        if search_results:
            found, missing = verify_pmids_in_results(target_pmids, search_results)
            coverage = (len(found) / len(target_pmids)) * 100
            
            results[query_name] = {
                'query': query,
                'total_results': total_count,
                'retrieved_results': len(search_results),
                'found_pmids': sorted(list(found)),
                'missing_pmids': sorted(list(missing)),
                'coverage': coverage
            }
            
            print(f"Results for {query_name}:")
            print(f"  Total search results: {total_count}")
            print(f"  Retrieved results: {len(search_results)}")
            print(f"  Found target PMIDs: {len(found)}/{len(target_pmids)}")
            print(f"  Coverage: {coverage:.1f}%")
            
            if found:
                print(f"  Found PMIDs: {sorted(list(found))}")
            
            if missing:
                print(f"  Missing PMIDs: {sorted(list(missing))}")
        else:
            print(f"No results returned for {query_name}")
            results[query_name] = {
                'query': query,
                'total_results': 0,
                'retrieved_results': 0,
                'found_pmids': [],
                'missing_pmids': sorted(target_pmids),
                'coverage': 0
            }
        
        print("\n" + "-"*60 + "\n")
        time.sleep(1)  # Rate limiting for NCBI API
    
    print("=== SUMMARY ===")
    for query_name, result in results.items():
        print(f"{query_name}: {result['coverage']:.1f}% coverage ({len(result['found_pmids'])}/{len(target_pmids)} PMIDs)")
    
    output_file = 'pubmed_verification_results.json'
    with open(output_file, 'w') as f:
        json.dump({
            'original_ovid_formula': ovid_formula,
            'target_pmids': target_pmids,
            'results': results
        }, f, indent=2)
    
    print(f"\nResults saved to {output_file}")
    
    return results

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Convert Ovid MEDLINE to PubMed and verify PMIDs')
    parser.add_argument('--ovid-formula', type=str, help='Ovid formula to convert')
    parser.add_argument('--pmids', type=str, help='Comma-separated list of PMIDs to verify')
    parser.add_argument('--output', type=str, default='pubmed_verification_results.json', 
                       help='Output file for results')
    return parser.parse_args()

if __name__ == "__main__":
    main()
