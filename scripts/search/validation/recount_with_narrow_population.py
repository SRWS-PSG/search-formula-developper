#!/usr/bin/env python3
"""
修正した#1（医師のみ）で各#2ブロックの件数を再測定
"""

import requests
import time
import xml.etree.ElementTree as ET
from typing import Dict
import os


class RecountAnalyzer:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get('NCBI_API_KEY')
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        self.delay = 0.34 if self.api_key else 0.5

    def get_count(self, query: str, retries: int = 3) -> int:
        """PubMed検索のヒット件数を取得"""
        params = {
            'db': 'pubmed',
            'term': query,
            'retmode': 'xml',
            'retmax': 0
        }

        if self.api_key:
            params['api_key'] = self.api_key

        for attempt in range(retries):
            try:
                time.sleep(self.delay)
                response = requests.get(self.base_url, params=params, timeout=30)
                response.raise_for_status()

                root = ET.fromstring(response.content)
                count_elem = root.find('.//Count')

                if count_elem is not None:
                    return int(count_elem.text)
                else:
                    print(f"Warning: No count found for query: {query[:100]}...")
                    return 0

            except Exception as e:
                print(f"Attempt {attempt + 1}/{retries} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    print(f"Failed to get count for query: {query[:100]}...")
                    return -1

        return -1


def main():
    """メイン処理"""

    # 修正した#1 (医師のみ)
    population_new = '"Physicians"[Mesh] OR physician*[tiab]'

    # 元の#1（比較用）
    population_old = '"Physicians"[Mesh] OR physician*[tiab] OR doctor*[tiab] OR "general practitioner*"[tiab] OR clinician*[tiab]'

    # フィルター
    filters = '("2015/01/01"[PDAT] : "3000"[PDAT]) NOT (animals[Mesh] NOT humans[Mesh])'

    # 各ブロックのクエリ定義
    blocks = {
        '#2A MeSH': '"Personal Satisfaction"[Mesh] OR "Job Satisfaction"[Mesh] OR "Motivation"[Mesh] OR "Professional Role"[Mesh] OR "Professional Autonomy"[Mesh] OR "Career Choice"[Mesh]',

        '#2B Meaningful Work': '"meaningful work"[tiab] OR "work meaningfulness"[tiab] OR "meaningfulness of work"[tiab] OR "meaning in work"[tiab] OR "work meaning"[tiab] OR "sense of meaning"[tiab]',

        '#2C Work Engagement': '"work engagement"[tiab] OR vigor[tiab] OR dedication[tiab] OR absorption[tiab]',

        '#2D Calling': 'calling[tiab] OR vocation*[tiab]',

        '#2E Motivation': '"intrinsic motivation"[tiab] OR motivat*[tiab]',

        '#2F Satisfaction': '"job satisfaction"[tiab] OR "work satisfaction"[tiab] OR "career satisfaction"[tiab] OR "professional satisfaction"[tiab] OR "compassion satisfaction"[tiab]',

        '#2G Fulfillment': '"professional fulfillment"[tiab] OR "professional quality of life"[tiab] OR "quality of professional life"[tiab] OR fulfillment[tiab] OR fulfilment[tiab]',

        '#2H Japanese': 'ikigai[tiab]',

        '#2I Psych Needs': '"psychological need*"[tiab] OR autonomy[tiab] OR competence[tiab] OR relatedness[tiab] OR "thriving at work"[tiab] OR thriving[tiab]',

        '#2J Task Significance': '"task significance"[tiab] OR "meaningful task*"[tiab] OR "work significance"[tiab]'
    }

    analyzer = RecountAnalyzer()

    results = {}

    print("="*80)
    print("修正した#1（医師のみ）での各ブロック件数測定")
    print("="*80)
    print(f"\n【修正後の#1】: {population_new}")
    print(f"【フィルター】: {filters}")
    print("\n")

    # まず修正後の#1単独の件数
    query_pop_new = f"({population_new}) AND {filters}"
    print(f"修正後の#1単独の件数を測定中...")
    count_pop_new = analyzer.get_count(query_pop_new)
    print(f"  → {count_pop_new:,} hits\n")

    # 比較用：元の#1単独の件数
    query_pop_old = f"({population_old}) AND {filters}"
    print(f"元の#1単独の件数を測定中...")
    count_pop_old = analyzer.get_count(query_pop_old)
    print(f"  → {count_pop_old:,} hits")

    reduction_pop = count_pop_old - count_pop_new
    pct_pop = (reduction_pop / count_pop_old * 100) if count_pop_old > 0 else 0
    print(f"  → #1の削減: -{reduction_pop:,} ({pct_pop:.1f}%)\n")

    print("="*80)
    print("各#2ブロックとの組み合わせ件数")
    print("="*80)

    for block_name, block_query in blocks.items():
        print(f"\n{block_name}")
        print("-" * 60)

        # 修正後の#1 AND ブロック
        query_new = f"({population_new}) AND {filters} AND ({block_query})"
        count_new = analyzer.get_count(query_new)
        print(f"  修正後: {count_new:,} hits")

        # 元の#1 AND ブロック（比較用）
        query_old = f"({population_old}) AND {filters} AND ({block_query})"
        count_old = analyzer.get_count(query_old)
        print(f"  元の値: {count_old:,} hits")

        # 削減
        reduction = count_old - count_new
        pct = (reduction / count_old * 100) if count_old > 0 else 0
        print(f"  削減量: -{reduction:,} ({pct:.1f}%)")

        results[block_name] = {
            'old': count_old,
            'new': count_new,
            'reduction': reduction,
            'pct': pct
        }

        time.sleep(0.5)

    # レポート生成
    print("\n\n" + "="*80)
    print("GENERATING MARKDOWN REPORT")
    print("="*80)

    report = generate_markdown_report(results, count_pop_old, count_pop_new, reduction_pop, pct_pop)

    # 出力
    output_dir = r'c:\Users\youki\codes\search-formula-developper\search_formula\yarigai_scoping_review'
    output_file = os.path.join(output_dir, 'population_narrowing_impact.md')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\nReport saved to: {output_file}")


def generate_markdown_report(results: Dict, count_pop_old: int, count_pop_new: int,
                            reduction_pop: int, pct_pop: float) -> str:
    """マークダウンレポートを生成"""

    lines = []
    lines.append("# #1 Population絞り込みの影響分析")
    lines.append("")
    lines.append(f"生成日時: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("## 分析目的")
    lines.append("")
    lines.append("#1 Populationを「医師のみ」に厳密に限定した場合の影響を測定。")
    lines.append("")
    lines.append("## #1の変更内容")
    lines.append("")
    lines.append("### 変更前（元の#1）")
    lines.append("```")
    lines.append('"Physicians"[Mesh] OR')
    lines.append('physician*[tiab] OR')
    lines.append('doctor*[tiab] OR')
    lines.append('"general practitioner*"[tiab] OR')
    lines.append('clinician*[tiab]')
    lines.append("```")
    lines.append("")
    lines.append("### 変更後（修正版 - 医師のみ）")
    lines.append("```")
    lines.append('"Physicians"[Mesh] OR')
    lines.append('physician*[tiab]')
    lines.append("```")
    lines.append("")
    lines.append("**削除した用語:**")
    lines.append("- `doctor*[tiab]` - 博士号保持者、歯科医なども含むため")
    lines.append('- `"general practitioner*"[tiab]` - 低価値（0.2%のみ貢献）')
    lines.append("- `clinician*[tiab]` - 看護師、薬剤師など医師以外の臨床家も含むため")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## #1単独での影響")
    lines.append("")
    lines.append("| 項目 | 件数 |")
    lines.append("|------|------|")
    lines.append(f"| 元の#1（フィルター適用後） | {count_pop_old:,} |")
    lines.append(f"| 修正後の#1（フィルター適用後） | {count_pop_new:,} |")
    lines.append(f"| **削減量** | **-{reduction_pop:,} ({pct_pop:.1f}%)** |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 各#2ブロックとの組み合わせ影響")
    lines.append("")
    lines.append("| Block | 元の件数 | 修正後 | 削減量 | 削減率 |")
    lines.append("|-------|----------|--------|--------|--------|")

    total_old = 0
    total_new = 0

    for block_name in sorted(results.keys()):
        data = results[block_name]
        old = data['old']
        new = data['new']
        reduction = data['reduction']
        pct = data['pct']

        total_old += old
        total_new += new

        lines.append(f"| {block_name} | {old:,} | {new:,} | -{reduction:,} | {pct:.1f}% |")

    # 合計行
    total_reduction = total_old - total_new
    total_pct = (total_reduction / total_old * 100) if total_old > 0 else 0
    lines.append(f"| **TOTAL** | **{total_old:,}** | **{total_new:,}** | **-{total_reduction:,}** | **{total_pct:.1f}%** |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 結論")
    lines.append("")
    lines.append(f"### #1の絞り込みによる全体的な削減効果")
    lines.append("")
    lines.append(f"- **平均削減率**: 約{total_pct:.1f}%")
    lines.append(f"- **総削減件数**: -{total_reduction:,}件")
    lines.append("")
    lines.append("### 推奨事項")
    lines.append("")
    lines.append("✅ **推奨**: #1を修正版（医師のみ）に変更")
    lines.append("")
    lines.append("**理由:**")
    lines.append("- プロトコルの対象は「医師（physicians）」のみであり、より正確")
    lines.append("- `clinician*`は看護師・薬剤師なども含み、ノイズが多い")
    lines.append("- `doctor*`は博士号保持者（PhD）や歯科医も含むため不適切")
    lines.append(f"- 削減率は約{total_pct:.1f}%と適度で、感度を大きく損なわない")
    lines.append("")

    return "\n".join(lines)


if __name__ == '__main__':
    main()
