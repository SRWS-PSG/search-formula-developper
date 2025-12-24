#!/usr/bin/env python3
"""
ERIC Thesaurus Scraper Module

ERIC シソーラス（ディスクリプタ）のWebページをスクレイピングし、
用語の階層関係や関連用語を取得するモジュール。

Usage:
    from scripts.search.eric.eric_thesaurus import get_thesaurus_info
    
    info = get_thesaurus_info("Medical School Faculty")
    print(info.related_terms)
"""

import requests
import time
import re
from typing import List, Optional
from dataclasses import dataclass, field
from urllib.parse import quote, unquote

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


# ERIC Thesaurus URL Configuration
ERIC_THESAURUS_BASE_URL = "https://eric.ed.gov/"


@dataclass
class ThesaurusInfo:
    """ERICシソーラス用語の情報を格納するデータクラス"""
    term: str                                  # 用語
    exists: bool = False                       # 存在するか
    category: str = ""                         # カテゴリ
    broader_terms: List[str] = field(default_factory=list)   # 上位語
    narrower_terms: List[str] = field(default_factory=list)  # 下位語
    related_terms: List[str] = field(default_factory=list)   # 関連語
    used_for: List[str] = field(default_factory=list)        # 過去の用語
    scope_note: str = ""                       # スコープノート
    error_message: str = ""                    # エラーメッセージ


def get_thesaurus_url(term: str) -> str:
    """シソーラスページのURLを生成"""
    encoded_term = quote(term, safe='')
    return f"{ERIC_THESAURUS_BASE_URL}?qt={encoded_term}&ti={encoded_term}"


def get_thesaurus_info(term: str, retry_count: int = 3) -> ThesaurusInfo:
    """
    指定用語のシソーラス情報を取得する。
    
    Args:
        term: シソーラス用語
        retry_count: リトライ回数
    
    Returns:
        ThesaurusInfo: シソーラス情報
    
    Example:
        >>> info = get_thesaurus_info("Medical School Faculty")
        >>> print(info.category)
        "Students, Teachers, School Personnel"
        >>> print(info.related_terms)
        ["Graduate School Faculty", "Dental School Faculty", ...]
    """
    if not HAS_BS4:
        return ThesaurusInfo(
            term=term,
            exists=False,
            error_message="beautifulsoup4 is not installed. Run: pip install beautifulsoup4"
        )
    
    url = get_thesaurus_url(term)
    
    last_error = None
    for attempt in range(retry_count):
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            return _parse_thesaurus_page(term, response.text)
            
        except requests.exceptions.RequestException as e:
            last_error = e
            if attempt < retry_count - 1:
                time.sleep(1)
                continue
    
    return ThesaurusInfo(
        term=term,
        exists=False,
        error_message=f"Error: {str(last_error)}"
    )


def _parse_thesaurus_page(term: str, html: str) -> ThesaurusInfo:
    """
    シソーラスページのHTMLをパースする。
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    info = ThesaurusInfo(term=term)
    
    # h2タグで用語名を確認
    h2_tag = soup.find('h2')
    if not h2_tag:
        info.exists = False
        info.error_message = "Term not found in thesaurus"
        return info
    
    found_term = h2_tag.get_text(strip=True)
    
    # 用語が見つかったかチェック (大文字小文字無視で比較)
    if found_term.lower() != term.lower():
        # 検索結果ページが表示されている可能性
        if "Search Results" in html or "No results" in html:
            info.exists = False
            info.error_message = "Term not found in thesaurus"
            return info
    
    info.exists = True
    info.term = found_term  # 正式な用語名に更新
    
    # リンクを全て取得
    all_links = soup.find_all('a')
    
    related_terms = []
    category = ""
    
    for link in all_links:
        href = link.get('href', '')
        text = link.get_text(strip=True)
        
        # カテゴリリンク (数字が含まれるti=パラメータ)
        if 'ti=' in href and re.search(r'ti=\d+', href):
            if not category:  # 最初のカテゴリのみ
                category = text
        
        # シソーラス用語へのリンク
        elif 'ti=' in href and text and text != found_term:
            # 過去の用語 (Former Terms) のパターン
            if '(' in text and ')' in text and any(year in text for year in ['1966', '1967', '1980', '1990', '2000']):
                info.used_for.append(text)
            # 検索リンクやナビゲーションを除外
            elif text not in ['Notes', 'FAQ', 'Contact Us', 'Thesaurus', 'Search Tips', 
                             'Advanced', 'Collection', 'Browse', 'Back to Search Results',
                             'Privacy', 'Copyright', 'Selection Policy', 'API', 'Metrics',
                             'Journals', 'Non-Journals', 'Download', 'Submit', 'Multimedia', 'Widget']:
                # Search collection linkを除外
                if 'Search collection' not in text:
                    related_terms.append(text)
    
    info.category = category
    info.related_terms = related_terms
    
    return info


def check_term_exists(term: str) -> bool:
    """
    用語がERICシソーラスに存在するか確認する。
    
    Args:
        term: 確認する用語
    
    Returns:
        bool: 存在する場合True
    """
    info = get_thesaurus_info(term)
    return info.exists


def get_broader_terms(term: str) -> List[str]:
    """
    指定用語の上位語を取得する。
    
    Note:
        ERICのシソーラスページでは上位語・下位語の明確な区別が
        表示されない場合があります。その場合は空のリストを返します。
    """
    info = get_thesaurus_info(term)
    return info.broader_terms


def get_narrower_terms(term: str) -> List[str]:
    """
    指定用語の下位語を取得する。
    """
    info = get_thesaurus_info(term)
    return info.narrower_terms


def get_related_terms(term: str) -> List[str]:
    """
    指定用語の関連語を取得する。
    """
    info = get_thesaurus_info(term)
    return info.related_terms


def format_thesaurus_info(info: ThesaurusInfo) -> str:
    """
    シソーラス情報を表示用にフォーマットする。
    """
    lines = []
    
    if not info.exists:
        lines.append(f"[NOT FOUND] {info.term}")
        if info.error_message:
            lines.append(f"  Error: {info.error_message}")
        return '\n'.join(lines)
    
    lines.append(f"[{info.term}]")
    
    if info.category:
        lines.append(f"  Category: {info.category}")
    
    if info.broader_terms:
        lines.append(f"  Broader Terms: {'; '.join(info.broader_terms)}")
    
    if info.narrower_terms:
        lines.append(f"  Narrower Terms: {'; '.join(info.narrower_terms)}")
    
    if info.related_terms:
        lines.append(f"  Related Terms ({len(info.related_terms)}):")
        for rt in info.related_terms[:10]:
            lines.append(f"    - {rt}")
        if len(info.related_terms) > 10:
            lines.append(f"    ... and {len(info.related_terms) - 10} more")
    
    if info.used_for:
        lines.append(f"  Former Terms: {'; '.join(info.used_for)}")
    
    return '\n'.join(lines)


def build_search_query_with_related(term: str, include_related: bool = True) -> str:
    """
    シソーラス用語とその関連語を含む検索クエリを構築する。
    
    Args:
        term: 基本となるシソーラス用語
        include_related: 関連語を含めるか
    
    Returns:
        str: ERIC検索クエリ
    
    Example:
        >>> query = build_search_query_with_related("Medical School Faculty")
        >>> print(query)
        'subject:"Medical School Faculty" OR subject:"Graduate School Faculty" OR ...'
    """
    info = get_thesaurus_info(term)
    
    if not info.exists:
        return f'subject:"{term}"'
    
    terms = [info.term]
    
    if include_related and info.related_terms:
        # 最大10個の関連語を追加
        terms.extend(info.related_terms[:10])
    
    query_parts = [f'subject:"{t}"' for t in terms]
    return ' OR '.join(query_parts)


if __name__ == "__main__":
    # テスト実行
    if not HAS_BS4:
        print("Error: beautifulsoup4 is required.")
        print("Install with: pip install beautifulsoup4")
        exit(1)
    
    print("=== ERIC Thesaurus Scraper Test ===\n")
    
    test_terms = [
        "Medical School Faculty",
        "Faculty Development",
        "Nonexistent Term XYZ123"
    ]
    
    for term in test_terms:
        print(f"Looking up: {term}")
        info = get_thesaurus_info(term)
        print(format_thesaurus_info(info))
        print()
        time.sleep(1)  # Rate limiting
