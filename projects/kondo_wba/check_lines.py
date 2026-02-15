"""
kondo_wba 検索式の各行チェックスクリプト
各ブロック内の検索語ごとにPubMedヒット件数を取得し、
ブロック全体およびAND結合の件数も確認する。
"""

import os
import re
import sys
import time
import requests
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

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


def get_count(query: str) -> Dict[str, Any]:
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
            # Use POST for long queries
            if len(query) > 1500:
                resp = requests.post(BASE_URL, data=params, timeout=30)
            else:
                resp = requests.get(BASE_URL, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            result = data.get("esearchresult", {})

            # Check for API-level warnings
            warnings = []
            if result.get("warninglist"):
                wl = result["warninglist"]
                if wl.get("phrasesnotfound"):
                    warnings.append(f"phrase not found: {wl['phrasesnotfound']}")
                if wl.get("quotedphrasesnotfound"):
                    warnings.append(f"quoted phrase not found: {wl['quotedphrasesnotfound']}")

            count = int(result.get("count", 0))
            return {"count": count, "warnings": warnings, "error": None}

        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(2 ** attempt)
                continue
            return {"count": None, "warnings": [], "error": str(e)}


def fmt(n: Any) -> str:
    if n is None:
        return "ERROR"
    return f"{n:,}"


def parse_block(text: str) -> List[str]:
    """ブロックテキストからOR区切りで個別の検索語を抽出"""
    # 改行とORで分割
    combined = " ".join(line.strip() for line in text.strip().splitlines())
    # 外側の括弧を除去
    combined = combined.strip()
    if combined.startswith("(") and combined.endswith(")"):
        combined = combined[1:-1].strip()

    # OR で分割（括弧内のORは無視）
    terms = []
    current = ""
    depth = 0
    i = 0
    while i < len(combined):
        c = combined[i]
        if c == "(":
            depth += 1
            current += c
        elif c == ")":
            depth -= 1
            current += c
        elif depth == 0 and combined[i:i+4] == " OR ":
            terms.append(current.strip())
            current = ""
            i += 4
            continue
        else:
            current += c
        i += 1
    if current.strip():
        terms.append(current.strip())
    return terms


def main():
    # --- Define blocks ---
    block1_text = """
"generative artificial intelligence"[tiab] OR "generative AI"[tiab] OR
"large language model*"[tiab] OR ChatGPT[tiab] OR GPT-4[tiab] OR
GPT-4o[tiab] OR GPT-3.5[tiab] OR GPT4[tiab] OR GPT-4V[tiab] OR
GPT-4.1[tiab] OR GPT-4.5[tiab] OR GPT-5[tiab] OR Claude[tiab] OR
Gemini[tiab] OR LLaMA[tiab] OR "Llama 2"[tiab] OR "Llama 3"[tiab] OR
DeepSeek[tiab] OR "multimodal AI"[tiab] OR "AI chatbot*"[tiab] OR
"foundation model*"[tiab] OR "text generat*"[tiab] OR
"Natural Language Processing"[mh] OR
"Generative Artificial Intelligence"[mh] OR
"Large Language Models"[mh] OR Chatbot[mh]
"""

    block2_text = """
"medical education"[tiab] OR "clinical education"[tiab] OR
"graduate medical education"[tiab] OR
"undergraduate medical education"[tiab] OR
"postgraduate medical education"[tiab] OR
"health profession* education"[tiab] OR "residency training"[tiab] OR
residency[tiab] OR "medical student*"[tiab] OR
"resident physician*"[tiab] OR "clinical clerkship*"[tiab] OR
"clinical training"[tiab] OR "clinical teach*"[tiab] OR
trainee*[tiab] OR "medical trainee*"[tiab] OR
"Education, Medical"[mh] OR "Education, Medical, Graduate"[mh] OR
"Education, Medical, Undergraduate"[mh] OR
"Education, Medical, Continuing"[mh] OR
"Internship and Residency"[mh] OR "Students, Medical"[mh] OR
"Clinical Clerkship"[mh]
"""

    block3_text = """
"workplace-based assessment*"[tiab] OR
"workplace based assessment*"[tiab] OR
"work-based assessment*"[tiab] OR "work based assessment*"[tiab] OR
Mini-CEX[tiab] OR "mini clinical evaluation exercise*"[tiab] OR
"direct observation of procedural skill*"[tiab] OR
"direct observation*"[tiab] OR
"entrustable professional activit*"[tiab] OR
"multisource feedback"[tiab] OR "multi-source feedback"[tiab] OR
"360-degree feedback"[tiab] OR
"competency-based medical education"[tiab] OR
"competency based medical education"[tiab] OR
"competency-based assessment*"[tiab] OR
"competency based assessment*"[tiab] OR
"programmatic assessment"[tiab] OR milestone*[tiab] OR
"narrative feedback"[tiab] OR "narrative assessment*"[tiab] OR
"assessment feedback"[tiab] OR "supervisor* feedback"[tiab] OR
"assessment scoring"[tiab] OR "clinical note*"[tiab] OR
"medical record*"[tiab] OR "chart review*"[tiab] OR
"Clinical Competence"[mh] OR "Educational Measurement"[mh] OR
"Competency-Based Education"[mh] OR "Formative Feedback"[mh]
"""

    blocks = [
        ("#1 AI/LLM", block1_text),
        ("#2 Medical Education", block2_text),
        ("#3 Workplace-Based Assessment", block3_text),
    ]

    output_path = "projects/kondo_wba/log/search_lines_check.md"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []
    lines.append(f"<!--")
    lines.append(f"Generated by: projects/kondo_wba/check_lines.py")
    lines.append(f"Generated on: {now}")
    lines.append(f"-->")
    lines.append("")
    lines.append("# kondo_wba 検索式 各行チェック結果")
    lines.append("")

    block_queries = {}  # store full block query for final AND

    for block_name, block_text in blocks:
        terms = parse_block(block_text)
        full_block_query = " OR ".join(terms)
        block_queries[block_name] = f"({full_block_query})"

        lines.append(f"## {block_name}")
        lines.append("")
        lines.append(f"検索語数: {len(terms)}")
        lines.append("")
        lines.append("| # | 検索語 | ヒット件数 | 警告 |")
        lines.append("|---|--------|-----------|------|")

        print(f"\n{'='*60}")
        print(f"  {block_name} ({len(terms)} terms)")
        print(f"{'='*60}")

        zero_terms = []
        warning_terms = []

        for i, term in enumerate(terms, 1):
            print(f"  [{i}/{len(terms)}] {term}...", end=" ", flush=True)
            result = get_count(term)
            count_str = fmt(result["count"])
            warn_str = "; ".join(result["warnings"]) if result["warnings"] else ""
            if result["error"]:
                warn_str = f"ERROR: {result['error']}"

            print(f"{count_str}")

            if result["count"] == 0:
                zero_terms.append(term)
                lines.append(f"| {i} | `{term}` | **{count_str}** | ⚠️ 0件 |")
            elif result["warnings"]:
                warning_terms.append((term, result["warnings"]))
                lines.append(f"| {i} | `{term}` | {count_str} | ⚠️ {warn_str} |")
            elif result["error"]:
                lines.append(f"| {i} | `{term}` | {count_str} | ❌ {warn_str} |")
            else:
                lines.append(f"| {i} | `{term}` | {count_str} | |")

        # Block total
        print(f"  [Block Total] ...", end=" ", flush=True)
        block_result = get_count(block_queries[block_name])
        block_count = fmt(block_result["count"])
        print(f"{block_count}")

        lines.append("")
        lines.append(f"**ブロック全体 (OR結合):** {block_count} 件")
        lines.append("")

        # Summary
        if zero_terms:
            lines.append(f"> [!WARNING]")
            lines.append(f"> **0件の検索語が {len(zero_terms)} 個あります:**")
            for t in zero_terms:
                lines.append(f"> - `{t}`")
            lines.append("")

        if warning_terms:
            lines.append(f"> [!NOTE]")
            lines.append(f"> **警告付きの検索語が {len(warning_terms)} 個あります:**")
            for t, w in warning_terms:
                lines.append(f"> - `{t}`: {'; '.join(w)}")
            lines.append("")

        lines.append("---")
        lines.append("")

    # Final AND combination
    print(f"\n{'='*60}")
    print(f"  Final AND combination")
    print(f"{'='*60}")

    final_query = " AND ".join(block_queries.values()) + " AND 2022:3000[dp] AND english[la]"
    print(f"  Querying...", end=" ", flush=True)
    final_result = get_count(final_query)
    final_count = fmt(final_result["count"])
    print(f"{final_count}")

    lines.append("## 最終検索結果 (#1 AND #2 AND #3 AND 2022:3000[dp] AND english[la])")
    lines.append("")
    lines.append(f"**最終ヒット件数: {final_count} 件**")
    lines.append("")
    if final_result["warnings"]:
        lines.append(f"> [!WARNING]")
        lines.append(f"> {'; '.join(final_result['warnings'])}")
        lines.append("")

    # Write output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n結果を {output_path} に保存しました。")


if __name__ == "__main__":
    main()
