#!/usr/bin/env python3
"""
過去5年フィルターでの件数を再測定
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
    population = '"Physicians"[Mesh] OR physician*[tiab]'

    # フィルター（10年 vs 5年）
    filters_10y = '("2015/01/01"[PDAT] : "3000"[PDAT]) NOT (animals[Mesh] NOT humans[Mesh])'
    filters_5y = '("2020/01/01"[PDAT] : "3000"[PDAT]) NOT (animals[Mesh] NOT humans[Mesh])'

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
    print("過去5年フィルターでの各ブロック件数測定")
    print("="*80)
    print(f"\n【#1】: {population}")
    print(f"【フィルター（5年）】: {filters_5y}")
    print("\n")

    # まず#1単独の件数（5年 vs 10年）
    query_pop_5y = f"({population}) AND {filters_5y}"
    print(f"過去5年 - #1単独の件数を測定中...")
    count_pop_5y = analyzer.get_count(query_pop_5y)
    print(f"  → {count_pop_5y:,} hits\n")

    # 比較用：10年
    query_pop_10y = f"({population}) AND {filters_10y}"
    print(f"過去10年 - #1単独の件数を測定中...")
    count_pop_10y = analyzer.get_count(query_pop_10y)
    print(f"  → {count_pop_10y:,} hits")

    reduction_pop = count_pop_10y - count_pop_5y
    pct_pop = (reduction_pop / count_pop_10y * 100) if count_pop_10y > 0 else 0
    print(f"  → 削減: -{reduction_pop:,} ({pct_pop:.1f}%)\n")

    print("="*80)
    print("各#2ブロックとの組み合わせ件数")
    print("="*80)

    for block_name, block_query in blocks.items():
        print(f"\n{block_name}")
        print("-" * 60)

        # 過去5年
        query_5y = f"({population}) AND {filters_5y} AND ({block_query})"
        count_5y = analyzer.get_count(query_5y)
        print(f"  過去5年: {count_5y:,} hits")

        # 過去10年（比較用）
        query_10y = f"({population}) AND {filters_10y} AND ({block_query})"
        count_10y = analyzer.get_count(query_10y)
        print(f"  過去10年: {count_10y:,} hits")

        # 削減
        reduction = count_10y - count_5y
        pct = (reduction / count_10y * 100) if count_10y > 0 else 0
        print(f"  削減量: -{reduction:,} ({pct:.1f}%)")

        results[block_name] = {
            '10y': count_10y,
            '5y': count_5y,
            'reduction': reduction,
            'pct': pct
        }

        time.sleep(0.5)

    # レポート生成
    print("\n\n" + "="*80)
    print("GENERATING MARKDOWN REPORT")
    print("="*80)

    report = generate_markdown_report(results, count_pop_10y, count_pop_5y, reduction_pop, pct_pop)

    # 出力
    output_dir = r'c:\Users\youki\codes\search-formula-developper\search_formula\yarigai_scoping_review'
    output_file = os.path.join(output_dir, 'five_year_filter_impact.md')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\nReport saved to: {output_file}")


def generate_markdown_report(results: Dict, count_pop_10y: int, count_pop_5y: int,
                            reduction_pop: int, pct_pop: float) -> str:
    """マークダウンレポートを生成"""

    lines = []
    lines.append("# 過去5年フィルターの影響分析")
    lines.append("")
    lines.append(f"生成日時: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("## 分析目的")
    lines.append("")
    lines.append("過去10年 → 過去5年に変更した場合の削減効果を測定。")
    lines.append("")
    lines.append("## フィルター設定")
    lines.append("")
    lines.append("### 過去10年")
    lines.append('```')
    lines.append('("2015/01/01"[PDAT] : "3000"[PDAT])')
    lines.append('```')
    lines.append("")
    lines.append("### 過去5年")
    lines.append('```')
    lines.append('("2020/01/01"[PDAT] : "3000"[PDAT])')
    lines.append('```')
    lines.append("")
    lines.append("**共通フィルター:**")
    lines.append("- Animal除外: `NOT (animals[Mesh] NOT humans[Mesh])`")
    lines.append("- #1（医師のみ）: `\"Physicians\"[Mesh] OR physician*[tiab]`")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## #1単独での影響")
    lines.append("")
    lines.append("| 項目 | 件数 |")
    lines.append("|------|------|")
    lines.append(f"| 過去10年 | {count_pop_10y:,} |")
    lines.append(f"| 過去5年 | {count_pop_5y:,} |")
    lines.append(f"| **削減量** | **-{reduction_pop:,} ({pct_pop:.1f}%)** |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 各#2ブロックとの組み合わせ影響")
    lines.append("")
    lines.append("| Block | 過去10年 | 過去5年 | 削減量 | 削減率 |")
    lines.append("|-------|----------|---------|--------|--------|")

    total_10y = 0
    total_5y = 0

    for block_name in sorted(results.keys()):
        data = results[block_name]
        count_10y = data['10y']
        count_5y = data['5y']
        reduction = data['reduction']
        pct = data['pct']

        total_10y += count_10y
        total_5y += count_5y

        lines.append(f"| {block_name} | {count_10y:,} | {count_5y:,} | -{reduction:,} | {pct:.1f}% |")

    # 合計行
    total_reduction = total_10y - total_5y
    total_pct = (total_reduction / total_10y * 100) if total_10y > 0 else 0
    lines.append(f"| **TOTAL** | **{total_10y:,}** | **{total_5y:,}** | **-{total_reduction:,}** | **{total_pct:.1f}%** |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 結論")
    lines.append("")
    lines.append(f"### 過去5年フィルターの削減効果")
    lines.append("")
    lines.append(f"- **平均削減率**: 約{total_pct:.1f}%")
    lines.append(f"- **総削減件数**: -{total_reduction:,}件")
    lines.append(f"- **最終件数**: {total_5y:,}件")
    lines.append("")
    lines.append("### 推奨事項")
    lines.append("")
    lines.append("✅ **推奨**: 過去5年フィルターに変更")
    lines.append("")
    lines.append("**理由:**")
    lines.append("- より最近の文献に焦点を当てることで、現代的な「やりがい」概念を捉えられる")
    lines.append("- COVID-19パンデミック後の医師の働き方・価値観の変化を反映")
    lines.append(f"- 大幅な削減効果（{total_pct:.1f}%削減）")
    lines.append("")
    lines.append("**注意点:**")
    lines.append("- Seed papers（5本）がすべて過去5年以内に含まれるか要確認")
    lines.append("- 古典的な重要文献を取りこぼす可能性があるため、seed papersで検証必須")
    lines.append("")

    return "\n".join(lines)


if __name__ == '__main__':
    main()
