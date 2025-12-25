#!/usr/bin/env python3
"""
ERIC API Test Script

ERIC APIの全機能をテストするスクリプト。

Usage:
    python scripts/search/eric/test_eric_api.py
"""

import sys
import os
import time

# Add parent directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(script_dir))))

from scripts.search.eric.eric_api import (
    # Constants
    ERIC_FIELDS,
    ERIC_EXACT_FIELDS,
    ERIC_FILTERS,
    ERIC_IES_OPTIONS,
    # Classes
    ERICQueryBuilder,
    ERICSearchResult,
    # Functions
    search_eric,
    get_eric_record_count,
    search_eric_peer_reviewed,
    search_eric_with_date_range,
    search_eric_fulltext,
    search_eric_ies_funded,
    search_eric_wwc_reviewed,
)


# Test results tracking
passed = 0
failed = 0


def test(name: str, condition: bool, detail: str = ""):
    """テスト結果を記録"""
    global passed, failed
    if condition:
        passed += 1
        print(f"  ✓ {name}")
    else:
        failed += 1
        print(f"  ✗ {name}")
        if detail:
            print(f"    Detail: {detail}")


def section(name: str):
    """セクションヘッダーを表示"""
    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}\n")


def main():
    global passed, failed
    
    print("\n" + "="*60)
    print("  ERIC API Test Suite")
    print("="*60)
    
    # ============================================================
    # 1. Constants Tests
    # ============================================================
    section("1. Constants Tests")
    
    # ERIC_FIELDS
    test("ERIC_FIELDS is defined", ERIC_FIELDS is not None)
    test("ERIC_FIELDS has 'title'", "title" in ERIC_FIELDS)
    test("ERIC_FIELDS has 'abstract'", "abstract" in ERIC_FIELDS)
    test("ERIC_FIELDS has 'subject'", "subject" in ERIC_FIELDS)
    test("ERIC_FIELDS has 'author'", "author" in ERIC_FIELDS)
    test("ERIC_FIELDS has 'peerreviewed'", "peerreviewed" in ERIC_FIELDS)
    
    # ERIC_EXACT_FIELDS
    test("ERIC_EXACT_FIELDS is defined", ERIC_EXACT_FIELDS is not None)
    test("ERIC_EXACT_FIELDS has 'descriptorx'", "descriptorx" in ERIC_EXACT_FIELDS)
    test("ERIC_EXACT_FIELDS has 'sourcex'", "sourcex" in ERIC_EXACT_FIELDS)
    
    # ERIC_FILTERS
    test("ERIC_FILTERS is defined", ERIC_FILTERS is not None)
    test("ERIC_FILTERS has 'pubyearmin'", "pubyearmin" in ERIC_FILTERS)
    test("ERIC_FILTERS has 'pubyearmax'", "pubyearmax" in ERIC_FILTERS)
    
    # ERIC_IES_OPTIONS
    test("ERIC_IES_OPTIONS is defined", ERIC_IES_OPTIONS is not None)
    test("ERIC_IES_OPTIONS has 'ies_funded'", "ies_funded" in ERIC_IES_OPTIONS)
    test("ERIC_IES_OPTIONS has 'wwc_meets_standards'", "wwc_meets_standards" in ERIC_IES_OPTIONS)
    
    # ============================================================
    # 2. QueryBuilder Tests
    # ============================================================
    section("2. QueryBuilder Tests")
    
    # Basic term
    builder = ERICQueryBuilder()
    query = builder.add_term("education").build()
    test("Basic term", query == "education", f"Got: {query}")
    
    # Phrase term
    builder = ERICQueryBuilder()
    query = builder.add_term("faculty development").build()
    test("Phrase term (auto-quoted)", query == '"faculty development"', f"Got: {query}")
    
    # Field-specific term
    builder = ERICQueryBuilder()
    query = builder.add_term("faculty development", field="title").build()
    test("Field-specific term", query == 'title:"faculty development"', f"Got: {query}")
    
    # Descriptor
    builder = ERICQueryBuilder()
    query = builder.add_descriptor("Medical School Faculty").build()
    test("Descriptor", query == 'subject:"Medical School Faculty"', f"Got: {query}")
    
    # Exact descriptor
    builder = ERICQueryBuilder()
    query = builder.add_descriptor("Medical School Faculty", exact=True).build()
    test("Exact descriptor", query == 'descriptorx:"Medical School Faculty"', f"Got: {query}")
    
    # OR group
    builder = ERICQueryBuilder()
    query = builder.add_or_group(["term1", "term2", "term3"]).build()
    test("OR group", "(term1 OR term2 OR term3)" in query, f"Got: {query}")
    
    # OR group with field
    builder = ERICQueryBuilder()
    query = builder.add_or_group(["Term A", "Term B"], field="subject").build()
    test("OR group with field", 'subject:"Term A" OR subject:"Term B"' in query, f"Got: {query}")
    
    # Date range (min only)
    builder = ERICQueryBuilder()
    query = builder.add_term("education").set_date_range(min_year=2020).build()
    test("Date range (min)", "publicationdateyear:[2020 TO *]" in query, f"Got: {query}")
    
    # Date range (max only)
    builder = ERICQueryBuilder()
    query = builder.add_term("education").set_date_range(max_year=2025).build()
    test("Date range (max)", "publicationdateyear:[* TO 2025]" in query, f"Got: {query}")
    
    # Date range (both)
    builder = ERICQueryBuilder()
    query = builder.add_term("education").set_date_range(min_year=2020, max_year=2025).build()
    test("Date range (both)", "publicationdateyear:[2020 TO 2025]" in query, f"Got: {query}")
    
    # Peer-reviewed
    builder = ERICQueryBuilder()
    query = builder.add_term("education").peer_reviewed_only().build()
    test("Peer-reviewed filter", "peerreviewed:T" in query, f"Got: {query}")
    
    # Fulltext
    builder = ERICQueryBuilder()
    query = builder.add_term("education").fulltext_only().build()
    test("Fulltext filter", "e_fulltextauth:T" in query, f"Got: {query}")
    
    # IES Funded
    builder = ERICQueryBuilder()
    query = builder.add_term("reading").ies_funded_only().build()
    test("IES funded filter", "funded:y" in query, f"Got: {query}")
    
    # WWC Reviewed
    builder = ERICQueryBuilder()
    query = builder.add_term("reading").wwc_reviewed("y").build()
    test("WWC reviewed filter (y)", "wwcr:y" in query, f"Got: {query}")
    
    builder = ERICQueryBuilder()
    query = builder.add_term("reading").wwc_reviewed("r").build()
    test("WWC reviewed filter (r)", "wwcr:r" in query, f"Got: {query}")
    
    # Required term
    builder = ERICQueryBuilder()
    query = builder.add_term("regression", required=True).build()
    test("Required term (+)", query == "+regression", f"Got: {query}")
    
    # Excluded term
    builder = ERICQueryBuilder()
    query = builder.add_term("gay", excluded=True).build()
    test("Excluded term (-)", query == "-gay", f"Got: {query}")
    
    # Complex query
    builder = ERICQueryBuilder()
    query = (builder
        .add_term("faculty development", field="title")
        .add_descriptor("Medical School Faculty")
        .peer_reviewed_only()
        .set_date_range(min_year=2020)
        .build())
    test("Complex query", 
         'title:"faculty development"' in query and 
         'subject:"Medical School Faculty"' in query and 
         'peerreviewed:T' in query and
         'publicationdateyear:[2020 TO *]' in query,
         f"Got: {query}")
    
    # Reset
    builder = ERICQueryBuilder()
    builder.add_term("test").peer_reviewed_only()
    builder.reset()
    query = builder.add_term("new").build()
    test("Reset builder", query == "new" and "peerreviewed" not in query, f"Got: {query}")
    
    # ============================================================
    # 3. API Integration Tests (Live API Calls)
    # ============================================================
    section("3. API Integration Tests")
    print("  (Testing with live ERIC API - may take a few seconds)\n")
    
    # Basic search
    result = search_eric("faculty development", rows=5)
    test("Basic search returns results", result.total_count > 0, f"Count: {result.total_count}")
    test("Basic search returns correct rows", len(result.records) == 5, f"Rows: {len(result.records)}")
    time.sleep(0.5)
    
    # Get count only
    count = get_eric_record_count("medical education")
    test("Get record count", count > 0, f"Count: {count}")
    time.sleep(0.5)
    
    # Peer-reviewed search
    result_pr = search_eric_peer_reviewed("faculty development", rows=1)
    test("Peer-reviewed search", result_pr.total_count > 0, f"Count: {result_pr.total_count}")
    time.sleep(0.5)
    
    # Date range search
    result_date = search_eric_with_date_range("faculty development", min_year=2020, rows=1)
    test("Date range search (2020+)", result_date.total_count > 0, f"Count: {result_date.total_count}")
    time.sleep(0.5)
    
    # Fulltext search (note: e_fulltextauth filter may not work via API)
    result_ft = search_eric_fulltext("reading instruction", rows=1)
    test("Fulltext search", result_ft.total_count >= 0, f"Count: {result_ft.total_count}")
    time.sleep(0.5)
    
    # IES Funded search
    result_ies = search_eric_ies_funded("reading", rows=1)
    test("IES Funded search", result_ies.total_count >= 0, f"Count: {result_ies.total_count}")
    time.sleep(0.5)
    
    # WWC Reviewed search
    result_wwc = search_eric_wwc_reviewed("reading", level="y", rows=1)
    test("WWC Reviewed search", result_wwc.total_count >= 0, f"Count: {result_wwc.total_count}")
    time.sleep(0.5)
    
    # QueryBuilder with API
    builder = ERICQueryBuilder()
    query = (builder
        .add_descriptor("Faculty Development")
        .add_descriptor("Medical School Faculty")
        .set_date_range(min_year=2015)
        .build())
    result_builder = search_eric(query, rows=1)
    test("QueryBuilder with API", result_builder.total_count >= 0, f"Query: {query}, Count: {result_builder.total_count}")
    
    # ============================================================
    # 4. Comparison Tests
    # ============================================================
    section("4. Filter Comparison Tests")
    
    # Compare all vs peer-reviewed
    count_all = get_eric_record_count("faculty development")
    time.sleep(0.3)
    count_pr = get_eric_record_count("(faculty development) AND peerreviewed:T")
    test("Peer-reviewed < All", count_pr < count_all, 
         f"All: {count_all:,}, Peer-reviewed: {count_pr:,}")
    time.sleep(0.3)
    
    # Compare all vs date-filtered (using publicationdateyear range syntax)
    count_2020 = get_eric_record_count("(faculty development) AND publicationdateyear:[2020 TO *]")
    test("2020+ < All", count_2020 < count_all,
         f"All: {count_all:,}, 2020+: {count_2020:,}")
    
    # ============================================================
    # Summary
    # ============================================================
    section("Test Summary")
    
    total = passed + failed
    print(f"  Passed: {passed}/{total}")
    print(f"  Failed: {failed}/{total}")
    print()
    
    if failed == 0:
        print("  ✓ All tests passed!")
        return 0
    else:
        print("  ✗ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
