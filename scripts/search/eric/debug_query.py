#!/usr/bin/env python3
"""
Debug ERIC search query syntax
"""
import sys
sys.path.insert(0, '.')
from scripts.search.eric.eric_api import get_eric_record_count, search_eric

def test(label, query):
    count = get_eric_record_count(query)
    print(f"{label}: {count:,}")
    return count

print("=" * 60)
print("ERIC Query Syntax Debug")
print("=" * 60)

# Test basic queries
test("1. Free text 'faculty development'", "faculty development")
test("2. subject:Faculty Development", 'subject:"Faculty Development"')
test("3. descriptor:Faculty Development", 'descriptor:"Faculty Development"')
test("4. Medical School Faculty (subject)", 'subject:"Medical School Faculty"')
test("5. Medical faculty (free text)", '"medical faculty"')

print("\n--- Testing OR syntax ---")
test("6. Simple OR", '"medical faculty" OR "clinical educator"')
test("7. subject OR", 'subject:"Faculty Development" OR subject:"Professional Development"')

print("\n--- Testing AND syntax ---")
test("8. Simple AND", '"faculty development" AND "medical"')

print("\n--- Final combined test ---")
# Simpler version
block1_simple = '"medical faculty" OR "clinical educator" OR "medical educator"'
block2_simple = '"faculty development" OR "professional development"'
combined_simple = f'({block1_simple}) AND ({block2_simple})'

test("9. Block 1 (simple)", block1_simple)
test("10. Block 2 (simple)", block2_simple)
test("11. Combined (simple)", combined_simple)

print("\n" + "=" * 60)
