#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PubMed検索式リンターのテスト

テスト対象:
1. フレーズ検索後のワイルドカード検出
2. ハイフン付きバリエーションの冗長性検出
"""

import pytest
from scripts.validation.pubmed_syntax_linter import (
    normalize_term_for_comparison,
    check_phrase_wildcard,
    check_redundant_hyphen_variants,
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
