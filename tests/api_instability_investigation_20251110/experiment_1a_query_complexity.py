#!/usr/bin/env python3
"""
Experiment 1A: Query Complexity and Timeout Correlation

Purpose: Test if complex queries cause timeouts or failures
Hypothesis: Complex queries (with population AND conditions) are more likely to timeout
"""

import json
import os
import statistics
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
NUM_REPETITIONS = 3  # Test each query 3 times for reliability

# Test queries with varying complexity levels
TEST_QUERIES = [
    # Level 1: Simple single-term queries
    {
        "id": "L1_simple_phrase",
        "query": '"meaningful work"[tiab]',
        "complexity": "Level 1: Simple",
        "description": "Single phrase search",
    },
    {
        "id": "L1_simple_word",
        "query": 'calling[tiab]',
        "complexity": "Level 1: Simple",
        "description": "Single word search",
    },
    {
        "id": "L1_simple_mesh",
        "query": '"Job Satisfaction"[Mesh]',
        "complexity": "Level 1: Simple",
        "description": "Single MeSH term",
    },
    # Level 2: Population-only queries
    {
        "id": "L2_pop_mesh",
        "query": '"Physicians"[Mesh]',
        "complexity": "Level 2: Population only",
        "description": "Physicians MeSH only",
    },
    {
        "id": "L2_pop_tiab",
        "query": 'physician*[tiab]',
        "complexity": "Level 2: Population only",
        "description": "Physicians text word with wildcard",
    },
    {
        "id": "L2_pop_combined",
        "query": '("Physicians"[Mesh] OR physician*[tiab])',
        "complexity": "Level 2: Population only",
        "description": "Combined population filter",
    },
    # Level 3: Population AND single concept
    {
        "id": "L3_pop_and_phrase",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND "meaningful work"[tiab])',
        "complexity": "Level 3: Pop AND concept",
        "description": "Population AND phrase",
    },
    {
        "id": "L3_pop_and_word",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND calling[tiab])',
        "complexity": "Level 3: Pop AND concept",
        "description": "Population AND single word",
    },
    {
        "id": "L3_pop_and_mesh",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND "Job Satisfaction"[Mesh])',
        "complexity": "Level 3: Pop AND concept",
        "description": "Population AND MeSH",
    },
    # Level 4: Population AND multiple OR concepts
    {
        "id": "L4_pop_and_3terms",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND (calling[tiab] OR vocation[tiab] OR "career calling"[tiab]))',
        "complexity": "Level 4: Pop AND multi-OR",
        "description": "Population AND 3 OR terms",
    },
    {
        "id": "L4_pop_and_5terms",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND (autonomy[tiab] OR competence[tiab] OR relatedness[tiab] OR "self determination"[tiab] OR "psychological needs"[tiab]))',
        "complexity": "Level 4: Pop AND multi-OR",
        "description": "Population AND 5 OR terms",
    },
    # Level 5: Population AND nested conditions
    {
        "id": "L5_nested_moderate",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND (motivat*[tiab] AND (work*[tiab] OR job*[tiab])))',
        "complexity": "Level 5: Nested AND/OR",
        "description": "Population AND (term AND 2-OR)",
    },
    {
        "id": "L5_nested_complex",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND ((autonomy[tiab] OR competence[tiab] OR relatedness[tiab]) AND (work*[tiab] OR job*[tiab] OR professional*[tiab] OR workplace[tiab])))',
        "complexity": "Level 5: Nested AND/OR",
        "description": "Population AND (3-OR AND 4-OR)",
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


def call_pubmed_api(query: str, timeout: int) -> Dict[str, Any]:
    """Call PubMed API with specific timeout"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = build_request_params(query)

    result = {
        "success": False,
        "count": None,
        "status_code": None,
        "response_time": None,
        "error_type": None,
        "error_message": None,
    }

    try:
        start_time = time.time()
        response = requests.get(base_url, params=params, timeout=timeout)
        end_time = time.time()

        result["status_code"] = response.status_code
        result["response_time"] = end_time - start_time

        if response.status_code != 200:
            result["error_type"] = f"HTTP_{response.status_code}"
            result["error_message"] = f"HTTP {response.status_code}"
            return result

        data = response.json()
        esearch_result = data.get("esearchresult", {})

        # Check for errors
        if esearch_result.get("errorlist"):
            result["error_type"] = "API_ERROR"
            result["error_message"] = str(esearch_result['errorlist'])
            return result
        if esearch_result.get("ERROR"):
            result["error_type"] = "API_ERROR"
            result["error_message"] = str(esearch_result['ERROR'])
            return result

        # Extract count
        count_str = esearch_result.get("count")
        if count_str is not None:
            try:
                result["count"] = int(count_str)
                result["success"] = True
            except (ValueError, TypeError):
                result["error_type"] = "PARSE_ERROR"
                result["error_message"] = f"Invalid count: {count_str}"
        else:
            result["error_type"] = "MISSING_COUNT"
            result["error_message"] = "Count field missing"

        return result

    except requests.exceptions.Timeout:
        result["error_type"] = "TIMEOUT"
        result["error_message"] = f"Timeout after {timeout}s"
        result["response_time"] = timeout
        return result
    except Exception as e:
        result["error_type"] = "EXCEPTION"
        result["error_message"] = str(e)
        return result


def run_experiment() -> List[Dict[str, Any]]:
    """Run the experiment"""
    all_results = []

    print("=" * 80)
    print("Experiment 1A: Query Complexity vs Success Rate")
    print("=" * 80)
    print(f"Testing {len(TEST_QUERIES)} queries, {NUM_REPETITIONS} times each")
    print(f"Timeout: {REQUEST_TIMEOUT}s, Interval: {REQUEST_INTERVAL}s")
    print()

    for idx, test_case in enumerate(TEST_QUERIES, 1):
        print(f"[{idx}/{len(TEST_QUERIES)}] {test_case['id']}")
        print(f"  Complexity: {test_case['complexity']}")
        print(f"  Query length: {len(test_case['query'])} chars")
        print(f"  Running {NUM_REPETITIONS}x...", end=" ")

        repetition_results = []
        for rep in range(NUM_REPETITIONS):
            if idx > 1 or rep > 0:
                time.sleep(REQUEST_INTERVAL)

            result = call_pubmed_api(test_case['query'], REQUEST_TIMEOUT)
            result["repetition"] = rep + 1
            result["timestamp"] = datetime.now().isoformat()
            repetition_results.append(result)

        # Aggregate results
        successful = [r for r in repetition_results if r['success']]
        failed = [r for r in repetition_results if not r['success']]

        success_rate = len(successful) / NUM_REPETITIONS
        avg_response_time = statistics.mean([r['response_time'] for r in repetition_results if r['response_time']])

        counts = [r['count'] for r in successful]
        most_common_count = max(set(counts), key=counts.count) if counts else None

        error_types = [r['error_type'] for r in failed]
        most_common_error = max(set(error_types), key=error_types.count) if error_types else None

        aggregated = {
            **test_case,
            "query_length": len(test_case['query']),
            "num_repetitions": NUM_REPETITIONS,
            "num_successful": len(successful),
            "num_failed": len(failed),
            "success_rate": success_rate,
            "avg_response_time": avg_response_time,
            "min_response_time": min([r['response_time'] for r in repetition_results if r['response_time']]),
            "max_response_time": max([r['response_time'] for r in repetition_results if r['response_time']]),
            "most_common_count": most_common_count,
            "most_common_error": most_common_error,
            "all_repetitions": repetition_results,
        }

        all_results.append(aggregated)

        # Print summary
        if success_rate == 1.0:
            print(f"✓ {success_rate*100:.0f}% success, {avg_response_time:.2f}s avg, {most_common_count:,} hits")
        elif success_rate > 0:
            print(f"⚠️ {success_rate*100:.0f}% success, {avg_response_time:.2f}s avg")
        else:
            print(f"✗ 0% success, error: {most_common_error}")

    return all_results


def analyze_results(results: List[Dict[str, Any]]) -> str:
    """Generate analysis report"""
    report = []
    report.append("# Experiment 1A: Query Complexity Analysis")
    report.append("")
    report.append("<!--")
    report.append("Generated by: tests/api_instability_investigation_20251110/experiment_1a_query_complexity.py")
    report.append(f"Execution time: {datetime.now().isoformat()}")
    report.append(f"Repetitions per query: {NUM_REPETITIONS}")
    report.append(f"Timeout: {REQUEST_TIMEOUT}s")
    report.append("-->")
    report.append("")

    # Summary by complexity level
    report.append("## Summary by Complexity Level")
    report.append("")

    complexity_levels = sorted(set(r['complexity'] for r in results))

    for level in complexity_levels:
        level_results = [r for r in results if r['complexity'] == level]
        avg_success = statistics.mean([r['success_rate'] for r in level_results])
        avg_time = statistics.mean([r['avg_response_time'] for r in level_results])

        report.append(f"### {level}")
        report.append("")
        report.append(f"- **Average success rate**: {avg_success*100:.1f}%")
        report.append(f"- **Average response time**: {avg_time:.2f}s")
        report.append(f"- **Queries tested**: {len(level_results)}")
        report.append("")

    # Detailed results table
    report.append("## Detailed Results")
    report.append("")
    report.append("| ID | Complexity | Query Length | Success Rate | Avg Time | Count |")
    report.append("|----|------------|--------------|--------------|----------|-------|")

    for r in results:
        success_pct = f"{r['success_rate']*100:.0f}%"
        avg_time = f"{r['avg_response_time']:.2f}s"
        count = f"{r['most_common_count']:,}" if r['most_common_count'] is not None else "FAIL"

        report.append(
            f"| {r['id']} | {r['complexity']} | {r['query_length']} | "
            f"{success_pct} | {avg_time} | {count} |"
        )

    report.append("")

    # Correlation analysis
    report.append("## Correlation Analysis")
    report.append("")

    # Query length vs success rate
    lengths = [r['query_length'] for r in results]
    success_rates = [r['success_rate'] for r in results]

    if len(set(success_rates)) > 1:  # Only if there's variation
        import math
        mean_len = statistics.mean(lengths)
        mean_sr = statistics.mean(success_rates)
        covariance = sum((lengths[i] - mean_len) * (success_rates[i] - mean_sr) for i in range(len(lengths))) / len(lengths)
        std_len = statistics.stdev(lengths) if len(lengths) > 1 else 0
        std_sr = statistics.stdev(success_rates) if len(success_rates) > 1 else 0
        correlation = covariance / (std_len * std_sr) if std_len > 0 and std_sr > 0 else 0

        report.append(f"**Query Length vs Success Rate correlation**: {correlation:.3f}")
        report.append("")
        if correlation < -0.3:
            report.append("⚠️ Negative correlation detected: Longer queries are less successful")
        elif correlation > 0.3:
            report.append("✓ Positive correlation: Longer queries are more successful")
        else:
            report.append("✓ No strong correlation between length and success")
        report.append("")

    # Response time vs complexity
    report.append("### Response Time by Complexity")
    report.append("")
    for level in complexity_levels:
        level_results = [r for r in results if r['complexity'] == level]
        avg_time = statistics.mean([r['avg_response_time'] for r in level_results])
        max_time = max([r['max_response_time'] for r in level_results])
        report.append(f"- **{level}**: {avg_time:.2f}s avg, {max_time:.2f}s max")
    report.append("")

    # Failed queries
    failed_queries = [r for r in results if r['success_rate'] < 1.0]
    if failed_queries:
        report.append("## Failed Queries")
        report.append("")
        report.append(f"Total: {len(failed_queries)} queries had at least one failure")
        report.append("")
        for r in failed_queries:
            report.append(f"- **{r['id']}** ({r['complexity']}): {r['success_rate']*100:.0f}% success")
            report.append(f"  - Error: {r['most_common_error']}")
            report.append("")

    # Hypothesis evaluation
    report.append("## Hypothesis Evaluation")
    report.append("")
    report.append("**Hypothesis 1**: Complex queries cause timeouts or failures")
    report.append("")

    simple_results = [r for r in results if "Level 1" in r['complexity'] or "Level 2" in r['complexity']]
    complex_results = [r for r in results if "Level 4" in r['complexity'] or "Level 5" in r['complexity']]

    if simple_results and complex_results:
        simple_success = statistics.mean([r['success_rate'] for r in simple_results])
        complex_success = statistics.mean([r['success_rate'] for r in complex_results])

        report.append(f"- **Simple queries (L1-L2)**: {simple_success*100:.1f}% success")
        report.append(f"- **Complex queries (L4-L5)**: {complex_success*100:.1f}% success")
        report.append("")

        if complex_success < simple_success - 0.2:
            report.append("**Result**: ✓ CONFIRMED - Complex queries have lower success rate")
        elif abs(complex_success - simple_success) < 0.1:
            report.append("**Result**: ❌ REJECTED - No significant difference between simple and complex")
        else:
            report.append("**Result**: ⚠️ INCONCLUSIVE - Further investigation needed")
    else:
        report.append("**Result**: ⚠️ INSUFFICIENT DATA")

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
    raw_output_path = os.path.join(output_dir, "exp_1a_raw_results.json")
    with open(raw_output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n\nRaw results saved to: {raw_output_path}")

    # Generate and save report
    report = analyze_results(results)
    report_path = os.path.join(output_dir, "exp_1a_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Analysis report saved to: {report_path}")

    print()
    print("=" * 80)
    print("Experiment 1A completed successfully")
    print("=" * 80)


if __name__ == "__main__":
    main()
