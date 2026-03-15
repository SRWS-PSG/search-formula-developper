#!/usr/bin/env python3
"""
Anthropological Index Online (AIO) Client

AIO (https://aio.therai.org.uk/) への検索機能を提供する。
CSRF トークン管理とセッション維持を行う。

Usage:
    from aio_client import AIOClient
    
    client = AIOClient()
    results_id = client.quick_search("autoethnography")
    ris_data = client.download_results(results_id, mimetype="ris")
"""

import requests
from bs4 import BeautifulSoup
import re
import time
from typing import Optional, List, Tuple
from urllib.parse import urljoin

BASE_URL = "https://aio.therai.org.uk/"

# Rate limiting (respect free tier: ~100 searches/year)
DEFAULT_DELAY_SEC = 2.0


class AIOClient:
    """Anthropological Index Online クライアント"""
    
    def __init__(self, delay_sec: float = DEFAULT_DELAY_SEC):
        """
        Args:
            delay_sec: リクエスト間の待機時間（秒）
        """
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "AIO-Research-Client/1.0 (Academic Research)"
        })
        self.delay_sec = delay_sec
        self._last_request_time = 0.0
    
    def _wait_for_rate_limit(self):
        """レート制限のための待機"""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.delay_sec:
            time.sleep(self.delay_sec - elapsed)
        self._last_request_time = time.time()
    
    def _get_csrf_token(self, path: str) -> str:
        """
        指定パスからCSRFトークンを取得
        
        Args:
            path: 取得元パス（例: "/quick-search"）
            
        Returns:
            CSRFトークン文字列
        """
        self._wait_for_rate_limit()
        url = urljoin(BASE_URL, path)
        response = self.session.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        token_input = soup.find("input", {"name": "_token"})
        
        if not token_input or not token_input.get("value"):
            raise ValueError(f"CSRF token not found at {url}")
        
        return token_input["value"]
    
    def quick_search(
        self,
        keyword: str,
        decades: List[str] = None,
        results_mode: str = "bib",
        sort: str = "year_d",
        filter_type: str = "*"
    ) -> str:
        """
        Quick Search を実行
        
        Args:
            keyword: 検索キーワード
            decades: 年代フィルタ（例: ["recent", "all"]）
            results_mode: 結果表示モード（bib/full/fullkeywords）
            sort: ソート順（year_d/year_a/title_a/title_d）
            filter_type: フィルタ（*/Article/Film）
            
        Returns:
            検索結果ID
        """
        if decades is None:
            decades = ["all"]
        
        # CSRFトークン取得
        token = self._get_csrf_token("/quick-search")
        
        # 検索実行
        self._wait_for_rate_limit()
        data = {
            "_token": token,
            "qs_keyword": keyword,
            "qs_decades[]": decades,
            "qs_resultsmode": results_mode,
            "qs_sort": sort,
            "qs_filter": filter_type
        }
        
        response = self.session.post(
            urljoin(BASE_URL, "/quick-search"),
            data=data,
            allow_redirects=False
        )
        
        # リダイレクトURLから results_id を抽出
        if response.status_code in (301, 302, 303):
            location = response.headers.get("Location", "")
            # 形式: /quick-search/<results_id>/<mode>
            match = re.search(r"/quick-search/([^/]+)/", location)
            if match:
                return match.group(1)
        
        # リダイレクトがない場合はレスポンスから抽出を試みる
        response.raise_for_status()
        
        # URLから抽出
        if "/quick-search/" in response.url:
            match = re.search(r"/quick-search/([^/]+)/", response.url)
            if match:
                return match.group(1)
        
        raise ValueError(f"Could not extract results_id from response. URL: {response.url}")
    
    def download_results(
        self,
        results_id: str,
        mimetype: str = "ris",
        charset: str = "UTF-8"
    ) -> str:
        """
        検索結果をダウンロード
        
        Args:
            results_id: 検索結果ID（quick_searchの戻り値）
            mimetype: 出力形式（ris/csv/html/endnote）
            charset: 文字コード（UTF-8/Latin1/ASCII/DEFAULT）
            
        Returns:
            ダウンロードしたデータ（文字列）
        """
        self._wait_for_rate_limit()
        
        params = {
            "action": "downloadresults",
            "resultsid": results_id,
            "mimetype": mimetype,
            "charset": charset
        }
        
        url = urljoin(BASE_URL, f"/results/{results_id}/download")
        response = self.session.get(url, params=params)
        response.raise_for_status()
        
        return response.text
    
    def get_result_count_from_ris(self, ris_data: str) -> int:
        """
        RISデータから件数を取得
        
        Args:
            ris_data: RIS形式のデータ
            
        Returns:
            レコード件数
        """
        return ris_data.count("TY  -")


def get_aio_search_count(keyword: str) -> int:
    """
    キーワードで検索し件数を返す（便利関数）
    
    Args:
        keyword: 検索キーワード
        
    Returns:
        検索結果件数
    """
    client = AIOClient()
    results_id = client.quick_search(keyword)
    ris_data = client.download_results(results_id)
    return client.get_result_count_from_ris(ris_data)


if __name__ == "__main__":
    # テスト実行
    print("AIO Client - Test")
    print("=" * 50)
    
    keyword = "autoethnography"
    print(f"Searching for: {keyword}")
    
    try:
        count = get_aio_search_count(keyword)
        print(f"Results: {count} records")
    except Exception as e:
        print(f"Error: {e}")
