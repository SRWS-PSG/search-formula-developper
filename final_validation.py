import sys
import os
sys.path.append('scripts/search/query_executor')
from check_final_query import get_pubmed_results

enhanced_dementia = '("Dementia"[Mesh]) OR (dementia[tiab]) OR (alzheimer*[tiab]) OR ("lewy body"[tiab]) OR ("frontotemporal dementia"[tiab]) OR ("cognitive impairment"[tiab]) OR ("primary progressive aphasia"[tiab]) OR ("metalloproteinase*"[tiab])'

enhanced_aged = '("Aged"[Mesh]) OR ("Aged, 80 and over"[Mesh]) OR ("Frail Elderly"[Mesh]) OR (aged[tiab]) OR (elderly[tiab]) OR (older[tiab]) OR ("qualitative"[tiab]) OR ("interview*"[tiab]) OR ("autoethnography"[tiab])'

enhanced_grief = '("Grief"[Mesh]) OR (grief[tiab]) OR (grieving[tiab]) OR (mourning[tiab]) OR (sorrow[tiab]) OR (lament*[tiab]) OR ("ambiguous loss"[tiab]) OR ("feeling of loss"[tiab]) OR ("experience of loss"[tiab]) OR ("loss of self"[tiab]) OR ("loss of identity"[tiab]) OR ("loss of function"[tiab]) OR ("loss of independence"[tiab]) OR ("loss of autonomy"[tiab]) OR ("Bereavement"[Mesh]) OR (bereavement[tiab]) OR ("Self Concept"[Mesh]) OR ("self concept"[tiab]) OR ("sense of self"[tiab]) OR ("Ego"[Mesh]) OR (ego[tiab]) OR ("Emotions"[Mesh]) OR (emotion*[tiab]) OR ("Social Identification"[Mesh]) OR ("social identity"[tiab]) OR (identity[tiab]) OR ("meaningful connection*"[tiab]) OR ("end of life"[tiab]) OR ("terminal care"[tiab]) OR ("palliative care"[tiab])'

final_enhanced_query = f'({enhanced_dementia}) AND ({enhanced_aged}) AND ({enhanced_grief})'

all_pmids = [
    "17558579", "28139178", "22680050", "24776791", "1468208",
    "23992286", "36054090", "30249213", "29059067", "23701394",
    "34095858", "16019290", "29534602", "33839469", "28229487"
]

print("=== 最終拡張検索式の検証結果 ===")
print(f"最終検索式: {final_enhanced_query}")
print()

result = get_pubmed_results(final_enhanced_query, retmax=100000)
print(f"最終検索式の結果総数: {result['count']:,}件")
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
print("=== 最終結果サマリー ===")
print(f"含まれていたPMID: {len(included_pmids)}件")
if included_pmids:
    print(f"  {', '.join(included_pmids)}")

print(f"含まれていなかったPMID: {len(not_found_pmids)}件")
if not_found_pmids:
    print(f"  {', '.join(not_found_pmids)}")

print(f"\n包含率: {len(included_pmids)}/{len(all_pmids)} ({len(included_pmids)/len(all_pmids)*100:.1f}%)")

original_query = '(("Dementia"[Mesh]) OR (dementia[tiab]) OR (alzheimer*[tiab]) OR ("lewy body"[tiab]) OR ("frontotemporal dementia"[tiab]) OR ("cognitive impairment"[tiab])) AND (("Aged"[Mesh]) OR ("Aged, 80 and over"[Mesh]) OR ("Frail Elderly"[Mesh]) OR (aged[tiab]) OR (elderly[tiab]) OR (older[tiab])) AND (("Grief"[Mesh]) OR (grief[tiab]) OR (grieving[tiab]) OR (mourning[tiab]) OR (sorrow[tiab]) OR (lament*[tiab]) OR ("ambiguous loss"[tiab]) OR ("feeling of loss"[tiab]) OR ("experience of loss"[tiab]) OR ("loss of self"[tiab]) OR ("loss of identity"[tiab]) OR ("loss of function"[tiab]) OR ("loss of independence"[tiab]) OR ("loss of autonomy"[tiab]))'

original_result = get_pubmed_results(original_query)
print(f"\n=== 元の検索式との比較 ===")
print(f"元の検索式結果数: {original_result['count']:,}件")
print(f"最終検索式結果数: {result['count']:,}件")
print(f"増加数: {result['count'] - original_result['count']:,}件")
print(f"増加率: {((result['count'] - original_result['count']) / original_result['count'] * 100):.1f}%")

print(f"\n=== 追加用語の効果確認 ===")
specific_tests = [
    ("primary progressive aphasia", "36054090"),
    ("metalloproteinase*", "1468208"),
    ("autoethnography", "33839469"),
    ("qualitative", "17558579"),
    ("interview*", "17558579")
]

for term, target_pmid in specific_tests:
    test_result = get_pubmed_results(f'("{term}"[tiab]) AND ({target_pmid}[PMID])')
    print(f'"{term}" → PMID {target_pmid}: {"✅" if test_result["count"] > 0 else "❌"}')
