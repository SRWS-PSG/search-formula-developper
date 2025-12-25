#!/usr/bin/env python3
"""
ERIC API Client Module

ERIC (Education Resources Information Center) APIを使用して
教育研究データベースの検索を行うモジュール。

API Endpoint: https://api.ies.ed.gov/eric/
Documentation: https://eric.ed.gov/?api

Usage:
    from scripts.search.eric.eric_api import search_eric, get_eric_record_count
    
    # 基本検索
    results = search_eric("medical education")
    
    # シソーラス検索
    results = search_eric('subject:"Medical School Faculty"')
"""

import requests
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


# ERIC API Configuration
ERIC_API_BASE_URL = "https://api.ies.ed.gov/eric/"
DEFAULT_ROWS = 20
MAX_ROWS = 2000
DEFAULT_FORMAT = "json"


@dataclass
class ERICSearchResult:
    """ERIC検索結果を格納するデータクラス"""
    total_count: int
    start: int
    rows: int
    records: List[Dict[str, Any]]
    query: str
    message: str = "Success"


# ============================================================
# ERIC Search Fields (from ERIC FAQ)
# ============================================================
ERIC_FIELDS = {
    "abstract": "abstract",
    "assessment": "assessment",
    "audience": "audience",
    "author": "author",
    "descriptor": "descriptor",      # シソーラス (subject と同義)
    "subject": "subject",            # シソーラス (descriptor と同義)
    "educationlevel": "educationlevel",
    "e_yearadded": "e_yearadded",
    "iesgrantcontractnum": "iesgrantcontractnum",
    "institution": "institution",
    "language": "language",
    "law": "law",
    "location": "location",
    "publicationtype": "publicationtype",
    "pubyear": "pubyear",
    "publicationdateyear": "publicationdateyear",
    "source": "source",
    "sponsor": "sponsor",
    "title": "title",
    "id": "id",                      # ERIC ID (EJ/ED番号)
    "peerreviewed": "peerreviewed",  # T/F
}

# Exact match fields (case-sensitive)
ERIC_EXACT_FIELDS = {
    "descriptorx": "descriptorx",
    "sourcex": "sourcex",
    "locationx": "locationx",
    "lawx": "lawx",
    "assessmentx": "assessmentx",
}

# ERIC Filters (must be combined with other search terms)
ERIC_FILTERS = {
    "pubyearmin": "pubyearmin",
    "pubyearmax": "pubyearmax",
}

# IES/WWC Options
ERIC_IES_OPTIONS = {
    "ies_funded": "funded:y",
    "wwc_meets_standards": "wwcr:y",           # Meets Evidence Standards without Reservations
    "wwc_meets_with_reservations": "wwcr:r",   # Meets Evidence Standards with Reservations
    "wwc_does_not_meet": "wwcr:n",             # Does Not Meet Evidence Standards
}


class ERICQueryBuilder:
    """
    ERIC検索クエリを構築するビルダークラス
    
    Example:
        >>> builder = ERICQueryBuilder()
        >>> query = (builder
        ...     .add_term("faculty development", field="title")
        ...     .add_descriptor("Medical School Faculty")
        ...     .peer_reviewed_only()
        ...     .set_date_range(min_year=2020)
        ...     .build())
        >>> print(query)
        'title:"faculty development" AND subject:"Medical School Faculty" AND peerreviewed:T pubyearmin:2020'
    """
    
    def __init__(self):
        self._terms: List[str] = []
        self._filters: Dict[str, str] = {}
        self._peer_reviewed: bool = False
        self._fulltext_only: bool = False
        self._ies_funded: bool = False
        self._wwc_reviewed: Optional[str] = None
    
    def add_term(self, term: str, field: Optional[str] = None, 
                 required: bool = False, excluded: bool = False) -> 'ERICQueryBuilder':
        """
        検索語を追加
        
        Args:
            term: 検索語
            field: フィールド名 (title, abstract, author等)
            required: +演算子を使用するか
            excluded: -演算子を使用するか
        """
        if field:
            # フレーズ検索の場合はダブルクォートで囲む
            if ' ' in term and not term.startswith('"'):
                term_str = f'{field}:"{term}"'
            else:
                term_str = f'{field}:{term}'
        else:
            if ' ' in term and not term.startswith('"'):
                term_str = f'"{term}"'
            else:
                term_str = term
        
        if required:
            term_str = f'+{term_str}'
        elif excluded:
            term_str = f'-{term_str}'
        
        self._terms.append(term_str)
        return self
    
    def add_descriptor(self, descriptor: str, exact: bool = False) -> 'ERICQueryBuilder':
        """
        シソーラス用語(Descriptor)を追加
        
        Args:
            descriptor: シソーラス用語
            exact: 大文字小文字を区別する場合True
        """
        field = "descriptorx" if exact else "subject"
        self._terms.append(f'{field}:"{descriptor}"')
        return self
    
    def add_or_group(self, terms: List[str], field: Optional[str] = None) -> 'ERICQueryBuilder':
        """
        OR条件でグループ化した検索語を追加
        
        Args:
            terms: 検索語リスト
            field: フィールド名
        """
        if field:
            parts = [f'{field}:"{t}"' for t in terms]
        else:
            parts = [f'"{t}"' if ' ' in t else t for t in terms]
        
        group = f'({" OR ".join(parts)})'
        self._terms.append(group)
        return self
    
    def set_date_range(self, min_year: Optional[int] = None, 
                       max_year: Optional[int] = None) -> 'ERICQueryBuilder':
        """
        年代範囲を設定
        
        Args:
            min_year: 最小出版年
            max_year: 最大出版年
        
        Note:
            publicationdateyear:[min TO max] 構文を使用します。
            pubyearmin/pubyearmax はAPI経由では動作しない場合があります。
        """
        if min_year or max_year:
            min_val = str(min_year) if min_year else '*'
            max_val = str(max_year) if max_year else '*'
            self._filters['date_range'] = f'publicationdateyear:[{min_val} TO {max_val}]'
        return self
    
    def peer_reviewed_only(self) -> 'ERICQueryBuilder':
        """Peer-reviewedのみに制限"""
        self._peer_reviewed = True
        return self
    
    def fulltext_only(self) -> 'ERICQueryBuilder':
        """フルテキスト利用可能のみに制限"""
        self._fulltext_only = True
        return self
    
    def ies_funded_only(self) -> 'ERICQueryBuilder':
        """IES助成研究のみに制限"""
        self._ies_funded = True
        return self
    
    def wwc_reviewed(self, level: str = "y") -> 'ERICQueryBuilder':
        """
        WWCレビュー済みのみに制限
        
        Args:
            level: "y" (Meets Standards), "r" (With Reservations), "n" (Does Not Meet)
        """
        if level in ["y", "r", "n"]:
            self._wwc_reviewed = level
        return self
    
    def build(self) -> str:
        """クエリ文字列を構築"""
        parts = []
        
        # メイン検索語をANDで結合
        if self._terms:
            if len(self._terms) == 1:
                parts.append(self._terms[0])
            else:
                parts.append(' AND '.join(self._terms))
        
        # Peer-reviewed フィルター
        if self._peer_reviewed:
            parts.append('peerreviewed:T')
        
        # フルテキスト フィルター
        if self._fulltext_only:
            parts.append('e_fulltextauth:T')
        
        # IES Funded フィルター
        if self._ies_funded:
            parts.append('funded:y')
        
        # WWC Reviewed フィルター
        if self._wwc_reviewed:
            parts.append(f'wwcr:{self._wwc_reviewed}')
        
        # クエリ部分を結合
        query = ' AND '.join(parts) if len(parts) > 1 else (parts[0] if parts else '')
        
        # フィルターを追加
        filter_parts = []
        for k, v in self._filters.items():
            if k == 'date_range':
                # date_range はそのまま追加
                filter_parts.append(v)
            else:
                filter_parts.append(f'{k}:{v}')
        
        if filter_parts:
            if query:
                query = f'{query} AND {" AND ".join(filter_parts)}'
            else:
                query = ' AND '.join(filter_parts)
        
        return query
    
    def reset(self) -> 'ERICQueryBuilder':
        """ビルダーをリセット"""
        self._terms = []
        self._filters = {}
        self._peer_reviewed = False
        self._fulltext_only = False
        self._ies_funded = False
        self._wwc_reviewed = None
        return self


def search_eric(
    query: str,
    format: str = DEFAULT_FORMAT,
    start: int = 0,
    rows: int = DEFAULT_ROWS,
    fields: Optional[List[str]] = None,
    retry_count: int = 3
) -> ERICSearchResult:
    """
    ERIC APIを使用して検索を実行する。
    
    Args:
        query: 検索クエリ
            - フリーワード検索: "medical education"
            - フィールド指定: title:"faculty development"
            - シソーラス検索: subject:"Medical School Faculty"
            - 複合検索: subject:"Medical School Faculty" AND burnout
            - peer-reviewed: peerreviewed:T
        format: レスポンス形式 (json/xml/csv)
        start: 開始レコード番号 (ページネーション用)
        rows: 取得件数 (1-2000)
        fields: 取得フィールドのリスト (省略時は頻出フィールドすべて)
        retry_count: リトライ回数
    
    Returns:
        ERICSearchResult: 検索結果
    
    Example:
        >>> result = search_eric("medical education", rows=10)
        >>> print(f"Total: {result.total_count} records")
        >>> for rec in result.records:
        ...     print(rec.get('title'))
    """
    # Validate rows parameter
    if rows < 1:
        rows = 1
    elif rows > MAX_ROWS:
        rows = MAX_ROWS
    
    # Build request parameters
    params = {
        'search': query,
        'format': format,
        'start': start,
        'rows': rows
    }
    
    if fields:
        params['fields'] = ','.join(fields)
    
    # Execute request with retry
    last_error = None
    for attempt in range(retry_count):
        try:
            response = requests.get(ERIC_API_BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            
            if format == 'json':
                data = response.json()
                return _parse_json_response(data, query)
            else:
                # XML/CSV形式の場合は生データを返す
                return ERICSearchResult(
                    total_count=0,
                    start=start,
                    rows=rows,
                    records=[{'raw_response': response.text}],
                    query=query,
                    message=f"Raw {format.upper()} response returned"
                )
                
        except requests.exceptions.RequestException as e:
            last_error = e
            if attempt < retry_count - 1:
                time.sleep(1)  # Wait before retry
                continue
    
    # All retries failed
    return ERICSearchResult(
        total_count=0,
        start=start,
        rows=rows,
        records=[],
        query=query,
        message=f"Error: {str(last_error)}"
    )


def _parse_json_response(data: Dict, query: str) -> ERICSearchResult:
    """
    ERIC JSON レスポンスをパースする。
    """
    response_data = data.get('response', {})
    
    total_count = response_data.get('numFound', 0)
    start = response_data.get('start', 0)
    docs = response_data.get('docs', [])
    
    return ERICSearchResult(
        total_count=total_count,
        start=start,
        rows=len(docs),
        records=docs,
        query=query
    )


def get_eric_record_count(query: str) -> int:
    """
    指定したクエリの検索結果件数のみを取得する。
    
    Args:
        query: 検索クエリ
    
    Returns:
        int: 検索結果件数
    """
    result = search_eric(query, rows=0)
    return result.total_count


def check_eric_id_in_query(eric_id: str, query: str) -> bool:
    """
    指定したERIC IDが検索クエリの結果に含まれているか確認する。
    
    Args:
        eric_id: ERIC ID (例: "EJ1234567", "ED7654321")
        query: 検索クエリ
    
    Returns:
        bool: 含まれている場合True
    """
    # ERIC ID を使った絞り込み検索
    check_query = f'({query}) AND id:{eric_id}'
    result = search_eric(check_query, rows=1)
    return result.total_count > 0


def export_results_to_ris(
    records: List[Dict[str, Any]],
    output_path: str
) -> None:
    """
    ERIC検索結果をRIS形式でエクスポートする。
    
    Args:
        records: ERIC検索結果レコードのリスト
        output_path: 出力ファイルパス
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for rec in records:
            # TY - Type
            f.write("TY  - JOUR\n")
            
            # ID - ERIC Number
            if rec.get('id'):
                f.write(f"ID  - {rec['id']}\n")
            
            # TI - Title
            if rec.get('title'):
                f.write(f"TI  - {rec['title']}\n")
            
            # AU - Authors
            authors = rec.get('author', [])
            if isinstance(authors, list):
                for author in authors:
                    f.write(f"AU  - {author}\n")
            elif authors:
                f.write(f"AU  - {authors}\n")
            
            # AB - Abstract
            if rec.get('description'):
                f.write(f"AB  - {rec['description']}\n")
            
            # PY - Publication Year
            if rec.get('publicationdateyear'):
                f.write(f"PY  - {rec['publicationdateyear']}\n")
            
            # JF - Journal/Source
            if rec.get('source'):
                f.write(f"JF  - {rec['source']}\n")
            
            # KW - Keywords (Subjects/Descriptors)
            subjects = rec.get('subject', [])
            if isinstance(subjects, list):
                for subj in subjects:
                    f.write(f"KW  - {subj}\n")
            elif subjects:
                f.write(f"KW  - {subjects}\n")
            
            # SN - ISSN
            if rec.get('issn'):
                f.write(f"SN  - {rec['issn']}\n")
            
            # UR - URL
            if rec.get('url'):
                f.write(f"UR  - {rec['url']}\n")
            
            # End of record
            f.write("ER  -\n\n")


def format_record_for_display(record: Dict[str, Any]) -> str:
    """
    ERIC レコードを表示用にフォーマットする。
    
    Args:
        record: ERIC レコード
    
    Returns:
        str: フォーマットされた文字列
    """
    lines = []
    
    # ID and Title
    eric_id = record.get('id', 'N/A')
    title = record.get('title', 'N/A')
    lines.append(f"[{eric_id}] {title}")
    
    # Authors
    authors = record.get('author', [])
    if authors:
        if isinstance(authors, list):
            lines.append(f"  Authors: {'; '.join(authors)}")
        else:
            lines.append(f"  Authors: {authors}")
    
    # Source and Year
    source = record.get('source', '')
    year = record.get('publicationdateyear', '')
    if source or year:
        lines.append(f"  Source: {source} ({year})")
    
    # Peer Reviewed
    peer_reviewed = record.get('peerreviewed', 'F')
    if peer_reviewed == 'T':
        lines.append("  [Peer Reviewed]")
    
    # Subjects (Thesaurus terms)
    subjects = record.get('subject', [])
    if subjects:
        if isinstance(subjects, list):
            lines.append(f"  Descriptors: {'; '.join(subjects[:5])}")
            if len(subjects) > 5:
                lines.append(f"    ... and {len(subjects) - 5} more")
        else:
            lines.append(f"  Descriptors: {subjects}")
    
    return '\n'.join(lines)


# ============================================================
# Convenience Search Functions
# ============================================================

def search_eric_peer_reviewed(
    query: str,
    rows: int = DEFAULT_ROWS,
    start: int = 0,
    **kwargs
) -> ERICSearchResult:
    """
    Peer-reviewed論文のみを検索
    
    Args:
        query: 検索クエリ
        rows: 取得件数
        start: 開始位置
        **kwargs: search_ericに渡す追加引数
    
    Returns:
        ERICSearchResult: 検索結果
    """
    full_query = f'({query}) AND peerreviewed:T'
    return search_eric(full_query, rows=rows, start=start, **kwargs)


def search_eric_with_date_range(
    query: str,
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    rows: int = DEFAULT_ROWS,
    start: int = 0,
    **kwargs
) -> ERICSearchResult:
    """
    年代範囲を指定して検索
    
    Args:
        query: 検索クエリ
        min_year: 最小出版年
        max_year: 最大出版年
        rows: 取得件数
        start: 開始位置
        **kwargs: search_ericに渡す追加引数
    
    Returns:
        ERICSearchResult: 検索結果
    
    Note:
        publicationdateyear:[min TO max] 構文を使用します。
    """
    if min_year or max_year:
        min_val = str(min_year) if min_year else '*'
        max_val = str(max_year) if max_year else '*'
        date_filter = f'publicationdateyear:[{min_val} TO {max_val}]'
        full_query = f'({query}) AND {date_filter}'
    else:
        full_query = query
    
    return search_eric(full_query, rows=rows, start=start, **kwargs)


def search_eric_fulltext(
    query: str,
    rows: int = DEFAULT_ROWS,
    start: int = 0,
    **kwargs
) -> ERICSearchResult:
    """
    フルテキスト利用可能な論文のみを検索
    
    Args:
        query: 検索クエリ
        rows: 取得件数
        start: 開始位置
        **kwargs: search_ericに渡す追加引数
    
    Returns:
        ERICSearchResult: 検索結果
    """
    full_query = f'({query}) AND e_fulltextauth:T'
    return search_eric(full_query, rows=rows, start=start, **kwargs)


def search_eric_ies_funded(
    query: str,
    rows: int = DEFAULT_ROWS,
    start: int = 0,
    **kwargs
) -> ERICSearchResult:
    """
    IES助成研究のみを検索
    
    Args:
        query: 検索クエリ
        rows: 取得件数
        start: 開始位置
        **kwargs: search_ericに渡す追加引数
    
    Returns:
        ERICSearchResult: 検索結果
    """
    full_query = f'({query}) AND funded:y'
    return search_eric(full_query, rows=rows, start=start, **kwargs)


def search_eric_wwc_reviewed(
    query: str,
    level: str = "y",
    rows: int = DEFAULT_ROWS,
    start: int = 0,
    **kwargs
) -> ERICSearchResult:
    """
    WWC (What Works Clearinghouse) レビュー済み研究のみを検索
    
    Args:
        query: 検索クエリ
        level: レビューレベル
            - "y": Meets Evidence Standards without Reservations
            - "r": Meets Evidence Standards with Reservations
            - "n": Does Not Meet Evidence Standards
        rows: 取得件数
        start: 開始位置
        **kwargs: search_ericに渡す追加引数
    
    Returns:
        ERICSearchResult: 検索結果
    """
    if level not in ["y", "r", "n"]:
        level = "y"
    full_query = f'({query}) AND wwcr:{level}'
    return search_eric(full_query, rows=rows, start=start, **kwargs)


if __name__ == "__main__":
    # 簡単なテスト
    print("=== ERIC API Test ===\n")
    
    # 基本検索テスト
    result = search_eric("faculty development", rows=3)
    print(f"Query: {result.query}")
    print(f"Total results: {result.total_count:,}")
    print(f"Returned: {len(result.records)} records\n")
    
    for rec in result.records:
        print(format_record_for_display(rec))
        print()
