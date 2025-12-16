#!/usr/bin/env python3
"""
Test the fixed check_block_overlap.py script

Purpose: Verify that the bug fix works correctly
Tests:
1. Known good queries (should all succeed)
2. Queries that previously reported 0 (should now show correct values)
"""

import sys
import os
import tempfile

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../scripts/search/term_validator'))

from check_block_overlap import analyze_block_overlap, parse_block_from_text

# Test cases
TEST_BLOCK = """
(("Physicians"[Mesh] OR physician*[tiab]) AND "meaningful work"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "work engagement"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND vigor[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND calling[tiab])
"""

EXPECTED_RESULTS = {
    "meaningful work": 50,
    "work engagement": 151,
    "vigor": 78,
    "calling": 948,
}

def test_fixed_script():
    """Test the fixed script with known queries"""
    print("=" * 80)
    print("Testing Fixed check_block_overlap.py")
    print("=" * 80)
    print()

    # Parse the test block
    search_terms = parse_block_from_text(TEST_BLOCK)
    print(f"Parsed {len(search_terms)} search terms")
    print()

    # Run analysis
    results, report = analyze_block_overlap(search_terms, block_name="Test Block")

    print()
    print("=" * 80)
    print("Validation Results")
    print("=" * 80)
    print()

    all_passed = True

    # Check each result
    for i, result in enumerate(results):
        term = result['term']
        individual = result['individual_count']
        cumulative = result['cumulative_count']
        added = result['added_count']

        # Find expected value
        expected = None
        for keyword, expected_count in EXPECTED_RESULTS.items():
            if keyword in term:
                expected = expected_count
                break

        # Validate
        status = "✓ PASS"
        if individual is None:
            status = "✗ FAIL - Individual count is None"
            all_passed = False
        elif cumulative is None:
            status = "✗ FAIL - Cumulative count is None"
            all_passed = False
        elif expected and individual != expected:
            status = f"✗ FAIL - Expected {expected}, got {individual}"
            all_passed = False
        elif i > 0 and cumulative < results[i-1]['cumulative_count']:
            status = "✗ FAIL - Cumulative decreased"
            all_passed = False

        print(f"Line {result['line']}: {status}")
        print(f"  Term: {term[:60]}...")
        print(f"  Individual: {individual}")
        print(f"  Cumulative: {cumulative}")
        print(f"  Added: {added}")
        if expected:
            print(f"  Expected: {expected}")
        print()

    # Final summary
    print("=" * 80)
    if all_passed:
        print("✓ ALL TESTS PASSED")
    else:
        print("✗ SOME TESTS FAILED")
    print("=" * 80)
    print()

    # Save report
    output_path = "tests/api_instability_investigation_20251110/test_report.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Test Report for Fixed check_block_overlap.py\n\n")
        f.write("## Test Date\n\n")
        from datetime import datetime
        f.write(f"{datetime.now().isoformat()}\n\n")
        f.write("## Test Results\n\n")
        if all_passed:
            f.write("✓ **All tests passed**\n\n")
        else:
            f.write("✗ **Some tests failed**\n\n")
        f.write("## Analysis Report\n\n")
        f.write(report)

    print(f"Report saved to: {output_path}")

    return all_passed

if __name__ == "__main__":
    success = test_fixed_script()
    sys.exit(0 if success else 1)
