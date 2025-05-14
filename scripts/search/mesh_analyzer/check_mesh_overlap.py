#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import re
import requests
import json
import os
import time
from datetime import datetime
from typing import Dict, List, Set, Tuple

def parse_search_formula(file_path: str) -> Dict[str, List[str]]:
    """
    検索式ファイル（MD形式）からMeSH用語とキーワードを抽出する
    
    Args:
        file_path: 検索式ファイルのパス
        
    Returns:
        Dict: {
            'mesh_p': [MeSH用語（P）のリスト],
            'mesh_i': [MeSH用語（I）のリスト],
            'keyword_p': [キーワード（P）のリスト],
            'keyword_i': [キーワード（I）のリスト],
        }
    """
    # check_term.pyの関数を再利用
    import sys
    sys.path.append('scripts/validation/term_validator')
    from check_term import parse_search_formula as parse_formula
    
    return parse_formula(file_path)

def check_mesh_hierarchy(mesh_term: str) -> Dict:
    """
    MeSH用語の階層関係を確認する
    
    Args:
        mesh_term: 確認するMeSH用語
        
    Returns:
        Dict: MeSH用語の階層情報
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    search_url = f"{base_url}/esearch.fcgi"
    fetch_url = f"{base_url}/efetch.fcgi"
    
    # まずMeSH用語のUIDを検索
    search_params = {
        'db': 'mesh',
        'term': mesh_term,
        'retmode': 'json'
    }
    
    try:
        search_response = requests.get(search_url, params=search_params)
        search_response.raise_for_status()
        search_data = search_response.json()
        
        ids = search_data['esearchresult'].get('idlist', [])
        
        if not ids:
            return {
                'term': mesh_term,
                'exists': False,
                'tree_numbers': [],
                'parents': [],
                'children': [],
                'message': 'MeSH用語が見つかりませんでした。'
            }
        
        # MeSH用語の詳細情報を取得
        fetch_params = {
            'db': 'mesh',
            'id': ids[0],
            'retmode': 'xml'
        }
        
        fetch_response = requests.get(fetch_url, params=fetch_params)
        fetch_response.raise_for_status()
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(fetch_response.text, 'lxml')
        
        # Tree NumbersとDescriptorNameを抽出
        descriptor_name = soup.find('descriptorname').text if soup.find('descriptorname') else mesh_term
        tree_numbers = [tn.text for tn in soup.find_all('treenumber')]
        
        # 親と子のMeSH用語を取得
        parents = []
        for tn in tree_numbers:
            # 親のTree Numberを取得（最後のピリオド以降を削除）
            if '.' in tn:
                parent_tn = tn.rsplit('.', 1)[0]
                
                # 親のTree Numberに対応するMeSH用語を検索
                parent_search_params = {
                    'db': 'mesh',
                    'term': f"{parent_tn}[TreeNumber]",
                    'retmode': 'json'
                }
                
                parent_search_response = requests.get(search_url, params=parent_search_params)
                parent_search_response.raise_for_status()
                parent_search_data = parent_search_response.json()
                
                parent_ids = parent_search_data['esearchresult'].get('idlist', [])
                
                if parent_ids:
                    # 親のMeSH用語名を取得
                    parent_fetch_params = {
                        'db': 'mesh',
                        'id': parent_ids[0],
                        'retmode': 'xml'
                    }
                    
                    parent_fetch_response = requests.get(fetch_url, params=parent_fetch_params)
                    parent_fetch_response.raise_for_status()
                    
                    parent_soup = BeautifulSoup(parent_fetch_response.text, 'lxml')
                    parent_name = parent_soup.find('descriptorname').text if parent_soup.find('descriptorname') else ''
                    
                    if parent_name:
                        parents.append({
                            'term': parent_name,
                            'tree_number': parent_tn
                        })
                
                # APIの制限を考慮して少し待機
                time.sleep(1)
        
        # 子のMeSH用語を取得（各Tree Numberに対して直接の子を検索）
        children = []
        for tn in tree_numbers:
            # 子のTree Numberのパターンを作成
            child_pattern = f"{tn}.*"
            
            # 子のTree Numberに対応するMeSH用語を検索
            child_search_params = {
                'db': 'mesh',
                'term': f"{child_pattern}[TreeNumber]",
                'retmode': 'json'
            }
            
            child_search_response = requests.get(search_url, params=child_search_params)
            child_search_response.raise_for_status()
            child_search_data = child_search_response.json()
            
            child_count = int(child_search_data['esearchresult'].get('count', 0))
            
            if child_count > 0:
                children.append({
                    'count': child_count,
                    'tree_pattern': child_pattern
                })
            
            # APIの制限を考慮して少し待機
            time.sleep(1)
        
        return {
            'term': descriptor_name,
            'exists': True,
            'tree_numbers': tree_numbers,
            'parents': parents,
            'children': children,
            'message': 'Success'
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'term': mesh_term,
            'exists': False,
            'tree_numbers': [],
            'parents': [],
            'children': [],
            'message': f'Error: {str(e)}'
        }

def check_term_co_occurrence(term1: str, field1: str, term2: str, field2: str) -> Dict:
    """
    二つの検索用語の共起関係を確認する
    
    Args:
        term1: 検索用語1
        field1: フィールドタグ1（例: [Mesh], [tiab]）
        term2: 検索用語2
        field2: フィールドタグ2（例: [Mesh], [tiab]）
    
    Returns:
        Dict: 共起関係の結果
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    search_url = f"{base_url}/esearch.fcgi"
    
    # 検索クエリの構築
    query1 = f'"{term1}"{field1}'
    query2 = f'"{term2}"{field2}'
    combined_query = f'({query1}) AND ({query2})'
    
    try:
        # 用語1の検索結果
        params1 = {
            'db': 'pubmed',
            'term': query1,
            'retmode': 'json'
        }
        
        response1 = requests.get(search_url, params=params1)
        response1.raise_for_status()
        data1 = response1.json()
        count1 = int(data1['esearchresult'].get('count', 0))
        
        # 用語2の検索結果
        params2 = {
            'db': 'pubmed',
            'term': query2,
            'retmode': 'json'
        }
        
        response2 = requests.get(search_url, params=params2)
        response2.raise_for_status()
        data2 = response2.json()
        count2 = int(data2['esearchresult'].get('count', 0))
        
        # 二つの用語を組み合わせた検索結果
        params_combined = {
            'db': 'pubmed',
            'term': combined_query,
            'retmode': 'json'
        }
        
        response_combined = requests.get(search_url, params=params_combined)
        response_combined.raise_for_status()
        data_combined = response_combined.json()
        count_combined = int(data_combined['esearchresult'].get('count', 0))
        
        # 包含率の計算
        inclusion_ratio1 = count_combined / count1 if count1 > 0 else 0
        inclusion_ratio2 = count_combined / count2 if count2 > 0 else 0
        
        return {
            'term1': term1,
            'field1': field1,
            'count1': count1,
            'term2': term2,
            'field2': field2,
            'count2': count2,
            'combined_count': count_combined,
            'inclusion_ratio1': inclusion_ratio1,
            'inclusion_ratio2': inclusion_ratio2,
            'message': 'Success'
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'term1': term1,
            'field1': field1,
            'count1': 0,
            'term2': term2,
            'field2': field2,
            'count2': 0,
            'combined_count': 0,
            'inclusion_ratio1': 0,
            'inclusion_ratio2': 0,
            'message': f'Error: {str(e)}'
        }

def analyze_mesh_overlap(terms: Dict[str, List[str]]) -> Dict:
    """
    MeSH用語の重複関係を分析する
    
    Args:
        terms: 検索式から抽出したMeSH用語とキーワード
        
    Returns:
        Dict: 重複分析結果
    """
    results = {
        'mesh_p_hierarchy': [],
        'mesh_i_hierarchy': [],
        'mesh_term_overlap': [],
        'keyword_overlap': []
    }
    
    # Population MeSH用語の階層関係
    print("\n=== Population MeSH用語の階層関係分析... ===")
    for term in terms['mesh_p']:
        print(f"\n用語: {term}")
        hierarchy = check_mesh_hierarchy(term)
        results['mesh_p_hierarchy'].append(hierarchy)
        
        # 親用語の表示
        if hierarchy['parents']:
            print("親用語:")
            for parent in hierarchy['parents']:
                print(f"- {parent['term']} ({parent['tree_number']})")
        
        # 子用語の情報
        if hierarchy['children']:
            print("子用語:")
            for child in hierarchy['children']:
                print(f"- {child['count']}個の子用語 ({child['tree_pattern']})")
        
        # APIの制限を考慮して少し待機
        time.sleep(1)
    
    # Intervention MeSH用語の階層関係
    print("\n=== Intervention MeSH用語の階層関係分析... ===")
    for term in terms['mesh_i']:
        print(f"\n用語: {term}")
        hierarchy = check_mesh_hierarchy(term)
        results['mesh_i_hierarchy'].append(hierarchy)
        
        # 親用語の表示
        if hierarchy['parents']:
            print("親用語:")
            for parent in hierarchy['parents']:
                print(f"- {parent['term']} ({parent['tree_number']})")
        
        # 子用語の情報
        if hierarchy['children']:
            print("子用語:")
            for child in hierarchy['children']:
                print(f"- {child['count']}個の子用語 ({child['tree_pattern']})")
        
        # APIの制限を考慮して少し待機
        time.sleep(1)
    
    # Population MeSH用語間の重複関係
    if len(terms['mesh_p']) > 1:
        print("\n=== Population MeSH用語間の重複関係分析... ===")
        for i in range(len(terms['mesh_p'])):
            for j in range(i+1, len(terms['mesh_p'])):
                term1 = terms['mesh_p'][i]
                term2 = terms['mesh_p'][j]
                
                print(f"\n{term1} と {term2} の関係を分析中...")
                overlap = check_term_co_occurrence(term1, "[Mesh]", term2, "[Mesh]")
                results['mesh_term_overlap'].append(overlap)
                
                # 結果の表示
                print(f"{term1}[Mesh]: {overlap['count1']:,}件")
                print(f"{term2}[Mesh]: {overlap['count2']:,}件")
                print(f"共通: {overlap['combined_count']:,}件")
                print(f"{term1}に対する{term2}の包含率: {overlap['inclusion_ratio1']:.2f}")
                print(f"{term2}に対する{term1}の包含率: {overlap['inclusion_ratio2']:.2f}")
                
                # 重複の可能性の判定
                if overlap['inclusion_ratio1'] > 0.9:
                    print(f"⚠️ {term1}は{term2}にほぼ包含されている可能性があります")
                elif overlap['inclusion_ratio2'] > 0.9:
                    print(f"⚠️ {term2}は{term1}にほぼ包含されている可能性があります")
                
                # APIの制限を考慮して少し待機
                time.sleep(1)
    
    # Intervention MeSH用語間の重複関係
    if len(terms['mesh_i']) > 1:
        print("\n=== Intervention MeSH用語間の重複関係分析... ===")
        for i in range(len(terms['mesh_i'])):
            for j in range(i+1, len(terms['mesh_i'])):
                term1 = terms['mesh_i'][i]
                term2 = terms['mesh_i'][j]
                
                print(f"\n{term1} と {term2} の関係を分析中...")
                overlap = check_term_co_occurrence(term1, "[Mesh]", term2, "[Mesh]")
                results['mesh_term_overlap'].append(overlap)
                
                # 結果の表示
                print(f"{term1}[Mesh]: {overlap['count1']:,}件")
                print(f"{term2}[Mesh]: {overlap['count2']:,}件")
                print(f"共通: {overlap['combined_count']:,}件")
                print(f"{term1}に対する{term2}の包含率: {overlap['inclusion_ratio1']:.2f}")
                print(f"{term2}に対する{term1}の包含率: {overlap['inclusion_ratio2']:.2f}")
                
                # 重複の可能性の判定
                if overlap['inclusion_ratio1'] > 0.9:
                    print(f"⚠️ {term1}は{term2}にほぼ包含されている可能性があります")
                elif overlap['inclusion_ratio2'] > 0.9:
                    print(f"⚠️ {term2}は{term1}にほぼ包含されている可能性があります")
                
                # APIの制限を考慮して少し待機
                time.sleep(1)
    
    # Population キーワード間の重複関係（サンプルとして一部を分析）
    if len(terms['keyword_p']) > 1:
        print("\n=== Population キーワード間の重複関係分析（サンプル）... ===")
        # 計算量が多くなるため、最初の5つの用語間で分析
        max_terms = min(5, len(terms['keyword_p']))
        
        for i in range(max_terms):
            for j in range(i+1, max_terms):
                term1 = terms['keyword_p'][i]
                term2 = terms['keyword_p'][j]
                
                print(f"\n{term1} と {term2} の関係を分析中...")
                overlap = check_term_co_occurrence(term1, "[tiab]", term2, "[tiab]")
                results['keyword_overlap'].append(overlap)
                
                # 結果の表示
                print(f"{term1}[tiab]: {overlap['count1']:,}件")
                print(f"{term2}[tiab]: {overlap['count2']:,}件")
                print(f"共通: {overlap['combined_count']:,}件")
                print(f"{term1}に対する{term2}の包含率: {overlap['inclusion_ratio1']:.2f}")
                print(f"{term2}に対する{term1}の包含率: {overlap['inclusion_ratio2']:.2f}")
                
                # 重複の可能性の判定
                if overlap['inclusion_ratio1'] > 0.9:
                    print(f"⚠️ {term1}は{term2}にほぼ包含されている可能性があります")
                elif overlap['inclusion_ratio2'] > 0.9:
                    print(f"⚠️ {term2}は{term1}にほぼ包含されている可能性があります")
                
                # APIの制限を考慮して少し待機
                time.sleep(1)
    
    # Intervention キーワード間の重複関係（サンプルとして一部を分析）
    if len(terms['keyword_i']) > 1:
        print("\n=== Intervention キーワード間の重複関係分析（サンプル）... ===")
        # 計算量が多くなるため、最初の5つの用語間で分析
        max_terms = min(5, len(terms['keyword_i']))
        
        for i in range(max_terms):
            for j in range(i+1, max_terms):
                term1 = terms['keyword_i'][i]
                term2 = terms['keyword_i'][j]
                
                print(f"\n{term1} と {term2} の関係を分析中...")
                overlap = check_term_co_occurrence(term1, "[tiab]", term2, "[tiab]")
                results['keyword_overlap'].append(overlap)
                
                # 結果の表示
                print(f"{term1}[tiab]: {overlap['count1']:,}件")
                print(f"{term2}[tiab]: {overlap['count2']:,}件")
                print(f"共通: {overlap['combined_count']:,}件")
                print(f"{term1}に対する{term2}の包含率: {overlap['inclusion_ratio1']:.2f}")
                print(f"{term2}に対する{term1}の包含率: {overlap['inclusion_ratio2']:.2f}")
                
                # 重複の可能性の判定
                if overlap['inclusion_ratio1'] > 0.9:
                    print(f"⚠️ {term1}は{term2}にほぼ包含されている可能性があります")
                elif overlap['inclusion_ratio2'] > 0.9:
                    print(f"⚠️ {term2}は{term1}にほぼ包含されている可能性があります")
                
                # APIの制限を考慮して少し待機
                time.sleep(1)
    
    return results

def generate_llm_analysis(terms: Dict[str, List[str]], mesh_analysis: Dict) -> str:
    """
    LLMを使用して検索式の最適化提案を生成する
    
    Args:
        terms: 検索式から抽出したMeSH用語とキーワード
        mesh_analysis: MeSH用語の階層・重複分析結果
        
    Returns:
        str: LLMによる分析結果と提案
    """
    # ここでLLMのAPIを呼び出すことも可能ですが、このサンプルでは
    # 構造的な分析に基づいて提案を作成します
    
    suggestions = []
    
    # MeSH用語の階層関係に基づく提案
    parent_child_relations = []
    for hierarchy in mesh_analysis['mesh_p_hierarchy'] + mesh_analysis['mesh_i_hierarchy']:
        if hierarchy['parents']:
            for parent in hierarchy['parents']:
                parent_child_relations.append(f"- {hierarchy['term']}は{parent['term']}の下位語です。")
        
        if hierarchy['children'] and any(child['count'] > 0 for child in hierarchy['children']):
            parent_child_relations.append(f"- {hierarchy['term']}には下位語があります（自動的に検索に含まれます）。")
    
    if parent_child_relations:
        suggestions.append("### MeSH用語の階層関係\n" + "\n".join(parent_child_relations))
    
    # MeSH用語の重複関係に基づく提案
    overlap_relations = []
    for overlap in mesh_analysis['mesh_term_overlap']:
        if overlap['inclusion_ratio1'] > 0.9:
            overlap_relations.append(f"- {overlap['term1']}[{overlap['field1']}]は{overlap['term2']}[{overlap['field2']}]にほぼ包含されています（包含率: {overlap['inclusion_ratio1']:.2f}）。")
        elif overlap['inclusion_ratio2'] > 0.9:
            overlap_relations.append(f"- {overlap['term2']}[{overlap['field2']}]は{overlap['term1']}[{overlap['field1']}]にほぼ包含されています（包含率: {overlap['inclusion_ratio2']:.2f}）。")
    
    for overlap in mesh_analysis['keyword_overlap']:
        if overlap['inclusion_ratio1'] > 0.9:
            overlap_relations.append(f"- {overlap['term1']}[{overlap['field1']}]は{overlap['term2']}[{overlap['field2']}]にほぼ包含されています（包含率: {overlap['inclusion_ratio1']:.2f}）。")
        elif overlap['inclusion_ratio2'] > 0.9:
            overlap_relations.append(f"- {overlap['term2']}[{overlap['field2']}]は{overlap['term1']}[{overlap['field1']}]にほぼ包含されています（包含率: {overlap['inclusion_ratio2']:.2f}）。")
    
    if overlap_relations:
        suggestions.append("### 検索用語の重複関係\n" + "\n".join(overlap_relations))
    
    # キーワード数に基づく提案
    if len(terms['keyword_p']) > 20:
        suggestions.append("### キーワード数の最適化\n- Population用のキーワードが多すぎる可能性があります（現在: {}個）。ノイズを減らすために、より重要な用語に絞ることを検討してください。".format(len(terms['keyword_p'])))
    
    if len(terms['keyword_i']) > 10:
        suggestions.append("### キーワード数の最適化\n- Intervention用のキーワードが多すぎる可能性があります（現在: {}個）。ノイズを減らすために、より重要な用語に絞ることを検討してください。".format(len(terms['keyword_i'])))
    
    # 最終的な提案をまとめる
    final_analysis = "# 検索式の構造分析と最適化提案\n\n"
    
    if suggestions:
        final_analysis += "\n\n".join(suggestions)
    else:
        final_analysis += "検索式の構造に特に問題は見つかりませんでした。"
    
    final_analysis += "\n\n## 総合的な提案\n\n"
    final_analysis += "上記の分析結果に基づいて、以下の検討が推奨されます：\n\n"
    
    # 総合的な提案を追加
    recommendations = []
    
    # 用語の重複に関する提案
    has_overlap = any("包含されています" in relation for relation in overlap_relations) if overlap_relations else False
    if has_overlap:
        recommendations.append("1. **重複する用語の削減**: 他の用語にほぼ包含される用語は、検索結果に大きな影響を与えずに削除できる可能性があります。")
    
    # MeSH用語の階層関係に関する提案
    has_hierarchy = len(parent_child_relations) > 0
    if has_hierarchy:
        recommendations.append("2. **MeSH階層の確認**: 上位語と下位語の関係を考慮して、必要に応じて検索式を調整してください。")
    
    # キーワード数に関する提案
    has_many_keywords = len(terms['keyword_p']) > 20 or len(terms['keyword_i']) > 10
    if has_many_keywords:
        recommendations.append("3. **キーワードの最適化**: 頻出するキーワードとあまり使われないキーワードを検討し、検索精度と再現率のバランスを取ってください。")
    
    # 検索構造に関する提案
    recommendations.append("4. **検索構造の確認**: 各ブロック間の関係（AND, OR）が適切に設定されているか確認してください。")
    
    final_analysis += "\n".join(recommendations)
    
    return final_analysis

def ensure_directory_exists(path: str) -> None:
    """
    ディレクトリが存在しない場合は作成する
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description='検索式の構造と重複を分析するスクリプト')
    parser.add_argument('--input', required=True, help='検索式ファイルのパス')
    parser.add_argument('--output', help='出力ファイルのパス（指定しない場合はlogs/validation/に保存）')
    
    args = parser.parse_args()
    input_file = args.input
    
    if args.output:
        output_file = args.output
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"logs/validation/search_overlap_{timestamp}.md"
    
    # 出力ディレクトリの確保
    ensure_directory_exists(output_file)
    
    # 検索式の解析
    print(f"\n検索式ファイル {input_file} を解析中...")
    terms = parse_search_formula(input_file)
    
    print(f"\n分析された検索用語:")
    print(f"- Population MeSH: {len(terms['mesh_p'])}個")
    print(f"- Intervention MeSH: {len(terms['mesh_i'])}個")
    print(f"- Population キーワード: {len(terms['keyword_p'])}個")
    print(f"- Intervention キーワード: {len(terms['keyword_i'])}個")
    
    # MeSH用語の重複分析
    print(f"\nMeSH用語の重複と階層関係を分析中...")
    mesh_analysis = analyze_mesh_overlap(terms)
    
    # LLMによる分析と提案
    print(f"\n検索式の構造分析と最適化提案を生成中...")
    llm_analysis = generate_llm_analysis(terms, mesh_analysis)
    
    # 結果をMarkdownファイルに保存
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(llm_analysis)
    
    print(f"\n分析結果を {output_file} に保存しました。")

if __name__ == "__main__":
    main()
