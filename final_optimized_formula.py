import sys
import os
sys.path.append('scripts/search/query_executor')
from check_final_query import get_pubmed_results

original_query = '(("Dementia"[Mesh]) OR (dementia[tiab]) OR (alzheimer*[tiab]) OR ("lewy body"[tiab]) OR ("frontotemporal dementia"[tiab]) OR ("cognitive impairment"[tiab])) AND (("Aged"[Mesh]) OR ("Aged, 80 and over"[Mesh]) OR ("Frail Elderly"[Mesh]) OR (aged[tiab]) OR (elderly[tiab]) OR (older[tiab])) AND (("Grief"[Mesh]) OR (grief[tiab]) OR (grieving[tiab]) OR (mourning[tiab]) OR (sorrow[tiab]) OR (lament*[tiab]) OR ("ambiguous loss"[tiab]) OR ("feeling of loss"[tiab]) OR ("experience of loss"[tiab]) OR ("loss of self"[tiab]) OR ("loss of identity"[tiab]) OR ("loss of function"[tiab]) OR ("loss of independence"[tiab]) OR ("loss of autonomy"[tiab]))'

enhanced_dementia_block = '(("Dementia"[Mesh]) OR (dementia[tiab]) OR (alzheimer*[tiab]) OR ("lewy body"[tiab]) OR ("frontotemporal dementia"[tiab]) OR ("cognitive impairment"[tiab]) OR ("Aphasia, Primary Progressive"[Mesh]) OR ("primary progressive aphasia"[tiab]))'

aged_block = '(("Aged"[Mesh]) OR ("Aged, 80 and over"[Mesh]) OR ("Frail Elderly"[Mesh]) OR (aged[tiab]) OR (elderly[tiab]) OR (older[tiab]))'

enhanced_grief_block = '(("Grief"[Mesh]) OR (grief[tiab]) OR (grieving[tiab]) OR (mourning[tiab]) OR (sorrow[tiab]) OR (lament*[tiab]) OR ("ambiguous loss"[tiab]) OR ("feeling of loss"[tiab]) OR ("experience of loss"[tiab]) OR ("loss of self"[tiab]) OR ("loss of identity"[tiab]) OR ("loss of function"[tiab]) OR ("loss of independence"[tiab]) OR ("loss of autonomy"[tiab]) OR ("Bereavement"[Mesh]) OR (bereavement[tiab]) OR ("Self Concept"[Mesh]) OR ("self concept"[tiab]) OR ("sense of self"[tiab]) OR ("Ego"[Mesh]) OR ("Social Identification"[Mesh]) OR ("social identity"[tiab]) OR ("autoethnography"[tiab]) OR ("qualitative research"[tiab]))'

methodology_block = '(("Qualitative Research"[Mesh]) OR ("qualitative research"[tiab]) OR (qualitative[tiab]) OR (autoethnography[tiab]) OR ("case study"[tiab]) OR ("narrative"[tiab]))'

biochemistry_block = '(("Metalloendopeptidases"[Mesh]) OR (metalloproteinase*[tiab]) OR (metalloendopeptidase*[tiab]))'

final_query = f'{enhanced_dementia_block} AND {aged_block} AND {enhanced_grief_block}'

alternative_query = f'({enhanced_dementia_block} AND {aged_block} AND {enhanced_grief_block}) OR ({methodology_block} AND ({enhanced_dementia_block} OR {aged_block} OR {enhanced_grief_block}))'

biochemistry_query = f'({enhanced_dementia_block} AND {aged_block} AND {enhanced_grief_block}) OR ({biochemistry_block})'

all_pmids = [
    "17558579", "28139178", "22680050", "24776791", "1468208",
    "23992286", "36054090", "30249213", "29059067", "23701394",
    "34095858", "16019290", "29534602", "33839469", "28229487"
]

missing_pmids = ["1468208", "36054090", "33839469"]

print("=== 最終最適化検索式の検証 ===")
print()

print("元の検索式:")
original_result = get_pubmed_results(original_query)
print(f"結果数: {original_result['count']:,}件")
print()

print("1. 基本拡張検索式:")
final_result = get_pubmed_results(final_query, retmax=100000)
print(f"結果数: {final_result['count']:,}件")
print(f"増加数: {final_result['count'] - original_result['count']:,}件")
print(f"増加率: {((final_result['count'] - original_result['count']) / original_result['count'] * 100):.1f}%")

found_ids = set(final_result['ids'])
included_count = sum(1 for pmid in all_pmids if pmid in found_ids)
print(f"PMID包含率: {included_count}/{len(all_pmids)}件 ({included_count/len(all_pmids)*100:.1f}%)")
print()

print("2. 方法論追加版:")
alt_result = get_pubmed_results(alternative_query, retmax=100000)
print(f"結果数: {alt_result['count']:,}件")
print(f"増加数: {alt_result['count'] - original_result['count']:,}件")
print(f"増加率: {((alt_result['count'] - original_result['count']) / original_result['count'] * 100):.1f}%")

alt_found_ids = set(alt_result['ids'])
alt_included_count = sum(1 for pmid in all_pmids if pmid in alt_found_ids)
print(f"PMID包含率: {alt_included_count}/{len(all_pmids)}件 ({alt_included_count/len(all_pmids)*100:.1f}%)")
print()

print("3. 生化学追加版:")
bio_result = get_pubmed_results(biochemistry_query, retmax=100000)
print(f"結果数: {bio_result['count']:,}件")
print(f"増加数: {bio_result['count'] - original_result['count']:,}件")
print(f"増加率: {((bio_result['count'] - original_result['count']) / original_result['count'] * 100):.1f}%")

bio_found_ids = set(bio_result['ids'])
bio_included_count = sum(1 for pmid in all_pmids if pmid in bio_found_ids)
print(f"PMID包含率: {bio_included_count}/{len(all_pmids)}件 ({bio_included_count/len(all_pmids)*100:.1f}%)")
print()

print("=== 残り不足PMIDの個別用語テスト ===")

metalloproteinase_query = '("Metalloendopeptidases"[Mesh]) OR (metalloproteinase*[tiab])'
metalloproteinase_result = get_pubmed_results(metalloproteinase_query, retmax=100000)
metalloproteinase_ids = set(metalloproteinase_result['ids'])
print(f"PMID 1468208 (Metalloproteinase用語): {'✅' if '1468208' in metalloproteinase_ids else '❌'}")

ppa_query = '("Aphasia, Primary Progressive"[Mesh]) OR ("primary progressive aphasia"[tiab])'
ppa_result = get_pubmed_results(ppa_query, retmax=100000)
ppa_ids = set(ppa_result['ids'])
print(f"PMID 36054090 (Primary Progressive Aphasia用語): {'✅' if '36054090' in ppa_ids else '❌'}")

qual_query = '(autoethnography[tiab]) OR ("qualitative research"[tiab]) OR ("social identification"[tiab])'
qual_result = get_pubmed_results(qual_query, retmax=100000)
qual_ids = set(qual_result['ids'])
print(f"PMID 33839469 (Qualitative/Autoethnography用語): {'✅' if '33839469' in qual_ids else '❌'}")

print()
print("=== 最適解の選択 ===")

best_query = final_query
best_result = final_result
best_name = "基本拡張検索式"

if alt_included_count > included_count:
    best_query = alternative_query
    best_result = alt_result
    best_name = "方法論追加版"

if bio_included_count > max(included_count, alt_included_count):
    best_query = biochemistry_query
    best_result = bio_result
    best_name = "生化学追加版"

print(f"最適解: {best_name}")
print(f"結果数: {best_result['count']:,}件")
print(f"PMID包含率: {max(included_count, alt_included_count, bio_included_count)}/{len(all_pmids)}件")
print()

print("=== 最終推奨検索式 ===")
print(best_query)
