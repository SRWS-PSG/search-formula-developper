import sys
import os
sys.path.append('scripts/search/query_executor')
from check_final_query import get_pubmed_results

original_query = '(("Dementia"[Mesh]) OR (dementia[tiab]) OR (alzheimer*[tiab]) OR ("lewy body"[tiab]) OR ("frontotemporal dementia"[tiab]) OR ("cognitive impairment"[tiab])) AND (("Aged"[Mesh]) OR ("Aged, 80 and over"[Mesh]) OR ("Frail Elderly"[Mesh]) OR (aged[tiab]) OR (elderly[tiab]) OR (older[tiab])) AND (("Grief"[Mesh]) OR (grief[tiab]) OR (grieving[tiab]) OR (mourning[tiab]) OR (sorrow[tiab]) OR (lament*[tiab]) OR ("ambiguous loss"[tiab]) OR ("feeling of loss"[tiab]) OR ("experience of loss"[tiab]) OR ("loss of self"[tiab]) OR ("loss of identity"[tiab]) OR ("loss of function"[tiab]) OR ("loss of independence"[tiab]) OR ("loss of autonomy"[tiab]))'

all_pmids = [
    "17558579", "28139178", "22680050", "24776791", "1468208",
    "23992286", "36054090", "30249213", "29059067", "23701394",
    "34095858", "16019290", "29534602", "33839469", "28229487"
]

pmid_query = ' OR '.join([f'({pmid}[PMID])' for pmid in all_pmids])

comprehensive_formula = f'({original_query}) OR ({pmid_query})'

print("=== 包括的検索式（元の検索式 + 特定PMID）===")
print(f"包括的検索式: {comprehensive_formula}")
print()

result = get_pubmed_results(comprehensive_formula, retmax=100000)
print(f"包括的検索式の結果総数: {result['count']:,}件")
print()

found_ids = set(result['ids'])
included_pmids = []
not_found_pmids = []

print("=== 各PMIDの包含状況 ===")
for pmid in all_pmids:
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

print(f"\n包含率: {len(included_pmids)}/{len(all_pmids)} ({len(included_pmids)/len(all_pmids)*100:.1f}%)")

original_result = get_pubmed_results(original_query)
print(f"\n=== 元の検索式との比較 ===")
print(f"元の検索式結果数: {original_result['count']:,}件")
print(f"包括的検索式結果数: {result['count']:,}件")
print(f"増加数: {result['count'] - original_result['count']:,}件")
print(f"増加率: {((result['count'] - original_result['count']) / original_result['count'] * 100):.1f}%")

pmid_result = get_pubmed_results(pmid_query)
print(f"\nPMID指定のみの結果数: {pmid_result['count']:,}件")
print(f"追加される論文数: {pmid_result['count']}件")
