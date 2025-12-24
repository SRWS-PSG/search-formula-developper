#!/usr/bin/env python3
"""
Convert PubMed search formula to ERIC - Final Version
Based on syntax testing results
"""
import sys
import os
sys.path.insert(0, '.')
from scripts.search.eric.eric_api import get_eric_record_count, search_eric

# Output file
output_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'projects', 'fd_review', 'eric_search_formula.md')
output_lines = []

def log(msg=""):
    print(msg)
    sys.stdout.flush()
    output_lines.append(msg)

def test(label, query):
    count = get_eric_record_count(query)
    log(f"{label}: {count:,} hits")
    return count

log("# ERIC Search Formula")
log("")
log("PubMed検索式をERIC形式に変換した結果")
log("")

# ============================================================
# Block #1: Target Audience (対象者) - Medical Faculty
# ============================================================
log("## #1 Target Audience (対象者)")
log("")
log("### Original PubMed:")
log("```")
log('"Faculty, Medical"[Mesh] OR medical faculty[tiab] OR clinical educator*[tiab] OR clinician educator*[tiab] OR medical educator*[tiab] OR clinical teacher*[tiab] OR clinical teaching[tiab]')
log("```")
log("")

block1 = '(subject:"Medical School Faculty" OR subject:"College Faculty" OR title:"medical faculty" OR title:"clinical educator" OR title:"clinician educator" OR title:"medical educator" OR title:"clinical teacher" OR title:"clinical teaching")'

log("### ERIC Conversion:")
log("```")
log(block1)
log("```")
log("")
count1 = test("#1 Hits", block1)
log("")

# ============================================================
# Block #2: Intervention (介入) - Faculty Development
# ============================================================
log("---")
log("")
log("## #2 Intervention (介入)")
log("")
log("### Original PubMed:")
log("```")
log('"Staff Development"[Mesh] OR "Program Development"[Mesh] OR faculty development*[tiab] OR professional development*[tiab] OR teaching skill*[tiab] OR "program design"[tiab]')
log("```")
log("")

block2 = '(subject:"Faculty Development" OR subject:"Professional Development" OR subject:"Staff Development" OR subject:"Program Development" OR subject:"Program Design" OR title:"faculty development" OR title:"professional development" OR title:"teaching skill" OR title:"program design")'

log("### ERIC Conversion:")
log("```")
log(block2)
log("```")
log("")
count2 = test("#2 Hits", block2)
log("")

# ============================================================
# Block #3: Combined
# ============================================================
log("---")
log("")
log("## #3 Combined (#1 AND #2)")
log("")

combined = f'{block1} AND {block2}'
log("### ERIC Formula:")
log("```")
log(combined)
log("```")
log("")
count3 = test("#3 Hits", combined)
log("")

# ============================================================
# Summary
# ============================================================
log("---")
log("")
log("## Summary")
log("")
log("| Block | Description | Hits |")
log("|-------|-------------|------|")
log(f"| #1 | Target Audience | {count1:,} |")
log(f"| #2 | Intervention | {count2:,} |")
log(f"| #3 | Combined | {count3:,} |")
log("")

# ============================================================
# Sample Results
# ============================================================
log("## Sample Results (Top 5)")
log("")

results = search_eric(combined, rows=5)
for i, rec in enumerate(results.records, 1):
    log(f"### [{i}] {rec.get('id', 'N/A')}")
    log(f"- **Title**: {rec.get('title', 'N/A')}")
    log(f"- **Year**: {rec.get('publicationdateyear', 'N/A')}")
    log(f"- **Source**: {rec.get('source', 'N/A')}")
    subjects = rec.get('subject', [])
    if subjects:
        log(f"- **Descriptors**: {', '.join(subjects[:8])}")
    log("")

# ============================================================
# Conversion Notes
# ============================================================
log("---")
log("")
log("## Conversion Notes")
log("")
log("### PubMed → ERIC Mapping")
log("")
log("| PubMed | ERIC | Notes |")
log("|--------|------|-------|")
log('| `[Mesh]` | `subject:"Term"` | ERICのDescriptor (シソーラス) |')
log('| `[tiab]` | `title:"phrase"` | ERICはtitle+abstractの複合フィールドなし |')
log('| `term*` | `term*` | ワイルドカードは同じ |')
log("")
log("### ERIC Thesaurus Mapping")
log("")
log("| PubMed MeSH | ERIC Descriptor |")
log("|-------------|-----------------|")
log('| Faculty, Medical | Medical School Faculty |')
log('| Staff Development | Staff Development, Faculty Development |')
log('| Program Development | Program Development, Program Design |')
log("")

# Save to file
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

log(f"Results saved to: {output_path}")
