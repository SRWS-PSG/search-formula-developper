#!/usr/bin/env python3
"""
統合レポートに5年限定(2021年以降)のIndividual Count列を追加

使用方法:
    python3 tests/add_five_year_simple.py

入力:
    tests/yarigai_comprehensive_line_counts_20251110.md
    tests/yarigai_line_counts_refined_20251109/five_year_counts_2021plus.md

出力:
    tests/yarigai_comprehensive_line_counts_with_5y_20251110.md
"""

import re
from datetime import datetime

def load_five_year_data():
    """five_year_counts_2021plus.md から検索語ごとの5年限定件数を抽出"""

    five_year_file = "tests/yarigai_line_counts_refined_20251109/five_year_counts_2021plus.md"

    # 完全な検索式 → 5年限定件数のマッピング
    term_to_five_year = {}

    with open(five_year_file, 'r', encoding='utf-8') as f:
        for line in f:
            # テーブル行のパターン: | #番号 | `検索式` | 総件数 | 2021年以降 | 備考 |
            match = re.match(r'\|\s*#\d+\s*\|\s*`(.+?)`\s*\|\s*[\d,]+\s*\|\s*(\d+)\s*\|', line)
            if match:
                full_query = match.group(1).strip()
                five_year_count = int(match.group(2))

                term_to_five_year[full_query] = five_year_count

    return term_to_five_year

def find_five_year_count(term, term_to_five_year):
    """検索語に対応する5年限定件数を検索"""

    # #1 AND を実際のPopulation条件に戻す
    if term.startswith('#1 AND '):
        concept = term.replace('#1 AND ', '').strip()
        full_query = f'("Physicians"[Mesh] OR physician*[tiab]) AND {concept}'
    elif term == '"Physicians"[Mesh]':
        # Populationの最初の行は特別扱い
        return 135710  # five_year_counts_2021plus.mdの#1の値
    elif term == 'physician*[tiab]':
        # Populationの2行目も特別扱い（正確なデータなし）
        return None  # N/Aとして扱う
    else:
        full_query = term

    # 完全一致を試す
    if full_query in term_to_five_year:
        return term_to_five_year[full_query]

    # 括弧の有無を試す
    if full_query.startswith('(') and full_query.endswith(')'):
        without_parens = full_query[1:-1]
        if without_parens in term_to_five_year:
            return term_to_five_year[without_parens]
    else:
        with_parens = f'({full_query})'
        if with_parens in term_to_five_year:
            return term_to_five_year[with_parens]

    return None

def add_five_year_column(input_file, output_file, term_to_five_year):
    """統合レポートに5年限定の列を追加"""

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    output_lines = []
    in_table = False

    i = 0
    while i < len(lines):
        line = lines[i]

        # テーブルヘッダーを検出して5年限定列を追加
        if '| Line | Term |' in line and 'Individual Count' in line:
            # ヘッダー行を置き換え
            output_lines.append('| Line | Term | Individual (All) | Individual (5y 2021+) | Cumulative (OR) | Added | % of Total |\n')
            in_table = True
            i += 1
            continue
        elif in_table and line.startswith('|------'):
            # 区切り行を置き換え
            output_lines.append('|------|------|------------------|----------------------|-----------------|-------|------------|\n')
            i += 1
            continue
        elif in_table and line.startswith('| ') and not line.startswith('| Line'):
            # データ行を解析して5年限定データを追加
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 7 and parts[1].isdigit():  # Line番号があるか確認
                line_num = parts[1]
                term = parts[2].strip('`')
                individual = parts[3]
                cumulative = parts[4]
                added = parts[5]
                percent = parts[6]

                # 5年限定データを検索
                five_year_count = find_five_year_count(term, term_to_five_year)

                if five_year_count is not None:
                    five_year_str = f"{five_year_count:,}"
                else:
                    five_year_str = 'N/A'

                # 新しい行を構築
                new_line = f"| {line_num} | `{term}` | {individual} | {five_year_str} | {cumulative} | {added} | {percent} |\n"
                output_lines.append(new_line)
                i += 1
                continue
            else:
                # テーブル外の行（Total行など）
                output_lines.append(line)
                if '**Total**' in line:
                    in_table = False
                i += 1
                continue

        # その他の行はそのまま
        output_lines.append(line)
        if '---' in line or line.startswith('# '):
            in_table = False
        i += 1

    # ファイルに書き込み
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)

def main():
    print("=" * 80)
    print("5年限定データ列の追加（Individual Count のみ）")
    print("=" * 80)
    print()

    # 5年限定データを読み込み
    print("5年限定データを読み込み中...")
    term_to_five_year = load_five_year_data()
    print(f"  読み込んだ検索語数: {len(term_to_five_year)}")
    print()

    # 統合レポートに列を追加
    input_file = "tests/yarigai_comprehensive_line_counts_20251110.md"
    output_file = "tests/yarigai_comprehensive_line_counts_with_5y_20251110.md"

    print(f"入力: {input_file}")
    print(f"出力: {output_file}")
    print()

    print("統合レポートに5年限定列を追加中...")
    add_five_year_column(input_file, output_file, term_to_five_year)

    print()
    print(f"✓ 完了: {output_file}")
    print()
    print("=" * 80)
    print("注意:")
    print("  - Individual Count (5y 2021+) のみ追加されています")
    print("  - Cumulative (OR) と Added は全期間のデータです")
    print("  - 5年限定の累積カウントを取得するには、別途5年フィルター付きで")
    print("    全ブロックを再実行する必要があります")
    print("=" * 80)

if __name__ == "__main__":
    main()
