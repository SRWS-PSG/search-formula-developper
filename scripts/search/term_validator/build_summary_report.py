#!/usr/bin/env python3
"""
Generate SUMMARY_REPORT.md from block_* and analysis_* files.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


BLOCK_ID_ORDER = ["2A", "2B", "2C", "2D", "2E", "2F", "2G", "2H", "2I", "2J"]
POP_CONDITION = '"Physicians"[Mesh] OR physician*[tiab]'


@dataclass
class TermRow:
    line: int
    term_full: str
    term_label: str
    individual: Optional[int]
    cumulative: Optional[int]
    added: int


def _clean_term_label(line: str) -> str:
    line = line.strip()
    if line.endswith("OR"):
        line = line[:-2].strip()
    if ") AND " in line:
        line = line.split(") AND ", 1)[1]
    line = line.strip()
    if line.endswith(")"):
        line = line[:-1].strip()
    return line


def parse_block_file(path: Path) -> Dict:
    header_label = ""
    header_title = ""
    terms: List[str] = []
    capture = False

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("####"):
            match = re.match(r"^####\s+#?(\d+[A-Z]?)\s*(.*)$", line)
            if match:
                header_label = match.group(1)
                header_title = match.group(2)
            continue

        if line.startswith("```"):
            capture = not capture
            continue

        if not capture or not line or line in {"OR", "AND"}:
            continue

        cleaned = _clean_term_label(line)
        terms.append(cleaned)

    if not header_label:
        raise ValueError(f"Unable to detect block label in {path}")

    return {
        "label": header_label,
        "title": header_title,
        "terms": terms,
    }


def _parse_int(token: str) -> Optional[int]:
    token = token.replace(",", "").strip()
    if not token or token.upper() in {"NA", "N/A"}:
        return None
    return int(token)


def parse_analysis_file(path: Path) -> List[Dict]:
    rows: List[Dict] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    in_table = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("| Line |"):
            in_table = True
            continue
        if not in_table:
            continue
        if not stripped or stripped.startswith("###"):
            break
        if stripped.startswith("|------"):
            continue

        parts = [p.strip() for p in stripped.split("|")[1:-1]]
        if len(parts) < 6:
            continue

        line_no = int(parts[0])
        term = parts[1]
        if term.startswith("`") and term.endswith("`"):
            term = term[1:-1]
        individual = _parse_int(parts[2])
        cumulative = _parse_int(parts[3])
        added = _parse_int(parts[4].replace("*", "").replace("+", ""))

        rows.append(
            {
                "line": line_no,
                "term_full": term,
                "individual": individual,
                "cumulative": cumulative,
                "added": added or 0,
            }
        )

    if not rows:
        raise ValueError(f"Failed to parse table in {path}")

    return rows


def format_count(val: Optional[int]) -> str:
    if val is None:
        return "NA"
    return f"{val:,}"


def build_section(block_meta: Dict, analysis_rows: List[Dict]) -> Dict[str, str]:
    terms = block_meta["terms"]
    if len(terms) != len(analysis_rows):
        raise ValueError(
            f"Term count mismatch for #{block_meta['label']}: "
            f"{len(terms)} terms vs {len(analysis_rows)} rows"
        )

    rows: List[TermRow] = []
    for term_label, row in zip(terms, analysis_rows):
        rows.append(
            TermRow(
                line=row["line"],
                term_full=row["term_full"],
                term_label=term_label,
                individual=row["individual"],
                cumulative=row["cumulative"],
                added=row["added"],
            )
        )

    total = rows[-1].cumulative or 0
    table_lines = [
        "| Line | 検索語 | 個別 | 累積 | 追加 | 割合 |",
        "|------|--------|------|------|------|------|",
    ]

    for row in rows:
        pct = (row.added / total * 100) if total else 0.0
        table_lines.append(
            f"| {row.line} | `{row.term_label}` | {format_count(row.individual)} | "
            f"{format_count(row.cumulative)} | +{row.added:,} | {pct:.1f}% |"
        )

    best = max(rows, key=lambda r: r.added)
    best_pct = (best.added / total * 100) if total else 0.0
    low_eff = [r.line for r in rows if total and (r.added / total * 100) < 1.0]
    high_overlap = [
        r.line
        for r in rows
        if r.individual not in (None, 0) and r.added / r.individual < 0.2
    ]
    na_lines = [r.line for r in rows if r.individual is None]

    summary_lines = [
        f"**累積総数**: {total:,}",
        f"**最も効果的**: Line {best.line} ({best.term_label}, +{best.added:,}件, {best_pct:.1f}%)",
    ]
    if low_eff:
        summary_lines.append(f"**低効率用語** (<1%): Line {', '.join(map(str, low_eff))}")
    if high_overlap:
        summary_lines.append(f"**高重複用語** (>80%): Line {', '.join(map(str, high_overlap))}")
    if na_lines:
        summary_lines.append(f"**注**: Line {', '.join(map(str, na_lines))} の個別カウントはAPIエラーで取得不可 (NA表示)")

    section_md = [
        f"## #{block_meta['label']} {block_meta['title']}",
        "",
        "\n".join(table_lines),
        "",
        "\n".join(summary_lines),
        "",
        "---",
        "",
    ]

    return {
        "markdown": "\n".join(section_md),
        "total": total,
        "has_na": bool(na_lines),
    }


def build_overview(sections: Dict[str, Dict], order: List[str]) -> str:
    lines = [
        "## 全体サマリー",
        "",
        "### ブロック別累積総数",
        "",
        "| ブロック | 累積総数 | 信頼性 |",
        "|----------|----------|--------|",
    ]

    for label in order:
        data = sections[label]
        total = data["total"]
        if total == 0:
            badge = "❌ 低"
        elif data["has_na"]:
            badge = "⚠️ 中"
        else:
            badge = "✅ 高"
        lines.append(f"| #{label} | {total:,} | {badge} |")

    lines.append("")
    lines.append("### 備考")
    lines.append("")
    lines.append("- NA = PubMed APIエラーで個別件数が取得できなかった項目")
    lines.append("- 累積カウントはORクエリの最新値。APIエラー時は直前値を引き継ぎ")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate SUMMARY_REPORT.md from analysis files.")
    parser.add_argument("--base-dir", required=True, type=Path, help="Directory that contains block_*.txt")
    parser.add_argument("--output", required=True, type=Path, help="Summary markdown path")
    args = parser.parse_args()

    block_files = list(args.base_dir.glob("block_*.txt"))
    analysis_files = list(args.base_dir.glob("analysis_*.md"))

    block_meta_by_id: Dict[str, Dict] = {}
    for path in block_files:
        meta = parse_block_file(path)
        block_meta_by_id[meta["label"]] = meta

    analysis_by_id: Dict[str, List[Dict]] = {}
    for path in analysis_files:
        text = path.read_text(encoding="utf-8")
        match = re.search(r"--block-name\s+\"#(\d+[A-Z]?)", text)
        if not match:
            continue
        block_id = match.group(1)
        analysis_by_id[block_id] = parse_analysis_file(path)

    sections_rendered: Dict[str, Dict] = {}
    markdown_sections: List[str] = []

    for block_id in BLOCK_ID_ORDER:
        if block_id not in block_meta_by_id or block_id not in analysis_by_id:
            continue
        section = build_section(block_meta_by_id[block_id], analysis_by_id[block_id])
        sections_rendered[block_id] = section
        markdown_sections.append(section["markdown"])

    header = [
        "# 待機時間延長版（5秒） - ブロック別検索数レポート",
        "",
        f"生成日時: {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Population条件: `{POP_CONDITION}`",
        "待機時間: 各API呼び出し間5秒、ブロック間10秒",
        "",
        "---",
        "",
    ]

    overview = build_overview(sections_rendered, [k for k in BLOCK_ID_ORDER if k in sections_rendered])

    content = "\n".join(header + markdown_sections + [overview])
    args.output.write_text(content.strip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
