#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PubMed検索式リンターのテスト

テスト対象:
1. フレーズ検索後のワイルドカード検出
2. ハイフン付きバリエーションの冗長性検出
"""

from unittest.mock import patch

import pytest
from scripts.validation.pubmed_syntax_linter import (
    normalize_term_for_comparison,
    check_phrase_wildcard,
    check_redundant_hyphen_variants,
    extract_mesh_terms_from_query,
    check_mesh_exact_match,
    lint_pubmed_query,
    format_lint_report,
    LintWarning,
)


class TestNormalizeTermForComparison:
    """用語正規化のテスト"""
    
    def test_hyphen_to_space(self):
        """ハイフンがスペースに変換されることを確認"""
        assert normalize_term_for_comparison("high-flow") == "high flow"
        assert normalize_term_for_comparison("high-flow nasal cannula") == "high flow nasal cannula"
    
    def test_multiple_hyphens(self):
        """複数のハイフンが正しく変換されることを確認"""
        assert normalize_term_for_comparison("high-flow-nasal-cannula") == "high flow nasal cannula"
    
    def test_case_insensitive(self):
        """大文字小文字が正規化されることを確認"""
        assert normalize_term_for_comparison("High-Flow") == "high flow"
        assert normalize_term_for_comparison("HIGH FLOW") == "high flow"
    
    def test_multiple_spaces(self):
        """連続するスペースが単一スペースに正規化されることを確認"""
        assert normalize_term_for_comparison("high  flow") == "high flow"
        assert normalize_term_for_comparison("high   flow  nasal") == "high flow nasal"
    
    def test_trim_whitespace(self):
        """前後の空白が削除されることを確認"""
        assert normalize_term_for_comparison("  high flow  ") == "high flow"


class TestCheckPhraseWildcard:
    """フレーズ検索後のワイルドカード検出のテスト"""
    
    def test_detect_phrase_wildcard(self):
        """フレーズ後のワイルドカードが検出されることを確認"""
        query = '"high flow nasal cannula"*[tiab]'
        warnings = check_phrase_wildcard(query)
        assert len(warnings) == 1
        assert warnings[0].rule_id == "PHRASE_WILDCARD"
        assert "high flow nasal cannula" in warnings[0].original_term
    
    def test_detect_multiple_phrase_wildcards(self):
        """複数のフレーズワイルドカードが検出されることを確認"""
        query = '"term1"*[tiab] OR "term2"*[Mesh]'
        warnings = check_phrase_wildcard(query)
        assert len(warnings) == 2
    
    def test_no_warning_for_normal_phrase(self):
        """通常のフレーズ検索では警告が出ないことを確認"""
        query = '"high flow nasal cannula"[tiab]'
        warnings = check_phrase_wildcard(query)
        assert len(warnings) == 0
    
    def test_no_warning_for_single_word_wildcard(self):
        """単一語のワイルドカードでは警告が出ないことを確認"""
        query = 'cannula*[tiab]'
        warnings = check_phrase_wildcard(query)
        assert len(warnings) == 0
    
    def test_phrase_wildcard_with_space_before_field(self):
        """フィールドタグ前にスペースがある場合も検出されることを確認"""
        query = '"high flow nasal cannula"* [tiab]'
        warnings = check_phrase_wildcard(query)
        assert len(warnings) == 1


class TestCheckRedundantHyphenVariants:
    """ハイフン付きバリエーションの冗長性検出のテスト"""
    
    def test_detect_hyphen_space_redundancy(self):
        """ハイフン版とスペース版の重複が検出されることを確認"""
        query = '"high-flow nasal cannula"[tiab] OR "high flow nasal cannula"[tiab]'
        warnings = check_redundant_hyphen_variants(query)
        assert len(warnings) == 1
        assert warnings[0].rule_id == "REDUNDANT_HYPHEN_VARIANT"
    
    def test_no_warning_for_different_terms(self):
        """異なる用語では警告が出ないことを確認"""
        query = '"high flow nasal cannula"[tiab] OR "oxygen therapy"[tiab]'
        warnings = check_redundant_hyphen_variants(query)
        assert len(warnings) == 0
    
    def test_no_warning_for_different_fields(self):
        """異なるフィールドでは警告が出ないことを確認（同じ用語でも別フィールドは別扱い）"""
        query = '"high flow nasal cannula"[tiab] OR "high-flow nasal cannula"[Mesh]'
        warnings = check_redundant_hyphen_variants(query)
        # 異なるフィールドなので警告なし
        assert len(warnings) == 0
    
    def test_detect_multiple_redundancies(self):
        """複数の冗長性が検出されることを確認"""
        query = '"high-flow"[tiab] OR "high flow"[tiab] OR "low-flow"[tiab] OR "low flow"[tiab]'
        warnings = check_redundant_hyphen_variants(query)
        assert len(warnings) == 2
    
    def test_case_insensitive_redundancy(self):
        """大文字小文字の違いも冗長として検出されることを確認"""
        query = '"High-Flow"[tiab] OR "high flow"[tiab]'
        warnings = check_redundant_hyphen_variants(query)
        assert len(warnings) == 1


class TestLintPubmedQuery:
    """統合リントチェックのテスト"""
    
    def test_combined_warnings(self):
        """複数の問題が同時に検出されることを確認"""
        query = '"high flow nasal cannula"*[tiab] OR "high-flow nasal cannula"[tiab]'
        warnings = lint_pubmed_query(query)
        # ワイルドカード警告1つ + 冗長性警告1つ
        assert len(warnings) == 2
        rule_ids = {w.rule_id for w in warnings}
        assert "PHRASE_WILDCARD" in rule_ids
        assert "REDUNDANT_HYPHEN_VARIANT" in rule_ids
    
    def test_no_warnings_for_clean_query(self):
        """問題のない検索式では警告が出ないことを確認"""
        query = '"high flow nasal cannula"[tiab] OR hfnc[tiab] OR "Respiratory Insufficiency"[Mesh]'
        warnings = lint_pubmed_query(query)
        assert len(warnings) == 0
    
    def test_real_world_query(self):
        """実際の検索式でのテスト"""
        query = '''("high flow nasal cannula"* [tiab] OR "high flow oxygen therapy"* [tiab] OR "nasal high flow therapy"[tiab] OR hfnc[tiab] OR "heated humidified high flow" [tiab] OR "Precision Flow"[tiab] OR "HVT"[tiab] OR ProSoft[tiab]) AND ("Respiratory Insufficiency"[Mesh] OR "Respiratory Failure"[tiab] OR "Acute respiratory failure"[tiab] OR hypercapnia[Mesh] OR hypercapnia[tiab] OR hypercapnic[tiab])'''
        warnings = lint_pubmed_query(query)
        # ワイルドカード警告が2つあるはず
        wildcard_warnings = [w for w in warnings if w.rule_id == "PHRASE_WILDCARD"]
        assert len(wildcard_warnings) == 2


class TestExtractMeshTermsFromQuery:
    """MeSH用語抽出のテスト"""

    def test_extract_quoted_mesh_terms(self):
        """引用符付きMeSH用語が正しく抽出されることを確認"""
        query = '"Respiratory Distress Syndrome"[Mesh] OR "Acute Lung Injury"[Mesh]'
        terms = extract_mesh_terms_from_query(query)
        assert len(terms) == 2
        assert "Respiratory Distress Syndrome" in terms
        assert "Acute Lung Injury" in terms

    def test_extract_with_space_before_tag(self):
        """タグ前にスペースがあっても抽出されることを確認"""
        query = '"Shock, Cardiogenic" [Mesh]'
        terms = extract_mesh_terms_from_query(query)
        assert len(terms) == 1
        assert "Shock, Cardiogenic" in terms

    def test_no_mesh_terms(self):
        """MeSH用語がない場合は空リストを返すことを確認"""
        query = 'ARDS[tiab] OR "acute respiratory distress syndrome"[tiab]'
        terms = extract_mesh_terms_from_query(query)
        assert len(terms) == 0

    def test_case_insensitive_tag(self):
        """[Mesh]タグの大文字小文字を区別しないことを確認"""
        query = '"Pulmonary Edema"[MESH] OR "Shock"[mesh]'
        terms = extract_mesh_terms_from_query(query)
        assert len(terms) == 2

    def test_mixed_tags(self):
        """MeSHタグとtiabタグが混在する場合、MeSHのみ抽出されることを確認"""
        query = '"Extracorporeal Membrane Oxygenation"[Mesh] OR ecmo[tiab] OR "ARDS"[tiab]'
        terms = extract_mesh_terms_from_query(query)
        assert len(terms) == 1
        assert "Extracorporeal Membrane Oxygenation" in terms


class TestCheckMeshExactMatch:
    """MeSH exact matchチェックのテスト（APIはモックで代替）"""

    @patch('scripts.validation.pubmed_syntax_linter.fetch_mesh_preferred_name')
    def test_entry_term_detected(self, mock_fetch):
        """Entry Termが検出され警告が生成されることを確認"""
        # "Respiratory Distress Syndrome, Adult" はEntry Term
        # 正式名は "Respiratory Distress Syndrome"
        mock_fetch.return_value = "Respiratory Distress Syndrome"
        query = '"Respiratory Distress Syndrome, Adult"[Mesh]'
        warnings = check_mesh_exact_match(query)
        assert len(warnings) == 1
        assert warnings[0].rule_id == "MESH_NOT_PREFERRED"
        assert "Entry Term" in warnings[0].message
        assert '"Respiratory Distress Syndrome"[Mesh]' in warnings[0].suggestion

    @patch('scripts.validation.pubmed_syntax_linter.fetch_mesh_preferred_name')
    def test_preferred_term_no_warning(self, mock_fetch):
        """正式なDescriptorNameでは警告が出ないことを確認"""
        mock_fetch.return_value = "Respiratory Distress Syndrome"
        query = '"Respiratory Distress Syndrome"[Mesh]'
        warnings = check_mesh_exact_match(query)
        assert len(warnings) == 0

    @patch('scripts.validation.pubmed_syntax_linter.fetch_mesh_preferred_name')
    def test_not_found_term(self, mock_fetch):
        """MeSHに存在しない用語でMESH_NOT_FOUND警告が生成されることを確認"""
        mock_fetch.return_value = None
        query = '"Nonexistent Term XYZ"[Mesh]'
        warnings = check_mesh_exact_match(query)
        assert len(warnings) == 1
        assert warnings[0].rule_id == "MESH_NOT_FOUND"

    @patch('scripts.validation.pubmed_syntax_linter.fetch_mesh_preferred_name')
    def test_multiple_terms_mixed(self, mock_fetch):
        """複数のMeSH用語が混在する場合のテスト"""
        def side_effect(term):
            mapping = {
                "Respiratory Distress Syndrome, Adult": "Respiratory Distress Syndrome",
                "Acute Lung Injury": "Acute Lung Injury",
                "Shock, Cardiogenic": "Shock, Cardiogenic",
            }
            return mapping.get(term)

        mock_fetch.side_effect = side_effect
        query = (
            '"Respiratory Distress Syndrome, Adult"[Mesh] '
            'OR "Acute Lung Injury"[Mesh] '
            'OR "Shock, Cardiogenic"[Mesh]'
        )
        warnings = check_mesh_exact_match(query)
        # 1件のみ: "Respiratory Distress Syndrome, Adult" がEntry Term
        assert len(warnings) == 1
        assert warnings[0].rule_id == "MESH_NOT_PREFERRED"
        assert "Respiratory Distress Syndrome, Adult" in warnings[0].message

    @patch('scripts.validation.pubmed_syntax_linter.fetch_mesh_preferred_name')
    def test_case_insensitive_match(self, mock_fetch):
        """大文字小文字を無視した一致確認"""
        mock_fetch.return_value = "Extracorporeal Membrane Oxygenation"
        query = '"extracorporeal membrane oxygenation"[Mesh]'
        warnings = check_mesh_exact_match(query)
        assert len(warnings) == 0


class TestLintPubmedQueryWithMesh:
    """check_mesh=Trueでの統合テスト"""

    @patch('scripts.validation.pubmed_syntax_linter.fetch_mesh_preferred_name')
    def test_mesh_check_included_when_enabled(self, mock_fetch):
        """check_mesh=Trueの場合MeSHチェックが実行されることを確認"""
        mock_fetch.return_value = "Respiratory Distress Syndrome"
        query = '"Respiratory Distress Syndrome, Adult"[Mesh]'
        warnings = lint_pubmed_query(query, check_mesh=True)
        mesh_warnings = [w for w in warnings if w.rule_id == "MESH_NOT_PREFERRED"]
        assert len(mesh_warnings) == 1

    def test_mesh_check_not_included_by_default(self):
        """デフォルトではMeSHチェックが実行されないことを確認"""
        query = '"Respiratory Distress Syndrome, Adult"[Mesh]'
        warnings = lint_pubmed_query(query)
        mesh_warnings = [w for w in warnings if w.rule_id in ("MESH_NOT_PREFERRED", "MESH_NOT_FOUND")]
        assert len(mesh_warnings) == 0


class TestFormatLintReport:
    """レポートフォーマットのテスト"""
    
    def test_no_warnings_message(self):
        """警告がない場合のメッセージを確認"""
        report = format_lint_report([])
        assert "問題は検出されませんでした" in report
    
    def test_warnings_in_report(self):
        """警告がレポートに含まれることを確認"""
        warnings = [
            LintWarning(
                rule_id="TEST_RULE",
                message="テストメッセージ",
                original_term="test term",
                suggestion="テスト推奨",
                severity="warning"
            )
        ]
        report = format_lint_report(warnings)
        assert "TEST_RULE" in report
        assert "テストメッセージ" in report
        assert "test term" in report
        assert "テスト推奨" in report
    
    def test_query_in_report_with_warnings(self):
        """警告がある場合、検索式がレポートに含まれることを確認"""
        query = "test query"
        warnings = [
            LintWarning(
                rule_id="TEST_RULE",
                message="テストメッセージ",
                original_term="test term",
                suggestion="テスト推奨",
                severity="warning"
            )
        ]
        report = format_lint_report(warnings, query)
        assert query in report
    
    def test_no_query_in_report_without_warnings(self):
        """警告がない場合、シンプルなメッセージのみ返すことを確認"""
        query = "test query"
        report = format_lint_report([], query)
        # 警告がない場合はシンプルなメッセージのみ
        assert "問題は検出されませんでした" in report
