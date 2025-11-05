#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOIまたはタイトルからPMIDを検索するスクリプト

使用方法:
    python scripts/utils/find_pmid_from_doi.py --doi "10.1177/1069072711436160"
    python scripts/utils/find_pmid_from_doi.py --title "Measuring Meaningful Work"
    python scripts/utils/find_pmid_from_doi.py --author "Steger MF" --title "meaningful work"
"""

import requests
import time
import argparse
import sys
from typing import Optional, Dict, List

# Windows環境での文字化け対策
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def search_by_doi(doi: str) -> Optional[str]:
    """DOIからPMIDを検索"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    # DOIの正規化（https://doi.org/ を除去）
    clean_doi = doi.replace("https://doi.org/", "").replace("http://doi.org/", "")

    params = {
        "db": "pubmed",
        "term": f"{clean_doi}[DOI]",
        "retmode": "json",
        "retmax": 1
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        id_list = data.get("esearchresult", {}).get("idlist", [])
        if id_list:
            return id_list[0]
        return None
    except Exception as e:
        print(f"Error searching by DOI: {e}")
        return None

def search_by_title_author(title: Optional[str] = None, author: Optional[str] = None, year: Optional[str] = None) -> List[Dict]:
    """タイトルと著者からPMIDを検索"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    # 検索クエリの構築
    query_parts = []
    if title:
        query_parts.append(f'({title}[Title])')
    if author:
        query_parts.append(f'({author}[Author])')
    if year:
        query_parts.append(f'({year}[Publication Date])')

    if not query_parts:
        return []

    query = " AND ".join(query_parts)

    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 5  # 上位5件を取得
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        id_list = data.get("esearchresult", {}).get("idlist", [])
        if not id_list:
            return []

        # PMIDの詳細情報を取得
        time.sleep(0.34)  # API rate limit
        return get_paper_details(id_list)
    except Exception as e:
        print(f"Error searching by title/author: {e}")
        return []

def get_paper_details(pmids: List[str]) -> List[Dict]:
    """PMIDから論文の詳細情報を取得"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "json"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        results = []
        for pmid in pmids:
            if pmid in data.get("result", {}):
                paper = data["result"][pmid]
                results.append({
                    "pmid": pmid,
                    "title": paper.get("title", ""),
                    "authors": ", ".join([a.get("name", "") for a in paper.get("authors", [])[:3]]),
                    "journal": paper.get("fulljournalname", paper.get("source", "")),
                    "year": paper.get("pubdate", "").split()[0] if paper.get("pubdate") else "",
                    "doi": paper.get("elocationid", "").replace("doi: ", "") if "doi:" in paper.get("elocationid", "") else ""
                })
        return results
    except Exception as e:
        print(f"Error getting paper details: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="DOIまたはタイトル/著者からPMIDを検索")
    parser.add_argument("--doi", help="DOI (例: 10.1177/1069072711436160)")
    parser.add_argument("--title", help="論文タイトル (部分一致可)")
    parser.add_argument("--author", help="著者名 (例: Steger MF)")
    parser.add_argument("--year", help="出版年 (例: 2012)")

    args = parser.parse_args()

    if not any([args.doi, args.title, args.author]):
        parser.error("--doi, --title, --author のいずれかを指定してください")

    # DOI検索を優先
    if args.doi:
        print(f"\nDOIで検索中: {args.doi}")
        pmid = search_by_doi(args.doi)
        if pmid:
            print(f"✓ PMID見つかりました: {pmid}")
            # 詳細情報を取得
            time.sleep(0.34)
            details = get_paper_details([pmid])
            if details:
                paper = details[0]
                print(f"\nタイトル: {paper['title']}")
                print(f"著者: {paper['authors']} et al.")
                print(f"ジャーナル: {paper['journal']}")
                print(f"年: {paper['year']}")
                if paper['doi']:
                    print(f"DOI: {paper['doi']}")
        else:
            print("✗ PMIDが見つかりませんでした")
            print("  → PubMedに索引されていない可能性があります")

    # タイトル/著者検索
    elif args.title or args.author:
        print(f"\n検索中...")
        if args.title:
            print(f"  タイトル: {args.title}")
        if args.author:
            print(f"  著者: {args.author}")
        if args.year:
            print(f"  年: {args.year}")

        results = search_by_title_author(args.title, args.author, args.year)

        if results:
            print(f"\n{len(results)}件の論文が見つかりました:\n")
            for i, paper in enumerate(results, 1):
                print(f"{i}. PMID: {paper['pmid']}")
                print(f"   タイトル: {paper['title']}")
                print(f"   著者: {paper['authors']}")
                print(f"   ジャーナル: {paper['journal']} ({paper['year']})")
                if paper['doi']:
                    print(f"   DOI: {paper['doi']}")
                print()
        else:
            print("\n✗ 該当する論文が見つかりませんでした")
            print("  → PubMedに索引されていない可能性があります")
            print("  → タイトルや著者名を変更して再検索してください")

if __name__ == "__main__":
    main()
