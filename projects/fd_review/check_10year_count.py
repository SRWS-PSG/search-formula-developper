#!/usr/bin/env python3
"""
過去10年フィルターでのFD Review検索式の件数を測定
"""

import requests
import time
import xml.etree.ElementTree as ET


def get_count(query):
    """PubMed検索のヒット件数を取得"""
    params = {
        'db': 'pubmed',
        'term': query,
        'retmode': 'xml',
        'retmax': 0
    }
    response = requests.get(
        'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi',
        params=params,
        timeout=30
    )
    root = ET.fromstring(response.content)
    count_elem = root.find('.//Count')
    return int(count_elem.text) if count_elem is not None else 0


def main():
    # 検索式のブロック (#1 AND #2)
    block1 = (
        '"Faculty, Medical"[Mesh] OR medical faculty[tiab] OR '
        'clinical educator*[tiab] OR clinician educator*[tiab] OR '
        'medical educator*[tiab] OR clinical teacher*[tiab] OR clinical teaching[tiab]'
    )
    block2 = (
        '"Staff Development"[Mesh] OR "Program Development"[Mesh] OR '
        'faculty development*[tiab] OR professional development*[tiab] OR '
        'teaching skill*[tiab] OR "program design"[tiab]'
    )
    base_query = f'({block1}) AND ({block2})'

    # 年代制限: 過去10年 (2015-2025)
    year_filter_10y = '("2015/01/01"[PDAT] : "3000"[PDAT])'

    print('=== fd_review 検索式の件数確認 ===')
    print()

    # 制限なしの件数
    print('現在の検索式（制限なし）...', end=' ', flush=True)
    count_no_limit = get_count(base_query)
    print(f'{count_no_limit:,} 件')

    time.sleep(0.5)

    # 過去10年の件数
    print('過去10年に制限した場合......', end=' ', flush=True)
    query_10y = f'{base_query} AND {year_filter_10y}'
    count_10y = get_count(query_10y)
    print(f'{count_10y:,} 件')

    print()
    print('=== 結果サマリー ===')
    print(f'制限なし:  {count_no_limit:,} 件')
    print(f'過去10年:  {count_10y:,} 件')
    reduction = count_no_limit - count_10y
    pct = (reduction / count_no_limit * 100) if count_no_limit > 0 else 0
    print(f'削減量:    -{reduction:,} 件 ({pct:.1f}%)')

    # シード論文の捕捉確認
    print()
    print('=== シード論文の捕捉確認（過去10年フィルター適用時）===')
    seed_pmids = ['35173512', '19811202', '21821215', '38442199', '21869655']
    
    captured = []
    missed = []
    
    for pmid in seed_pmids:
        check_query = f'({query_10y}) AND {pmid}[PMID]'
        time.sleep(0.35)
        count = get_count(check_query)
        if count > 0:
            captured.append(pmid)
            print(f'  ✅ PMID {pmid}: 捕捉')
        else:
            missed.append(pmid)
            print(f'  ❌ PMID {pmid}: 捕捉できず（2015年以前の可能性）')
    
    print()
    print(f'捕捉: {len(captured)}/{len(seed_pmids)} 件')
    if missed:
        print(f'⚠️ 捕捉できないシード論文: {", ".join(missed)}')


if __name__ == '__main__':
    main()
