#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nitta_depression検索式検証スクリプト
シード論文が検索式の各ブロックおよび最終検索式でヒットするかを検証する
"""

import requests
import time
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple

# シード論文リスト
SEED_PMIDS = ["32779276", "33070280", "35001472", "40879352", "35109805"]

# 検索式ブロック
SEARCH_BLOCKS = {
    "Block1_Cancer": '(neoplasms[MeSH] OR neoplasm*[tiab] OR cancer*[tiab] OR carcinoma*[tiab] OR tumour*[tiab] OR tumor*[tiab] OR adenocarcinoma*[tiab] OR leukemi*[tiab] OR leukaemi*[tiab] OR lymphoma*[tiab] OR myeloma*[tiab] OR sarcoma*[tiab] OR melanoma*[tiab] OR glioma*[tiab] OR malignan*[tiab] OR oncolog*[tiab] OR metastati*[tiab] OR metastas*[tiab])',
    
    "Block2_Database": '((NDB[tiab] OR "National Database"[tiab]) OR (JMDC[tiab] OR "Japan Medical Data Center"[tiab]) OR DeSC[tiab] OR ("DPC"[tiab] OR "Diagnosis Procedure Combination database"[tiab]) OR (NCD[tiab] OR "National Clinical Database"[tiab]) OR ("MID-NET"[tiab] OR "Medical Information Database Network"[tiab]) OR (NCDA[tiab] OR "National Hospital Organization Clinical Data Archives"[tiab]) OR JAMDAS[tiab] OR (FHRD[tiab] OR "Flatiron"[tiab]) OR ("LIFE Study"[tiab] OR "longevity improvement and fair evidence study"[tiab]) OR REZULT[tiab] OR IQVIA[tiab] OR (NHWS[tiab] OR "National Health and Wellness Survey"[tiab]) OR (KDB[tiab] OR Kokuho[tiab]) OR (MDV[tiab] OR "Medical data Vision"[tiab]) OR ((RWD[tiab] OR "real-world data"[tiab]) OR administrative data*[tiab] OR claims data*[tiab] OR insurance data*[tiab] OR payer data*[tiab] OR ("record linkage"[tiab] OR "data linkage"[tiab] OR linked data*[tiab]) OR registry[tiab] OR "cancer registry"[tiab]))',
    
    "Block3_Japan": '(Japan[Mesh] OR Japan*[tiab] OR Japanese[tiab])',
    
    "Block4_Depression": '(depression[MeSH] OR "depressive disorder"[MeSH] OR depress*[tiab])'
}


def get_pubmed_details(pmid: str) -> Dict:
    """PubMed APIから論文の詳細情報を取得"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    fetch_url = f"{base_url}/efetch.fcgi"
    
    params = {
        'db': 'pubmed',
        'id': pmid,
        'retmode': 'xml'
    }
    
    try:
        response = requests.get(fetch_url, params=params)
        response.raise_for_status()
        xml_text = response.text
        
        # タイトル抽出
        title = "N/A"
        if '<ArticleTitle>' in xml_text:
            title_start = xml_text.find('<ArticleTitle>') + 14
            title_end = xml_text.find('</ArticleTitle>')
            title = xml_text[title_start:title_end]
        
        # 著者抽出
        authors = []
        if '<AuthorList' in xml_text:
            author_section = xml_text.split('<AuthorList')[1].split('</AuthorList>')[0]
            for author_block in author_section.split('<Author '):
                if '<LastName>' in author_block:
                    last_start = author_block.find('<LastName>') + 10
                    last_end = author_block.find('</LastName>')
                    last_name = author_block[last_start:last_end]
                    authors.append(last_name)
        
        # MeSH用語抽出
        mesh_terms = []
        if '<MeshHeadingList>' in xml_text:
            mesh_section = xml_text.split('<MeshHeadingList>')[1].split('</MeshHeadingList>')[0]
            for mesh_block in mesh_section.split('<DescriptorName'):
                if '>' in mesh_block and '</' in mesh_block:
                    term_start = mesh_block.find('>') + 1
                    term_end = mesh_block.find('</DescriptorName')
                    if term_end > term_start:
                        mesh_terms.append(mesh_block[term_start:term_end])
        
        # 出版年
        year = "N/A"
        if '<PubDate>' in xml_text:
            pub_section = xml_text.split('<PubDate>')[1].split('</PubDate>')[0]
            if '<Year>' in pub_section:
                year_start = pub_section.find('<Year>') + 6
                year_end = pub_section.find('</Year>')
                year = pub_section[year_start:year_end]
        
        return {
            'pmid': pmid,
            'title': title,
            'authors': authors[:3],  # 最初の3著者のみ
            'year': year,
            'mesh_terms': mesh_terms,
            'found': True
        }
    except Exception as e:
        return {
            'pmid': pmid,
            'title': f"Error: {str(e)}",
            'authors': [],
            'year': "N/A",
            'mesh_terms': [],
            'found': False
        }


def check_pmid_in_query(pmid: str, query: str) -> Tuple[bool, int]:
    """指定PMIDがクエリ結果に含まれるかチェック"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    search_url = f"{base_url}/esearch.fcgi"
    
    # クエリにPMIDフィルターを追加
    filtered_query = f"({query}) AND {pmid}[PMID]"
    
    params = {
        'db': 'pubmed',
        'term': filtered_query,
        'retmode': 'json'
    }
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        count = int(data['esearchresult'].get('count', 0))
        return count > 0, count
    except Exception as e:
        print(f"  Error: {str(e)}")
        return False, 0


def get_total_hits(query: str) -> int:
    """検索式の総ヒット数を取得"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    search_url = f"{base_url}/esearch.fcgi"
    
    params = {
        'db': 'pubmed',
        'term': query,
        'retmode': 'json',
        'retmax': 0
    }
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        return int(data['esearchresult'].get('count', 0))
    except:
        return -1


def main():
    print("=" * 60)
    print("nitta_depression PubMed検索式検証")
    print("=" * 60)
    print(f"\n実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"シード論文数: {len(SEED_PMIDS)}")
    
    # 出力ディレクトリ（スクリプトと同じディレクトリ）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = script_dir
    
    results = {
        'paper_details': [],
        'block_results': {},
        'final_results': []
    }
    
    # Step 1: シード論文の詳細取得
    print("\n" + "-" * 40)
    print("Step 1: シード論文の詳細情報を取得")
    print("-" * 40)
    
    for pmid in SEED_PMIDS:
        print(f"\n  PMID {pmid} を取得中...")
        time.sleep(0.4)
        details = get_pubmed_details(pmid)
        results['paper_details'].append(details)
        
        if details['found']:
            print(f"    タイトル: {details['title'][:60]}...")
            print(f"    年: {details['year']}")
            print(f"    MeSH用語数: {len(details['mesh_terms'])}")
        else:
            print(f"    [ERROR] 取得失敗")
    
    # Step 2: 各ブロックでの検証
    print("\n" + "-" * 40)
    print("Step 2: 各検索ブロックでのヒット確認")
    print("-" * 40)
    
    for block_name, block_query in SEARCH_BLOCKS.items():
        print(f"\n  {block_name}:")
        time.sleep(0.3)
        total_hits = get_total_hits(block_query)
        print(f"    総ヒット数: {total_hits:,}")
        
        results['block_results'][block_name] = {
            'total_hits': total_hits,
            'pmid_results': {}
        }
        
        for pmid in SEED_PMIDS:
            time.sleep(0.3)
            found, _ = check_pmid_in_query(pmid, block_query)
            results['block_results'][block_name]['pmid_results'][pmid] = found
            status = " OK " if found else "[NG]"
            print(f"    PMID {pmid}: {status}")
    
    # Step 3: 最終検索式での検証
    print("\n" + "-" * 40)
    print("Step 3: 最終検索式での検証")
    print("-" * 40)
    
    # 4ブロックを組み合わせ
    final_query = f"({SEARCH_BLOCKS['Block1_Cancer']}) AND ({SEARCH_BLOCKS['Block2_Database']}) AND ({SEARCH_BLOCKS['Block3_Japan']}) AND ({SEARCH_BLOCKS['Block4_Depression']}) NOT (animals[mh] NOT humans[mh])"
    
    time.sleep(0.3)
    total_hits = get_total_hits(final_query)
    print(f"\n  最終検索式の総ヒット数: {total_hits:,}")
    
    for pmid in SEED_PMIDS:
        time.sleep(0.4)
        found, _ = check_pmid_in_query(pmid, final_query)
        
        paper_info = next((p for p in results['paper_details'] if p['pmid'] == pmid), None)
        results['final_results'].append({
            'pmid': pmid,
            'found': found,
            'title': paper_info['title'] if paper_info else "N/A"
        })
        
        status = " OK " if found else "[NG]"
        print(f"  PMID {pmid}: {status}")
    
    # Step 4: 結果サマリー
    print("\n" + "=" * 60)
    print("検証結果サマリー")
    print("=" * 60)
    
    found_count = sum(1 for r in results['final_results'] if r['found'])
    not_found_count = len(results['final_results']) - found_count
    
    print(f"\n最終検索式でのシード論文検出:")
    print(f"  検出: {found_count}/{len(SEED_PMIDS)} ({found_count/len(SEED_PMIDS)*100:.1f}%)")
    print(f"  未検出: {not_found_count}/{len(SEED_PMIDS)} ({not_found_count/len(SEED_PMIDS)*100:.1f}%)")
    
    if not_found_count > 0:
        print("\n[WARNING] 未検出の論文:")
        for r in results['final_results']:
            if not r['found']:
                print(f"  - PMID {r['pmid']}: {r['title'][:50]}...")
                
                # どのブロックで落ちているか分析
                print("    ブロック別:")
                for block_name in SEARCH_BLOCKS.keys():
                    block_found = results['block_results'][block_name]['pmid_results'].get(r['pmid'], False)
                    status = " OK " if block_found else "[NG]"
                    print(f"      {block_name}: {status}")
    
    # レポートをMarkdownファイルとして保存
    report_path = os.path.join(project_dir, "verification_report.md")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# nitta_depression 検索式検証レポート\n\n")
        f.write(f"**実行日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## シード論文\n\n")
        f.write("| PMID | タイトル | 年 | 最終検索式 |\n")
        f.write("|------|----------|----|-----------|\n")
        for i, details in enumerate(results['paper_details']):
            final_found = results['final_results'][i]['found']
            status = "✓" if final_found else "✗"
            title_short = details['title'][:50] + "..." if len(details['title']) > 50 else details['title']
            f.write(f"| [{details['pmid']}](https://pubmed.ncbi.nlm.nih.gov/{details['pmid']}/) | {title_short} | {details['year']} | {status} |\n")
        
        f.write("\n## 各ブロックでのヒット状況\n\n")
        f.write("| PMID | Block1_Cancer | Block2_Database | Block3_Japan | Block4_Depression |\n")
        f.write("|------|---------------|-----------------|--------------|-------------------|\n")
        for pmid in SEED_PMIDS:
            row = f"| {pmid} |"
            for block_name in SEARCH_BLOCKS.keys():
                found = results['block_results'][block_name]['pmid_results'].get(pmid, False)
                row += " ✓ |" if found else " ✗ |"
            f.write(row + "\n")
        
        f.write("\n## 各ブロックの検索ヒット数\n\n")
        for block_name in SEARCH_BLOCKS.keys():
            hits = results['block_results'][block_name]['total_hits']
            f.write(f"- **{block_name}**: {hits:,} 件\n")
        
        f.write(f"\n## 最終検索式\n\n")
        f.write(f"**総ヒット数**: {total_hits:,} 件\n\n")
        f.write(f"**シード論文検出率**: {found_count}/{len(SEED_PMIDS)} ({found_count/len(SEED_PMIDS)*100:.1f}%)\n\n")
        
        if not_found_count > 0:
            f.write("## 未検出論文の分析\n\n")
            for r in results['final_results']:
                if not r['found']:
                    f.write(f"### PMID: {r['pmid']}\n\n")
                    paper_info = next((p for p in results['paper_details'] if p['pmid'] == r['pmid']), None)
                    if paper_info:
                        f.write(f"**タイトル**: {paper_info['title']}\n\n")
                        f.write(f"**MeSH用語**: {', '.join(paper_info['mesh_terms'][:10])}\n\n")
                    
                    f.write("**ブロック別ヒット状況**:\n\n")
                    for block_name in SEARCH_BLOCKS.keys():
                        block_found = results['block_results'][block_name]['pmid_results'].get(r['pmid'], False)
                        status = "✓ ヒット" if block_found else "✗ 未ヒット"
                        f.write(f"- {block_name}: {status}\n")
                    f.write("\n")
    
    print(f"\n[OK] レポートを保存しました: {report_path}")
    
    return results


if __name__ == "__main__":
    main()
