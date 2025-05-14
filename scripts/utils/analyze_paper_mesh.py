#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import requests
import time
import json
import os
from datetime import datetime
from typing import Dict, List, Set, Optional

def get_paper_details(pmid: str) -> Dict:
    """
    PubMed E-utilities APIを使用して論文の詳細情報を取得する
    
    Args:
        pmid: 論文のPMID
        
    Returns:
        Dict: 論文の詳細情報
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
        return {
            'pmid': pmid,
            'xml': response.text,
            'status': 'success'
        }
    except requests.exceptions.RequestException as e:
        return {
            'pmid': pmid,
            'xml': None,
            'status': 'error',
            'message': str(e)
        }

def extract_mesh_terms(xml_data: str) -> List[Dict]:
    """
    XMLデータからMeSH用語を抽出する
    
    Args:
        xml_data: PubMed論文のXMLデータ
        
    Returns:
        List[Dict]: MeSH用語のリスト
    """
    from bs4 import BeautifulSoup
    
    mesh_terms = []
    
    if not xml_data:
        return mesh_terms
    
    soup = BeautifulSoup(xml_data, 'lxml')
    
    # MeSH用語の抽出
    mesh_headings = soup.find_all('meshheading')
    
    for heading in mesh_headings:
        descriptor = heading.find('descriptorname')
        
        if descriptor:
            # 修飾語の抽出
            qualifiers = []
            for qualifier in heading.find_all('qualifiername'):
                qualifier_name = qualifier.text
                major_topic = qualifier.get('majortopicyn', 'N') == 'Y'
                qualifiers.append({
                    'name': qualifier_name,
                    'major_topic': major_topic
                })
            
            # 主要トピックかどうか
            major_topic = descriptor.get('majortopicyn', 'N') == 'Y'
            
            mesh_terms.append({
                'descriptor': descriptor.text,
                'major_topic': major_topic,
                'qualifiers': qualifiers
            })
    
    return mesh_terms

def extract_title_abstract(xml_data: str) -> Dict:
    """
    XMLデータからタイトルと抄録を抽出する
    
    Args:
        xml_data: PubMed論文のXMLデータ
        
    Returns:
        Dict: タイトルと抄録
    """
    from bs4 import BeautifulSoup
    
    if not xml_data:
        return {'title': '', 'abstract': ''}
    
    soup = BeautifulSoup(xml_data, 'lxml')
    
    # タイトルの抽出
    title_element = soup.find('articletitle')
    title = title_element.text if title_element else ''
    
    # 抄録の抽出
    abstract_texts = soup.find_all('abstracttext')
    abstract = ' '.join([text.text for text in abstract_texts]) if abstract_texts else ''
    
    return {
        'title': title,
        'abstract': abstract
    }

def extract_publication_info(xml_data: str) -> Dict:
    """
    XMLデータから出版情報を抽出する
    
    Args:
        xml_data: PubMed論文のXMLデータ
        
    Returns:
        Dict: 出版情報
    """
    from bs4 import BeautifulSoup
    
    if not xml_data:
        return {
            'journal': '',
            'year': '',
            'authors': []
        }
    
    soup = BeautifulSoup(xml_data, 'lxml')
    
    # ジャーナル名の抽出
    journal_element = soup.find('journal')
    journal = journal_element.find('title').text if journal_element and journal_element.find('title') else ''
    
    # 出版年の抽出
    pub_date = soup.find('pubdate')
    year = pub_date.find('year').text if pub_date and pub_date.find('year') else ''
    
    # 著者の抽出
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
    
    return {
        'journal': journal,
        'year': year,
        'authors': authors
    }

def analyze_mesh_coverage(paper_mesh_terms: List[Dict], search_mesh_terms: List[str]) -> Dict:
    """
    論文のMeSH用語が検索式のMeSH用語でカバーされているか分析する
    
    Args:
        paper_mesh_terms: 論文のMeSH用語リスト
        search_mesh_terms: 検索式のMeSH用語リスト
        
    Returns:
        Dict: カバレッジ分析結果
    """
    # 論文のMeSH用語の集合（ディスクリプタのみ）
    paper_mesh_descriptors = {term['descriptor'].lower() for term in paper_mesh_terms}
    
    # 検索式のMeSH用語の集合
    search_mesh_lower = {term.lower() for term in search_mesh_terms}
    
    # 共通のMeSH用語
    common_terms = paper_mesh_descriptors.intersection(search_mesh_lower)
    
    # 論文にあるが検索式にないMeSH用語
    missing_terms = paper_mesh_descriptors - search_mesh_lower
    
    return {
        'total_paper_terms': len(paper_mesh_descriptors),
        'total_search_terms': len(search_mesh_lower),
        'common_terms': list(common_terms),
        'common_count': len(common_terms),
        'missing_terms': list(missing_terms),
        'missing_count': len(missing_terms),
        'coverage_ratio': len(common_terms) / len(paper_mesh_descriptors) if paper_mesh_descriptors else 0
    }

def ensure_directory_exists(path: str) -> None:
    """
    ディレクトリが存在しない場合は作成する
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description='組入論文のMeSH用語を分析するスクリプト')
    parser.add_argument('--pmids', required=True, help='分析するPMIDのカンマ区切りリスト')
    parser.add_argument('--search_formula', required=True, help='検索式ファイルのパス')
    parser.add_argument('--output', help='出力ファイルのパス（指定しない場合はlogs/analysis/に保存）')
    
    args = parser.parse_args()
    pmids = args.pmids.split(',')
    search_formula_path = args.search_formula
    
    if args.output:
        output_file = args.output
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"logs/analysis/paper_mesh_analysis_{timestamp}.json"
    
    # 出力ディレクトリの確保
    ensure_directory_exists(output_file)
    
    # 検索式の解析（check_term.pyのparse_search_formulaを使用）
    import sys
    sys.path.append('scripts/validation/term_validator')
    from check_term import parse_search_formula
    
    search_terms = parse_search_formula(search_formula_path)
    
    # 全MeSH用語のリスト（P + I）
    all_search_mesh_terms = search_terms['mesh_p'] + search_terms['mesh_i']
    
    # 結果を格納する辞書
    results = {
        'papers': [],
        'summary': {
            'total_papers': len(pmids),
            'total_search_mesh_terms': len(all_search_mesh_terms),
            'search_mesh_terms': all_search_mesh_terms,
            'papers_with_matching_mesh': 0,
            'papers_without_matching_mesh': 0,
            'suggested_mesh_terms': []
        }
    }
    
    # 論文の分析
    print(f"\n=== {len(pmids)}件の組入論文のMeSH用語分析を開始... ===")
    
    for pmid in pmids:
        print(f"\nPMID: {pmid}の分析中...")
        
        # 論文の詳細情報を取得
        paper_details = get_paper_details(pmid)
        
        if paper_details['status'] == 'error':
            print(f"エラー: {paper_details['message']}")
            continue
        
        # MeSH用語の抽出
        mesh_terms = extract_mesh_terms(paper_details['xml'])
        
        # タイトルと抄録の抽出
        title_abstract = extract_title_abstract(paper_details['xml'])
        
        # 出版情報の抽出
        pub_info = extract_publication_info(paper_details['xml'])
        
        # MeSHカバレッジの分析
        coverage = analyze_mesh_coverage(mesh_terms, all_search_mesh_terms)
        
        # 結果の表示
        print(f"タイトル: {title_abstract['title']}")
        print(f"ジャーナル: {pub_info['journal']} ({pub_info['year']})")
        print(f"著者: {', '.join(pub_info['authors'])}")
        print(f"MeSH用語数: {len(mesh_terms)}")
        print(f"検索式とマッチするMeSH用語数: {coverage['common_count']}")
        print(f"カバレッジ率: {coverage['coverage_ratio']:.2f}")
        
        if coverage['common_count'] > 0:
            print("マッチしたMeSH用語:")
            for term in coverage['common_terms']:
                print(f"- {term}")
        
        if coverage['missing_count'] > 0:
            print("\n検索式にないMeSH用語（追加検討候補）:")
            for term in coverage['missing_terms']:
                print(f"- {term}")
        
        # 論文データを結果に追加
        paper_data = {
            'pmid': pmid,
            'title': title_abstract['title'],
            'journal': pub_info['journal'],
            'year': pub_info['year'],
            'authors': pub_info['authors'],
            'mesh_terms': mesh_terms,
            'coverage': coverage
        }
        
        results['papers'].append(paper_data)
        
        # サマリーの更新
        if coverage['common_count'] > 0:
            results['summary']['papers_with_matching_mesh'] += 1
        else:
            results['summary']['papers_without_matching_mesh'] += 1
        
        # API制限を考慮して少し待機
        time.sleep(1)
    
    # 追加検討候補のMeSH用語の集計
    all_missing_terms = []
    for paper in results['papers']:
        all_missing_terms.extend(paper['coverage']['missing_terms'])
    
    # 頻度でソート
    from collections import Counter
    term_counter = Counter(all_missing_terms)
    suggested_terms = [{'term': term, 'count': count} for term, count in term_counter.most_common()]
    
    results['summary']['suggested_mesh_terms'] = suggested_terms
    
    # JSON形式で結果を保存
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # Markdown形式のレポートも生成
    md_output_file = output_file.replace('.json', '.md')
    
    with open(md_output_file, 'w', encoding='utf-8') as f:
        f.write(f"# 組入論文のMeSH用語分析レポート\n")
        f.write(f"日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## 分析サマリー\n\n")
        f.write(f"- 分析論文数: {results['summary']['total_papers']}件\n")
        f.write(f"- 検索式のMeSH用語数: {results['summary']['total_search_mesh_terms']}個\n")
        f.write(f"- 検索式とマッチするMeSH用語を持つ論文: {results['summary']['papers_with_matching_mesh']}件\n")
        f.write(f"- 検索式とマッチするMeSH用語を持たない論文: {results['summary']['papers_without_matching_mesh']}件\n\n")
        
        f.write("## 検索式のMeSH用語\n\n")
        for term in results['summary']['search_mesh_terms']:
            f.write(f"- {term}\n")
        
        f.write("\n## 追加検討候補のMeSH用語\n\n")
        f.write("以下のMeSH用語は組入論文に付与されていますが、検索式に含まれていません：\n\n")
        for term_info in results['summary']['suggested_mesh_terms']:
            f.write(f"- {term_info['term']} ({term_info['count']}件の論文に出現)\n")
        
        f.write("\n## 論文別分析\n\n")
        for paper in results['papers']:
            f.write(f"### PMID: {paper['pmid']}\n\n")
            f.write(f"- タイトル: {paper['title']}\n")
            f.write(f"- ジャーナル: {paper['journal']} ({paper['year']})\n")
            f.write(f"- 著者: {', '.join(paper['authors'])}\n")
            f.write(f"- MeSH用語数: {len(paper['mesh_terms'])}\n")
            f.write(f"- 検索式とマッチするMeSH用語数: {paper['coverage']['common_count']}\n")
            f.write(f"- カバレッジ率: {paper['coverage']['coverage_ratio']:.2f}\n\n")
            
            if paper['coverage']['common_terms']:
                f.write("#### マッチしたMeSH用語\n\n")
                for term in paper['coverage']['common_terms']:
                    f.write(f"- {term}\n")
                f.write("\n")
            
            if paper['coverage']['missing_terms']:
                f.write("#### 検索式にないMeSH用語（追加検討候補）\n\n")
                for term in paper['coverage']['missing_terms']:
                    f.write(f"- {term}\n")
                f.write("\n")
            
            f.write("#### 全MeSH用語\n\n")
            for term in paper['mesh_terms']:
                major_indicator = "*" if term['major_topic'] else ""
                qualifier_text = ""
                
                if term['qualifiers']:
                    qualifier_list = []
                    for qualifier in term['qualifiers']:
                        q_indicator = "*" if qualifier['major_topic'] else ""
                        qualifier_list.append(f"{qualifier['name']}{q_indicator}")
                    
                    qualifier_text = f" / {', '.join(qualifier_list)}"
                
                f.write(f"- {term['descriptor']}{major_indicator}{qualifier_text}\n")
            
            f.write("\n---\n\n")
    
    print(f"\n分析が完了しました。")
    print(f"結果を次のファイルに保存しました：")
    print(f"- JSON形式: {output_file}")
    print(f"- Markdown形式: {md_output_file}")

if __name__ == "__main__":
    main()
