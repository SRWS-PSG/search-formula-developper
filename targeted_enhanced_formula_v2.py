import sys
import os
sys.path.append('scripts/search/query_executor')
from check_final_query import get_pubmed_results

original_query = '(("Dementia"[Mesh]) OR (dementia[tiab]) OR (alzheimer*[tiab]) OR ("lewy body"[tiab]) OR ("frontotemporal dementia"[tiab]) OR ("cognitive impairment"[tiab])) AND (("Aged"[Mesh]) OR ("Aged, 80 and over"[Mesh]) OR ("Frail Elderly"[Mesh]) OR (aged[tiab]) OR (elderly[tiab]) OR (older[tiab])) AND (("Grief"[Mesh]) OR (grief[tiab]) OR (grieving[tiab]) OR (mourning[tiab]) OR (sorrow[tiab]) OR (lament*[tiab]) OR ("ambiguous loss"[tiab]) OR ("feeling of loss"[tiab]) OR ("experience of loss"[tiab]) OR ("loss of self"[tiab]) OR ("loss of identity"[tiab]) OR ("loss of function"[tiab]) OR ("loss of independence"[tiab]) OR ("loss of autonomy"[tiab]))'

targeted_dementia_block = '(("Dementia"[Mesh]) OR (dementia[tiab]) OR (alzheimer*[tiab]) OR ("lewy body"[tiab]) OR ("frontotemporal dementia"[tiab]) OR ("cognitive impairment"[tiab]) OR ("Aphasia, Primary Progressive"[Mesh]) OR ("primary progressive aphasia"[tiab]))'

aged_block = '(("Aged"[Mesh]) OR ("Aged, 80 and over"[Mesh]) OR ("Frail Elderly"[Mesh]) OR (aged[tiab]) OR (elderly[tiab]) OR (older[tiab]))'

targeted_grief_block = '(("Grief"[Mesh]) OR (grief[tiab]) OR (grieving[tiab]) OR (mourning[tiab]) OR (sorrow[tiab]) OR (lament*[tiab]) OR ("ambiguous loss"[tiab]) OR ("feeling of loss"[tiab]) OR ("experience of loss"[tiab]) OR ("loss of self"[tiab]) OR ("loss of identity"[tiab]) OR ("loss of function"[tiab]) OR ("loss of independence"[tiab]) OR ("loss of autonomy"[tiab]) OR ("Bereavement"[Mesh]) OR (bereavement[tiab]) OR ("Self Concept"[Mesh]) OR ("self concept"[tiab]) OR ("sense of self"[tiab]) OR ("Ego"[Mesh]) OR ("Social Identification"[Mesh]) OR ("social identity"[tiab]))'

targeted_query = f'{targeted_dementia_block} AND {aged_block} AND {targeted_grief_block}'

missing_pmids = ["24776791", "1468208", "36054090", "30249213", "33839469"]
all_pmids = [
    "17558579", "28139178", "22680050", "24776791", "1468208",
    "23992286", "36054090", "30249213", "29059067", "23701394",
    "34095858", "16019290", "29534602", "33839469", "28229487"
]

print("=== ターゲット型拡張検索式の検証 ===")
print()

print("元の検索式:")
original_result = get_pubmed_results(original_query)
print(f"結果数: {original_result['count']:,}件")
print()

print("ターゲット型拡張検索式:")
targeted_result = get_pubmed_results(targeted_query, retmax=100000)
print(f"結果数: {targeted_result['count']:,}件")
print(f"増加数: {targeted_result['count'] - original_result['count']:,}件")
print(f"増加率: {((targeted_result['count'] - original_result['count']) / original_result['count'] * 100):.1f}%")
print()

found_ids = set(targeted_result['ids'])
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
print("=== 残り不足PMIDの個別ブロック分析 ===")

dementia_result = get_pubmed_results(targeted_dementia_block, retmax=100000)
aged_result = get_pubmed_results(aged_block, retmax=100000)
grief_result = get_pubmed_results(targeted_grief_block, retmax=100000)

dementia_ids = set(dementia_result['ids'])
aged_ids = set(aged_result['ids'])
grief_ids = set(grief_result['ids'])

for pmid in not_found_pmids:
    print(f"PMID {pmid}:")
    print(f"  認知症ブロック: {'✅' if pmid in dementia_ids else '❌'}")
    print(f"  高齢者ブロック: {'✅' if pmid in aged_ids else '❌'}")
    print(f"  悲嘆ブロック: {'✅' if pmid in grief_ids else '❌'}")
    
    missing_blocks = []
    if pmid not in dementia_ids:
        missing_blocks.append("認知症")
    if pmid not in aged_ids:
        missing_blocks.append("高齢者")
    if pmid not in grief_ids:
        missing_blocks.append("悲嘆")
    
    if missing_blocks:
        print(f"  → 不足ブロック: {', '.join(missing_blocks)}")
    print()

print("=== 残り不足PMIDの特定用語テスト ===")

metalloproteinase_query = '("Metalloendopeptidases"[Mesh]) OR (metalloproteinase*[tiab]) OR (metalloendopeptidase*[tiab])'
metalloproteinase_result = get_pubmed_results(metalloproteinase_query, retmax=100000)
metalloproteinase_ids = set(metalloproteinase_result['ids'])
print(f"Metalloproteinase用語でPMID 1468208: {'✅' if '1468208' in metalloproteinase_ids else '❌'}")

ppa_query = '("Aphasia, Primary Progressive"[Mesh]) OR ("primary progressive aphasia"[tiab])'
ppa_result = get_pubmed_results(ppa_query, retmax=100000)
ppa_ids = set(ppa_result['ids'])
print(f"Primary Progressive Aphasia用語でPMID 36054090: {'✅' if '36054090' in ppa_ids else '❌'}")

autoethnography_query = '(autoethnography[tiab]) OR ("qualitative research"[tiab]) OR ("social identification"[tiab])'
autoethnography_result = get_pubmed_results(autoethnography_query, retmax=100000)
autoethnography_ids = set(autoethnography_result['ids'])
print(f"Autoethnography用語でPMID 33839469: {'✅' if '33839469' in autoethnography_ids else '❌'}")

print()
print("=== PubMed検索式（コピー&ペースト用）===")
print(targeted_query)
