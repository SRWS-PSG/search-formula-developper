import sys
import os
sys.path.append('scripts/search/query_executor')
from check_final_query import get_pubmed_results

final_query = '(("Dementia"[Mesh]) OR (dementia[tiab]) OR (alzheimer*[tiab]) OR ("lewy body"[tiab]) OR ("frontotemporal dementia"[tiab]) OR ("cognitive impairment"[tiab])) AND (("Aged"[Mesh]) OR ("Aged, 80 and over"[Mesh]) OR ("Frail Elderly"[Mesh]) OR (aged[tiab]) OR (elderly[tiab]) OR (older[tiab])) AND (("Grief"[Mesh]) OR (grief[tiab]) OR (grieving[tiab]) OR (mourning[tiab]) OR (sorrow[tiab]) OR (lament*[tiab]) OR ("ambiguous loss"[tiab]) OR ("feeling of loss"[tiab]) OR ("experience of loss"[tiab]) OR ("loss of self"[tiab]) OR ("loss of identity"[tiab]) OR ("loss of function"[tiab]) OR ("loss of independence"[tiab]) OR ("loss of autonomy"[tiab]))'

pmids_to_check = [
    "17558579", "28139178", "22680050", "24776791", "1468208",
    "23992286", "36054090", "30249213", "29059067", "23701394",
    "34095858", "16019290", "29534602", "33839469", "28229487"
]

print("=== PMID検証結果 ===")
print(f"検索式: {final_query}")
print()

result = get_pubmed_results(final_query, retmax=100000)
print(f"検索結果総数: {result['count']:,}件")
print()

found_ids = set(result['ids'])
included_pmids = []
not_found_pmids = []

print("=== 各PMIDの包含状況 ===")
for pmid in pmids_to_check:
    if pmid in found_ids:
        included_pmids.append(pmid)
        print(f"✅ PMID {pmid}: 含まれています")
    else:
        not_found_pmids.append(pmid)
        print(f"❌ PMID {pmid}: 含まれていません")

print()
print("=== 結果サマリー ===")
print(f"含まれていたPMID: {len(included_pmids)}件")
if included_pmids:
    print(f"  {', '.join(included_pmids)}")

print(f"含まれていなかったPMID: {len(not_found_pmids)}件")
if not_found_pmids:
    print(f"  {', '.join(not_found_pmids)}")

print(f"\n包含率: {len(included_pmids)}/{len(pmids_to_check)} ({len(included_pmids)/len(pmids_to_check)*100:.1f}%)")
