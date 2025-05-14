#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Biopythonを使用した検索式検証ツール

検索式ファイル（MDファイル）から検索式を抽出し、以下の検証を行います：
- MeSH用語とキーワードごとの検索件数確認
- 検索式全体の検索結果件数確認
- 組入論文が検索結果に含まれることの検証
- 組入論文のMeSH用語分析

結果は元の検索式ファイルが含まれるフォルダに保存されます。
"""

import os
import re
import sys
import time
import json
import argparse
import logging
from datetime import datetime
from typing import Dict, List, Set, Tuple, Any, Optional

try:
    from Bio import Entrez
except ImportError:
    print("このスクリプトはBiopythonライブラリが必要です。")
    print("以下のコマンドでインストールしてください：")
    print("pip install biopython")
    sys.exit(1)

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("biopython_validator")

# NCBIのAPIリクエスト間の待機時間（秒）
API_DELAY = 0.34  # NCBIの制限：3リクエスト/秒

class SearchFormulaParser:
    """検索式ファイル（MDファイル）からMeSH用語、キーワード、PMIDを抽出するパーサー"""
    
    def __init__(self, file_path: str):
        """
        初期化
        
        Args:
            file_path: 検索式ファイルのパス
        """
        self.file_path = file_path
        self.content = self._read_file()
        
    def _read_file(self) -> str:
        """ファイルを読み込む"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"ファイル読み込みエラー: {str(e)}")
            return ""
    
    def parse(self) -> Dict[str, Any]:
        """
        検索式を解析して構造化されたデータを返す
        
        Returns:
            Dict: 解析結果
        """
        result = {
            'mesh_p': self._extract_mesh_p(),
            'mesh_i': self._extract_mesh_i(),
            'keyword_p': self._extract_keyword_p(),
            'keyword_i': self._extract_keyword_i(),
            'pmids': self._extract_pmids(),
            'search_formula': self._build_search_formula()
        }
        
        return result
    
    def _extract_mesh_p(self) -> List[str]:
        """Population MeSH用語を抽出"""
        mesh_p_match = re.search(r'統制語\s*\(P.*?\).*?\[(MeSH|mh)\].*?\((.*?)\)', self.content, re.DOTALL)
        if mesh_p_match:
            mesh_p_block = mesh_p_match.group(2)
            # 各MeSH用語を抽出
            mesh_p_terms = re.findall(r'\(\s*"([^"]+)"\s*\[\s*(?:MeSH|mh)\s*\]\s*\)', mesh_p_block)
            return mesh_p_terms
        return []
    
    def _extract_mesh_i(self) -> List[str]:
        """Intervention MeSH用語を抽出"""
        mesh_i_match = re.search(r'統制語\s*\(\s*I.*?\).*?\[(MeSH|mh)\].*?\((.*?)\)', self.content, re.DOTALL)
        if mesh_i_match:
            mesh_i_block = mesh_i_match.group(2)
            # 各MeSH用語を抽出
            mesh_i_terms = re.findall(r'\(\s*"([^"]+)"\s*\[\s*(?:MeSH|mh)\s*\]\s*\)', mesh_i_block)
            return mesh_i_terms
        return []
    
    def _extract_keyword_p(self) -> List[str]:
        """Population キーワードを抽出"""
        keyword_p_match = re.search(r'フリーワード\s*\(P.*?\).*?\[tiab\](.*?)\((?:\(|"統制語|$)', self.content, re.DOTALL)
        if keyword_p_match:
            keyword_p_block = keyword_p_match.group(1)
            # 各キーワードを抽出
            keyword_p_terms = re.findall(r'\(\s*"([^"]+)"\s*\[\s*tiab\s*\]\s*\)', keyword_p_block)
            return keyword_p_terms
        return []
    
    def _extract_keyword_i(self) -> List[str]:
        """Intervention キーワードを抽出"""
        keyword_i_match = re.search(r'フリーワード\s*\(\s*I.*?\).*?\[tiab\](.*?)(?:\Z|\(#|\n#)', self.content, re.DOTALL)
        if keyword_i_match:
            keyword_i_block = keyword_i_match.group(1)
            # 各キーワードを抽出
            keyword_i_terms = re.findall(r'\(\s*"([^"]+)"\s*\[\s*tiab\s*\]\s*\)', keyword_i_block)
            return keyword_i_terms
        return []
    
    def _extract_pmids(self) -> List[str]:
        """組入論文のPMIDを抽出"""
        pmids = re.findall(r'PMID:\s*(\d+)', self.content)
        return pmids
    
    def _build_search_formula(self) -> str:
        """完全な検索式を構築"""
        mesh_p_terms = [f'"{term}"[Mesh]' for term in self._extract_mesh_p()]
        mesh_i_terms = [f'"{term}"[Mesh]' for term in self._extract_mesh_i()]
        keyword_p_terms = [f'"{term}"[tiab]' for term in self._extract_keyword_p()]
        keyword_i_terms = [f'"{term}"[tiab]' for term in self._extract_keyword_i()]
        
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
        
        # 完全な検索式
        if p_combined and i_combined:
            return f"{p_combined} AND {i_combined}"
        elif p_combined:
            return p_combined
        elif i_combined:
            return i_combined
        else:
            return ""


class PubMedQueryExecutor:
    """PubMedでクエリを実行するクラス"""
    
    def __init__(self, email: str):
        """
        初期化
        
        Args:
            email: Entrez APIに提供するemail
        """
        Entrez.email = email
        self.last_request_time = 0
    
    def _wait_for_api_limit(self):
        """API制限を考慮して待機"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < API_DELAY:
            time.sleep(API_DELAY - time_since_last_request)
        
        self.last_request_time = time.time()
    
    def execute_query(self, query: str) -> Dict[str, Any]:
        """
        PubMedクエリを実行
        
        Args:
            query: PubMed検索クエリ
            
        Returns:
            Dict: 検索結果
        """
        self._wait_for_api_limit()
        
        try:
            # Entrez.esearchを使用してクエリを実行
            handle = Entrez.esearch(db="pubmed", term=query, retmax=0)
            record = Entrez.read(handle)
            handle.close()
            
            count = int(record["Count"])
            
            # IDリストが必要な場合は別のリクエストで取得（大量の場合は分割取得）
            ids = []
            if count > 0 and count <= 10000:  # 10000件を超える場合は処理が重くなるため制限
                self._wait_for_api_limit()
                handle = Entrez.esearch(db="pubmed", term=query, retmax=min(count, 10000))
                record = Entrez.read(handle)
                ids = record["IdList"]
                handle.close()
            
            return {
                'count': count,
                'ids': ids,
                'query': query,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"PubMedクエリ実行エラー: {str(e)}")
            return {
                'count': 0,
                'ids': [],
                'query': query,
                'status': 'error',
                'message': str(e)
            }
    
    def get_paper_details(self, pmid: str) -> Dict[str, Any]:
        """
        PMIDを使用して論文の詳細情報を取得
        
        Args:
            pmid: 論文のPMID
            
        Returns:
            Dict: 論文の詳細情報
        """
        self._wait_for_api_limit()
        
        try:
            handle = Entrez.efetch(db="pubmed", id=pmid, retmode="xml")
            records = Entrez.read(handle)
            handle.close()
            
            # 必要な情報を抽出
            article = records['PubmedArticle'][0]
            
            # MeSH用語の抽出
            mesh_terms = []
            if 'MeshHeadingList' in article['MedlineCitation']:
                for mesh_heading in article['MedlineCitation']['MeshHeadingList']:
                    descriptor = mesh_heading['DescriptorName']
                    term = descriptor.attributes['UI'] + ': ' + descriptor
                    
                    # MajorTopicYNの取得
                    is_major = descriptor.attributes.get('MajorTopicYN', 'N') == 'Y'
                    
                    # 修飾語（Qualifier）の取得
                    qualifiers = []
                    if 'QualifierName' in mesh_heading:
                        for qualifier in mesh_heading['QualifierName']:
                            qualifier_text = qualifier.attributes['UI'] + ': ' + qualifier
                            qualifier_major = qualifier.attributes.get('MajorTopicYN', 'N') == 'Y'
                            qualifiers.append({
                                'name': qualifier_text,
                                'major_topic': qualifier_major
                            })
                    
                    mesh_terms.append({
                        'descriptor': term,
                        'major_topic': is_major,
                        'qualifiers': qualifiers
                    })
            
            # 基本情報の抽出
            article_title = article['MedlineCitation']['Article'].get('ArticleTitle', '')
            
            # 著者の抽出
            authors = []
            if 'AuthorList' in article['MedlineCitation']['Article']:
                for author in article['MedlineCitation']['Article']['AuthorList']:
                    if 'LastName' in author and 'ForeName' in author:
                        authors.append(f"{author['LastName']} {author['ForeName']}")
                    elif 'LastName' in author:
                        authors.append(author['LastName'])
                    elif 'CollectiveName' in author:
                        authors.append(author['CollectiveName'])
            
            # ジャーナル情報
            journal = article['MedlineCitation']['Article']['Journal'].get('Title', '')
            
            # 出版年
            pub_date = article['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']
            year = pub_date.get('Year', '')
            
            return {
                'pmid': pmid,
                'title': article_title,
                'authors': authors,
                'journal': journal,
                'year': year,
                'mesh_terms': mesh_terms,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"論文詳細取得エラー: {str(e)}")
            return {
                'pmid': pmid,
                'status': 'error',
                'message': str(e)
            }


class SearchFormulaValidator:
    """検索式の検証を行うクラス"""
    
    def __init__(self, search_data: Dict[str, Any], executor: PubMedQueryExecutor):
        """
        初期化
        
        Args:
            search_data: 検索式データ
            executor: PubMedクエリエグゼキュータ
        """
        self.search_data = search_data
        self.executor = executor
        self.validation_results = {
            'term_validation': {
                'mesh_p': [],
                'mesh_i': [],
                'keyword_p': [],
                'keyword_i': []
            },
            'formula_validation': None,
            'paper_validation': {
                'papers': [],
                'total_papers': len(search_data['pmids']),
                'included_papers': 0,
                'inclusion_rate': 0
            },
            'mesh_analysis': {
                'papers': [],
                'summary': {
                    'total_papers': len(search_data['pmids']),
                    'search_mesh_terms': search_data['mesh_p'] + search_data['mesh_i'],
                    'papers_with_matching_mesh': 0,
                    'suggested_mesh_terms': []
                }
            }
        }
    
    def validate_terms(self):
        """各MeSH用語とキーワードの検索件数を検証"""
        logger.info("各MeSH用語とキーワードの検証を開始...")
        
        # Population MeSH用語の検証
        for term in self.search_data['mesh_p']:
            logger.info(f"Population MeSH用語を検証中: {term}")
            query = f'"{term}"[Mesh]'
            result = self.executor.execute_query(query)
            result['term'] = term
            result['field'] = '[Mesh]'
            result['category'] = 'Population'
            self.validation_results['term_validation']['mesh_p'].append(result)
        
        # Intervention MeSH用語の検証
        for term in self.search_data['mesh_i']:
            logger.info(f"Intervention MeSH用語を検証中: {term}")
            query = f'"{term}"[Mesh]'
            result = self.executor.execute_query(query)
            result['term'] = term
            result['field'] = '[Mesh]'
            result['category'] = 'Intervention'
            self.validation_results['term_validation']['mesh_i'].append(result)
        
        # Population キーワードの検証
        for term in self.search_data['keyword_p']:
            logger.info(f"Population キーワードを検証中: {term}")
            query = f'"{term}"[tiab]'
            result = self.executor.execute_query(query)
            result['term'] = term
            result['field'] = '[tiab]'
            result['category'] = 'Population'
            self.validation_results['term_validation']['keyword_p'].append(result)
        
        # Intervention キーワードの検証
        for term in self.search_data['keyword_i']:
            logger.info(f"Intervention キーワードを検証中: {term}")
            query = f'"{term}"[tiab]'
            result = self.executor.execute_query(query)
            result['term'] = term
            result['field'] = '[tiab]'
            result['category'] = 'Intervention'
            self.validation_results['term_validation']['keyword_i'].append(result)
        
        logger.info("各MeSH用語とキーワードの検証が完了しました")
    
    def validate_formula(self):
        """検索式全体の検索結果件数を確認"""
        logger.info("検索式全体の検証を開始...")
        formula = self.search_data['search_formula']
        
        if not formula:
            logger.warning("検索式が空です")
            self.validation_results['formula_validation'] = {
                'count': 0,
                'ids': [],
                'query': "",
                'status': 'error',
                'message': '検索式が空です'
            }
            return
        
        result = self.executor.execute_query(formula)
        self.validation_results['formula_validation'] = result
        
        logger.info(f"検索式の検索結果件数: {result['count']:,}件")
    
    def validate_papers(self):
        """組入論文が検索結果に含まれるか検証"""
        logger.info("組入論文の検証を開始...")
        formula = self.search_data['search_formula']
        
        if not formula:
            logger.warning("検索式が空のため、組入論文の検証をスキップします")
            return
        
        included_count = 0
        
        for pmid in self.search_data['pmids']:
            logger.info(f"PMID: {pmid} の検証中...")
            
            # 論文の存在確認
            pmid_query = f"{pmid}[uid]"
            pmid_result = self.executor.execute_query(pmid_query)
            
            if pmid_result['count'] == 0:
                logger.warning(f"PMID: {pmid} の論文がPubMedに存在しません")
                
                paper_validation = {
                    'pmid': pmid,
                    'exists': False,
                    'included': False,
                    'message': 'PMIDが存在しません'
                }
                
                self.validation_results['paper_validation']['papers'].append(paper_validation)
                continue
            
            # 検索式と組み合わせて検索
            combined_query = f"({formula}) AND {pmid}[uid]"
            combined_result = self.executor.execute_query(combined_query)
            
            # 包含状態の確認
            included = combined_result['count'] > 0
            
            if included:
                included_count += 1
            
            # 論文詳細の取得
            paper_details = self.executor.get_paper_details(pmid)
            
            # 非包含の場合の原因分析
            analysis = None
            if not included:
                analysis = self._analyze_non_inclusion(formula, pmid)
            
            paper_validation = {
                'pmid': pmid,
                'exists': True,
                'included': included,
                'details': paper_details,
                'analysis': analysis,
                'message': 'Success'
            }
            
            self.validation_results['paper_validation']['papers'].append(paper_validation)
        
        # 包含率の計算
        total_papers = len(self.search_data['pmids'])
        inclusion_rate = included_count / total_papers if total_papers > 0 else 0
        
        self.validation_results['paper_validation']['included_papers'] = included_count
        self.validation_results['paper_validation']['inclusion_rate'] = inclusion_rate
        
        logger.info(f"組入論文の検証が完了しました（包含率: {inclusion_rate:.2f}）")
    
    def _analyze_non_inclusion(self, formula: str, pmid: str) -> Dict[str, Any]:
        """検索式に含まれない論文の原因を分析"""
        # 構造化された検索式の各ブロックを分析
        mesh_p_terms = [f'"{term}"[Mesh]' for term in self.search_data['mesh_p']]
        mesh_i_terms = [f'"{term}"[Mesh]' for term in self.search_data['mesh_i']]
        keyword_p_terms = [f'"{term}"[tiab]' for term in self.search_data['keyword_p']]
        keyword_i_terms = [f'"{term}"[tiab]' for term in self.search_data['keyword_i']]
        
        p_mesh_block = f"({' OR '.join(mesh_p_terms)})" if mesh_p_terms else ""
        p_keyword_block = f"({' OR '.join(keyword_p_terms)})" if keyword_p_terms else ""
        i_mesh_block = f"({' OR '.join(mesh_i_terms)})" if mesh_i_terms else ""
        i_keyword_block = f"({' OR '.join(keyword_i_terms)})" if keyword_i_terms else ""
        
        # Population ブロック全体
        p_blocks = []
        if p_mesh_block:
            p_blocks.append(p_mesh_block)
        if p_keyword_block:
            p_blocks.append(p_keyword_block)
        
        p_block = f"({' OR '.join(p_blocks)})" if p_blocks else ""
        
        # Intervention ブロック全体
        i_blocks = []
        if i_mesh_block:
            i_blocks.append(i_mesh_block)
        if i_keyword_block:
            i_blocks.append(i_keyword_block)
        
        i_block = f"({' OR '.join(i_blocks)})" if i_blocks else ""
        
        # 各ブロックのマッチング確認
        p_query = f"{p_block} AND {pmid}[uid]" if p_block else ""
        i_query = f"{i_block} AND {pmid}[uid]" if i_block else ""
        
        p_result = self.executor.execute_query(p_query) if p_query else {'count': 0}
        i_result = self.executor.execute_query(i_query) if i_query else {'count': 0}
        
        p_match = p_result['count'] > 0
        i_match = i_result['count'] > 0
        
        # 非包含の原因を特定
        if not p_match and not i_match:
            reason = "論文はPopulationとIntervention両方の条件を満たしていません"
        elif not p_match:
            reason = "論文はPopulation条件を満たしていません"
        elif not i_match:
            reason = "論文はIntervention条件を満たしていません"
        else:
            reason = "不明な理由で検索結果に含まれていません"
        
        return {
            'p_block': {
                'match': p_match,
                'count': p_result.get('count', 0)
            },
            'i_block': {
                'match': i_match,
                'count': i_result.get('count', 0)
            },
            'exclusion_reason': reason
        }
    
    def analyze_paper_mesh(self):
        """組入論文のMeSH用語を分析"""
        logger.info("組入論文のMeSH用語分析を開始...")
        
        # 検索式のMeSH用語
        search_mesh_terms = self.search_data['mesh_p'] + self.search_data['mesh_i']
        search_mesh_lower = {term.lower() for term in search_mesh_terms}
        
        papers_with_matching_mesh = 0
        all_missing_terms = []
        
        for paper_validation in self.validation_results['paper_validation']['papers']:
            if not paper_validation.get('exists', False):
                continue
            
            paper_details = paper_validation.get('details', {})
            mesh_terms = paper_details.get('mesh_terms', [])
            
            # 論文のMeSH用語（ディスクリプタのみ）
            paper_mesh_descriptors = set()
            for term in mesh_terms:
                descriptor = term.get('descriptor', '')
                if ':' in descriptor:
                    # UI:用語 の形式から用語部分だけ抽出
                    descriptor = descriptor.split(':', 1)[1].strip()
                paper_mesh_descriptors.add(descriptor.lower())
            
            # 共通のMeSH用語と検索式にないMeSH用語
            common_terms = paper_mesh_descriptors.intersection(search_mesh_lower)
            missing_terms = paper_mesh_descriptors - search_mesh_lower
            
            # 結果の記録
            coverage = {
                'total_paper_terms': len(paper_mesh_descriptors),
                'total_search_terms': len(search_mesh_lower),
                'common_terms': list(common_terms),
                'common_count': len(common_terms),
                'missing_terms': list(missing_terms),
                'missing_count': len(missing_terms),
                'coverage_ratio': len(common_terms) / len(paper_mesh_descriptors) if paper_mesh_descriptors else 0
            }
            
            paper_analysis = {
                'pmid': paper_validation['pmid'],
                'title': paper_details.get('title', ''),
                'journal': paper_details.get('journal', ''),
                'year': paper_details.get('year', ''),
                'authors': paper_details.get('authors', []),
                'mesh_terms': mesh_terms,
                'coverage': coverage
            }
            
            # 一致するMeSH用語がある場合
            if len(common_terms) > 0:
                papers_with_matching_mesh += 1
            
            # 検索式にないMeSH用語を収集
            all_missing_terms.extend(list(missing_terms))
            
            self.validation_results['mesh_analysis']['papers'].append(paper_analysis)
        
        # 頻出する追加検討候補の集計
        from collections import Counter
        term_counter = Counter(all_missing_terms)
        suggested_terms = [{'term': term, 'count': count} for term, count in term_counter.most_common()]
        
        # サマリーを更新
        self.validation_results['mesh_analysis']['summary']['papers_with_matching_mesh'] = papers_with_matching_mesh
        self.validation_results['mesh_analysis']['summary']['papers_without_matching_mesh'] = len(self.search_data['pmids']) - papers_with_matching_mesh
        self.validation_results['mesh_analysis']['summary']['suggested_mesh_terms'] = suggested_terms
        
        logger.info("組入論文のMeSH用語分析が完了しました")
    
    def validate(self, steps: List[str] = None):
        """
        検証を実行
        
        Args:
            steps: 実行するステップのリスト（省略時は全て実行）
        """
        all_steps = ['term', 'formula', 'papers', 'mesh']
        steps_to_run = steps if steps else all_steps
        
        if 'term' in steps_to_run:
            self.validate_terms()
        
        if 'formula' in steps_to_run:
            self.validate_formula()
        
        if 'papers' in steps_to_run:
            self.validate_papers()
        
        if 'mesh' in steps_to_run:
            self.analyze_paper_mesh()
        
        return self.validation_results


class ReportGenerator:
    """検証結果のレポートを生成するクラス"""
    
    def __init__(self, validation_results: Dict[str, Any], search_data: Dict[str, Any]):
        """
        初期化
        
        Args:
            validation_results: 検証結果
            search_data: 検索式データ
        """
        self.validation_results = validation_results
        self.search_data = search_data
    
    def generate_markdown_report(self) -> str:
        """Markdown形式の検証レポートを生成"""
        # タイムスタンプ
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # レポートのヘッダー
        report = f"# 検索式検証レポート\n"
        report += f"日時: {timestamp}\n\n"
        
        # 検索式
        report += "## 検索式\n\n"
        report += f"```\n{self.search_data['search_formula']}\n```\n\n"
        
        # 検索結果の概要
        formula_validation = self.validation_results.get('formula_validation', {})
        total_count = formula_validation.get('count', 0) if formula_validation else 0
        
        paper_validation = self.validation_results.get('paper_validation', {})
        total_papers = paper_validation.get('total_papers', 0)
        included_papers = paper_validation.get('included_papers', 0)
        inclusion_rate = paper_validation.get('inclusion_rate', 0)
        
        report += "## 検索結果の概要\n\n"
        report += f"- 総検索結果件数: {total_count:,}件\n"
        report += f"- 検証論文数: {total_papers}件\n"
        report += f"- 包含論文数: {included_papers}件\n"
        report += f"- 包含率: {inclusion_rate:.2f}（{included_papers}/{total_papers}）\n\n"
        
        # 用語の検証結果
        report += "## 検索用語の検証結果\n\n"
        
        # Population MeSH用語
        report += "### Population MeSH用語\n\n"
        mesh_p_results = self.validation_results.get('term_validation', {}).get('mesh_p', [])
        for result in mesh_p_results:
            report += f"- 用語: {result.get('term', '')}[Mesh]\n"
            report += f"  - 検索結果: {result.get('count', 0):,}件\n"
            if result.get('status') == 'error':
                report += f"  - エラー: {result.get('message', '不明なエラー')}\n"
        
        # Intervention MeSH用語
        report += "\n### Intervention MeSH用語\n\n"
        mesh_i_results = self.validation_results.get('term_validation', {}).get('mesh_i', [])
        for result in mesh_i_results:
            report += f"- 用語: {result.get('term', '')}[Mesh]\n"
            report += f"  - 検索結果: {result.get('count', 0):,}件\n"
            if result.get('status') == 'error':
                report += f"  - エラー: {result.get('message', '不明なエラー')}\n"
        
        # Population キーワード
        report += "\n### Population キーワード\n\n"
        keyword_p_results = self.validation_results.get('term_validation', {}).get('keyword_p', [])
        for result in keyword_p_results:
            report += f"- 用語: {result.get('term', '')}[tiab]\n"
            report += f"  - 検索結果: {result.get('count', 0):,}件\n"
            if result.get('status') == 'error':
                report += f"  - エラー: {result.get('message', '不明なエラー')}\n"
        
        # Intervention キーワード
        report += "\n### Intervention キーワード\n\n"
        keyword_i_results = self.validation_results.get('term_validation', {}).get('keyword_i', [])
        for result in keyword_i_results:
            report += f"- 用語: {result.get('term', '')}[tiab]\n"
            report += f"  - 検索結果: {result.get('count', 0):,}件\n"
            if result.get('status') == 'error':
                report += f"  - エラー: {result.get('message', '不明なエラー')}\n"
        
        # 注意が必要な検索用語の特定
        low_count_terms = []
        for category, results_list in [
            ("Population MeSH", mesh_p_results),
            ("Intervention MeSH", mesh_i_results),
            ("Population キーワード", keyword_p_results),
            ("Intervention キーワード", keyword_i_results)
        ]:
            for result in results_list:
                count = result.get('count', 0)
                term = result.get('term', '')
                field = result.get('field', '')
                
                if count == 0:
                    low_count_terms.append((category, term, field, count, "検索結果なし"))
                elif count < 10:
                    low_count_terms.append((category, term, field, count, "検索結果が少ない"))
        
        if low_count_terms:
            report += "\n### 注意が必要な検索用語\n\n"
            for category, term, field, count, note in low_count_terms:
                report += f"- [{category}] {term}{field}: {count:,}件 - {note}\n"
        
        # 組入論文の包含状況
        report += "\n## 組入論文の包含状況\n\n"
        
        papers = paper_validation.get('papers', [])
        for paper in papers:
            pmid = paper.get('pmid', '')
            exists = paper.get('exists', False)
            included = paper.get('included', False)
            
            if exists:
                status = "✅ 包含" if included else "❌ 非包含"
                report += f"### PMID: {pmid} - {status}\n\n"
                
                details = paper.get('details', {})
                title = details.get('title', '')
                authors = details.get('authors', [])
                journal = details.get('journal', '')
                year = details.get('year', '')
                
                # 論文情報
                report += f"- タイトル: {title}\n"
                report += f"- 著者: {', '.join(authors)}\n"
                report += f"- ジャーナル: {journal} ({year})\n\n"
                
                # 非包含の場合は原因分析
                if not included and 'analysis' in paper:
                    analysis = paper['analysis']
                    report += f"非包含の原因: {analysis.get('exclusion_reason', '不明')}\n\n"
                    
                    if 'p_block' in analysis:
                        p_status = "満たしている" if analysis['p_block'].get('match', False) else "満たしていない"
                        report += f"- Population条件: {p_status}\n"
                    
                    if 'i_block' in analysis:
                        i_status = "満たしている" if analysis['i_block'].get('match', False) else "満たしていない"
                        report += f"- Intervention条件: {i_status}\n"
                    
                    report += "\n"
            else:
                report += f"### PMID: {pmid} - ⚠️ エラー\n\n"
                report += f"メッセージ: {paper.get('message', '不明なエラー')}\n\n"
            
            report += "---\n\n"
        
        # MeSH用語分析
        mesh_analysis = self.validation_results.get('mesh_analysis', {})
        summary = mesh_analysis.get('summary', {})
        suggested_terms = summary.get('suggested_mesh_terms', [])
        
        report += "## 組入論文のMeSH用語分析\n\n"
        report += f"- 分析論文数: {summary.get('total_papers', 0)}件\n"
        report += f"- 検索式のMeSH用語数: {len(summary.get('search_mesh_terms', []))}個\n"
        report += f"- 検索式とマッチするMeSH用語を持つ論文: {summary.get('papers_with_matching_mesh', 0)}件\n"
        report += f"- 検索式とマッチするMeSH用語を持たない論文: {summary.get('papers_without_matching_mesh', 0)}件\n\n"
        
        if suggested_terms:
            report += "### 追加検討候補のMeSH用語\n\n"
            report += "以下のMeSH用語は組入論文に付与されていますが、検索式に含まれていません：\n\n"
            
            for term_info in suggested_terms:
                term = term_info.get('term', '')
                count = term_info.get('count', 0)
                if term and count > 0:
                    report += f"- {term} ({count}件の論文に出現)\n"
        
        # 推奨される対応
        report += "\n## 推奨される対応\n\n"
        
        if inclusion_rate == 1.0:
            report += "✅ すべての組入論文が検索式に含まれています。検索式の調整は必要ありません。\n"
        elif inclusion_rate >= 0.8:
            report += "⚠️ 一部の組入論文が検索式に含まれていません。以下の対応を検討してください：\n\n"
            report += "1. 非包含論文に付与されているMeSH用語を検索式に追加\n"
            report += "2. 非包含論文に共通するキーワードを検索式に追加\n"
            report += "3. 必要に応じて検索構造（AND/OR）の調整\n"
        else:
            report += "❌ 多くの組入論文が検索式に含まれていません。検索式の大幅な見直しが必要です：\n\n"
            report += "1. Population・Intervention両方のブロックの見直し\n"
            report += "2. 非包含論文の特徴を詳細に分析\n"
            report += "3. MeSH用語だけでなく、フリーワードも適切に追加\n"
            report += "4. 検索構造の再設計（より包括的な検索になるよう調整）\n"
        
        return report
    
    def generate_json_report(self) -> Dict[str, Any]:
        """JSON形式の検証レポートを生成"""
        # タイムスタンプ
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # レポートデータ
        report_data = {
            'timestamp': timestamp,
            'search_formula': self.search_data['search_formula'],
            'validation_results': self.validation_results
        }
        
        return report_data
    
    def save_reports(self, output_dir: str) -> Tuple[str, str]:
        """
        検証レポートを保存
        
        Args:
            output_dir: 出力ディレクトリ
            
        Returns:
            Tuple[str, str]: Markdownファイルのパス, JSONファイルのパス
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Markdownレポート
        md_report = self.generate_markdown_report()
        md_file_path = os.path.join(output_dir, f"biopython_validation_{timestamp}.md")
        
        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(md_report)
        
        # JSONレポート
        json_report = self.generate_json_report()
        json_file_path = os.path.join(output_dir, f"biopython_validation_{timestamp}.json")
        
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(json_report, f, ensure_ascii=False, indent=2)
        
        return md_file_path, json_file_path


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(description='Biopythonを使用した検索式検証ツール')
    parser.add_argument('--input', required=True, help='検索式ファイルのパス')
    parser.add_argument('--output', help='出力ディレクトリ（指定しない場合は検索式と同じフォルダ）')
    parser.add_argument('--email', default='example@example.com', help='Entrez APIに提供するemail')
    parser.add_argument('--steps', default='all', help='実行するステップ（カンマ区切り: term,formula,papers,mesh,all）')
    
    args = parser.parse_args()
    
    # 入力ファイルのパス
    input_file = args.input
    
    # 出力ディレクトリの設定
    if args.output:
        output_dir = args.output
    else:
        # 入力ファイルと同じディレクトリに出力
        output_dir = os.path.dirname(os.path.abspath(input_file))
    
    # 出力ディレクトリが存在しない場合は作成
    os.makedirs(output_dir, exist_ok=True)
    
    # 実行するステップの設定
    if args.steps == 'all':
        steps = None  # 全て実行
    else:
        steps = args.steps.split(',')
    
    # 検索式パーサーの初期化
    parser = SearchFormulaParser(input_file)
    search_data = parser.parse()
    
    # PubMedクエリエグゼキュータの初期化
    executor = PubMedQueryExecutor(args.email)
    
    # 検索式バリデータの初期化
    validator = SearchFormulaValidator(search_data, executor)
    
    # 検証の実行
    validation_results = validator.validate(steps)
    
    # レポートジェネレータの初期化
    report_generator = ReportGenerator(validation_results, search_data)
    
    # レポートの保存
    md_file, json_file = report_generator.save_reports(output_dir)
    
    logger.info(f"検証が完了しました。")
    logger.info(f"Markdownレポート: {md_file}")
    logger.info(f"JSONレポート: {json_file}")


if __name__ == "__main__":
    main()
