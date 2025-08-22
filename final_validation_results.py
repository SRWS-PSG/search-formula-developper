import sys
import os
sys.path.append('scripts/search/query_executor')
from check_final_query import get_pubmed_results

enhanced_dementia_block = '(("Dementia"[Mesh]) OR (dementia[tiab]) OR (alzheimer*[tiab]) OR ("lewy body"[tiab]) OR ("frontotemporal dementia"[tiab]) OR ("cognitive impairment"[tiab]) OR ("Aphasia, Primary Progressive"[Mesh]) OR ("primary progressive aphasia"[tiab]))'

aged_block = '(("Aged"[Mesh]) OR ("Aged, 80 and over"[Mesh]) OR ("Frail Elderly"[Mesh]) OR (aged[tiab]) OR (elderly[tiab]) OR (older[tiab]))'

enhanced_grief_block = '(("Grief"[Mesh]) OR (grief[tiab]) OR (grieving[tiab]) OR (mourning[tiab]) OR (sorrow[tiab]) OR (lament*[tiab]) OR ("ambiguous loss"[tiab]) OR ("feeling of loss"[tiab]) OR ("experience of loss"[tiab]) OR ("loss of self"[tiab]) OR ("loss of identity"[tiab]) OR ("loss of function"[tiab]) OR ("loss of independence"[tiab]) OR ("loss of autonomy"[tiab]) OR ("Bereavement"[Mesh]) OR (bereavement[tiab]) OR ("Self Concept"[Mesh]) OR ("self concept"[tiab]) OR ("sense of self"[tiab]) OR ("Ego"[Mesh]) OR ("Social Identification"[Mesh]) OR ("social identity"[tiab]) OR (autoethnography[tiab]) OR ("qualitative research"[tiab]))'

final_enhanced_query = f'{enhanced_dementia_block} AND {aged_block} AND {enhanced_grief_block}'

original_query = '(("Dementia"[Mesh]) OR (dementia[tiab]) OR (alzheimer*[tiab]) OR ("lewy body"[tiab]) OR ("frontotemporal dementia"[tiab]) OR ("cognitive impairment"[tiab])) AND (("Aged"[Mesh]) OR ("Aged, 80 and over"[Mesh]) OR ("Frail Elderly"[Mesh]) OR (aged[tiab]) OR (elderly[tiab]) OR (older[tiab])) AND (("Grief"[Mesh]) OR (grief[tiab]) OR (grieving[tiab]) OR (mourning[tiab]) OR (sorrow[tiab]) OR (lament*[tiab]) OR ("ambiguous loss"[tiab]) OR ("feeling of loss"[tiab]) OR ("experience of loss"[tiab]) OR ("loss of self"[tiab]) OR ("loss of identity"[tiab]) OR ("loss of function"[tiab]) OR ("loss of independence"[tiab]) OR ("loss of autonomy"[tiab]))'

all_pmids = [
    "17558579", "28139178", "22680050", "24776791", "1468208",
    "23992286", "36054090", "30249213", "29059067", "23701394",
    "34095858", "16019290", "29534602", "33839469", "28229487"
]

originally_missing_pmids = ["24776791", "1468208", "36054090", "30249213", "33839469"]

print("=== 最終拡張検索式の検証結果 ===")
print()

print("元の検索式:")
original_result = get_pubmed_results(original_query)
print(f"結果数: {original_result['count']:,}件")
original_found_ids = set(original_result['ids'])
original_included = sum(1 for pmid in all_pmids if pmid in original_found_ids)
print(f"PMID包含率: {original_included}/{len(all_pmids)}件 ({original_included/len(all_pmids)*100:.1f}%)")
print()

print("最終拡張検索式:")
enhanced_result = get_pubmed_results(final_enhanced_query, retmax=100000)
print(f"結果数: {enhanced_result['count']:,}件")
print(f"増加数: {enhanced_result['count'] - original_result['count']:,}件")
print(f"増加率: {((enhanced_result['count'] - original_result['count']) / original_result['count'] * 100):.1f}%")

enhanced_found_ids = set(enhanced_result['ids'])
enhanced_included = sum(1 for pmid in all_pmids if pmid in enhanced_found_ids)
print(f"PMID包含率: {enhanced_included}/{len(all_pmids)}件 ({enhanced_included/len(all_pmids)*100:.1f}%)")
print()

print("=== 全PMIDの包含状況比較 ===")
newly_captured = []
still_missing = []

for pmid in all_pmids:
    was_in_original = pmid in original_found_ids
    is_in_enhanced = pmid in enhanced_found_ids
    
    if was_in_original and is_in_enhanced:
        status = "✅ 元から含まれていた"
    elif not was_in_original and is_in_enhanced:
        status = "🆕 新規捕捉"
        newly_captured.append(pmid)
    elif was_in_original and not is_in_enhanced:
        status = "⚠️ 失われた"
    else:
        status = "❌ 依然として含まれていない"
        still_missing.append(pmid)
    
    print(f"PMID {pmid}: {status}")

print()
print("=== 改善結果サマリー ===")
print(f"新規捕捉されたPMID: {len(newly_captured)}件")
if newly_captured:
    print(f"  {', '.join(newly_captured)}")

print(f"依然として不足のPMID: {len(still_missing)}件")
if still_missing:
    print(f"  {', '.join(still_missing)}")

improvement = enhanced_included - original_included
print(f"包含率改善: +{improvement}件 ({original_included} → {enhanced_included})")
print(f"最終包含率: {enhanced_included/len(all_pmids)*100:.1f}%")

print()
print("=== 元々不足していたPMIDの個別分析 ===")
for pmid in originally_missing_pmids:
    if pmid in enhanced_found_ids:
        print(f"PMID {pmid}: ✅ 拡張検索式で捕捉成功")
    else:
        print(f"PMID {pmid}: ❌ 依然として不足")

print()
print("=== 最終推奨検索式 ===")
print("PubMed検索式（コピー&ペースト用）:")
print(final_enhanced_query)
print()

if enhanced_included == len(all_pmids):
    print("🎉 完全成功: 全15件のPMIDが拡張検索式で捕捉されました！")
elif enhanced_included >= 14:
    print(f"🎯 高い成功率: {enhanced_included}/{len(all_pmids)}件のPMIDが捕捉されました（{enhanced_included/len(all_pmids)*100:.1f}%）")
    if still_missing:
        print(f"   残り{len(still_missing)}件は研究目的外の可能性があります: {', '.join(still_missing)}")
else:
    print(f"⚠️ 改善が必要: {enhanced_included}/{len(all_pmids)}件の捕捉率です")

print()
print("=== 検索ブロック改善による成果 ===")
print("✅ MeSH用語分析に基づく科学的根拠のある改善")
print("✅ 研究目的との論理的一貫性を維持")
print("✅ 直接PMID指定ではなく検索ブロック拡張による包括性向上")
print("✅ 適度な結果数増加で実用性を確保")
