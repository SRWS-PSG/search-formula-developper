#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import time
import json
import argparse
import requests
from datetime import datetime
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Entrez config
NCBI_EMAIL = os.getenv("NCBI_EMAIL", "tool@example.com")
NCBI_API_KEY = os.getenv("NCBI_API_KEY")

API_DELAY = 0.34  # Seconds between requests

class PPSFormulaAnalyzer:
    def __init__(self, formula_path: str):
        self.formula_path = formula_path
        self.terms: List[str] = []
        self.total_block_query = ""
        self.last_request_time = 0

    def _wait_for_api(self):
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < API_DELAY:
            time.sleep(API_DELAY - time_since_last)
        self.last_request_time = time.time()

    def parse_formula(self) -> bool:
        """Parses the specific format of seach_formula_2.md"""
        if not os.path.exists(self.formula_path):
            print(f"Error: File not found {self.formula_path}")
            return False
            
        with open(self.formula_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Line 1: Mesh terms (index 0)
        # Line 3: Tiab terms (index 2)
        
        raw_terms = []
        
        if len(lines) >= 1:
            line1 = lines[0].strip()
            # Normalize quotes
            line1 = line1.replace('“', '"').replace('”', '"')
            # Remove line numbers if present (e.g. "1: ")
            line1 = re.sub(r'^\d+:\s*', '', line1)
            # Split by OR - be careful with terms containing OR if any, but standard format implies OR separator
            # Using ' OR ' splitting is safe for standard PubMed strings unless ' OR ' is inside a quoted string. 
            # Assuming standard separation for now.
            terms1 = [t.strip() for t in line1.split(' OR ') if t.strip()]
            raw_terms.extend(terms1)
            
        if len(lines) >= 3:
            line3 = lines[2].strip()
            line3 = line3.replace('“', '"').replace('”', '"')
            line3 = re.sub(r'^\d+:\s*', '', line3)
            terms3 = [t.strip() for t in line3.split(' OR ') if t.strip()]
            raw_terms.extend(terms3)
            
        # Clean terms (remove trailing OR if it existed in split, or empty strings)
        self.terms = [t for t in raw_terms if t and t != 'OR']
        
        # Construct the full block query
        self.total_block_query = " OR ".join(self.terms)
        
        print(f"Parsed {len(self.terms)} terms.")
        return True

    def get_count(self, query: str) -> int:
        """Executes a PubMed count query using requests"""
        self._wait_for_api()
        
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": query,
            "retmode": "json",
            "retmax": 0,
            "email": NCBI_EMAIL
        }
        if NCBI_API_KEY:
            params["api_key"] = NCBI_API_KEY
            
        try:
            response = requests.get(base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if "esearchresult" in data and "count" in data["esearchresult"]:
                return int(data["esearchresult"]["count"])
            else:
                print(f"Unexpected response format for '{query}': {data}")
                return -1
                
        except Exception as e:
            print(f"Error querying '{query}': {e}")
            return -1

    def analyze(self):
        if not self.terms:
            print("No terms to analyze.")
            return

        print(f"Analyzing {len(self.terms)} terms...")
        
        # 1. Total Block Count
        total_count = self.get_count(self.total_block_query)
        print(f"Total Block Count: {total_count}")
        
        results = []
        
        for i, term in enumerate(self.terms):
            print(f"Processing {i+1}/{len(self.terms)}: {term}")
            
            # 2. Individual Count
            individual_count = self.get_count(term)
            
            # 3. Contribution (Total - (Block excluding Term))
            # Construct query without this term
            other_terms = self.terms[:i] + self.terms[i+1:]
            if not other_terms:
                # Only one term in total
                contribution = total_count
            else:
                exclusion_query = " OR ".join(other_terms)
                exclusion_count = self.get_count(exclusion_query)
                contribution = total_count - exclusion_count
            
            # Keep contribution non-negative (can be negative if live data changes during queries, but unlikely)
            contribution = max(0, contribution)
            
            results.append({
                "term": term,
                "count": individual_count,
                "contribution": contribution
            })
            
        return total_count, results

    def generate_report(self, total_count: int, results: List[Dict[str, Any]], output_path: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Sort by contribution (descending)
        results.sort(key=lambda x: x['contribution'], reverse=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# P-Block Analysis Report\n")
            f.write(f"**Date**: {timestamp}\n")
            f.write(f"**Source File**: `{self.formula_path}`\n")
            f.write(f"**Total Block Count**: {total_count:,}\n\n")
            
            f.write("| Rank | Term | Hit Count | Unique Contribution | % Contribution |\n")
            f.write("|---|---|---|---|---|\n")
            
            for i, r in enumerate(results):
                cont_percent = (r['contribution'] / total_count * 100) if total_count > 0 else 0
                term_cell = r['term'].replace('|', '\|') # Escape pipes
                f.write(f"| {i+1} | `{term_cell}` | {r['count']:,} | {r['contribution']:,} | {cont_percent:.2f}% |\n")
        
        print(f"Report saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Analyze P-block search formula components.")
    parser.add_argument("formula_file", help="Path to the search formula markdown file")
    parser.add_argument("--output", "-o", help="Output report file path", default="analysis_report.md")
    
    args = parser.parse_args()
    
    analyzer = PPSFormulaAnalyzer(args.formula_file)
    if analyzer.parse_formula():
        total, results = analyzer.analyze()
        if results is not None:
            # If output path is just a filename, put it in the same dir as the formula
            output_path = args.output
            if os.path.basename(output_path) == output_path:
                output_path = os.path.join(os.path.dirname(args.formula_file), output_path)
                
            analyzer.generate_report(total, results, output_path)

if __name__ == "__main__":
    main()

