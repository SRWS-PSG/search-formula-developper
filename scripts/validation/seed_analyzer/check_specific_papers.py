#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import requests
import json
import os
import time
import sys
from datetime import datetime
from typing import Dict, List, Tuple, Set

def parse_search_formula(file_path: str) -> Dict:
    """
    検索式ファイル（MD形式）から検索式と組入論文を抽出する
    
    Args:
        file_path: 検索式ファイルのパス
        
    Returns:
        Dict: {
            'search_formula': 完全な検索式,
            'pmids': 組入論文のPMIDリスト
        }
    """
    # check_term.pyの関数を再利用
    sys.path.append('scripts/validation/term_validator')
    
    try:
        from check_term import parse_search_formula as parse_formula
        from check_term import extract_pmids_from_file
        
        # 検索用語を抽出
        terms = parse_formula(file_path)
        
        # 組入論文のPMIDを抽出
        pmids = extract_pmids_from_file(file_path)
        
        # 完全な検索式を構築
        # (Population MeSH OR Population キーワード) AND (Intervention MeSH OR Intervention キーワード)
        mesh_p_terms = [f'"{term}"[Mesh]' for term in terms['mesh_p']]
        mesh_i_terms = [f'"{term}"[Mesh]' for term in terms['mesh_i']]
        keyword_p_terms = [f'"{term}"[tiab]' for term in terms['keyword_p']]
        keyword_i_terms = [f'"{term}"[tiab]' for term in terms['keyword_i']]
        
        p_mesh_block = f"({' OR '.join(mesh_p_terms)})" if mesh_p_terms else ""
        p_keyword_block = f"({' OR '.join(keyword_p_terms)})" if keyword_p_terms else ""
        i_mesh_block = f"({' OR '.join(mesh_i_terms)})" if mesh_i_terms else ""
        i_keyword_block = f"({' OR '.join(keyword_i_terms)})" if keyword_i_terms else ""
        
        p_block = []
        if p_mesh_block:
            p_block.append(p_mesh_block)
        if p_keyword_block:
            p_block.append(p_keyword_block)
        
        p_combined = f"({' OR '.join(p_block)})" if p_block else ""
        
        i_block = []
        if i_mesh_block:
            i_block.append(i_mesh_block)
        if i_keyword_block:
            i_block.append(i_keyword_block)
        
        i_combined = f"({' OR '.join(i_block)})" if i_block else ""
        
        search_formula = f"({p_combined}) AND ({i_combined})" if p_combined and i_combined else ""
        
        return {
            'search_formula': search_formula,
            'pmids': pmids
        }
        
    except ImportError:
        print("エラー: scripts/validation/term_validator/check_term.py モジュールをインポートできませんでした")
        # 代替の実装
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 検索式を直接抽出（簡易版）
        import re
        search_formula_match = re.search(r'```\s*\n(.*?)\n```', content, re.DOTALL)
        search_formula = search_formula_match.group(1) if search_formula_match else ""
        
        # PMIDを抽出
        pmids = re.findall(r'PMID:\s*(\d+)', content)
        
        return {
            'search_formula': search_formula,
            'pmids': pmids
        }

def get_pubmed_count(query: str) -> Dict:
    """
    PubMed E-utilities APIを使用して検索クエリの結果件数を取得する
    
    Args:
        query: 検索クエリ
        
    Returns:
        Dict: 検索結果の情報
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    search_url = f"{base_url}/esearch.fcgi"
    
    params = {
        'db': 'pubmed',
        'term': query,
        'retmode': 'json',
        'retmax': 0  # 結果の件数のみ取得
    }
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        return {
            'count': int(data['esearchresult'].get('count', 0)),
            'query': query,
            'status': 'success'
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'count': 0,
            'query': query,
            'status': 'error',
            'message': str(e)
        }

def check_pmid_inclusion(search_formula: str, pmid: str) -> Dict:
    """
    特定のPMIDの論文が検索式の結果に含まれるか確認する
    
    Args:
        search_formula: 検索式
        pmid: 確認するPMID
        
    Returns:
        Dict: 検証結果
    """
    # PMIDが存在するか確認
    pmid_check = get_pubmed_count(f"{pmid}[uid]")
    
    if pmid_check['count'] == 0:
        return {
            'pmid': pmid,
            'exists': False,
            'included': False,
            'message': 'PMIDが存在しません'
        }
    
    # 検索式とPMIDを組み合わせて検索
    combined_query = f"({search_formula}) AND {pmid}[uid]"
    combined_result = get_pubmed_count(combined_query)
    
    included = combined_result['count'] > 0
    
    return {
        'pmid': pmid,
        'exists': True,
        'included': included,
        'message': 'Success'
    }

def analyze_non_inclusion(search_formula: str, pmid: str) -> Dict:
    """
    検索式に含まれない論文の原因を分析する
    
    Args:
        search_formula: 検索式
        pmid: 分析するPMID
        
    Returns:
        Dict: 分析結果
    """
    # パーツに分解して分析
    # 検索式の構造: (P_Block) AND (I_Block)
    parts = {}
    
    # 論文の情報を取得
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
        xml_data = response.text
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(xml_data, 'lxml')
        
        # 基本情報の抽出
        title_element = soup.find('articletitle')
        title = title_element.text if title_element else 'タイトル不明'
        
        # MeSH用語の抽出
        mesh_headings = []
        for heading in soup.find_all('meshheading'):
            descriptor = heading.find('descriptorname')
            if descriptor:
                mesh_headings.append(descriptor.text)
        
        # 論文の基本情報を格納
        parts['paper_info'] = {
            'title': title,
            'mesh_terms': mesh_headings
        }
        
        # Population部分の分析
        import re
        p_block_match = re.search(r'\(\((.*?)\)\)', search_formula)
        p_block = p_block_match.group(1) if p_block_match else ""
        
        p_query = f"({p_block}) AND {pmid}[uid]"
        p_result = get_pubmed_count(p_query)
        parts['p_block'] = {
            'match': p_result['count'] > 0,
            'count': p_result['count']
        }
        
        # Intervention部分の分析
        i_block_match = re.search(r'\)\s+AND\s+\(\((.*?)\)\)', search_formula)
        i_block = i_block_match.group(1) if i_block_match else ""
        
        i_query = f"({i_block}) AND {pmid}[uid]"
        i_result = get_pubmed_count(i_query)
        parts['i_block'] = {
            'match': i_result['count'] > 0,
            'count': i_result['count']
        }
        
        # 各部分のマッチ状態から非包含の原因を特定
        if not parts['p_block']['match'] and not parts['i_block']['match']:
            reason = "論文はPopulationとIntervention両方の条件を満たしていません"
        elif not parts['p_block']['match']:
            reason = "論文はPopulation条件を満たしていません"
        elif not parts['i_block']['match']:
            reason = "論文はIntervention条件を満たしていません"
        else:
            reason = "不明な理由で検索結果に含まれていません"
        
        parts['exclusion_reason'] = reason
        
        return parts
        
    except requests.exceptions.RequestException as e:
        return {
            'error': str(e),
            'exclusion_reason': "論文の詳細情報を取得できませんでした"
        }

def get_paper_citation(pmid: str) -> str:
    """
    PMIDから論文の引用情報を取得する
    
    Args:
        pmid: 論文のPMID
        
    Returns:
        str: 論文の引用情報
    """
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
        xml_data = response.text
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(xml_data, 'lxml')
        
        # タイトル
        title_element = soup.find('articletitle')
        title = title_element.text if title_element else 'タイトル不明'
        
        # 著者情報
        authors = []
        author_list = soup.find('authorlist')
        if author_list:
            for author in author_list.find_all('author'):
                last_name = author.find('lastname')
                fore_name = author.find('forename')
                
                if last_name and fore_name:
                    authors.append(f"{last_name.text} {fore_name.text}")
                elif last_name:
                    authors.append(last_name.text)
        
        authors_text = ", ".join(authors) if authors else "著者不明"
        
        # ジャーナル情報
        journal_element = soup.find('journal')
        journal = journal_element.find('title').text if journal_element and journal_element.find('title') else 'ジャーナル不明'
        
        # 出版年
        pub_date = soup.find('pubdate')
        year = pub_date.find('year').text if pub_date and pub_date.find('year') else '年不明'
        
        # 巻号ページ
        volume = soup.find('volume')
        volume_text = volume.text if volume else ""
        
        issue = soup.find('issue')
        issue_text = issue.text if issue else ""
        
        pagination = soup.find('pagination')
        pages = pagination.text if pagination else ""
        
        # 引用情報の組み立て
        citation = f"{authors_text}. {title}. {journal}. {year}"
        
        if volume_text:
            citation += f";{volume_text}"
        
        if issue_text:
            citation += f"({issue_text})"
        
        if pages:
            citation += f":{pages}"
        
        citation += f". PMID: {pmid}"
        
        return citation
        
    except requests.exceptions.RequestException as e:
        return f"引用情報の取得に失敗しました（PMID: {pmid}）: {str(e)}"

def ensure_directory_exists(path: str) -> None:
    """
    ディレクトリが存在しない場合は作成する
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description='検索式に組入論文が含まれるか検証するスクリプト')
    parser.add_argument('--input', required=True, help='検索式ファイルのパス')
    parser.add_argument('--pmids', help='検証するPMIDのカンマ区切りリスト（指定しない場合は検索式ファイルから抽出）')
    parser.add_argument('--output', help='出力ファイルのパス（指定しない場合はlogs/validation/に保存）')
    
    args = parser.parse_args()
    input_file = args.input
    
    if args.output:
        output_file = args.output
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"logs/validation/inclusion_check_{timestamp}.log"
    
    # 出力ディレクトリの確保
    ensure_directory_exists(output_file)
    
    # 検索式と組入論文の抽出
    print(f"\n検索式ファイル {input_file} を解析中...")
    data = parse_search_formula(input_file)
    
    search_formula = data['search_formula']
    
    if args.pmids:
        pmids = args.pmids.split(',')
    else:
        pmids = data['pmids']
    
    if not search_formula:
        print("エラー: 検索式を抽出できませんでした。")
        return
    
    if not pmids:
        print("エラー: 組入論文のPMIDが見つかりませんでした。")
        return
    
    print(f"検索式: {search_formula}")
    print(f"検証するPMID: {', '.join(pmids)}")
    
    # 検索結果の総件数を取得
    print("\n検索式の総件数を確認中...")
    total_result = get_pubmed_count(search_formula)
    total_count = total_result['count']
    print(f"検索結果: {total_count:,}件")
    
    # 各PMIDの包含状況を確認
    print("\n各論文の包含状況を確認中...")
    inclusion_results = []
    non_included_papers = []
    
    for pmid in pmids:
        print(f"\nPMID: {pmid} の確認中...")
        inclusion = check_pmid_inclusion(search_formula, pmid)
        
        if inclusion['exists']:
            status = "包含" if inclusion['included'] else "非包含"
            print(f"ステータス: {status}")
            
            # 引用情報の取得
            citation = get_paper_citation(pmid)
            print(f"論文: {citation}")
            
            inclusion['citation'] = citation
            inclusion_results.append(inclusion)
            
            # 非包含の場合は原因を分析
            if not inclusion['included']:
                print("非包含の原因を分析中...")
                analysis = analyze_non_inclusion(search_formula, pmid)
                inclusion['analysis'] = analysis
                non_included_papers.append((pmid, citation, analysis))
                
                # 分析結果の表示
                print(f"分析: {analysis['exclusion_reason']}")
                
                if 'p_block' in analysis:
                    p_status = "○" if analysis['p_block']['match'] else "×"
                    print(f"Population条件: {p_status}")
                
                if 'i_block' in analysis:
                    i_status = "○" if analysis['i_block']['match'] else "×"
                    print(f"Intervention条件: {i_status}")
        else:
            print(f"エラー: {inclusion['message']}")
            inclusion_results.append(inclusion)
        
        # API制限を考慮して少し待機
        time.sleep(1)
    
    # 包含率の計算
    included_count = sum(1 for r in inclusion_results if r.get('included', False))
    inclusion_rate = included_count / len(pmids) if pmids else 0
    
    # 結果のログファイル生成
    with open(output_file, 'w', encoding='utf-8') as f:
        # ヘッダー
        f.write(f"# 検索式の組入論文包含検証レポート\n")
        f.write(f"日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # 検索式
        f.write("## 検索式\n\n")
        f.write(f"```\n{search_formula}\n```\n\n")
        
        # 検索結果
        f.write("## 検索結果\n\n")
        f.write(f"- 総件数: {total_count:,}件\n")
        f.write(f"- 検証論文数: {len(pmids)}件\n")
        f.write(f"- 包含論文数: {included_count}件\n")
        f.write(f"- 包含率: {inclusion_rate:.2f}（{included_count}/{len(pmids)}）\n\n")
        
        # 各論文の包含状況
        f.write("## 論文別包含状況\n\n")
        
        for result in inclusion_results:
            if result.get('exists', False):
                status = "✅ 包含" if result.get('included', False) else "❌ 非包含"
                f.write(f"### PMID: {result['pmid']} - {status}\n\n")
                
                if 'citation' in result:
                    f.write(f"論文: {result['citation']}\n\n")
                
                # 非包含の場合は原因を記載
                if not result.get('included', False) and 'analysis' in result:
                    analysis = result['analysis']
                    f.write(f"非包含の原因: {analysis.get('exclusion_reason', '不明')}\n\n")
                    
                    if 'paper_info' in analysis:
                        f.write("論文情報:\n")
                        f.write(f"- タイトル: {analysis['paper_info'].get('title', '不明')}\n")
                        
                        if 'mesh_terms' in analysis['paper_info'] and analysis['paper_info']['mesh_terms']:
                            f.write("- MeSH用語:\n")
                            for term in analysis['paper_info']['mesh_terms']:
                                f.write(f"  - {term}\n")
                        f.write("\n")
                    
                    if 'p_block' in analysis:
                        p_status = "満たしている" if analysis['p_block'].get('match', False) else "満たしていない"
                        f.write(f"Population条件: {p_status}\n")
                    
                    if 'i_block' in analysis:
                        i_status = "満たしている" if analysis['i_block'].get('match', False) else "満たしていない"
                        f.write(f"Intervention条件: {i_status}\n")
                
                f.write("\n---\n\n")
            else:
                f.write(f"### PMID: {result['pmid']} - ⚠️ エラー\n\n")
                f.write(f"メッセージ: {result.get('message', '不明なエラー')}\n\n")
                f.write("\n---\n\n")
        
        # 非包含論文のサマリー
        if non_included_papers:
            f.write("## 非包含論文のサマリー\n\n")
            
            for pmid, citation, analysis in non_included_papers:
                reason = analysis.get('exclusion_reason', '不明')
                f.write(f"- PMID: {pmid}\n")
                f.write(f"  - 論文: {citation}\n")
                f.write(f"  - 原因: {reason}\n\n")
        
        # 推奨される対応
        f.write("## 推奨される対応\n\n")
        
        if inclusion_rate == 1.0:
            f.write("✅ すべての組入論文が検索式に含まれています。検索式の調整は必要ありません。\n")
        elif inclusion_rate >= 0.8:
            f.write("⚠️ 一部の組入論文が検索式に含まれていません。以下の対応を検討してください：\n\n")
            f.write("1. 非包含論文に付与されているMeSH用語を検索式に追加\n")
            f.write("2. 非包含論文に共通するキーワードを検索式に追加\n")
            f.write("3. 必要に応じて検索構造（AND/OR）の調整\n")
        else:
            f.write("❌ 多くの組入論文が検索式に含まれていません。検索式の大幅な見直しが必要です：\n\n")
            f.write("1. Population・Intervention両方のブロックの見直し\n")
            f.write("2. 非包含論文の特徴を詳細に分析\n")
            f.write("3. MeSH用語だけでなく、フリーワードも適切に追加\n")
            f.write("4. 検索構造の再設計（より包括的な検索になるよう調整）\n")
    
    print(f"\n検証が完了しました。")
    print(f"- 総件数: {total_count:,}件")
    print(f"- 検証論文数: {len(pmids)}件")
    print(f"- 包含論文数: {included_count}件")
    print(f"- 包含率: {inclusion_rate:.2f}（{included_count}/{len(pmids)}）")
    print(f"\n結果を {output_file} に保存しました。")

if __name__ == "__main__":
    main()
