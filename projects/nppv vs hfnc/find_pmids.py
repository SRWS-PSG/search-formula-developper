#!/usr/bin/env python3
"""Seed trialsのPMIDを特定"""

import requests

def search_pmid(query):
    r = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi', 
                     params={'db':'pubmed','term':query,'retmode':'json'})
    result = r.json()['esearchresult']
    return result.get('idlist', [])

# Pantazopoulos 2024
print("Pantazopoulos 2024:")
pmids = search_pmid('Pantazopoulos[Author] nasal high flow COPD 2024')
print(f"  PMIDs: {pmids}")

# JAMA 2025 BRIC-NET
print("\nJAMA 2025 BRIC-NET:")
pmids = search_pmid('High-Flow Nasal Oxygen Noninvasive Ventilation JAMA 2025 randomized')
print(f"  PMIDs: {pmids}")
