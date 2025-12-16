#!/usr/bin/env python3
"""
既存の統合レポート (tests/yarigai_comprehensive_line_counts_20251110.md) に
過去3年 (2023+) の個別件数列を挿入するスクリプト。

事前に tests/get_three_year_counts.py を実行して
tests/three_year_counts_2023plus.json を作成しておくこと。
"""

import json

REPORT_PATH = "tests/yarigai_comprehensive_line_counts_20251110.md"
THREE_YEAR_JSON = "tests/three_year_counts_2023plus.json"
COLUMN_LABEL = "Individual (3y 2023+)"


def load_three_year_mapping():
    with open(THREE_YEAR_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    mapping = {}
    for item in data["results"]:
        key = (item["block"], item["line"])
        mapping[key] = item["three_year_count"]
    return mapping


def format_value(value):
    if value is None:
        return "-"
    return f"{value:,}"


def update_report(mapping):
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = []
    current_block = None
    in_table = False

    for raw_line in lines:
        line = raw_line
        stripped = raw_line.strip()

        if stripped.startswith("## "):
            current_block = stripped[2:].strip()

        if "| Line | Term |" in raw_line and "Individual (All)" in raw_line:
            header = raw_line.replace(
                "Individual (All) | Individual (5y 2021+)",
                f"Individual (All) | {COLUMN_LABEL} | Individual (5y 2021+)",
            )
            line = header
            in_table = True
        elif in_table and raw_line.startswith("|------"):
            line = raw_line.replace(
                "------------------|----------------------|",
                "------------------|----------------------|----------------------|",
            )
        elif in_table and raw_line.startswith("| ") and not raw_line.startswith("| Line"):
            parts = raw_line.split("|")
            if len(parts) >= 8 and parts[1].strip().isdigit():
                line_no = int(parts[1].strip())
                key = (current_block, line_no)
                three_year_value = format_value(mapping.get(key))

                # parts layout: ['', ' line ', ' term ', ' all ', ' five ', ... , '']
                # insert after Individual (All)
                parts.insert(4, f" {three_year_value} ")
                line = "|".join(parts)

        if in_table and ("**Total**" in raw_line or raw_line.strip() == ""):
            in_table = False

        updated_lines.append(line)

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)


def main():
    print("=" * 80)
    print("統合レポートへ3年限定列を追加")
    print("=" * 80)
    mapping = load_three_year_mapping()
    print(f"  取得データ: {len(mapping)} 行")
    update_report(mapping)
    print("✓ 完了")


if __name__ == "__main__":
    main()
