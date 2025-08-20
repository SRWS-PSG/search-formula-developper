#!/usr/bin/env python3
"""
Dialog変換機能のテストスクリプト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from search_converter import normalize_pubmed_input, validate_search_syntax, convert_to_dialog

def test_normalize_input():
    """入力正規化のテスト"""
    print("=== 入力正規化テスト ===")
    
    test_cases = [
        "1. exp Lung Diseases, Interstitial/",
        "2 (Interstitial adj3 lung$).tw.",
        "3. ILD.ti,ab.",
        "4 or 5 or 6"
    ]
    
    input_text = '\n'.join(test_cases)
    normalized = normalize_pubmed_input(input_text)
    
    print("入力:")
    print(input_text)
    print("\n正規化後:")
    print(normalized)
    print()

def test_syntax_validation():
    """構文検証のテスト"""
    print("=== 構文検証テスト ===")
    
    error_text = """1. exp Lung Diseases, Interstitial/
2 (Interstitial adj3 lung$).tw.
3. exp Fear
4. 1 or 2 or 3"""
    
    errors = validate_search_syntax(error_text)
    print("エラーがある検索式:")
    print(error_text)
    print("\n検出されたエラー:")
    for error in errors:
        print(f"  - {error}")
    print()

def test_dialog_conversion():
    """Dialog変換のテスト"""
    print("=== Dialog変換テスト ===")
    
    pubmed_query = """1. exp Lung Diseases, Interstitial/
2. (Interstitial adj3 (lung$ or pulmonary)).tw.
3. ILD.ti,ab.
4. 1 or 2 or 3"""
    
    print("PubMed検索式:")
    print(pubmed_query)
    print("\nDialog変換結果:")
    dialog_result = convert_to_dialog(pubmed_query)
    print(dialog_result)
    print()

if __name__ == "__main__":
    test_normalize_input()
    test_syntax_validation()
    test_dialog_conversion()
    print("✅ すべてのテストが完了しました。")
