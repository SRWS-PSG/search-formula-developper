#!/usr/bin/env python3
"""
Experiment 6A: Manual Cross-check

Purpose: Verify if "0 hits" are real or API errors
Hypothesis: Some queries genuinely return 0 results (not API instability)
Method: Run same query multiple times and compare with manual PubMed checks
"""

import json
import os
import time
from datetime import datetime
from typing import Any, Dict, List

import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# API Configuration
NCBI_API_KEY = os.getenv("NCBI_API_KEY")
NCBI_TOOL = os.getenv("NCBI_TOOL")
NCBI_EMAIL = os.getenv("NCBI_EMAIL")
REQUEST_INTERVAL = 0.5
REQUEST_TIMEOUT = 30
NUM_REPETITIONS = 5  # Run each query 5 times

# Zero-hit queries from yarigai validation
ZERO_HIT_QUERIES = [
    {
        "id": "2B_L1",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND "meaningful work"[tiab])',
        "query_without_population": '"meaningful work"[tiab]',
        "block": "#2B Meaningful Work",
        "reported_count": 0
    },
    {
        "id": "2B_L2",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND "work meaningfulness"[tiab])',
        "query_without_population": '"work meaningfulness"[tiab]',
        "block": "#2B Meaningful Work",
        "reported_count": 0
    },
    {
        "id": "2B_L4",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND "meaning in work"[tiab])',
        "query_without_population": '"meaning in work"[tiab]',
        "block": "#2B Meaningful Work",
        "reported_count": 0
    },
    {
        "id": "2C_L1",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND "work engagement"[tiab])',
        "query_without_population": '"work engagement"[tiab]',
        "block": "#2C Work Engagement",
        "reported_count": 0
    },
    {
        "id": "2C_L2",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND vigor[tiab])',
        "query_without_population": 'vigor[tiab]',
        "block": "#2C Work Engagement",
        "reported_count": 0
    },
    {
        "id": "2C_L3",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND dedication[tiab])',
        "query_without_population": 'dedication[tiab]',
        "block": "#2C Work Engagement",
        "reported_count": 0
    },
    {
        "id": "2D_L1",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND calling[tiab])',
        "query_without_population": 'calling[tiab]',
        "block": "#2D Calling",
        "reported_count": 0
    },
    {
        "id": "2F_L1",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND "job satisfaction"[tiab])',
        "query_without_population": '"job satisfaction"[tiab]',
        "block": "#2F Satisfaction",
        "reported_count": 0
    },
]


def build_request_params(query: str) -> Dict[str, str]:
    """Build API request parameters"""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": "0",
    }
    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY
    if NCBI_TOOL:
        params["tool"] = NCBI_TOOL
    if NCBI_EMAIL:
        params["email"] = NCBI_EMAIL
    return params


def call_pubmed_api(query: str) -> Dict[str, Any]:
    """Call PubMed API once and return result"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = build_request_params(query)

    result = {
        "success": False,
        "count": None,
        "status_code": None,
        "response_time": None,
        "error": None,
    }

    try:
        start_time = time.time()
        response = requests.get(base_url, params=params, timeout=REQUEST_TIMEOUT)
        end_time = time.time()

        result["status_code"] = response.status_code
        result["response_time"] = end_time - start_time

        if response.status_code != 200:
            result["error"] = f"HTTP {response.status_code}"
            return result

        data = response.json()
        esearch_result = data.get("esearchresult", {})

        # Check for errors
        if esearch_result.get("errorlist"):
            result["error"] = f"errorlist: {esearch_result['errorlist']}"
            return result
        if esearch_result.get("ERROR"):
            result["error"] = f"ERROR: {esearch_result['ERROR']}"
            return result

        # Extract count
        count_str = esearch_result.get("count")
        if count_str is not None:
            try:
                result["count"] = int(count_str)
                result["success"] = True
            except (ValueError, TypeError):
                result["error"] = f"Invalid count: {count_str}"
        else:
            result["error"] = "Missing count field"

        return result

    except requests.exceptions.Timeout:
        result["error"] = f"Timeout after {REQUEST_TIMEOUT}s"
        return result
    except Exception as e:
        result["error"] = str(e)
        return result


def run_repeated_queries(query: str, num_repetitions: int) -> List[Dict[str, Any]]:
    """Run the same query multiple times"""
    results = []
    for i in range(num_repetitions):
        if i > 0:
            time.sleep(REQUEST_INTERVAL)
        result = call_pubmed_api(query)
        result["repetition"] = i + 1
        result["timestamp"] = datetime.now().isoformat()
        results.append(result)
    return results


def run_experiment() -> List[Dict[str, Any]]:
    """Run the experiment"""
    all_results = []

    print("=" * 80)
    print("Experiment 6A: Manual Cross-check for Zero-hit Queries")
    print("=" * 80)
    print(f"Testing {len(ZERO_HIT_QUERIES)} queries, {NUM_REPETITIONS} times each")
    print()

    for idx, test_case in enumerate(ZERO_HIT_QUERIES, 1):
        print(f"\n[{idx}/{len(ZERO_HIT_QUERIES)}] Testing: {test_case['id']}")
        print(f"  Block: {test_case['block']}")
        print(f"  Reported count: {test_case['reported_count']}")
        print(f"  Query: {test_case['query'][:80]}...")
        print()

        # Test with population filter
        print(f"  Running with population filter ({NUM_REPETITIONS}x)...")
        with_pop_results = run_repeated_queries(test_case['query'], NUM_REPETITIONS)

        # Test without population filter
        print(f"  Running WITHOUT population filter ({NUM_REPETITIONS}x)...")
        without_pop_results = run_repeated_queries(
            test_case['query_without_population'], NUM_REPETITIONS
        )

        # Analyze consistency
        with_pop_counts = [r['count'] for r in with_pop_results if r['success']]
        without_pop_counts = [r['count'] for r in without_pop_results if r['success']]

        result_summary = {
            **test_case,
            "with_population": {
                "all_results": with_pop_results,
                "success_rate": sum(1 for r in with_pop_results if r['success']) / NUM_REPETITIONS,
                "counts": with_pop_counts,
                "unique_counts": list(set(with_pop_counts)),
                "consistent": len(set(with_pop_counts)) <= 1 if with_pop_counts else False,
                "most_common_count": max(set(with_pop_counts), key=with_pop_counts.count) if with_pop_counts else None,
            },
            "without_population": {
                "all_results": without_pop_results,
                "success_rate": sum(1 for r in without_pop_results if r['success']) / NUM_REPETITIONS,
                "counts": without_pop_counts,
                "unique_counts": list(set(without_pop_counts)),
                "consistent": len(set(without_pop_counts)) <= 1 if without_pop_counts else False,
                "most_common_count": max(set(without_pop_counts), key=without_pop_counts.count) if without_pop_counts else None,
            },
        }

        all_results.append(result_summary)

        # Print summary
        print(f"\n  WITH population filter:")
        if result_summary['with_population']['consistent']:
            count = result_summary['with_population']['most_common_count']
            print(f"    ✓ CONSISTENT: {count:,} hits across all {NUM_REPETITIONS} attempts")
        else:
            counts = result_summary['with_population']['unique_counts']
            print(f"    ⚠️ INCONSISTENT: Got different counts: {counts}")

        print(f"\n  WITHOUT population filter:")
        if result_summary['without_population']['consistent']:
            count = result_summary['without_population']['most_common_count']
            print(f"    ✓ CONSISTENT: {count:,} hits across all {NUM_REPETITIONS} attempts")
        else:
            counts = result_summary['without_population']['unique_counts']
            print(f"    ⚠️ INCONSISTENT: Got different counts: {counts}")

        print()

    return all_results


def analyze_results(results: List[Dict[str, Any]]) -> str:
    """Generate analysis report"""
    report = []
    report.append("# Experiment 6A: Manual Cross-check Analysis")
    report.append("")
    report.append("<!--")
    report.append("Generated by: tests/api_instability_investigation_20251110/experiment_6a_manual_crosscheck.py")
    report.append(f"Execution time: {datetime.now().isoformat()}")
    report.append(f"Repetitions per query: {NUM_REPETITIONS}")
    report.append("-->")
    report.append("")

    # Summary
    total_queries = len(results)
    with_pop_consistent = sum(1 for r in results if r['with_population']['consistent'])
    without_pop_consistent = sum(1 for r in results if r['without_population']['consistent'])

    report.append("## Summary")
    report.append("")
    report.append(f"- **Total queries tested**: {total_queries}")
    report.append(f"- **Consistent WITH population**: {with_pop_consistent}/{total_queries} ({with_pop_consistent/total_queries*100:.1f}%)")
    report.append(f"- **Consistent WITHOUT population**: {without_pop_consistent}/{total_queries} ({without_pop_consistent/total_queries*100:.1f}%)")
    report.append("")

    # Detailed results
    report.append("## Detailed Results")
    report.append("")
    report.append("| ID | Block | Reported | WITH Pop (Most Common) | Consistent? | WITHOUT Pop | Consistent? |")
    report.append("|----|-------|----------|------------------------|-------------|-------------|-------------|")

    for r in results:
        with_pop_count = r['with_population']['most_common_count']
        with_pop_consistent = "✓" if r['with_population']['consistent'] else "✗"
        without_pop_count = r['without_population']['most_common_count']
        without_pop_consistent = "✓" if r['without_population']['consistent'] else "✗"

        with_pop_display = f"{with_pop_count:,}" if with_pop_count is not None else "FAIL"
        without_pop_display = f"{without_pop_count:,}" if without_pop_count is not None else "FAIL"

        report.append(
            f"| {r['id']} | {r['block']} | {r['reported_count']} | "
            f"{with_pop_display} | {with_pop_consistent} | "
            f"{without_pop_display} | {without_pop_consistent} |"
        )

    report.append("")

    # Truly zero queries
    report.append("## Truly Zero-hit Queries")
    report.append("")
    truly_zero = [
        r for r in results
        if r['with_population']['most_common_count'] == 0
        and r['with_population']['consistent']
    ]

    if truly_zero:
        report.append(f"These {len(truly_zero)} queries consistently return 0 hits (likely genuine):")
        report.append("")
        for r in truly_zero:
            without_pop = r['without_population']['most_common_count']
            report.append(f"- **{r['id']}** ({r['block']})")
            report.append(f"  - WITH physician filter: 0 hits")
            report.append(f"  - WITHOUT physician filter: {without_pop:,} hits")
            report.append("")
    else:
        report.append("No queries consistently returned 0 hits.")
        report.append("")

    # False zeros (API errors)
    report.append("## False Zero-hits (API Instability)")
    report.append("")
    false_zeros = [
        r for r in results
        if r['reported_count'] == 0
        and (r['with_population']['most_common_count'] != 0
             or not r['with_population']['consistent'])
    ]

    if false_zeros:
        report.append(f"These {len(false_zeros)} queries were reported as 0 but actually have hits:")
        report.append("")
        for r in false_zeros:
            with_pop = r['with_population']['most_common_count']
            unique_counts = r['with_population']['unique_counts']
            report.append(f"- **{r['id']}** ({r['block']})")
            report.append(f"  - Reported: 0 hits")
            report.append(f"  - Actual (most common): {with_pop:,} hits")
            if not r['with_population']['consistent']:
                report.append(f"  - ⚠️ INCONSISTENT across runs: {unique_counts}")
            report.append("")
    else:
        report.append("All reported zero-hits were confirmed.")
        report.append("")

    # Manual verification instructions
    report.append("## Manual PubMed Verification")
    report.append("")
    report.append("Please manually verify the following queries on PubMed web interface:")
    report.append("")

    for r in results:
        pubmed_url = f"https://pubmed.ncbi.nlm.nih.gov/?term={requests.utils.quote(r['query'])}"
        report.append(f"### {r['id']} - {r['block']}")
        report.append("")
        report.append(f"**Query**: `{r['query']}`")
        report.append("")
        report.append(f"**API Result**: {r['with_population']['most_common_count']} hits")
        report.append("")
        report.append(f"**Manual Check**: [Open in PubMed]({pubmed_url})")
        report.append("")
        report.append("Manual result: _____ hits (fill in manually)")
        report.append("")

    # Hypothesis evaluation
    report.append("## Hypothesis Evaluation")
    report.append("")
    report.append("**Hypothesis 6**: Some 0-hit reports are genuine (not API errors)")
    report.append("")

    if len(truly_zero) > 0 and len(false_zeros) > 0:
        report.append(f"**Result**: ⚠️ MIXED")
        report.append(f"- {len(truly_zero)} queries are genuinely zero-hit")
        report.append(f"- {len(false_zeros)} queries are false zeros (API instability)")
    elif len(truly_zero) == total_queries:
        report.append("**Result**: ✓ CONFIRMED - All zero-hits are genuine")
    elif len(false_zeros) == total_queries:
        report.append("**Result**: ❌ REJECTED - All zero-hits are API errors")
    else:
        report.append("**Result**: ⚠️ INCONCLUSIVE - Manual verification required")

    report.append("")

    return "\n".join(report)


def main():
    """Main execution"""
    # Create output directory
    output_dir = "tests/api_instability_investigation_20251110/results"
    os.makedirs(output_dir, exist_ok=True)

    # Run experiment
    results = run_experiment()

    # Save raw results
    raw_output_path = os.path.join(output_dir, "exp_6a_raw_results.json")
    with open(raw_output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nRaw results saved to: {raw_output_path}")

    # Generate and save report
    report = analyze_results(results)
    report_path = os.path.join(output_dir, "exp_6a_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Analysis report saved to: {report_path}")

    print()
    print("=" * 80)
    print("Experiment 6A completed successfully")
    print("=" * 80)


if __name__ == "__main__":
    main()
