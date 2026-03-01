"""
block2の変更前後でPubMed検索結果がどれだけ増えたかを比較するスクリプト
protocol.md の block2 (旧) vs block2_education.txt (新) を比較
"""

import os
import time
import requests

NCBI_API_KEY = os.getenv("NCBI_API_KEY") or None
NCBI_TOOL = os.getenv("NCBI_TOOL") or None
NCBI_EMAIL = os.getenv("NCBI_EMAIL") or None

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
REQUEST_INTERVAL = 0.35 if NCBI_API_KEY else 1.1
_last_ts = 0.0


def _rate_limit():
    global _last_ts
    elapsed = time.time() - _last_ts
    if elapsed < REQUEST_INTERVAL:
        time.sleep(REQUEST_INTERVAL - elapsed)
    _last_ts = time.time()


def get_count(query: str) -> int:
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": "0"}
    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY
    if NCBI_TOOL:
        params["tool"] = NCBI_TOOL
    if NCBI_EMAIL:
        params["email"] = NCBI_EMAIL

    for attempt in range(3):
        _rate_limit()
        try:
            if len(query) > 1500:
                resp = requests.post(BASE_URL, data=params, timeout=30)
            else:
                resp = requests.get(BASE_URL, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            result = data.get("esearchresult", {})
            return int(result.get("count", 0))
        except Exception as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise


# Block 1 (AI) - 共通
block1 = (
    '("generative artificial intelligence"[tiab] OR "generative AI"[tiab] OR '
    '"large language model*"[tiab] OR ChatGPT[tiab] OR GPT*[tiab] OR '
    'GPT4[tiab] OR Claude[tiab] OR Gemini[tiab] OR llama[tiab] OR '
    'DeepSeek[tiab] OR "multimodal AI"[tiab] OR "AI chatbot*"[tiab] OR '
    '"foundation model*"[tiab] OR "text generat*"[tiab] OR '
    '"Natural Language Processing"[mh] OR '
    '"Generative Artificial Intelligence"[mh] OR '
    '"Large Language Models"[mh] OR Chatbot[mh])'
)

# Block 2 旧 (protocol.md)
block2_old = (
    '("medical education"[tiab] OR "clinical education"[tiab] OR '
    '"graduate medical education"[tiab] OR '
    '"undergraduate medical education"[tiab] OR '
    '"postgraduate medical education"[tiab] OR '
    '"health profession* education"[tiab] OR "residency training"[tiab] OR '
    'residency[tiab] OR "medical student*"[tiab] OR '
    '"resident physician*"[tiab] OR "clinical clerkship*"[tiab] OR '
    '"clinical training"[tiab] OR "clinical teach*"[tiab] OR '
    'trainee*[tiab] OR "medical trainee*"[tiab] OR '
    '"Education, Medical"[mh] OR "Education, Medical, Graduate"[mh] OR '
    '"Education, Medical, Undergraduate"[mh] OR '
    '"Education, Medical, Continuing"[mh] OR '
    '"Internship and Residency"[mh] OR "Students, Medical"[mh] OR '
    '"Clinical Clerkship"[mh])'
)

# Block 2 新 (block2_education.txt)
block2_new = (
    '("medical education"[tiab] OR "clinical education"[tiab] OR '
    '"graduate medical education"[tiab] OR '
    '"undergraduate medical education"[tiab] OR '
    '"postgraduate medical education"[tiab] OR '
    '"health profession* education"[tiab] OR "residency training"[tiab] OR '
    'residency[tiab] OR "medical student*"[tiab] OR '
    '"resident physician*"[tiab] OR "clinical clerkship*"[tiab] OR '
    '"clinical training"[tiab] OR "clinical teach*"[tiab] OR '
    'trainee*[tiab] OR "medical trainee*"[tiab] OR '
    '"clinical rotation*"[tiab] OR clerkship*[tiab] OR '
    '"clinical supervisor*"[tiab] OR "medical curriculum"[tiab] OR '
    '"Education, Medical"[mh] OR '
    '"Internship and Residency"[mh] OR "Students, Medical"[mh] OR '
    '"Clinical Clerkship"[mh])'
)

# Block 3 (WBA) - 共通
block3 = (
    '("workplace-based assessment*"[tiab] OR '
    '"workplace based assessment*"[tiab] OR '
    '"work-based assessment*"[tiab] OR "work based assessment*"[tiab] OR '
    'Mini-CEX[tiab] OR "mini clinical evaluation exercise*"[tiab] OR '
    '"direct observation of procedural skill*"[tiab] OR '
    '"direct observation*"[tiab] OR '
    '"entrustable professional activit*"[tiab] OR '
    '"multisource feedback"[tiab] OR "multi-source feedback"[tiab] OR '
    '"360-degree feedback"[tiab] OR '
    '"competency-based medical education"[tiab] OR '
    '"competency based medical education"[tiab] OR '
    '"competency-based assessment*"[tiab] OR '
    '"competency based assessment*"[tiab] OR '
    '"programmatic assessment"[tiab] OR milestone*[tiab] OR '
    '"narrative feedback"[tiab] OR "narrative assessment*"[tiab] OR '
    '"assessment feedback"[tiab] OR "supervisor* feedback"[tiab] OR '
    '"assessment scoring"[tiab] OR "clinical note*"[tiab] OR '
    '"medical record*"[tiab] OR "chart review*"[tiab] OR '
    '"Clinical Competence"[mh] OR "Educational Measurement"[mh] OR '
    '"Competency-Based Education"[mh] OR "Formative Feedback"[mh])'
)

date_filter = "AND 2022:3000[dp] AND english[la]"

# 旧式: block1 AND block2_old AND block3
query_old = f"{block1} AND {block2_old} AND {block3} {date_filter}"
# 新式: block1 AND block2_new AND block3
query_new = f"{block1} AND {block2_new} AND {block3} {date_filter}"
# 差分: 新にあって旧にないもの
query_diff = f"({query_new}) NOT ({query_old})"

print("=== Block2 変更前後の比較 ===\n")

print("旧 block2 (protocol.md) でのヒット数を取得中...")
count_old = get_count(query_old)
print(f"  旧: {count_old:,} 件")

print("新 block2 (block2_education.txt) でのヒット数を取得中...")
count_new = get_count(query_new)
print(f"  新: {count_new:,} 件")

print("差分 (新 NOT 旧) を取得中...")
count_diff = get_count(query_diff)
print(f"  追加: {count_diff:,} 件")

print(f"\n--- 結果まとめ ---")
print(f"旧 block2: {count_old:,} 件")
print(f"新 block2: {count_new:,} 件")
print(f"増加分:    +{count_diff:,} 件")
print(f"(新 - 旧 = {count_new - count_old:,} 件)")
