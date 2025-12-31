#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import time
import json
import argparse
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Any, Set
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup Entrez config
NCBI_EMAIL = os.getenv("NCBI_EMAIL", "tool@example.com")
NCBI_API_KEY = os.getenv("NCBI_API_KEY")

API_DELAY = 0.34

class MeshHierarchyAnalyzer:
    def __init__(self, formula_path: str):
        self.formula_path = formula_path
        self.mesh_terms: List[str] = []
        self.tree_numbers: Dict[str, List[str]] = {}
        self.last_request_time = 0

    def _wait_for_api(self):
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < API_DELAY:
            time.sleep(API_DELAY - time_since_last)
        self.last_request_time = time.time()

    def parse_mesh_terms(self) -> bool:
        """Parses MeSH terms from the first line of the formula file."""
        if not os.path.exists(self.formula_path):
            print(f"Error: File not found {self.formula_path}")
            return False
            
        with open(self.formula_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            return False

        line1 = lines[0].strip()
        line1 = line1.replace('“', '"').replace('”', '"')
        line1 = re.sub(r'^\d+:\s*', '', line1)
        
        # Split by OR
        terms = [t.strip() for t in line1.split(' OR ') if t.strip()]
        
        # Extract terms that are explicitly [Mesh]
        # Format: "Term"[Mesh] or "Term"[MeSH] or "Term" [Mesh] etc.
        self.mesh_terms = []
        for t in terms:
            # Simple regex to capture the term inside quotes before [Mesh]
            # Assumes format like "Term"[Mesh]
            m = re.match(r'^"?([^"]+)"?\s*\[(Mesh|MeSH|mh)\]', t, re.IGNORECASE)
            if m:
                self.mesh_terms.append(m.group(1))
            else:
                # Fallback: check if it looks like a mesh term even if regex is strict
                if '[mesh]' in t.lower() or '[mh]' in t.lower():
                     # Try to clean it up
                     cleaned = t.split('[')[0].strip('" ').strip()
                     self.mesh_terms.append(cleaned)

        print(f"Found {len(self.mesh_terms)} MeSH terms.")
        return True

    def fetch_tree_numbers(self, term: str) -> List[str]:
        """Fetches tree numbers for a single MeSH term."""
        self._wait_for_api()
        
        # 1. Search for the term to get UI (Descriptor UI)
        esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            "db": "mesh",
            "term": f"{term}[MeSH Terms]", # Use exact match restriction if possible, or just term
            "retmode": "json",
            "email": NCBI_EMAIL
        }
        if NCBI_API_KEY:
            params["api_key"] = NCBI_API_KEY

        try:
            resp = requests.get(esearch_url, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            
            id_list = data.get("esearchresult", {}).get("idlist", [])
            if not id_list:
                print(f"Warning: No MeSH ID found for '{term}'")
                return []
            
            # Use the first ID (usually the correct descriptor)
            mesh_id = id_list[0]
            
            # 2. Fetch details (Tree Numbers) using efetch
            self._wait_for_api()
            efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
            fetch_params = {
                "db": "mesh",
                "id": mesh_id,
                "retmode": "xml",
                "email": NCBI_EMAIL
            }
            if NCBI_API_KEY:
                fetch_params["api_key"] = NCBI_API_KEY
                
            fetch_resp = requests.get(efetch_url, params=fetch_params, timeout=30)
            fetch_resp.raise_for_status()
            
            # Parse XML
            root = ET.fromstring(fetch_resp.content)
            
            trees = []
            for tree_num in root.findall(".//TreeNumber"):
                trees.append(tree_num.text)
                
            return trees
            
        except Exception as e:
            print(f"Error fetching tree numbers for '{term}': {e}")
            return []

    def build_hierarchy(self):
        print("Fetching tree numbers for all terms...")
        for i, term in enumerate(self.mesh_terms):
            print(f"Processing {i+1}/{len(self.mesh_terms)}: {term}")
            trees = self.fetch_tree_numbers(term)
            if trees:
                self.tree_numbers[term] = trees
            else:
                self.tree_numbers[term] = []
                
    def check_redundancy(self) -> List[Dict[str, Any]]:
        """
        Checks if any term is a child of another term in the list.
        Term A is redundant if it is a child of Term B, because Term B[Mesh] includes Term A.
        """
        redundancies = []
        
        # Compare every pair
        for child_term in self.mesh_terms:
            child_trees = self.tree_numbers.get(child_term, [])
            if not child_trees:
                continue
                
            for parent_term in self.mesh_terms:
                if child_term == parent_term:
                    continue
                    
                parent_trees = self.tree_numbers.get(parent_term, [])
                if not parent_trees:
                    continue
                
                # Check if ANY child tree starts with ANY parent tree
                # (e.g. child C01.2.3 starts with parent C01.2)
                is_child = False
                matched_parent_tree = ""
                matched_child_tree = ""
                
                for c_tree in child_trees:
                    for p_tree in parent_trees:
                        if c_tree.startswith(p_tree + "."):
                            is_child = True
                            matched_parent_tree = p_tree
                            matched_child_tree = c_tree
                            break
                    if is_child:
                        break
                
                if is_child:
                    redundancies.append({
                        "child": child_term,
                        "parent": parent_term,
                        "child_tree": matched_child_tree,
                        "parent_tree": matched_parent_tree
                    })
                    # Once a parent is found, we know it's redundant. 
                    # We can stop searching for parents for this child if we only care about "is redundant".
                    # But listing all parents might be useful. For now, let's just record it.
                    
        return redundancies

    def generate_report(self, redundancies: List[Dict[str, Any]], output_path: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# MeSH Redundancy Report\n")
            f.write(f"**Date**: {timestamp}\n")
            f.write(f"**Source File**: `{self.formula_path}`\n\n")
            
            if not redundancies:
                f.write("No hierarchical redundancies found.\n")
            else:
                f.write(f"Found {len(redundancies)} redundant relationships.\n\n")
                f.write("| Redundant Term (Child) | Covered By (Parent) | Child Tree | Parent Tree |\n")
                f.write("|---|---|---|---|\n")
                for r in redundancies:
                    f.write(f"| {r['child']} | {r['parent']} | {r['child_tree']} | {r['parent_tree']} |\n")

        print(f"Report saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Check redundancy in MeSH terms.")
    parser.add_argument("formula_file", help="Path to the search formula markdown file")
    parser.add_argument("--output", "-o", help="Output report file path", default="mesh_redundancy_report.md")
    
    args = parser.parse_args()
    
    analyzer = MeshHierarchyAnalyzer(args.formula_file)
    if analyzer.parse_mesh_terms():
        analyzer.build_hierarchy()
        redundancies = analyzer.check_redundancy()
        
        output_path = args.output
        if os.path.basename(output_path) == output_path:
            output_path = os.path.join(os.path.dirname(args.formula_file), output_path)
            
        analyzer.generate_report(redundancies, output_path)

if __name__ == "__main__":
    main()
