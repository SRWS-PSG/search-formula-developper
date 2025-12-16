#!/usr/bin/env python3
"""
統合レポート内の各検索語をPubMed検索結果へのリンクに変換する。

使用前提:
    tests/yarigai_comprehensive_line_counts_20251110.md が最新。

実行方法:
    python3 tests/add_pubmed_links.py
"""

import urllib.parse

REPORT_PATH = "tests/yarigai_comprehensive_line_counts_20251110.md"
POPULATION = '("Physicians"[Mesh] OR physician*[tiab])'


def term_to_query(term: str) -> str:
    """テーブル表示中の検索語から実際のPubMedクエリを再構築する。"""
    term = term.strip()
    if term.startswith("#1 AND "):
        concept = term[len("#1 AND ") :].strip()
        return f"({POPULATION} AND {concept})"
    return term


def to_pubmed_url(query: str) -> str:
    encoded = urllib.parse.quote(query, safe="()[]\"*+ ")
    # replace spaces with +
    encoded = encoded.replace(" ", "+")
    return f"https://pubmed.ncbi.nlm.nih.gov/?term={encoded}"


def process_line(line: str) -> str:
    """データ行を検出し、必要ならリンク付き表示に変換する。"""
    if not line.startswith("|"):
        return line

    parts = line.split("|")
    if len(parts) < 4:
        return line

    line_no = parts[1].strip()
    if not line_no.isdigit():
        return line

    term_cell = parts[2]
    term_text = term_cell.strip()
    if term_text.startswith("[`") and "](" in term_text:
        return line

    if term_text.startswith("`") and term_text.endswith("`"):
        inner = term_text[1:-1]
    else:
        inner = term_text

    query = term_to_query(inner)
    url = to_pubmed_url(query)
    linked = f' [`{inner}`]({url}) '
    parts[2] = linked
    return "|".join(parts)


def main():
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated = [process_line(line) for line in lines]

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.writelines(updated)

    print("✓ PubMedリンクを挿入しました:", REPORT_PATH)


if __name__ == "__main__":
    main()
