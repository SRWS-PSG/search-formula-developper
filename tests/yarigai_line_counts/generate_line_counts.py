#!/usr/bin/env python3
"""
キーワード単位でPubMed件数を取得し、Markdownレポートとして出力するユーティリティ。
過去5年フィルター（2020/01/01以降）と動物除外を適用し、#1（医師条件）とANDした件数を算出する。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Callable, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.search.validation.recount_with_5years import RecountAnalyzer

FORMULA_PATH = Path("search_formula/yarigai_scoping_review/search_formula.md")
OUTPUT_PATH = Path("tests/yarigai_line_counts/line_counts.md")

# 過去5年 + 動物除外フィルター（recount_with_5years.py と揃える）
FILTER_5Y = '("2020/01/01"[PDAT] : "3000"[PDAT]) NOT (animals[Mesh] NOT humans[Mesh])'


def parse_line_queries(
    markdown_path: Path,
) -> List[Tuple[str, str, str, List[str]]]:
    """
    Markdown内の`#### #<ID>`ブロックに続くコードブロックから検索クエリを抽出する。
    返り値は (行ID, 見出し説明, クエリ文字列, 元の行リスト) のリスト。
    """
    entries: List[Tuple[str, str, str, List[str]]] = []
    current_label: str | None = None
    current_title: str = ""
    collecting = False
    buffer: List[str] = []

    lines = markdown_path.read_text(encoding="utf-8").splitlines()

    for raw_line in lines:
        line = raw_line.rstrip()

        if line.startswith("```"):
            if collecting and current_label:
                raw_lines = [part.strip() for part in buffer if part.strip()]
                query = " ".join(raw_lines)
                entries.append((current_label, current_title, query, raw_lines))
                buffer.clear()
                collecting = False
                current_label = None
            else:
                collecting = True
            continue

        if collecting:
            buffer.append(line)
            continue

        match = re.match(r"^####\s+(#\d+[A-Z]?)\s*(.*)$", line)
        if match:
            current_label = match.group(1).lstrip("#")
            current_title = match.group(2).strip()
            continue

    return entries


def build_query_resolver(
    entries: List[Tuple[str, str, str, List[str]]]
) -> Tuple[Callable[[str], str], Dict[str, str], Dict[str, str]]:
    """
    エントリから辞書を構築し、#参照を再帰的に解決できるようにする。
    """
    raw_queries: Dict[str, str] = {}
    titles: Dict[str, str] = {}

    for label, title, query, _ in entries:
        key = label.upper()
        raw_queries[key] = query
        titles[key] = title

    cache: Dict[str, str] = {}

    def resolve(label: str, stack: Tuple[str, ...] = ()) -> str:
        key = label.upper()
        if key in cache:
            return cache[key]
        if key in stack:
            raise ValueError(f"Circular reference detected: {' -> '.join(stack + (key,))}")
        if key not in raw_queries:
            raise KeyError(f"Label #{label} not found in search_formula.md")

        raw = raw_queries[key]

        def repl(match: re.Match[str]) -> str:
            inner = match.group(1).upper()
            return f"({resolve(inner, stack + (key,))})"

        resolved = re.sub(r"#([0-9]+[A-Z]?)", repl, raw)
        cache[key] = resolved
        return resolved

    return resolve, titles, raw_queries


def split_top_level_or(query: str) -> List[str]:
    """
    最上位のORでクエリを分割する。
    括弧や引用符内のORは分割対象外。
    """
    terms: List[str] = []
    depth = 0
    current: List[str] = []
    i = 0
    length = len(query)

    while i < length:
        c = query[i]

        if c == '"':
            current.append(c)
            i += 1
            while i < length:
                current.append(query[i])
                if query[i] == '"' and query[i - 1] != "\\":
                    i += 1
                    break
                i += 1
            continue

        if c == "(":
            depth += 1
        elif c == ")":
            if depth > 0:
                depth -= 1

        if depth == 0 and query.startswith(" OR ", i):
            term = "".join(current).strip()
            if term:
                terms.append(term)
            current = []
            i += 4
            continue

        current.append(c)
        i += 1

    if current:
        term = "".join(current).strip()
        if term:
            terms.append(term)

    return terms


def sanitize_term(term: str) -> str:
    """余計な外側括弧をすっきりさせる。"""
    trimmed = term.strip()
    if trimmed.startswith("(") and trimmed.endswith(")"):
        inner = trimmed[1:-1].strip()
        if inner.count("(") == inner.count(")"):
            return inner
    return trimmed


def main() -> None:
    entries = parse_line_queries(FORMULA_PATH)
    resolve, titles, raw_queries = build_query_resolver(entries)
    analyzer = RecountAnalyzer()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    ordered_labels = [
        "1",
        "2A", "2B", "2C", "2D", "2E", "2F", "2G", "2H", "2I", "2J",
        "3", "4",
    ]

    population_query = resolve("1")

    tables: List[str] = []

    for label in ordered_labels:
        key = label.upper()
        if key not in titles:
            continue

        raw_query = raw_queries[key]
        term_candidates = split_top_level_or(raw_query)

        # ORで分割できなかった場合はそのまま1タームとして扱う
        if not term_candidates:
            term_candidates = [raw_query]

        # 他のブロック参照のみの行は除外 (#2 など)
        terms = [
            sanitize_term(term)
            for term in term_candidates
            if "#" not in term
        ]

        if not terms:
            continue

        header = f"## #{label} {titles[key]}"
        lines = [header, ""]
        lines.append("| キーワード | 実行クエリ | 件数 (5y) |")
        lines.append("|-------------|------------|-----------|")

        for term in terms:
            if label == "1":
                full_query = f"({term}) AND {FILTER_5Y}"
            else:
                full_query = f"({population_query}) AND {FILTER_5Y} AND ({term})"

            count = analyzer.get_count(full_query)
            lines.append(f"| `{term}` | `{full_query}` | {count:,} |")

        tables.append("\n".join(lines))

    doc_lines: List[str] = []
    doc_lines.append("# キーワード別検索件数（過去5年フィルター適用）")
    doc_lines.append("")
    doc_lines.append(f"- 対象ファイル: `{FORMULA_PATH.as_posix()}`")
    doc_lines.append(f"- フィルター: `{FILTER_5Y}`")
    doc_lines.append("- 集計方法: `#1`（医師条件）とANDし、各キーワードを個別にPubMedで再検索")
    doc_lines.append("")
    doc_lines.extend(tables)

    OUTPUT_PATH.write_text("\n\n".join(doc_lines), encoding="utf-8")
    print(f"キーワード別件数を {OUTPUT_PATH} に保存しました。")


if __name__ == "__main__":
    main()
