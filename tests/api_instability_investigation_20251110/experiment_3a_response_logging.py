#!/usr/bin/env python3
"""
Experiment 3A: Response Structure Detailed Logging

Purpose: Log complete API responses to understand actual JSON structure
Hypothesis: API returns data correctly but parsing fails due to unexpected structure
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
REQUEST_INTERVAL = 0.5  # Conservative rate
REQUEST_TIMEOUT = 30

# Test queries: Known problematic queries from yarigai validation
TEST_QUERIES = [
    {
        "id": "2B_L1",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND "meaningful work"[tiab])',
        "expected": "unknown",
        "block": "#2B Meaningful Work"
    },
    {
        "id": "2B_L2",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND "work meaningfulness"[tiab])',
        "expected": "unknown",
        "block": "#2B Meaningful Work"
    },
    {
        "id": "2C_L1",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND "work engagement"[tiab])',
        "expected": "unknown",
        "block": "#2C Work Engagement"
    },
    {
        "id": "2C_L2",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND vigor[tiab])',
        "expected": "unknown",
        "block": "#2C Work Engagement"
    },
    {
        "id": "2D_L1",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND calling[tiab])',
        "expected": "unknown",
        "block": "#2D Calling"
    },
    {
        "id": "2F_L1",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND "job satisfaction"[tiab])',
        "expected": "unknown",
        "block": "#2F Satisfaction"
    },
    # Known successful queries for comparison
    {
        "id": "2A_L2_success",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND "Job Satisfaction"[Mesh])',
        "expected": "2314",
        "block": "#2A MeSH (known success)"
    },
    {
        "id": "2E_L4_success",
        "query": '(("Physicians"[Mesh] OR physician*[tiab]) AND (motivat*[tiab] AND (work*[tiab] OR job*[tiab] OR career*[tiab] OR professional*[tiab] OR workplace[tiab])))',
        "expected": "4081",
        "block": "#2E Motivation (known success)"
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
    """
    Call PubMed API and return complete response details

    Returns dict with:
    - success: bool
    - status_code: int
    - raw_response: complete JSON response
    - parsed_count: extracted count value (if available)
    - response_time: time taken (seconds)
    - error_message: error description (if any)
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = build_request_params(query)

    result = {
        "success": False,
        "status_code": None,
        "raw_response": None,
        "parsed_count": None,
        "response_time": None,
        "error_message": None,
        "count_field_path": None,
    }

    try:
        start_time = time.time()
        response = requests.get(base_url, params=params, timeout=REQUEST_TIMEOUT)
        end_time = time.time()

        result["status_code"] = response.status_code
        result["response_time"] = end_time - start_time

        if response.status_code != 200:
            result["error_message"] = f"HTTP {response.status_code}"
            result["raw_response"] = response.text
            return result

        # Parse JSON
        try:
            data = response.json()
            result["raw_response"] = data
        except json.JSONDecodeError as e:
            result["error_message"] = f"JSON parse error: {e}"
            result["raw_response"] = response.text
            return result

        # Try to extract count from various possible locations
        count_paths = [
            ("esearchresult", "count"),
            ("esearchresult", "Count"),
            ("result", "count"),
            ("count",),
            ("Count",),
        ]

        for path in count_paths:
            current = data
            valid_path = True
            for key in path:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    valid_path = False
                    break

            if valid_path:
                try:
                    result["parsed_count"] = int(current)
                    result["count_field_path"] = ".".join(path)
                    result["success"] = True
                    break
                except (ValueError, TypeError):
                    pass

        # Check for error fields
        if not result["success"]:
            esearch_result = data.get("esearchresult", {})
            if esearch_result.get("errorlist"):
                result["error_message"] = f"API errorlist: {esearch_result['errorlist']}"
            elif esearch_result.get("ERROR"):
                result["error_message"] = f"API ERROR: {esearch_result['ERROR']}"
            elif data.get("error"):
                result["error_message"] = f"API error: {data['error']}"
            else:
                result["error_message"] = "Count field not found in response"

        return result

    except requests.exceptions.Timeout:
        result["error_message"] = f"Timeout after {REQUEST_TIMEOUT}s"
        return result
    except requests.exceptions.RequestException as e:
        result["error_message"] = f"Request exception: {e}"
        return result
    except Exception as e:
        result["error_message"] = f"Unexpected error: {e}"
        return result


def run_experiment() -> List[Dict[str, Any]]:
    """Run the experiment and collect results"""
    results = []

    print("=" * 80)
    print("Experiment 3A: API Response Structure Logging")
    print("=" * 80)
    print(f"Testing {len(TEST_QUERIES)} queries...")
    print()

    for idx, test_case in enumerate(TEST_QUERIES, 1):
        print(f"[{idx}/{len(TEST_QUERIES)}] Testing: {test_case['id']}")
        print(f"  Block: {test_case['block']}")
        print(f"  Query: {test_case['query'][:80]}...")

        # Rate limiting
        if idx > 1:
            time.sleep(REQUEST_INTERVAL)

        # Call API
        api_result = call_pubmed_api(test_case['query'])

        # Combine test case info with API result
        full_result = {
            **test_case,
            **api_result,
            "timestamp": datetime.now().isoformat(),
        }
        results.append(full_result)

        # Print summary
        if api_result["success"]:
            print(f"  ✓ SUCCESS: Count = {api_result['parsed_count']:,} (from {api_result['count_field_path']})")
            print(f"  Response time: {api_result['response_time']:.2f}s")
        else:
            print(f"  ✗ FAILED: {api_result['error_message']}")
            if api_result['status_code']:
                print(f"  HTTP status: {api_result['status_code']}")

        print()

    return results


def analyze_results(results: List[Dict[str, Any]]) -> str:
    """Generate analysis report"""
    report = []
    report.append("# Experiment 3A: API Response Structure Analysis")
    report.append("")
    report.append("<!--")
    report.append("Generated by: tests/api_instability_investigation_20251110/experiment_3a_response_logging.py")
    report.append(f"Execution time: {datetime.now().isoformat()}")
    report.append("-->")
    report.append("")

    # Summary statistics
    total = len(results)
    successful = sum(1 for r in results if r["success"])
    failed = total - successful

    report.append("## Summary")
    report.append("")
    report.append(f"- **Total queries tested**: {total}")
    report.append(f"- **Successful**: {successful} ({successful/total*100:.1f}%)")
    report.append(f"- **Failed**: {failed} ({failed/total*100:.1f}%)")
    report.append("")

    # Success/Failure breakdown
    report.append("## Results by Query")
    report.append("")
    report.append("| ID | Block | Status | Count | Response Time | Error |")
    report.append("|----|-------|--------|-------|---------------|-------|")

    for r in results:
        status = "✓" if r["success"] else "✗"
        count = f"{r['parsed_count']:,}" if r['parsed_count'] is not None else "N/A"
        resp_time = f"{r['response_time']:.2f}s" if r['response_time'] else "N/A"
        error = r['error_message'] or "-"
        if len(error) > 50:
            error = error[:47] + "..."

        report.append(f"| {r['id']} | {r['block']} | {status} | {count} | {resp_time} | {error} |")

    report.append("")

    # Count field path analysis
    report.append("## Count Field Paths")
    report.append("")
    report.append("Location of 'count' field in successful responses:")
    report.append("")

    path_counts = {}
    for r in results:
        if r["success"] and r["count_field_path"]:
            path = r["count_field_path"]
            path_counts[path] = path_counts.get(path, 0) + 1

    if path_counts:
        for path, count in sorted(path_counts.items(), key=lambda x: -x[1]):
            report.append(f"- `{path}`: {count} queries")
    else:
        report.append("No successful responses with count field")

    report.append("")

    # Error pattern analysis
    report.append("## Error Patterns")
    report.append("")

    error_types = {}
    for r in results:
        if not r["success"] and r["error_message"]:
            # Extract error type
            error_msg = r["error_message"]
            if "Timeout" in error_msg:
                error_type = "Timeout"
            elif "HTTP" in error_msg:
                error_type = f"HTTP {r['status_code']}"
            elif "Count field not found" in error_msg:
                error_type = "Count field missing"
            elif "errorlist" in error_msg or "ERROR" in error_msg:
                error_type = "API error response"
            else:
                error_type = "Other"

            error_types[error_type] = error_types.get(error_type, [])
            error_types[error_type].append(r['id'])

    if error_types:
        for error_type, query_ids in sorted(error_types.items()):
            report.append(f"### {error_type} ({len(query_ids)} queries)")
            report.append("")
            for qid in query_ids:
                report.append(f"- {qid}")
            report.append("")
    else:
        report.append("No errors detected")
        report.append("")

    # Known success vs problematic queries
    report.append("## Known Success vs Problematic Queries")
    report.append("")

    known_success = [r for r in results if "success" in r["id"]]
    problematic = [r for r in results if "success" not in r["id"]]

    report.append(f"### Known Successful Queries ({len(known_success)})")
    report.append("")
    for r in known_success:
        status = "✓" if r["success"] else "✗"
        count = r["parsed_count"] if r["parsed_count"] is not None else "FAILED"
        report.append(f"- {status} **{r['id']}**: {count}")
    report.append("")

    report.append(f"### Problematic Queries ({len(problematic)})")
    report.append("")
    for r in problematic:
        status = "✓" if r["success"] else "✗"
        count = r["parsed_count"] if r["parsed_count"] is not None else "FAILED"
        report.append(f"- {status} **{r['id']}**: {count}")
    report.append("")

    # Hypothesis evaluation
    report.append("## Hypothesis Evaluation")
    report.append("")
    report.append("**Hypothesis 3**: API returns data correctly but parsing fails due to unexpected structure")
    report.append("")

    if failed == 0:
        report.append("**Result**: ❌ REJECTED - All queries succeeded, no parsing issues detected")
    elif all(r.get("count_field_path") == "esearchresult.count" for r in results if r["success"]):
        report.append("**Result**: ❌ REJECTED - All successful responses use expected field path")
    else:
        report.append("**Result**: ⚠️ PARTIALLY CONFIRMED - Investigate error patterns above")

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
    raw_output_path = os.path.join(output_dir, "exp_3a_raw_responses.json")
    with open(raw_output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Raw results saved to: {raw_output_path}")

    # Generate and save report
    report = analyze_results(results)
    report_path = os.path.join(output_dir, "exp_3a_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Analysis report saved to: {report_path}")

    print()
    print("=" * 80)
    print("Experiment 3A completed successfully")
    print("=" * 80)


if __name__ == "__main__":
    main()
