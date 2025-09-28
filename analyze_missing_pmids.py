#!/usr/bin/env python3

import sys
import os
import requests
import time
from typing import Dict, List
import xml.etree.ElementTree as ET

sys.path.append('/home/ubuntu/repos/search-formula-developper')

def fetch_pubmed_abstract(pmid: str) -> Dict:
    """
    PubMed E-utilities APIを使用して論文の詳細情報を取得する
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        'db': 'pubmed',
        'id': pmid,
        'retmode': 'xml'
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        article = root.find('.//Article')
        
        if article is None:
            return {'pmid': pmid, 'title': '', 'abstract': '', 'error': 'Article not found'}
        
        title_elem = article.find('.//ArticleTitle')
        title = title_elem.text if title_elem is not None else ''
        
        abstract_elem = article.find('.//AbstractText')
        abstract = abstract_elem.text if abstract_elem is not None else ''
        
        return {
            'pmid': pmid,
            'title': title,
            'abstract': abstract
        }
        
    except Exception as e:
        return {'pmid': pmid, 'title': '', 'abstract': '', 'error': str(e)}

def analyze_missing_pmids():
    """
    欠落しているPMIDを分析してNSAIDs関連用語を特定する
    """
    missing_pmids = ['10452677', '10520889', '12741450', '15940620', '17932759', '22732269', '38292123']
    
    print("=== Analysis of Missing PMIDs ===\n")
    
    nsaid_terms = set()
    peptic_terms = set()
    
    for pmid in missing_pmids:
        print(f"Analyzing PMID {pmid}...")
        time.sleep(1)  # API制限を考慮
        
        paper_info = fetch_pubmed_abstract(pmid)
        
        if 'error' in paper_info:
            print(f"  Error: {paper_info['error']}")
            continue
            
        title = paper_info['title'].lower()
        abstract = paper_info['abstract'].lower()
        full_text = f"{title} {abstract}"
        
        print(f"  Title: {paper_info['title'][:100]}...")
        
        potential_nsaid_terms = [
            'aspirin', 'ibuprofen', 'naproxen', 'diclofenac', 'indomethacin',
            'piroxicam', 'celecoxib', 'rofecoxib', 'meloxicam', 'ketoprofen',
            'sulindac', 'tolmetin', 'etodolac', 'ketorolac', 'flurbiprofen',
            'cox-2', 'cox2', 'cyclooxygenase', 'prostaglandin', 'anti-inflammatory',
            'antiinflammatory', 'analgesic', 'pain relief', 'inflammation'
        ]
        
        found_nsaid_terms = []
        for term in potential_nsaid_terms:
            if term in full_text:
                found_nsaid_terms.append(term)
                nsaid_terms.add(term)
        
        potential_peptic_terms = [
            'gastric', 'duodenal', 'peptic', 'ulcer', 'ulceration', 'erosion',
            'gastritis', 'gastropathy', 'mucosal', 'bleeding', 'hemorrhage',
            'perforation', 'gi', 'gastrointestinal'
        ]
        
        found_peptic_terms = []
        for term in potential_peptic_terms:
            if term in full_text:
                found_peptic_terms.append(term)
                peptic_terms.add(term)
        
        print(f"  NSAIDs terms found: {found_nsaid_terms}")
        print(f"  Peptic terms found: {found_peptic_terms}")
        print()
    
    print("=== Summary of Missing Terms ===")
    print(f"NSAIDs terms to add: {sorted(nsaid_terms)}")
    print(f"Peptic terms to add: {sorted(peptic_terms)}")
    
    return nsaid_terms, peptic_terms

def create_enhanced_search_formula(additional_nsaid_terms, additional_peptic_terms):
    """
    分析結果に基づいて拡張された検索式を作成する
    """
    helicobacter_block = '("Helicobacter"[Mesh] OR "Helicobacter Infections"[Mesh] OR (helicobacter OR campylobacter)[tiab] OR (pylori OR pyloridis OR HP)[tiab])'
    
    base_nsaid_terms = [
        '"Anti-Inflammatory Agents, Non-Steroidal"[Mesh]',
        'nsaid*[tiab]',
        '"non steroidal anti inflammatory"[tiab]',
        '"non steroid anti inflammatory"[tiab]',
        '"nonsteroidal anti inflammatory"[tiab]',
        '"nonsteroid anti inflammatory"[tiab]'
    ]
    
    additional_nsaid_search_terms = []
    for term in additional_nsaid_terms:
        if term in ['cox-2', 'cox2']:
            additional_nsaid_search_terms.append(f'"{term}"[tiab]')
        else:
            additional_nsaid_search_terms.append(f'{term}[tiab]')
    
    all_nsaid_terms = base_nsaid_terms + additional_nsaid_search_terms
    nsaid_block = f'({" OR ".join(all_nsaid_terms)})'
    
    base_peptic_terms = [
        '(("stomach"[Mesh] OR stomach[tiab] OR gastr*[tiab] OR "duodenum"[Mesh] OR duoden*[tiab]) AND (peptic*[tiab] OR "peptic ulcer"[Mesh]))',
        '"peptic ulcer"[tiab]',
        '"stomach ulcer"[tiab]',
        '"duodenal ulcer"[tiab]',
        '"gastroduodenal ulcer"[tiab]'
    ]
    
    additional_peptic_search_terms = []
    for term in additional_peptic_terms:
        if term not in ['peptic', 'ulcer', 'stomach', 'duodenal', 'gastric']:  # 既に含まれている用語は除外
            additional_peptic_search_terms.append(f'{term}*[tiab]')
    
    all_peptic_terms = base_peptic_terms + additional_peptic_search_terms
    peptic_block = f'({" OR ".join(all_peptic_terms)})'
    
    enhanced_formula = f'{helicobacter_block} AND {nsaid_block} AND {peptic_block}'
    
    return enhanced_formula

def main():
    print("Analyzing missing PMIDs to identify additional search terms...\n")
    
    nsaid_terms, peptic_terms = analyze_missing_pmids()
    
    print("\n" + "="*60)
    print("Creating enhanced search formula...")
    
    enhanced_formula = create_enhanced_search_formula(nsaid_terms, peptic_terms)
    
    print("\nEnhanced PubMed Search Formula:")
    print(enhanced_formula)
    
    return enhanced_formula

if __name__ == "__main__":
    main()
