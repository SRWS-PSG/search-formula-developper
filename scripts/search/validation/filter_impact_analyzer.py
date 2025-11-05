#!/usr/bin/env python3
"""
フィルター効果分析スクリプト

各検索ブロックに対して、段階的にフィルターを適用し、件数の変化を測定する。
"""

import requests
import time
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple
import os


class FilterImpactAnalyzer:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get('NCBI_API_KEY')
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        self.delay = 0.34 if self.api_key else 0.5  # API rate limit

    def get_count(self, query: str, retries: int = 3) -> int:
        """PubMed検索のヒット件数を取得"""
        params = {
            'db': 'pubmed',
            'term': query,
            'retmode': 'xml',
            'retmax': 0  # 件数のみ取得
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
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"Failed to get count for query: {query[:100]}...")
                    return -1

        return -1

    def analyze_block_with_filters(self, population: str, block_query: str, block_name: str) -> Dict[str, int]:
        """
        1つのブロックに対して、段階的にフィルターを適用して件数を測定

        Args:
            population: #1 Population query
            block_query: 個別ブロックのクエリ (e.g., #2A, #2B, etc.)
            block_name: ブロック名（表示用）

        Returns:
            各フィルター適用時の件数を含む辞書
        """
        print(f"\n{'='*60}")
        print(f"Analyzing: {block_name}")
        print(f"{'='*60}")

        results = {}

        # Base query (no filters)
        base_query = f"({population}) AND ({block_query})"
        print(f"\n[1/7] Base query (no filters)...")
        results['base'] = self.get_count(base_query)
        print(f"  → {results['base']:,} hits")

        # Filter 1: Past 10 years
        filter_10y = '("2015/01/01"[PDAT] : "3000"[PDAT])'
        query_10y = f"{base_query} AND {filter_10y}"
        print(f"\n[2/7] + Past 10 years filter...")
        results['10years'] = self.get_count(query_10y)
        reduction_10y = results['base'] - results['10years']
        pct_10y = (reduction_10y / results['base'] * 100) if results['base'] > 0 else 0
        print(f"  → {results['10years']:,} hits (-{reduction_10y:,}, -{pct_10y:.1f}%)")

        # Filter 2: Animal exclusion
        filter_animal = 'NOT (animals[Mesh] NOT humans[Mesh])'
        query_animal = f"{base_query} {filter_animal}"
        print(f"\n[3/7] + Animal exclusion...")
        results['no_animal'] = self.get_count(query_animal)
        reduction_animal = results['base'] - results['no_animal']
        pct_animal = (reduction_animal / results['base'] * 100) if results['base'] > 0 else 0
        print(f"  → {results['no_animal']:,} hits (-{reduction_animal:,}, -{pct_animal:.1f}%)")

        # Filter 3: Both (10y + animal)
        query_both = f"{base_query} AND {filter_10y} {filter_animal}"
        print(f"\n[4/7] + Both (10y + animal)...")
        results['10y_no_animal'] = self.get_count(query_both)
        reduction_both = results['base'] - results['10y_no_animal']
        pct_both = (reduction_both / results['base'] * 100) if results['base'] > 0 else 0
        print(f"  → {results['10y_no_animal']:,} hits (-{reduction_both:,}, -{pct_both:.1f}%)")

        # Filter 4: + Humans
        filter_humans = 'AND Humans[Mesh]'
        query_humans = f"{query_both} {filter_humans}"
        print(f"\n[5/7] + Humans[Mesh]...")
        results['with_humans'] = self.get_count(query_humans)
        reduction_humans = results['10y_no_animal'] - results['with_humans']
        pct_humans = (reduction_humans / results['10y_no_animal'] * 100) if results['10y_no_animal'] > 0 else 0
        print(f"  → {results['with_humans']:,} hits (-{reduction_humans:,}, -{pct_humans:.1f}%)")

        # Filter 5: + Language
        filter_lang = 'AND (English[lang] OR Japanese[lang])'
        query_lang = f"{query_humans} {filter_lang}"
        print(f"\n[6/7] + Language (EN/JA)...")
        results['with_lang'] = self.get_count(query_lang)
        reduction_lang = results['with_humans'] - results['with_lang']
        pct_lang = (reduction_lang / results['with_humans'] * 100) if results['with_humans'] > 0 else 0
        print(f"  → {results['with_lang']:,} hits (-{reduction_lang:,}, -{pct_lang:.1f}%)")

        # Filter 6: + Publication Type exclusion
        filter_pubtype = 'NOT (Editorial[PT] OR Letter[PT] OR Comment[PT])'
        query_pubtype = f"{query_lang} {filter_pubtype}"
        print(f"\n[7/7] + Pub Type exclusion...")
        results['with_pubtype'] = self.get_count(query_pubtype)
        reduction_pubtype = results['with_lang'] - results['with_pubtype']
        pct_pubtype = (reduction_pubtype / results['with_lang'] * 100) if results['with_lang'] > 0 else 0
        print(f"  → {results['with_pubtype']:,} hits (-{reduction_pubtype:,}, -{pct_pubtype:.1f}%)")

        # Summary
        total_reduction = results['base'] - results['with_pubtype']
        total_pct = (total_reduction / results['base'] * 100) if results['base'] > 0 else 0
        print(f"\n{'─'*60}")
        print(f"TOTAL REDUCTION: {results['base']:,} → {results['with_pubtype']:,}")
        print(f"                 (-{total_reduction:,}, -{total_pct:.1f}%)")
        print(f"{'─'*60}")

        return results


def main():
    """メイン処理"""

    # Population query (#1)
    population = '"Physicians"[Mesh] OR physician*[tiab] OR doctor*[tiab] OR "general practitioner*"[tiab] OR clinician*[tiab]'

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

    analyzer = FilterImpactAnalyzer()

    all_results = {}

    # 各ブロックを分析
    for block_name, block_query in blocks.items():
        results = analyzer.analyze_block_with_filters(population, block_query, block_name)
        all_results[block_name] = results
        time.sleep(1)  # ブロック間で少し待つ

    # マークダウンレポート生成
    print("\n\n" + "="*80)
    print("GENERATING MARKDOWN REPORT")
    print("="*80)

    report = generate_markdown_report(all_results, blocks)

    # 出力
    output_dir = r'c:\Users\youki\codes\search-formula-developper\search_formula\yarigai_scoping_review'
    output_file = os.path.join(output_dir, 'filter_impact_analysis.md')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\nReport saved to: {output_file}")


def generate_markdown_report(all_results: Dict[str, Dict[str, int]], blocks: Dict[str, str]) -> str:
    """マークダウンレポートを生成"""

    lines = []
    lines.append("# フィルター効果分析レポート")
    lines.append("")
    lines.append(f"生成日時: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("## 分析目的")
    lines.append("")
    lines.append("検索結果を2桁絞り込むために、各種フィルターの効果を段階的に測定。")
    lines.append("")
    lines.append("## フィルター適用順序")
    lines.append("")
    lines.append("1. **Base**: フィルターなし (#1 AND #2X)")
    lines.append("2. **+10 years**: 過去10年フィルター追加")
    lines.append("3. **+Animal**: 動物除外フィルター追加")
    lines.append("4. **Both**: 10年 + 動物除外")
    lines.append("5. **+Humans**: Humans[Mesh]追加")
    lines.append("6. **+Language**: English OR Japanese追加")
    lines.append("7. **+PubType**: Editorial/Letter/Comment除外")
    lines.append("")
    lines.append("---")
    lines.append("")

    # サマリーテーブル
    lines.append("## サマリーテーブル")
    lines.append("")
    lines.append("| Block | Base | +10y | +Animal | Both | +Humans | +Lang | +PubType | Total Reduction |")
    lines.append("|-------|------|------|---------|------|---------|-------|----------|-----------------|")

    total_base = 0
    total_final = 0

    for block_name in blocks.keys():
        results = all_results.get(block_name, {})
        base = results.get('base', 0)
        final = results.get('with_pubtype', 0)
        reduction = base - final
        pct = (reduction / base * 100) if base > 0 else 0

        total_base += base
        total_final += final

        lines.append(f"| {block_name} | {base:,} | {results.get('10years', 0):,} | {results.get('no_animal', 0):,} | {results.get('10y_no_animal', 0):,} | {results.get('with_humans', 0):,} | {results.get('with_lang', 0):,} | {final:,} | -{reduction:,} ({pct:.1f}%) |")

    # 合計行
    total_reduction = total_base - total_final
    total_pct = (total_reduction / total_base * 100) if total_base > 0 else 0
    lines.append(f"| **TOTAL** | **{total_base:,}** | - | - | - | - | - | **{total_final:,}** | **-{total_reduction:,} ({total_pct:.1f}%)** |")

    lines.append("")
    lines.append("---")
    lines.append("")

    # 各ブロックの詳細
    lines.append("## 各ブロック詳細")
    lines.append("")

    for block_name, block_query in blocks.items():
        results = all_results.get(block_name, {})
        lines.append(f"### {block_name}")
        lines.append("")
        lines.append("**検索式:**")
        lines.append("```")
        lines.append(block_query)
        lines.append("```")
        lines.append("")

        base = results.get('base', 0)

        lines.append("| Filter Stage | Hit Count | Reduction from Previous | Reduction from Base |")
        lines.append("|--------------|-----------|-------------------------|---------------------|")

        stages = [
            ('Base', 'base'),
            ('+10 years', '10years'),
            ('+Animal', 'no_animal'),
            ('Both (10y+Animal)', '10y_no_animal'),
            ('+Humans', 'with_humans'),
            ('+Language', 'with_lang'),
            ('+PubType', 'with_pubtype')
        ]

        prev_count = base
        for stage_name, key in stages:
            count = results.get(key, 0)
            diff = prev_count - count
            diff_pct = (diff / prev_count * 100) if prev_count > 0 else 0
            base_diff = base - count
            base_pct = (base_diff / base * 100) if base > 0 else 0

            if stage_name == 'Base':
                lines.append(f"| {stage_name} | {count:,} | - | - |")
            else:
                lines.append(f"| {stage_name} | {count:,} | -{diff:,} ({diff_pct:.1f}%) | -{base_diff:,} ({base_pct:.1f}%) |")

            prev_count = count

        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 結論と推奨事項")
    lines.append("")
    lines.append("### 最も効果的なフィルター")
    lines.append("")
    lines.append("各フィルターの平均削減率（全ブロック平均）:")
    lines.append("")

    # 各フィルターの効果を計算
    filter_effects = calculate_filter_effects(all_results, blocks)

    lines.append("| Filter | Avg Reduction % | Comment |")
    lines.append("|--------|-----------------|---------|")
    for filter_name, avg_pct in sorted(filter_effects.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"| {filter_name} | {avg_pct:.1f}% | |")

    lines.append("")
    lines.append("### 推奨フィルター組み合わせ")
    lines.append("")
    lines.append("- **Conservative (保守的)**: 10年 + 動物除外 → 約X%削減")
    lines.append("- **Moderate (中程度)**: 上記 + Humans + Language → 約Y%削減")
    lines.append("- **Aggressive (積極的)**: 上記 + PubType除外 → 約Z%削減")
    lines.append("")

    return "\n".join(lines)


def calculate_filter_effects(all_results: Dict[str, Dict[str, int]], blocks: Dict[str, str]) -> Dict[str, float]:
    """各フィルターの平均削減率を計算"""

    effects = {
        '10 years': [],
        'Animal exclusion': [],
        'Humans': [],
        'Language': [],
        'PubType': []
    }

    for block_name in blocks.keys():
        results = all_results.get(block_name, {})
        base = results.get('base', 0)

        if base == 0:
            continue

        # 10 years
        ten_y = results.get('10years', 0)
        pct_10y = ((base - ten_y) / base * 100) if base > 0 else 0
        effects['10 years'].append(pct_10y)

        # Animal (from base)
        animal = results.get('no_animal', 0)
        pct_animal = ((base - animal) / base * 100) if base > 0 else 0
        effects['Animal exclusion'].append(pct_animal)

        # Humans (from 10y+animal)
        both = results.get('10y_no_animal', 0)
        humans = results.get('with_humans', 0)
        pct_humans = ((both - humans) / both * 100) if both > 0 else 0
        effects['Humans'].append(pct_humans)

        # Language
        lang = results.get('with_lang', 0)
        pct_lang = ((humans - lang) / humans * 100) if humans > 0 else 0
        effects['Language'].append(pct_lang)

        # PubType
        pubtype = results.get('with_pubtype', 0)
        pct_pubtype = ((lang - pubtype) / lang * 100) if lang > 0 else 0
        effects['PubType'].append(pct_pubtype)

    # 平均を計算
    avg_effects = {}
    for filter_name, pct_list in effects.items():
        if pct_list:
            avg_effects[filter_name] = sum(pct_list) / len(pct_list)
        else:
            avg_effects[filter_name] = 0.0

    return avg_effects


if __name__ == '__main__':
    main()
