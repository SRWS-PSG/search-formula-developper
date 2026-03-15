#!/usr/bin/env python3
"""
Debug ERIC search query syntax - Test 2
"""
import sys
sys.path.insert(0, '.')
from scripts.search.eric.eric_api import get_eric_record_count

def test(label, query):
    count = get_eric_record_count(query)
    print(f"{label}: {count:,}")
    print(f"  Query: {query}")
    return count

print("=" * 60)
print("ERIC Query Syntax Debug - Phase 2")
print("=" * 60)

# Test phrase search without quotes
print("\n--- Phrase Search Tests ---")
test("1. With quotes", '"medical faculty"')
test("2. Without quotes", 'medical faculty')
test("3. title field", 'title:medical faculty')
test("4. title with quotes", 'title:"medical faculty"')

# Test subject field
print("\n--- Subject Field Tests ---")
test("5. subject with quotes", 'subject:"Medical School Faculty"')
test("6. subject without quotes", 'subject:Medical School Faculty')

# Test AND/OR
print("\n--- Boolean Tests ---")
test("7. AND test", 'medical AND faculty')
test("8. OR with parens", '(medical) OR (faculty)')
test("9. Complex", '(subject:"Faculty Development") AND (medical)')

print("\n" + "=" * 60)
