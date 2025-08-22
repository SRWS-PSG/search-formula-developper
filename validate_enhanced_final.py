import sys
import os
sys.path.append('scripts/search/query_executor')
from check_final_query import get_pubmed_results

original_query = '(("Dementia"[Mesh]) OR (dementia[tiab]) OR (alzheimer*[tiab]) OR ("lewy body"[tiab]) OR ("frontotemporal dementia"[tiab]) OR ("cognitive impairment"[tiab])) AND (("Aged"[Mesh]) OR ("Aged, 80 and over"[Mesh]) OR ("Frail Elderly"[Mesh]) OR (aged[tiab]) OR (elderly[tiab]) OR (older[tiab])) AND (("Grief"[Mesh]) OR (grief[tiab]) OR (grieving[tiab]) OR (mourning[tiab]) OR (sorrow[tiab]) OR (lament*[tiab]) OR ("ambiguous loss"[tiab]) OR ("feeling of loss"[tiab]) OR ("experience of loss"[tiab]) OR ("loss of self"[tiab]) OR ("loss of identity"[tiab]) OR ("loss of function"[tiab]) OR ("loss of independence"[tiab]) OR ("loss of autonomy"[tiab]))'

enhanced_dementia_block = '(("Dementia"[Mesh]) OR (dementia[tiab]) OR (alzheimer*[tiab]) OR ("lewy body"[tiab]) OR ("frontotemporal dementia"[tiab]) OR ("cognitive impairment"[tiab]) OR ("Aphasia, Primary Progressive"[Mesh]) OR ("primary progressive aphasia"[tiab]))'

aged_block = '(("Aged"[Mesh]) OR ("Aged, 80 and over"[Mesh]) OR ("Frail Elderly"[Mesh]) OR (aged[tiab]) OR (elderly[tiab]) OR (older[tiab]))'

enhanced_grief_block = '(("Grief"[Mesh]) OR (grief[tiab]) OR (grieving[tiab]) OR (mourning[tiab]) OR (sorrow[tiab]) OR (lament*[tiab]) OR ("ambiguous loss"[tiab]) OR ("feeling of loss"[tiab]) OR ("experience of loss"[tiab]) OR ("loss of self"[tiab]) OR ("loss of identity"[tiab]) OR ("loss of function"[tiab]) OR ("loss of independence"[tiab]) OR ("loss of autonomy"[tiab]) OR ("Bereavement"[Mesh]) OR (bereavement[tiab]) OR ("Self Concept"[Mesh]) OR ("self concept"[tiab]) OR ("sense of self"[tiab]) OR ("Ego"[Mesh]) OR (ego[tiab]) OR ("Emotions"[Mesh]) OR (emotion*[tiab]) OR ("Social Identification"[Mesh]) OR ("social identity"[tiab]) OR (identity[tiab]) OR ("meaningful connection*"[tiab]) OR ("end of life"[tiab]) OR ("terminal care"[tiab]) OR ("palliative care"[tiab]) OR ("interpersonal relation*"[tiab]))'

enhanced_query = f'{enhanced_dementia_block} AND {aged_block} AND {enhanced_grief_block}'

all_pmids = [
    "17558579", "28139178", "22680050", "24776791", "1468208",
    "23992286", "36054090", "30249213", "29059067", "23701394",
    "34095858", "16019290", "29534602", "33839469", "28229487"
]

missing_pmids = ["24776791", "1468208", "36054090", "30249213", "33839469"]

print("=== 拡張検索式の検証 ===")
print()

print("元の検索式:")
original_result = get_pubmed_results(original_query)
print(f"結果数: {original_result['count']:,}件")
print()

print("拡張検索式:")
print(f"拡張認知症ブロック: {enhanced_dementia_block}")
print(f"高齢者ブロック: {aged_block}")
print(f"拡張悲嘆ブロック: {enhanced_grief_block}")
print()

enhanced_result = get_pubmed_results(enhanced_query, retmax=100000)
print(f"拡張検索式結果数: {enhanced_result['count']:,}件")
print(f"増加数: {enhanced_result['count'] - original_result['count']:,}件")
print(f"増加率: {((enhanced_result['count'] - original_result['count']) / original_result['count'] * 100):.1f}%")
print()

found_ids = set(enhanced_result['ids'])
included_pmids = []
not_found_pmids = []

print("=== 全PMIDの包含状況 ===")
for pmid in all_pmids:
    if pmid in found_ids:
        included_pmids.append(pmid)
        status = "✅ 含まれています"
        if pmid in missing_pmids:
            status += " (新規捕捉)"
    else:
        not_found_pmids.append(pmid)
        status = "❌ 含まれていません"
    print(f"PMID {pmid}: {status}")

print()
print("=== 結果サマリー ===")
print(f"含まれていたPMID: {len(included_pmids)}/{len(all_pmids)}件 ({len(included_pmids)/len(all_pmids)*100:.1f}%)")
print(f"含まれていなかったPMID: {len(not_found_pmids)}件")

if not_found_pmids:
    print(f"  未包含PMID: {', '.join(not_found_pmids)}")

print()
print("=== 不足PMIDの個別検証 ===")
print()

print("1. 拡張認知症ブロック単体での検証:")
dementia_result = get_pubmed_results(enhanced_dementia_block, retmax=100000)
dementia_ids = set(dementia_result['ids'])
print(f"   結果数: {dementia_result['count']:,}件")
for pmid in missing_pmids:
    status = "✅ 含まれています" if pmid in dementia_ids else "❌ 含まれていません"
    print(f"   PMID {pmid}: {status}")

print()
print("2. 高齢者ブロック単体での検証:")
aged_result = get_pubmed_results(aged_block, retmax=100000)
aged_ids = set(aged_result['ids'])
print(f"   結果数: {aged_result['count']:,}件")
for pmid in missing_pmids:
    status = "✅ 含まれています" if pmid in aged_ids else "❌ 含まれていません"
    print(f"   PMID {pmid}: {status}")

print()
print("3. 拡張悲嘆ブロック単体での検証:")
grief_result = get_pubmed_results(enhanced_grief_block, retmax=100000)
grief_ids = set(grief_result['ids'])
print(f"   結果数: {grief_result['count']:,}件")
for pmid in missing_pmids:
    status = "✅ 含まれています" if pmid in grief_ids else "❌ 含まれていません"
    print(f"   PMID {pmid}: {status}")

print()
print("=== 各PMIDのブロック別包含パターン ===")
for pmid in missing_pmids:
    print(f"PMID {pmid}:")
    print(f"  認知症ブロック: {'✅' if pmid in dementia_ids else '❌'}")
    print(f"  高齢者ブロック: {'✅' if pmid in aged_ids else '❌'}")
    print(f"  悲嘆ブロック: {'✅' if pmid in grief_ids else '❌'}")
    
    if pmid in dementia_ids and pmid in aged_ids and pmid in grief_ids:
        print(f"  → AND検索で包含される ✅")
    else:
        missing_blocks = []
        if pmid not in dementia_ids:
            missing_blocks.append("認知症")
        if pmid not in aged_ids:
            missing_blocks.append("高齢者")
        if pmid not in grief_ids:
            missing_blocks.append("悲嘆")
        print(f"  → AND検索で除外される（{', '.join(missing_blocks)}ブロックに含まれていない）❌")
    print()

if len(included_pmids) == len(all_pmids):
    print("🎉 成功: 全15件のPMIDが拡張検索式で捕捉されました！")
else:
    print(f"⚠️  改善が必要: {len(not_found_pmids)}件のPMIDがまだ捕捉されていません")

print()
print("=== PubMed検索式（コピー&ペースト用）===")
print(enhanced_query)
