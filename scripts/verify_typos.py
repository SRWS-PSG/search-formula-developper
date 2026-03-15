#!/usr/bin/env python3
"""
Verify potentially misspelled search terms by checking PubMed hit counts.
"""

import time
import requests
from typing import List, Tuple
from urllib.parse import quote

ENTREZ_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

def count_pubmed_hits(term: str) -> int:
    """Query PubMed and return hit count for a given term."""
    try:
        params = {
            "db": "pubmed",
            "term": term,
            "retmax": 0,
            "retmode": "json"
        }
        response = requests.get(ENTREZ_BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        return int(data["esearchresult"]["count"])
    except Exception as e:
        print(f"Error querying '{term}': {e}")
        return -1

def verify_terms(term_pairs: List[Tuple[str, str]]):
    """
    Verify original vs corrected spellings.

    Args:
        term_pairs: List of (original_term, corrected_term) tuples
    """
    print("# Typo Verification Report\n")
    print("| Original Term | Hit Count | Corrected Term | Hit Count | Ratio |")
    print("|---|---|---|---|---|")

    for original, corrected in term_pairs:
        original_query = f'"{original}"[tiab]'
        corrected_query = f'"{corrected}"[tiab]'

        count_original = count_pubmed_hits(original_query)
        time.sleep(0.34)  # Rate limiting

        count_corrected = count_pubmed_hits(corrected_query)
        time.sleep(0.34)

        if count_corrected > 0:
            ratio = f"{count_corrected / max(count_original, 1):.1f}x"
        else:
            ratio = "-"

        print(f"| `{original}` | {count_original:,} | `{corrected}` | {count_corrected:,} | {ratio} |")

if __name__ == "__main__":
    # Define suspected typos and corrections
    terms_to_verify = [
        ("dysparenuia", "dyspareunia"),
        ("Disorder gut brain interaction", "Disorders of gut brain interaction"),
        ("Myalgic Enchphalomyelitis", "Myalgic Encephalomyelitis"),
        ("somatic cough syndrome", "chronic cough syndrome"),
        ("psychogenic syncope", "psychogenic syncope"),  # Baseline check
    ]

    verify_terms(terms_to_verify)
