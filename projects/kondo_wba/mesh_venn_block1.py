"""
Block 1 (AI/LLM) MeSH用語のベン図分析
4つのMeSH用語の重複関係を可視化し、各領域の件数を確認する。

MeSH用語:
  A: "Natural Language Processing"[mh]
  B: "Generative Artificial Intelligence"[mh]
  C: "Large Language Models"[mh]
  D: Chatbot[mh]
"""

import os
import sys
import time
import json
import requests
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.colors import to_rgba
from itertools import combinations
from datetime import datetime
from typing import Any, Dict, List, Tuple

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── API config ──────────────────────────────────────────
NCBI_API_KEY = os.getenv("NCBI_API_KEY") or None
NCBI_TOOL = os.getenv("NCBI_TOOL") or None
NCBI_EMAIL = os.getenv("NCBI_EMAIL") or None

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
REQUEST_INTERVAL = 0.35 if NCBI_API_KEY else 1.1
MAX_RETRIES = 3
_last_ts = 0.0


def _rate_limit():
    global _last_ts
    elapsed = time.time() - _last_ts
    if elapsed < REQUEST_INTERVAL:
        time.sleep(REQUEST_INTERVAL - elapsed)
    _last_ts = time.time()


def get_count(query: str) -> int:
    """PubMed E-utilities APIで検索件数を取得"""
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": "0"}
    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY
    if NCBI_TOOL:
        params["tool"] = NCBI_TOOL
    if NCBI_EMAIL:
        params["email"] = NCBI_EMAIL

    for attempt in range(MAX_RETRIES):
        _rate_limit()
        try:
            resp = requests.get(BASE_URL, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            result = data.get("esearchresult", {})
            return int(result.get("count", 0))
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(2 ** attempt)
                continue
            print(f"  ERROR: {e}")
            return -1


# ── MeSH terms ──────────────────────────────────────────
LABELS = ["NLP", "GenAI", "LLM", "Chatbot"]
MESH_TERMS = {
    "NLP":     '"Natural Language Processing"[mh]',
    "GenAI":   '"Generative Artificial Intelligence"[mh]',
    "LLM":     '"Large Language Models"[mh]',
    "Chatbot": 'Chatbot[mh]',
}


def build_and_query(keys: Tuple[str, ...]) -> str:
    """Build an AND query from one or more MeSH keys."""
    return " AND ".join(MESH_TERMS[k] for k in keys)


def query_all_combinations() -> Dict[Tuple[str, ...], int]:
    """Query PubMed for all 15 combinations (singles, pairs, triples, quad)."""
    results = {}
    total_queries = 15
    done = 0

    for r in range(1, len(LABELS) + 1):
        for combo in combinations(LABELS, r):
            q = build_and_query(combo)
            done += 1
            label = " ∩ ".join(combo)
            print(f"  [{done}/{total_queries}] {label}...", end=" ", flush=True)
            count = get_count(q)
            print(f"{count:,}" if count >= 0 else "ERROR")
            results[combo] = count

    return results


def compute_exclusive_regions(counts: Dict[Tuple[str, ...], int]) -> Dict[str, int]:
    """
    包除原理 (inclusion-exclusion) で各排他的領域の件数を計算する。
    4セットの場合、16個の排他的領域がある（空集合を含む）。

    各領域は、含まれるセットのビットマスクで表す:
      0b0001 = NLP only
      0b0010 = GenAI only
      ...
      0b1111 = NLP ∩ GenAI ∩ LLM ∩ Chatbot
    """
    n = len(LABELS)
    exclusive = {}

    # 各ビットマスク (1〜15) に対して排他的件数を計算
    for mask in range(1, 1 << n):
        # この領域に含まれるセット
        included = tuple(LABELS[i] for i in range(n) if mask & (1 << i))

        # 包除原理: |A_only ∩ B_only ∩ ...| を計算
        # mask のビットが立っている = そのセットに含まれる
        # mask のビットが立っていない = そのセットに含まれない
        #
        # 排他的領域 = Σ (-1)^(|S|-|included|) * |S|
        # where S は included を含む全ての上位集合
        total = 0
        for supermask in range(mask, 1 << n):
            if (supermask & mask) != mask:
                continue
            superset = tuple(LABELS[i] for i in range(n) if supermask & (1 << i))
            sign = (-1) ** (len(superset) - len(included))
            if superset in counts:
                total += sign * counts[superset]

        region_label = " ∩ ".join(included) + " only"
        exclusive[region_label] = total

    return exclusive


def draw_venn4(counts: Dict[Tuple[str, ...], int],
               exclusive: Dict[str, int],
               output_path: str):
    """
    4セットベン図を楕円で描画する。
    Edwards-style: 4つの楕円を対称的に配置。
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    ax.set_xlim(-4, 4)
    ax.set_ylim(-3.5, 4)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Block 1 (AI/LLM) — MeSH Terms Venn Diagram",
                 fontsize=16, fontweight="bold", pad=20)

    # 4 ellipses — arranged symmetrically
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A"]
    alphas = [0.25, 0.25, 0.25, 0.25]

    # Ellipse parameters: (cx, cy, width, height, angle)
    ellipse_params = [
        (-0.8,  0.6, 4.0, 2.6,  45),   # NLP
        ( 0.8,  0.6, 4.0, 2.6, -45),   # GenAI
        (-0.8, -0.2, 4.0, 2.6, -45),   # LLM
        ( 0.8, -0.2, 4.0, 2.6,  45),   # Chatbot
    ]

    for i, (cx, cy, w, h, angle) in enumerate(ellipse_params):
        e = Ellipse(
            (cx, cy), w, h, angle=angle,
            facecolor=to_rgba(colors[i], alphas[i]),
            edgecolor=colors[i],
            linewidth=2.5,
        )
        ax.add_patch(e)

    # Labels outside ellipses
    label_positions = [
        (-3.2,  3.0),   # NLP
        ( 3.2,  3.0),   # GenAI
        (-3.2, -2.5),   # LLM
        ( 3.2, -2.5),   # Chatbot
    ]
    full_names = [
        "Natural Language\nProcessing (NLP)",
        "Generative AI\n(GenAI)",
        "Large Language\nModels (LLM)",
        "Chatbot",
    ]

    for i, (lx, ly) in enumerate(label_positions):
        single_count = counts.get((LABELS[i],), 0)
        ax.text(lx, ly,
                f"{full_names[i]}\n({single_count:,})",
                ha="center", va="center",
                fontsize=10, fontweight="bold",
                color=colors[i],
                bbox=dict(boxstyle="round,pad=0.3",
                          facecolor="white", edgecolor=colors[i], alpha=0.8))

    # Place exclusive region counts
    n = len(LABELS)
    # Approximate center positions for each region
    # These are manually tuned for the 4-ellipse layout
    region_positions = {
        0b0001: (-2.2,  1.8),   # NLP only
        0b0010: ( 2.2,  1.8),   # GenAI only
        0b0100: (-2.2, -1.5),   # LLM only
        0b1000: ( 2.2, -1.5),   # Chatbot only
        0b0011: ( 0.0,  2.2),   # NLP ∩ GenAI
        0b0101: (-1.8,  0.0),   # NLP ∩ LLM
        0b1001: ( 0.0,  0.8),   # NLP ∩ Chatbot
        0b0110: ( 0.0, -0.2),   # GenAI ∩ LLM
        0b1010: ( 1.8,  0.0),   # GenAI ∩ Chatbot
        0b1100: ( 0.0, -1.6),   # LLM ∩ Chatbot
        0b0111: (-0.8,  0.8),   # NLP ∩ GenAI ∩ LLM
        0b1011: ( 0.6,  1.2),   # NLP ∩ GenAI ∩ Chatbot
        0b1101: (-0.6, -0.8),   # NLP ∩ LLM ∩ Chatbot
        0b1110: ( 0.8, -0.8),   # GenAI ∩ LLM ∩ Chatbot
        0b1111: ( 0.0,  0.2),   # All four
    }

    for mask, (px, py) in region_positions.items():
        included = tuple(LABELS[i] for i in range(n) if mask & (1 << i))
        region_label = " ∩ ".join(included) + " only"
        val = exclusive.get(region_label, 0)

        fontsize = 9
        fontweight = "bold" if mask == 0b1111 else "normal"
        color = "#333333"

        if val > 0:
            ax.text(px, py, f"{val:,}",
                    ha="center", va="center",
                    fontsize=fontsize, fontweight=fontweight,
                    color=color,
                    bbox=dict(boxstyle="round,pad=0.15",
                              facecolor="white", edgecolor="#cccccc",
                              alpha=0.85))
        elif val == 0:
            ax.text(px, py, "0",
                    ha="center", va="center",
                    fontsize=8, color="#999999")

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    plt.close()
    print(f"\n  Venn diagram saved to: {output_path}")


def generate_report(counts: Dict[Tuple[str, ...], int],
                    exclusive: Dict[str, int],
                    or_count: int,
                    output_path: str):
    """Markdown形式でレポートを生成"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []
    lines.append("<!--")
    lines.append(f"Generated by: projects/kondo_wba/mesh_venn_block1.py")
    lines.append(f"Generated on: {now}")
    lines.append("-->")
    lines.append("")
    lines.append("# Block 1 (AI/LLM) MeSH用語 ベン図分析")
    lines.append("")

    # MeSH terms table
    lines.append("## 対象MeSH用語")
    lines.append("")
    lines.append("| Label | MeSH用語 | 単独件数 |")
    lines.append("|-------|----------|---------|")
    for label in LABELS:
        c = counts.get((label,), -1)
        c_str = f"{c:,}" if c >= 0 else "ERROR"
        lines.append(f"| {label} | `{MESH_TERMS[label]}` | {c_str} |")
    lines.append("")

    # All combinations
    lines.append("## 全組み合わせの件数")
    lines.append("")
    lines.append("| 組み合わせ | PubMed件数 |")
    lines.append("|-----------|-----------|")
    for r in range(1, len(LABELS) + 1):
        for combo in combinations(LABELS, r):
            label = " ∩ ".join(combo)
            c = counts.get(combo, -1)
            c_str = f"{c:,}" if c >= 0 else "ERROR"
            lines.append(f"| {label} | {c_str} |")
    or_str = f"{or_count:,}" if or_count >= 0 else "ERROR"
    lines.append(f"| **全体 (OR結合)** | **{or_str}** |")
    lines.append("")

    # Exclusive regions
    lines.append("## 排他的領域の件数（包除原理）")
    lines.append("")
    lines.append("| 領域 | 排他的件数 |")
    lines.append("|------|-----------|")
    total_exclusive = 0
    for mask in range(1, 1 << len(LABELS)):
        included = tuple(LABELS[i] for i in range(len(LABELS)) if mask & (1 << i))
        region_label = " ∩ ".join(included) + " only"
        val = exclusive.get(region_label, 0)
        total_exclusive += val
        lines.append(f"| {region_label} | {val:,} |")
    lines.append(f"| **合計** | **{total_exclusive:,}** |")
    lines.append("")

    # Consistency check
    lines.append("## 整合性チェック")
    lines.append("")
    if or_count >= 0:
        if total_exclusive == or_count:
            lines.append(f"✅ 排他的領域の合計 ({total_exclusive:,}) = 全体OR件数 ({or_count:,}) — **一致**")
        else:
            lines.append(f"⚠️ 排他的領域の合計 ({total_exclusive:,}) ≠ 全体OR件数 ({or_count:,}) — **不一致**")
    else:
        lines.append("❌ 全体OR件数の取得に失敗しました")
    lines.append("")

    # Venn diagram reference
    lines.append("## ベン図")
    lines.append("")
    lines.append("![Block 1 MeSH Venn Diagram](mesh_venn_block1.png)")
    lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  Report saved to: {output_path}")


def main():
    print("=" * 60)
    print("  Block 1 (AI/LLM) MeSH Venn Diagram Analysis")
    print("=" * 60)

    # 1. Query all 15 AND combinations
    print("\n[Step 1] Querying all AND combinations...")
    counts = query_all_combinations()

    # 2. Query the OR union
    print("\n[Step 2] Querying OR union...")
    or_query = " OR ".join(MESH_TERMS.values())
    or_count = get_count(f"({or_query})")
    print(f"  全体 (OR): {or_count:,}" if or_count >= 0 else "  全体 (OR): ERROR")

    # 3. Compute exclusive regions
    print("\n[Step 3] Computing exclusive regions (inclusion-exclusion)...")
    exclusive = compute_exclusive_regions(counts)

    # Print summary
    total_exclusive = sum(exclusive.values())
    print(f"\n  排他的領域の合計: {total_exclusive:,}")
    print(f"  全体 (OR):        {or_count:,}")
    if total_exclusive == or_count:
        print("  ✅ 一致")
    else:
        print("  ⚠️ 不一致")

    # 4. Generate outputs
    log_dir = os.path.join(os.path.dirname(__file__), "log")
    os.makedirs(log_dir, exist_ok=True)

    png_path = os.path.join(log_dir, "mesh_venn_block1.png")
    md_path = os.path.join(log_dir, "mesh_venn_block1.md")

    print("\n[Step 4] Drawing Venn diagram...")
    draw_venn4(counts, exclusive, png_path)

    print("\n[Step 5] Generating report...")
    generate_report(counts, exclusive, or_count, md_path)

    print("\n" + "=" * 60)
    print("  完了!")
    print("=" * 60)


if __name__ == "__main__":
    main()
