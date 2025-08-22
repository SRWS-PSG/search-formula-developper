import sys
import os
sys.path.append('scripts/search/query_executor')
from check_final_query import get_pubmed_results

missing_pmids = ["17558579", "1468208", "36054090", "16019290", "33839469"]

print("=== 個別PMID分析 ===")

dementia_query = '("Dementia"[Mesh]) OR (dementia[tiab]) OR (alzheimer*[tiab]) OR ("lewy body"[tiab]) OR ("frontotemporal dementia"[tiab]) OR ("cognitive impairment"[tiab])'
aged_query = '("Aged"[Mesh]) OR ("Aged, 80 and over"[Mesh]) OR ("Frail Elderly"[Mesh]) OR (aged[tiab]) OR (elderly[tiab]) OR (older[tiab])'
grief_query = '("Grief"[Mesh]) OR (grief[tiab]) OR (grieving[tiab]) OR (mourning[tiab]) OR (sorrow[tiab]) OR (lament*[tiab]) OR ("ambiguous loss"[tiab]) OR ("feeling of loss"[tiab]) OR ("experience of loss"[tiab]) OR ("loss of self"[tiab]) OR ("loss of identity"[tiab]) OR ("loss of function"[tiab]) OR ("loss of independence"[tiab]) OR ("loss of autonomy"[tiab]) OR ("Bereavement"[Mesh]) OR (bereavement[tiab]) OR ("Self Concept"[Mesh]) OR ("self concept"[tiab]) OR ("sense of self"[tiab]) OR ("Ego"[Mesh]) OR (ego[tiab]) OR ("Emotions"[Mesh]) OR (emotion*[tiab]) OR ("Social Identification"[Mesh]) OR ("social identity"[tiab]) OR (identity[tiab]) OR ("meaningful connection*"[tiab]) OR ("end of life"[tiab]) OR ("terminal care"[tiab]) OR ("palliative care"[tiab])'

for pmid in missing_pmids:
    print(f"\n--- PMID {pmid} ---")
    
    dementia_result = get_pubmed_results(f'({dementia_query}) AND ({pmid}[PMID])')
    aged_result = get_pubmed_results(f'({aged_query}) AND ({pmid}[PMID])')
    grief_result = get_pubmed_results(f'({grief_query}) AND ({pmid}[PMID])')
    
    print(f"認知症ブロック: {'✅' if dementia_result['count'] > 0 else '❌'}")
    print(f"高齢者ブロック: {'✅' if aged_result['count'] > 0 else '❌'}")
    print(f"悲嘆ブロック: {'✅' if grief_result['count'] > 0 else '❌'}")
    
    if dementia_result['count'] == 0:
        print("  → 認知症関連用語が不足")
    if aged_result['count'] == 0:
        print("  → 高齢者関連用語が不足")
    if grief_result['count'] == 0:
        print("  → 悲嘆関連用語が不足")

print("\n=== 特定用語テスト ===")
test_terms = [
    '"Primary Progressive Aphasia"[Mesh]',
    '"primary progressive aphasia"[tiab]',
    '"metalloproteinase*"[tiab]',
    '"tissue inhibitor*"[tiab]',
    '"autoethnography"[tiab]',
    '"emergency"[tiab]',
    '"hospital"[tiab]',
    '"qualitative"[tiab]',
    '"interview*"[tiab]',
    '"narrative*"[tiab]'
]

for term in test_terms:
    result = get_pubmed_results(term)
    print(f"{term}: {result['count']:,}件")
    
    captured = []
    for pmid in missing_pmids:
        pmid_result = get_pubmed_results(f'({term}) AND ({pmid}[PMID])')
        if pmid_result['count'] > 0:
            captured.append(pmid)
    
    if captured:
        print(f"  → 捕捉PMID: {', '.join(captured)}")
