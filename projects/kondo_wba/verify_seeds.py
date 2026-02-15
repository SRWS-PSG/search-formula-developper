"""
Seed論文が更新後のblock1-3による検索式でヒットするか検証するスクリプト
"""
import os
import requests
import time

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

NCBI_API_KEY = os.getenv("NCBI_API_KEY") or None
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
INTERVAL = 0.35 if NCBI_API_KEY else 1.1

SEEDS = [
    {"name": "Burke HB et al. (2024) JMIR Med Educ", "pmid": "39118469"},
    {"name": "Kwan BYM et al. (2025) Ann Surg Open", "pmid": "41451174"},
]


def read_block(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    text = " ".join(lines)
    # Remove trailing OR
    while text.rstrip().endswith("OR"):
        text = text.rstrip()[:-2].rstrip()
    return text


def search(query, retmax="0"):
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": retmax}
    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY
    time.sleep(INTERVAL)
    if len(query) > 1500:
        resp = requests.post(BASE_URL, data=params, timeout=30)
    else:
        resp = requests.get(BASE_URL, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json().get("esearchresult", {})


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    b1 = read_block(os.path.join(base_dir, "block1_ai.txt"))
    b2 = read_block(os.path.join(base_dir, "block2_education.txt"))
    b3 = read_block(os.path.join(base_dir, "block3_wba.txt"))

    combined = f"(({b1}) AND ({b2}) AND ({b3})) AND 2022:3000[dp] AND english[la]"

    print("=" * 60)
    print("  Updated search formula verification")
    print("=" * 60)
    print()

    # Total hits
    result = search(combined)
    total = result.get("count", "?")
    print(f"Total hits with updated formula: {total}")
    print()

    # Check each block individually first
    for i, (label, block) in enumerate([
        ("Block1 AI/LLM", b1),
        ("Block2 Education", b2),
        ("Block3 WBA", b3),
    ], 1):
        for seed in SEEDS:
            q = f"({block}) AND {seed['pmid']}[uid]"
            r = search(q, retmax="10")
            found = seed["pmid"] in r.get("idlist", [])
            status = "FOUND" if found else "NOT FOUND"
            print(f"  {label} x {seed['name']}: {status} (count={r.get('count', '?')})")
        print()

    # Check combined formula for each seed
    print("-" * 60)
    print("  Combined formula check")
    print("-" * 60)
    all_found = True
    for seed in SEEDS:
        q = f"({combined}) AND {seed['pmid']}[uid]"
        r = search(q, retmax="10")
        found = seed["pmid"] in r.get("idlist", [])
        status = "FOUND" if found else "NOT FOUND"
        if not found:
            all_found = False
        print(f"  {seed['name']} (PMID {seed['pmid']}): {status}")

    print()
    if all_found:
        print("RESULT: Both seed papers are captured by the updated search formula!")
    else:
        print("RESULT: Some seed papers are MISSING from the search results.")
        print("Check individual block results above to identify which block is failing.")


if __name__ == "__main__":
    main()
