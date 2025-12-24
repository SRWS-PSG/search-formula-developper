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
