#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PubMed検索式の構文チェックとリンティングを行うモジュール

このモジュールは以下の機能を提供します：
1. ワイルドカード検出: フレーズ検索後のワイルドカード（"phrase"*）を検出し警告
2. 冗長性検出: PubMedが同一視する用語（ハイフン付きバリエーションなど）の重複を検出

PubMedの動作仕様:
- ハイフンはスペースと同等に扱われる（"high-flow" = "high flow"）
- フレーズ検索後のワイルドカード（*）は無視される
- フィールドタグ前のスペースは無視される
"""

import re
import time
import xml.etree.ElementTree as ET
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


@dataclass
class LintWarning:
    """リント警告を表すデータクラス"""
    rule_id: str
    message: str
    original_term: str
    suggestion: str = ""
    severity: str = "warning"  # "warning" or "info"


def normalize_term_for_comparison(term: str) -> str:
    """
    PubMedの正規化ルールに基づいて用語を正規化する

    PubMedでは以下の文字が同等に扱われる：
    - ハイフン（-）とスペース
    - 大文字と小文字

    Args:
        term: 正規化する用語

    Returns:
        正規化された用語
    """
    # ハイフンをスペースに変換
    normalized = term.replace('-', ' ')
    # 連続するスペースを単一スペースに
    normalized = re.sub(r'\s+', ' ', normalized)
    # 小文字に変換
    normalized = normalized.lower()
    # 前後の空白を削除
    normalized = normalized.strip()
    return normalized


def extract_search_terms(query: str) -> List[Tuple[str, str]]:
    """
    検索式から検索用語とフィールドタグを抽出する

    Args:
        query: PubMed検索式

    Returns:
        List of (term, field_tag) tuples
    """
    terms = []

    # フレーズ検索（引用符付き）のパターン
    # "term"[field] または "term"*[field] または "term" [field]
    phrase_pattern = re.compile(r'"([^"]+)"(\*?)\s*\[([^\]]+)\]')
    for match in phrase_pattern.finditer(query):
        term = match.group(1)
        has_wildcard = match.group(2) == '*'
        field = match.group(3)
        terms.append((term, field, has_wildcard))

    # 単一語検索のパターン: term[field] または term*[field]
    single_pattern = re.compile(
        r'(?<!["\w])([a-zA-Z][a-zA-Z0-9]*)(\*?)\[([^\]]+)\]'
    )
    for match in single_pattern.finditer(query):
        term = match.group(1)
        has_wildcard = match.group(2) == '*'
        field = match.group(3)
        # フレーズ検索で既に抽出されていないか確認
        if not any(t[0] == term for t in terms):
            terms.append((term, field, has_wildcard))

    return terms


def check_phrase_wildcard(query: str) -> List[LintWarning]:
    """
    フレーズ検索後のワイルドカードを検出する

    PubMedでは "phrase"* のようなパターンでワイルドカードは無視される。
    PubMedは「The following term was ignored: *」と表示する。

    Args:
        query: PubMed検索式

    Returns:
        検出された警告のリスト
    """
    warnings = []

    # "phrase"*[field] または "phrase"* [field] のパターンを検出
    pattern = re.compile(r'"([^"]+)"\*\s*\[([^\]]+)\]')

    for match in pattern.finditer(query):
        phrase = match.group(1)
        field = match.group(2)
        original = match.group(0)

        warning = LintWarning(
            rule_id="PHRASE_WILDCARD",
            message='フレーズ検索後のワイルドカード（*）はPubMedで無視されます。',
            original_term=original,
            suggestion=(
                f'"{phrase}"[{field}] に修正するか、'
                '切り捨て検索が必要な場合は別の方法を検討してください。'
            ),
            severity="warning"
        )
        warnings.append(warning)

    return warnings


def check_redundant_hyphen_variants(query: str) -> List[LintWarning]:
    """
    ハイフン付きバリエーションの冗長性を検出する

    PubMedではハイフンはスペースと同等に扱われるため、
    "high-flow" と "high flow" は同じ結果を返す。
    両方が検索式に含まれている場合は冗長。

    また、"phrase"*[field] と "phrase"[field] も同じ結果を返す
    （ワイルドカードは無視されるため）。

    Args:
        query: PubMed検索式

    Returns:
        検出された警告のリスト
    """
    warnings = []

    # フレーズ検索のパターンを抽出（ワイルドカード付きも含む）
    # "term"[field] または "term"*[field] または "term" [field] または "term"* [field]
    phrase_pattern = re.compile(r'"([^"]+)"\*?\s*\[([^\]]+)\]')
    phrases = []

    for match in phrase_pattern.finditer(query):
        term = match.group(1)
        field = match.group(2)
        original = match.group(0)
        normalized = normalize_term_for_comparison(term)
        phrases.append({
            'original': original,
            'term': term,
            'field': field,
            'normalized': normalized
        })

    # 正規化後の用語でグループ化
    normalized_groups: Dict[str, List[dict]] = {}
    for phrase in phrases:
        key = (phrase['normalized'], phrase['field'].lower())
        if key not in normalized_groups:
            normalized_groups[key] = []
        normalized_groups[key].append(phrase)

    # 重複があるグループを検出
    for key, group in normalized_groups.items():
        if len(group) > 1:
            # 重複している用語のリスト
            duplicates = [p['term'] for p in group]
            originals = [p['original'] for p in group]

            # 最初の用語を残すことを推奨
            keep_term = group[0]['term']
            remove_terms = duplicates[1:]

            dup_str = ", ".join(duplicates)
            remove_str = ", ".join(remove_terms)
            warning = LintWarning(
                rule_id="REDUNDANT_HYPHEN_VARIANT",
                message=(
                    'PubMedではハイフンとスペースは同等に扱われるため、'
                    f'以下の用語は冗長です: {dup_str}'
                ),
                original_term=", ".join(originals),
                suggestion=(
                    f'"{keep_term}" のみを使用することを推奨します。'
                    f'削除候補: {remove_str}'
                ),
                severity="info"
            )
            warnings.append(warning)

    return warnings


def extract_mesh_terms_from_query(query: str) -> List[str]:
    """
    検索式から[Mesh]タグ付きの用語を抽出する

    Args:
        query: PubMed検索式

    Returns:
        MeSH用語のリスト
    """
    pattern = re.compile(r'"([^"]+)"\s*\[Mesh\]', re.IGNORECASE)
    return [m.group(1) for m in pattern.finditer(query)]


def fetch_mesh_preferred_name(term: str) -> Optional[str]:
    """
    MeSHデータベースから用語を検索し、正式なDescriptorName（優先用語）を取得する。

    Entry Term（同義語）で検索した場合でも、対応する正式なDescriptorNameを返す。
    例: "Respiratory Distress Syndrome, Adult" → "Respiratory Distress Syndrome"

    Args:
        term: 検索するMeSH用語

    Returns:
        正式なDescriptorName。見つからない場合はNone。
    """
    if not HAS_REQUESTS:
        return None

    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    search_url = f"{base_url}/esearch.fcgi"
    fetch_url = f"{base_url}/efetch.fcgi"

    try:
        # Step 1: MeSHデータベースでUIDを検索
        search_params = {
            'db': 'mesh',
            'term': term,
            'retmode': 'json'
        }
        response = requests.get(search_url, params=search_params, timeout=30)
        response.raise_for_status()
        data = response.json()

        id_list = data.get('esearchresult', {}).get('idlist', [])
        if not id_list:
            return None

        # Step 2: efetchでDescriptorレコードのXMLを取得
        time.sleep(0.34)  # API rate limit
        fetch_params = {
            'db': 'mesh',
            'id': id_list[0],
            'retmode': 'xml'
        }
        fetch_resp = requests.get(fetch_url, params=fetch_params, timeout=30)
        fetch_resp.raise_for_status()

        root = ET.fromstring(fetch_resp.content)
        descriptor_name_elem = root.find('.//DescriptorName/String')
        if descriptor_name_elem is not None and descriptor_name_elem.text:
            return descriptor_name_elem.text

        return None

    except Exception:
        return None


def check_mesh_exact_match(query: str) -> List[LintWarning]:
    """
    MeSH用語が正式なDescriptorName（優先用語）と一致するかを検証する。

    Entry Term（同義語）のみの一致の場合、[Mesh]タグでは正確にヒットしない
    ため、正式なDescriptorNameへの修正を推奨する警告を生成する。

    注: requestsライブラリが利用できない場合、またはAPI呼び出しが失敗した場合は
    警告を生成しない（オフラインでも他のチェックは動作する）。

    Args:
        query: PubMed検索式

    Returns:
        検出された警告のリスト
    """
    warnings = []

    if not HAS_REQUESTS:
        return warnings

    mesh_terms = extract_mesh_terms_from_query(query)

    for term in mesh_terms:
        preferred_name = fetch_mesh_preferred_name(term)
        if preferred_name is None:
            # API失敗またはMeSHデータベースに存在しない
            warnings.append(LintWarning(
                rule_id="MESH_NOT_FOUND",
                message=f'MeSHデータベースで "{term}" が見つかりませんでした。用語名を確認してください。',
                original_term=f'"{term}"[Mesh]',
                suggestion='NLM MeSH Browser (https://meshb.nlm.nih.gov/) で正しい用語を確認してください。',
                severity="warning"
            ))
        elif term.lower() != preferred_name.lower():
            # Entry Term（同義語）であり、正式なDescriptorNameではない
            warnings.append(LintWarning(
                rule_id="MESH_NOT_PREFERRED",
                message=(
                    f'"{term}" はEntry Term（同義語）であり、正式なMeSH Descriptor Nameではありません。'
                    f'[Mesh]タグで正確にヒットしない可能性があります。'
                ),
                original_term=f'"{term}"[Mesh]',
                suggestion=f'"{preferred_name}"[Mesh] に修正してください。',
                severity="warning"
            ))
        # else: 正式なDescriptorNameと一致 → 問題なし

        time.sleep(0.34)  # API rate limit between terms

    return warnings


def lint_pubmed_query(query: str, check_mesh: bool = False) -> List[LintWarning]:
    """
    PubMed検索式に対してすべてのリントチェックを実行する

    Args:
        query: PubMed検索式
        check_mesh: MeSH用語のexact matchチェックを行うか（APIアクセスが必要）

    Returns:
        検出された警告のリスト
    """
    warnings = []

    # 1. フレーズ検索後のワイルドカードチェック
    warnings.extend(check_phrase_wildcard(query))

    # 2. ハイフン付きバリエーションの冗長性チェック
    warnings.extend(check_redundant_hyphen_variants(query))

    # 3. MeSH用語のexact matchチェック（オプション、API必要）
    if check_mesh:
        warnings.extend(check_mesh_exact_match(query))

    return warnings


def format_lint_report(warnings: List[LintWarning], query: str = "") -> str:
    """
    リント結果をフォーマットしたレポートを生成する

    Args:
        warnings: 警告のリスト
        query: 元の検索式（オプション）

    Returns:
        フォーマットされたレポート文字列
    """
    if not warnings:
        return "PubMed検索式のリントチェック: 問題は検出されませんでした。"

    lines = ["# PubMed検索式リントレポート", ""]

    if query:
        lines.append("## 検索式")
        lines.append("```")
        lines.append(query)
        lines.append("```")
        lines.append("")

    lines.append(f"## 検出された問題 ({len(warnings)}件)")
    lines.append("")

    for i, warning in enumerate(warnings, 1):
        severity_icon = "⚠️" if warning.severity == "warning" else "ℹ️"
        lines.append(f"### {i}. [{warning.rule_id}] {severity_icon}")
        lines.append(f"**問題**: {warning.message}")
        lines.append(f"**対象**: `{warning.original_term}`")
        if warning.suggestion:
            lines.append(f"**推奨**: {warning.suggestion}")
        lines.append("")

    return "\n".join(lines)


def main():
    """コマンドラインインターフェース"""
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description='PubMed検索式の構文チェックとリンティングを行うツール'
    )
    parser.add_argument(
        'input',
        nargs='?',
        help='PubMed検索式のテキストファイル（指定がなければ標準入力から読み込み）'
    )
    parser.add_argument(
        '--output', '-o',
        help='出力ファイルのパス（指定がなければ標準出力）'
    )
    parser.add_argument(
        '--format', '-f',
        choices=['text', 'json'],
        default='text',
        help='出力フォーマット（デフォルト: text）'
    )
    parser.add_argument(
        '--check-mesh',
        action='store_true',
        default=False,
        help='MeSH用語のexact matchチェックを有効にする（APIアクセスが必要）'
    )

    args = parser.parse_args()

    # 入力の読み込み
    if args.input:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                query = f.read()
        except Exception as e:
            print(f"ファイルの読み込みに失敗しました: {str(e)}", file=sys.stderr)
            sys.exit(1)
    else:
        print("PubMed検索式を入力してください（終了するには Ctrl+D を押してください）:",
              file=sys.stderr)
        query = sys.stdin.read()

    # リントチェックの実行
    warnings = lint_pubmed_query(query, check_mesh=args.check_mesh)

    # 結果の出力
    if args.format == 'json':
        import json
        result = {
            'query': query,
            'warnings': [
                {
                    'rule_id': w.rule_id,
                    'message': w.message,
                    'original_term': w.original_term,
                    'suggestion': w.suggestion,
                    'severity': w.severity
                }
                for w in warnings
            ]
        }
        output = json.dumps(result, ensure_ascii=False, indent=2)
    else:
        output = format_lint_report(warnings, query)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"レポートを {args.output} に保存しました。", file=sys.stderr)
    else:
        print(output)

    # 警告がある場合は終了コード1
    sys.exit(1 if warnings else 0)


if __name__ == "__main__":
    main()
