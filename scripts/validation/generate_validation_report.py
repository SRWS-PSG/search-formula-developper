#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import subprocess
import time
import json
import re
from datetime import datetime
from typing import Dict, List, Any

def ensure_directory_exists(path: str) -> None:
    """
    ディレクトリが存在しない場合は作成する
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

def extract_pmids_from_file(file_path: str) -> List[str]:
    """
    ファイルから組入論文のPMIDを抽出する
    
    Args:
        file_path: ファイルパス
    
    Returns:
        List[str]: PMIDのリスト
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # PMID抽出（PMID: 数字形式）
    pmids = re.findall(r'PMID:\s*(\d+)', content)
    
    return pmids

def run_term_validation(input_file: str, output_dir: str) -> str:
    """
    MeSH用語とキーワードの検証を実行する
    
    Args:
        input_file: 検索式ファイルのパス
        output_dir: 出力ディレクトリ
        
    Returns:
        str: 出力ファイルのパス
    """
    print("\n=== MeSH用語とキーワードの検証を実行中... ===")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(output_dir, f"term_check_{timestamp}.log")
    
    cmd = [
        sys.executable,
        'scripts/validation/term_validator/check_term.py',
        '--input', input_file,
        '--output', output_file
    ]
    
    process = subprocess.run(cmd, capture_output=True, text=True)
    
    if process.returncode != 0:
        print(f"エラー: MeSH用語とキーワードの検証に失敗しました。")
        print(f"エラー詳細: {process.stderr}")
        return ""
    
    print(f"MeSH用語とキーワードの検証が完了しました。結果: {output_file}")
    return output_file

def run_paper_mesh_analysis(input_file: str, output_dir: str) -> str:
    """
    組入論文のMeSH用語分析を実行する
    
    Args:
        input_file: 検索式ファイルのパス
        output_dir: 出力ディレクトリ
        
    Returns:
        str: 出力ファイルのパス（Markdown形式）
    """
    print("\n=== 組入論文のMeSH用語分析を実行中... ===")
    
    # 組入論文のPMIDを抽出
    pmids = extract_pmids_from_file(input_file)
    
    if not pmids:
        print("警告: 組入論文のPMIDが見つかりませんでした。MeSH用語分析をスキップします。")
        return ""
    
    # PMIDをカンマ区切りのリストに変換
    pmids_str = ",".join(pmids)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(output_dir, f"paper_mesh_analysis_{timestamp}.json")
    
    cmd = [
        sys.executable,
        'scripts/utils/analyze_paper_mesh.py',
        '--pmids', pmids_str,
        '--search_formula', input_file,
        '--output', output_file
    ]
    
    process = subprocess.run(cmd, capture_output=True, text=True)
    
    if process.returncode != 0:
        print(f"エラー: 組入論文のMeSH用語分析に失敗しました。")
        print(f"エラー詳細: {process.stderr}")
        return ""
    
    # 対応するMarkdownファイルのパスを返す
    md_output_file = output_file.replace('.json', '.md')
    print(f"組入論文のMeSH用語分析が完了しました。結果: {md_output_file}")
    return md_output_file

def run_mesh_overlap_analysis(input_file: str, output_dir: str) -> str:
    """
    MeSH用語の重複と階層関係を分析する
    
    Args:
        input_file: 検索式ファイルのパス
        output_dir: 出力ディレクトリ
        
    Returns:
        str: 出力ファイルのパス
    """
    print("\n=== MeSH用語の重複と階層関係を分析中... ===")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(output_dir, f"search_overlap_{timestamp}.md")
    
    cmd = [
        sys.executable,
        'scripts/search/mesh_analyzer/check_mesh_overlap.py',
        '--input', input_file,
        '--output', output_file
    ]
    
    process = subprocess.run(cmd, capture_output=True, text=True)
    
    if process.returncode != 0:
        print(f"エラー: MeSH用語の重複分析に失敗しました。")
        print(f"エラー詳細: {process.stderr}")
        return ""
    
    print(f"MeSH用語の重複分析が完了しました。結果: {output_file}")
    return output_file

def run_paper_inclusion_check(input_file: str, output_dir: str) -> str:
    """
    検索式での組入論文の包含確認を実行する
    
    Args:
        input_file: 検索式ファイルのパス
        output_dir: 出力ディレクトリ
        
    Returns:
        str: 出力ファイルのパス
    """
    print("\n=== 検索式での組入論文の包含確認を実行中... ===")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(output_dir, f"inclusion_check_{timestamp}.log")
    
    cmd = [
        sys.executable,
        'scripts/validation/seed_analyzer/check_specific_papers.py',
        '--input', input_file,
        '--output', output_file
    ]
    
    process = subprocess.run(cmd, capture_output=True, text=True)
    
    if process.returncode != 0:
        print(f"エラー: 組入論文の包含確認に失敗しました。")
        print(f"エラー詳細: {process.stderr}")
        return ""
    
    print(f"組入論文の包含確認が完了しました。結果: {output_file}")
    return output_file

def extract_content_from_file(file_path: str, section_title: str = None) -> str:
    """
    ファイルの内容を抽出する。sectionが指定されている場合は該当セクションのみ抽出する。
    
    Args:
        file_path: ファイルパス
        section_title: 抽出するセクションのタイトル（例: "## 検索結果"）
        
    Returns:
        str: 抽出した内容
    """
    if not os.path.exists(file_path):
        return ""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if section_title:
        # セクション抽出（"## セクション"から次の"## "の前まで）
        pattern = f"{section_title}(.*?)(?:^##\\s|\\Z)"
        match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
        return match.group(1).strip() if match else ""
    
    return content

def generate_final_report(
    input_file: str,
    term_check_file: str,
    paper_mesh_file: str,
    overlap_file: str,
    inclusion_file: str,
    output_file: str
) -> None:
    """
    最終的な検証レポートを生成する
    
    Args:
        input_file: 検索式ファイルのパス
        term_check_file: MeSH用語とキーワードの検証結果ファイル
        paper_mesh_file: 組入論文のMeSH用語分析結果ファイル
        overlap_file: MeSH用語の重複分析結果ファイル
        inclusion_file: 組入論文の包含確認結果ファイル
        output_file: 出力ファイルのパス
    """
    print("\n=== 最終検証レポートを生成中... ===")
    
    # 検索式ファイルの内容を取得
    with open(input_file, 'r', encoding='utf-8') as f:
        search_formula_content = f.read()
    
    # 検索式の抽出（コードブロック内）
    search_formula_match = re.search(r'```\s*\n(.*?)\n```', search_formula_content, re.DOTALL)
    search_formula = search_formula_match.group(1) if search_formula_match else "検索式を抽出できませんでした"
    
    # 各ファイルから必要なセクションを抽出
    term_check_summary = extract_content_from_file(term_check_file, "## 検索結果要約")
    paper_mesh_summary = extract_content_from_file(paper_mesh_file, "## 分析サマリー")
    overlap_summary = extract_content_from_file(overlap_file)
    inclusion_summary = extract_content_from_file(inclusion_file, "## 検索結果")
    recommendation = extract_content_from_file(inclusion_file, "## 推奨される対応")
    
    # 包含状況の詳細
    inclusion_details = extract_content_from_file(inclusion_file, "## 論文別包含状況")
    
    # 最終レポートの作成
    final_report = f"""# 検索式検証総合レポート
日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 検証対象の検索式
```
{search_formula}
```

## 検証サマリー

### 検索結果
{inclusion_summary}

### MeSH用語・キーワードの検証結果
{term_check_summary}

### 組入論文のMeSH用語分析
{paper_mesh_summary}

## 検索式の構造分析
{overlap_summary}

## 組入論文の包含状況
{inclusion_details}

## 推奨される対応
{recommendation}

## 詳細レポート参照先
- MeSH用語とキーワードの検証: {os.path.basename(term_check_file) if term_check_file else "なし"}
- 組入論文のMeSH用語分析: {os.path.basename(paper_mesh_file) if paper_mesh_file else "なし"}
- MeSH用語の重複分析: {os.path.basename(overlap_file) if overlap_file else "なし"}
- 組入論文の包含確認: {os.path.basename(inclusion_file) if inclusion_file else "なし"}
"""
    
    # レポートの保存
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_report)
    
    print(f"最終検証レポートを生成しました: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='検索式の総合検証を実行するスクリプト')
    parser.add_argument('--input', required=True, help='検索式ファイルのパス')
    parser.add_argument('--output_dir', help='出力ディレクトリ（指定しない場合はdocs/validation/に保存）')
    parser.add_argument('--steps', default='all', help='実行するステップ（カンマ区切り: term,mesh,overlap,inclusion,all）')
    
    args = parser.parse_args()
    input_file = args.input
    
    if args.output_dir:
        output_dir = args.output_dir
    else:
        output_dir = "docs/validation"
    
    # 出力ディレクトリの確保
    os.makedirs(output_dir, exist_ok=True)
    logs_dir = "logs/validation"
    os.makedirs(logs_dir, exist_ok=True)
    
    # 実行するステップの確認
    steps = args.steps.split(',')
    run_all = 'all' in steps
    
    # タイムスタンプ（最終レポート用）
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    final_report_file = os.path.join(output_dir, f"search_validation_report_{timestamp}.md")
    
    # 各ステップの実行
    term_check_file = ""
    paper_mesh_file = ""
    overlap_file = ""
    inclusion_file = ""
    
    if run_all or 'term' in steps:
        term_check_file = run_term_validation(input_file, logs_dir)
    
    if run_all or 'mesh' in steps:
        paper_mesh_file = run_paper_mesh_analysis(input_file, "logs/analysis")
    
    if run_all or 'overlap' in steps:
        overlap_file = run_mesh_overlap_analysis(input_file, logs_dir)
    
    if run_all or 'inclusion' in steps:
        inclusion_file = run_paper_inclusion_check(input_file, logs_dir)
    
    # 最終レポートの生成
    generate_final_report(
        input_file,
        term_check_file,
        paper_mesh_file,
        overlap_file,
        inclusion_file,
        final_report_file
    )
    
    print("\n検証が完了しました。")
    print(f"最終レポート: {final_report_file}")

if __name__ == "__main__":
    main()
