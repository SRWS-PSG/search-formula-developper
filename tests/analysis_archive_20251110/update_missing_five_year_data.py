#!/usr/bin/env python3
"""
不足していた5年限定データを統合レポートに追加

使用方法:
    python3 tests/update_missing_five_year_data.py
"""

import re

# 取得した5年限定データ
FIVE_YEAR_DATA = {
    '#2C L4': 170,   # absorption[tiab]
    '#2E L4': 1436,  # motivat*[tiab] AND ...
    '#2F L5': 18,    # "workplace satisfaction"[tiab]
    '#2G L2': 6,     # "career fulfillment"[tiab]
    '#2G L3': 288,   # fulfillment[tiab]
    '#2G L4': 55,    # "professional well-being"[tiab]
    '#2G L5': 8,     # "professional wellbeing"[tiab]
    '#2I L1': 520,   # (autonomy[tiab] AND work*[tiab])
    '#2I L2': 588,   # (competence[tiab] AND work*[tiab])
    '#2I L3': 26,    # (relatedness[tiab] AND work*[tiab])
    '#2I L4': 139,   # "self-determination"[tiab]
}

# 検索語 → ラベルのマッピング
TERM_TO_LABEL = {
    'absorption[tiab]': '#2C L4',
    '(motivat*[tiab] AND (work*[tiab] OR job*[tiab] OR career*[tiab] OR professional*[tiab] OR workplace[tiab])': '#2E L4',
    '"workplace satisfaction"[tiab]': '#2F L5',
    '"career fulfillment"[tiab]': '#2G L2',
    'fulfillment[tiab]': '#2G L3',
    '"professional well-being"[tiab]': '#2G L4',
    '"professional wellbeing"[tiab]': '#2G L5',
    '(autonomy[tiab] AND work*[tiab])': '#2I L1',
    '(competence[tiab] AND work*[tiab])': '#2I L2',
    '(relatedness[tiab] AND work*[tiab])': '#2I L3',
    '"self-determination"[tiab]': '#2I L4',
}

def update_report(input_file, output_file):
    """統合レポートのN/Aを実際の値で置き換え"""

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    output_lines = []

    for line in lines:
        # データ行を検出
        if line.startswith('| ') and ' | N/A | ' in line:
            # 行を解析
            parts = [p.strip() for p in line.split('|')]

            if len(parts) >= 7 and parts[1].isdigit():  # Line番号があるか確認
                term = parts[2].strip('`').replace('#1 AND ', '')

                # 対応するラベルを検索
                label = TERM_TO_LABEL.get(term)

                if label and label in FIVE_YEAR_DATA:
                    five_year_count = FIVE_YEAR_DATA[label]

                    # N/Aを実際の値に置き換え
                    line = line.replace(' | N/A | ', f' | {five_year_count:,} | ', 1)
                    print(f"  更新: {label} ({term[:40]}...) → {five_year_count:,}")

        output_lines.append(line)

    # ファイルに書き込み
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)

def main():
    print("=" * 80)
    print("不足していた5年限定データを統合レポートに追加")
    print("=" * 80)
    print()

    input_file = "tests/yarigai_comprehensive_line_counts_20251110.md"
    output_file = "tests/yarigai_comprehensive_line_counts_20251110.md"

    print(f"入力: {input_file}")
    print(f"出力: {output_file}")
    print()

    update_report(input_file, output_file)

    print()
    print("=" * 80)
    print("✓ 完了")
    print("=" * 80)

if __name__ == "__main__":
    main()
