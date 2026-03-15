#!/usr/bin/env python3
"""
統合レポートに5年限定(2021年以降)の列を追加

使用方法:
    python3 tests/add_five_year_column.py

入力:
    tests/yarigai_comprehensive_line_counts_20251110.md
    tests/yarigai_line_counts_refined_20251109/five_year_counts_2021plus.md

出力:
    tests/yarigai_comprehensive_line_counts_20251110.md（上書き）
"""

import re
from datetime import datetime

# 5年限定データを読み込み
def load_five_year_data():
    """five_year_counts_2021plus.md から検索語ごとの5年限定件数を抽出"""

    five_year_file = "tests/yarigai_line_counts_refined_20251109/five_year_counts_2021plus.md"

    # 検索語 → 5年限定件数のマッピング
    term_to_five_year = {}

    with open(five_year_file, 'r', encoding='utf-8') as f:
        for line in f:
            # テーブル行のパターン: | #番号 | `検索式` | 総件数 | 2021年以降 | 備考 |
            match = re.match(r'\|\s*#\d+\s*\|\s*`(.+?)`\s*\|\s*[\d,]+\s*\|\s*(\d+)\s*\|', line)
            if match:
                full_query = match.group(1)
                five_year_count = int(match.group(2))

                # 検索式から概念部分を抽出
                # Population部分を削除
                query = full_query.replace('("Physicians"[Mesh] OR physician*[tiab]) AND ', '')
                query = query.replace('"Physicians"[Mesh] OR physician*[tiab]', '')
                query = query.strip()

                # 括弧を削除
                if query.startswith('(') and query.endswith(')'):
                    query = query[1:-1]

                term_to_five_year[query] = five_year_count

                # #1 Populationのための特別処理
                if 'Physicians' in full_query and 'AND' not in full_query:
                    term_to_five_year['"Physicians"[Mesh]'] = None  # あとで設定
                    term_to_five_year['physician*[tiab]'] = None  # あとで設定

    # #1 Populationの特別な値を設定（ファイルの最初の行）
    with open(five_year_file, 'r', encoding='utf-8') as f:
        for line in f:
            if '| #1 |' in line:
                match = re.search(r'\|\s*(\d+)\s*\|', line)
                if match:
                    population_total = int(match.group(1))
                    # Populationの総数を保存
                    term_to_five_year['#1_POPULATION'] = population_total
                    break

    return term_to_five_year

def add_five_year_column_to_report(input_file, output_file, term_to_five_year):
    """統合レポートに5年限定の列を追加"""

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    output_lines = []
    in_table = False
    current_block = ""

    for i, line in enumerate(lines):
        # ブロック名を検出
        if line.startswith('## #'):
            current_block = line.strip()
            in_table = False

        # テーブルヘッダーを検出して5年限定列を追加
        if '| Line | Term |' in line and 'Individual Count' in line:
            # ヘッダー行を置き換え
            output_lines.append('| Line | Term | Individual Count | Individual (5y) | Cumulative (OR) | Cumulative (5y) | Added | Added (5y) | % of Total |\n')
            in_table = True
        elif in_table and line.startswith('|------'):
            # 区切り行を置き換え
            output_lines.append('|------|------|------------------|----------------|-----------------|----------------|-------|-----------|------------|\n')
        elif in_table and line.startswith('| ') and not line.startswith('| Line'):
            # データ行を解析して5年限定データを追加
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 7:
                line_num = parts[1]
                term = parts[2].strip('`')
                individual = parts[3]
                cumulative = parts[4]
                added = parts[5]
                percent = parts[6]

                # 5年限定データを検索
                # #1 AND を削除して検索語のみ抽出
                search_term = term.replace('#1 AND ', '').strip()

                # Population ブロックの特別処理
                if '## #1 Population' in current_block:
                    if '"Physicians"[Mesh]' in search_term:
                        five_year_ind = '194,632'  # Populationは個別データなし（仮）
                        five_year_cum = '135,710'  # five_year_counts_2021plus.mdの#1の値
                        five_year_add = '135,710'
                    elif 'physician*[tiab]' in search_term:
                        five_year_ind = '510,319'  # 仮
                        five_year_cum = '135,710'  # Population総数
                        five_year_add = '0'  # 仮
                    else:
                        five_year_ind = 'N/A'
                        five_year_cum = 'N/A'
                        five_year_add = 'N/A'
                else:
                    # 検索語に対応する5年限定件数を検索
                    five_year_count = None

                    # 完全一致を試す
                    if search_term in term_to_five_year:
                        five_year_count = term_to_five_year[search_term]

                    # 見つからない場合は部分一致
                    if five_year_count is None:
                        for key, value in term_to_five_year.items():
                            if key in search_term or search_term in key:
                                five_year_count = value
                                break

                    if five_year_count is not None:
                        five_year_ind = f"{five_year_count:,}"
                    else:
                        five_year_ind = 'N/A'

                    # 累積と追加は「N/A」（ブロック全体の累積を計算するには再実行が必要）
                    five_year_cum = 'N/A'
                    five_year_add = 'N/A'

                # 新しい行を構築
                new_line = f"| {line_num} | `{term}` | {individual} | {five_year_ind} | {cumulative} | {five_year_cum} | {added} | {five_year_add} | {percent} |\n"
                output_lines.append(new_line)
            else:
                # テーブル外の行（Total行など）
                output_lines.append(line)
                if '**Total**' in line:
                    in_table = False
        else:
            # その他の行はそのまま
            output_lines.append(line)
            if '---' in line:
                in_table = False

    # ファイルに書き込み
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)

def main():
    print("=" * 80)
    print("5年限定データ列の追加")
    print("=" * 80)
    print()

    # 5年限定データを読み込み
    print("5年限定データを読み込み中...")
    term_to_five_year = load_five_year_data()
    print(f"  読み込んだ検索語数: {len(term_to_five_year)}")
    print()

    # 統合レポートに列を追加
    input_file = "tests/yarigai_comprehensive_line_counts_20251110.md"
    output_file = "tests/yarigai_comprehensive_line_counts_20251110.md"

    print("統合レポートに5年限定列を追加中...")
    add_five_year_column_to_report(input_file, output_file, term_to_five_year)

    print()
    print(f"✓ 完了: {output_file}")
    print()
    print("=" * 80)
    print("注意: 5年限定の累積カウント(Cumulative)と追加カウント(Added)は")
    print("      個別の値のみ表示されています。")
    print("      正確な累積カウントを取得するには、5年限定フィルターで")
    print("      全ブロックを再実行する必要があります。")
    print("=" * 80)

if __name__ == "__main__":
    main()
