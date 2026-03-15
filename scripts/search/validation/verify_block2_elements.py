#!/usr/bin/env python3
"""
PubMed検索式 #2ブロック（Intervention）の各要素を検証するスクリプト

目的:
- #2の各要素のヒット数を測定
- シード論文がどの要素でマッチするか確認
- 削除可能な要素を特定
"""

import requests
import time
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple
import os
from datetime import datetime


class PubMedAnalyzer:
    """PubMed API を使用して検索件数とPMIDマッチングを行う"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get('NCBI_API_KEY')
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
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
                response = requests.get(
                    f"{self.base_url}/esearch.fcgi",
                    params=params,
                    timeout=30
                )
                response.raise_for_status()

                root = ET.fromstring(response.content)
                count_elem = root.find('.//Count')

                if count_elem is not None:
                    return int(count_elem.text)
                else:
                    print(f"Warning: No count found for query: {query[:80]}...")
                    return 0

            except Exception as e:
                print(f"Attempt {attempt + 1}/{retries} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    print(f"Failed to get count for query: {query[:80]}...")
                    return -1

        return -1

    def check_pmid_match(self, query: str, pmid: str) -> bool:
        """指定したPMIDが検索式にマッチするか確認"""
        check_query = f"({query}) AND {pmid}[pmid]"
        count = self.get_count(check_query)
        return count > 0


def main():
    """メイン処理"""

    # #1ブロック（Population - 対象者）
    block1 = (
        '"Faculty, Medical"[Mesh] OR medical faculty[tiab] OR '
        'clinical educator*[tiab] OR clinician educator*[tiab] OR '
        'medical educator*[tiab] OR clinical teacher*[tiab] OR '
        'clinical teaching[tiab]'
    )

    # #2ブロックの各要素
    block2_elements = {
        '#2a "Staff Development"[Mesh]': '"Staff Development"[Mesh]',
        '#2b "Program Development"[Mesh]': '"Program Development"[Mesh]',
        '#2c faculty development*[tiab]': 'faculty development*[tiab]',
        '#2d professional development*[tiab]': 'professional development*[tiab]',
        '#2e teaching skill*[tiab]': 'teaching skill*[tiab]',
        '#2f "program design"[tiab]': '"program design"[tiab]',
    }

    # 完全な#2ブロック
    block2_full = (
        '"Staff Development"[Mesh] OR "Program Development"[Mesh] OR '
        'faculty development*[tiab] OR professional development*[tiab] OR '
        'teaching skill*[tiab] OR "program design"[tiab]'
    )

    # シード論文
    seed_pmids = ['35173512', '19811202', '21821215', '38442199', '21869655']

    analyzer = PubMedAnalyzer()

    print("=" * 80)
    print("PubMed検索式 #2ブロック分析")
    print("=" * 80)
    print(f"\n開始時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    results = {}

    # Step 1: 各要素の単独ヒット数
    print("\n" + "=" * 80)
    print("Step 1: 各#2要素の単独ヒット数")
    print("=" * 80)

    for name, query in block2_elements.items():
        count = analyzer.get_count(query)
        print(f"  {name}: {count:,} hits")
        results[name] = {'solo': count}

    # Step 2: #1 AND 各要素の件数
    print("\n" + "=" * 80)
    print("Step 2: #1 AND 各#2要素の件数")
    print("=" * 80)

    for name, query in block2_elements.items():
        combined = f"({block1}) AND ({query})"
        count = analyzer.get_count(combined)
        print(f"  #1 AND {name}: {count:,} hits")
        results[name]['with_block1'] = count

    # Step 3: 完全な#3の件数
    print("\n" + "=" * 80)
    print("Step 3: 完全な#3（#1 AND #2）の件数")
    print("=" * 80)

    block3_full = f"({block1}) AND ({block2_full})"
    count_full = analyzer.get_count(block3_full)
    print(f"  #3 (full): {count_full:,} hits")

    # Step 4: 各要素を削除した場合の#3件数
    print("\n" + "=" * 80)
    print("Step 4: 各要素を削除した場合の#3件数")
    print("=" * 80)

    for name, query in block2_elements.items():
        # その要素を除いた#2を構築
        remaining_queries = [q for n, q in block2_elements.items() if n != name]
        block2_minus = ' OR '.join(remaining_queries)
        block3_minus = f"({block1}) AND ({block2_minus})"

        count = analyzer.get_count(block3_minus)
        reduction = count_full - count
        pct = (reduction / count_full * 100) if count_full > 0 else 0

        print(f"  Without {name}: {count:,} hits (削減: {reduction:,}, {pct:.1f}%)")
        results[name]['without'] = count
        results[name]['reduction'] = reduction
        results[name]['reduction_pct'] = pct

    # Step 5: シード論文のマッチング確認
    print("\n" + "=" * 80)
    print("Step 5: シード論文(5件)のマッチング確認")
    print("=" * 80)

    seed_results = {}
    for pmid in seed_pmids:
        seed_results[pmid] = {}
        print(f"\n  PMID: {pmid}")

        for name, query in block2_elements.items():
            match = analyzer.check_pmid_match(query, pmid)
            seed_results[pmid][name] = match
            status = "✓" if match else "✗"
            print(f"    {name}: {status}")

    # レポート生成
    print("\n" + "=" * 80)
    print("レポート生成中...")
    print("=" * 80)

    report = generate_report(results, seed_results, count_full, block2_elements, seed_pmids)

    # 出力
    output_dir = r'c:\Users\youki\codes\search-formula-developper\projects\fd_review'
    output_file = os.path.join(output_dir, 'block2_analysis.md')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\nレポート保存先: {output_file}")
    print(f"完了時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def generate_report(
    results: Dict,
    seed_results: Dict,
    count_full: int,
    block2_elements: Dict,
    seed_pmids: List[str]
) -> str:
    """マークダウンレポートを生成"""

    lines = []
    lines.append("# PubMed検索式 #2ブロック分析レポート")
    lines.append("")
    lines.append(f"生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    # 現在の#2ブロック
    lines.append("## 現在の#2ブロック（Intervention）")
    lines.append("")
    lines.append("```")
    lines.append('"Staff Development"[Mesh] OR "Program Development"[Mesh] OR')
    lines.append('faculty development*[tiab] OR professional development*[tiab] OR')
    lines.append('teaching skill*[tiab] OR "program design"[tiab]')
    lines.append("```")
    lines.append("")

    # 完全な#3の件数
    lines.append("## 完全な#3（#1 AND #2）の件数")
    lines.append("")
    lines.append(f"**{count_full:,} hits**")
    lines.append("")

    # 各要素の分析
    lines.append("---")
    lines.append("")
    lines.append("## 各要素の分析")
    lines.append("")
    lines.append("| 要素 | 単独件数 | #1 AND 要素 | 削除時#3 | 削減量 | 削減率 |")
    lines.append("|------|----------|-------------|----------|--------|--------|")

    for name in block2_elements.keys():
        data = results[name]
        lines.append(
            f"| {name} | {data['solo']:,} | {data['with_block1']:,} | "
            f"{data['without']:,} | {data['reduction']:,} | {data['reduction_pct']:.1f}% |"
        )

    lines.append("")

    # シード論文マッチング
    lines.append("---")
    lines.append("")
    lines.append("## シード論文マッチング")
    lines.append("")
    lines.append("各シード論文がどの#2要素にマッチするか:")
    lines.append("")

    # ヘッダー
    header = "| PMID |"
    separator = "|------|"
    for name in block2_elements.keys():
        short_name = name.split()[0]  # #2a, #2b, etc.
        header += f" {short_name} |"
        separator += "------|"

    lines.append(header)
    lines.append(separator)

    for pmid in seed_pmids:
        row = f"| {pmid} |"
        for name in block2_elements.keys():
            match = seed_results[pmid][name]
            row += " ✓ |" if match else " ✗ |"
        lines.append(row)

    lines.append("")

    # 要素別マッチ数
    lines.append("### 要素別マッチ数")
    lines.append("")
    lines.append("| 要素 | マッチ数 | 必須性 |")
    lines.append("|------|----------|--------|")

    for name in block2_elements.keys():
        match_count = sum(1 for pmid in seed_pmids if seed_results[pmid][name])
        if match_count == 0:
            necessity = "❌ 削除可能"
        elif match_count <= 2:
            necessity = "⚠️ 要検討"
        else:
            necessity = "✅ 必須"
        lines.append(f"| {name} | {match_count}/5 | {necessity} |")

    lines.append("")

    # 削除候補の推奨
    lines.append("---")
    lines.append("")
    lines.append("## 削除候補の推奨")
    lines.append("")

    # 削除可能な要素を特定
    removable = []
    for name in block2_elements.keys():
        match_count = sum(1 for pmid in seed_pmids if seed_results[pmid][name])
        if match_count == 0:
            removable.append(name)

    if removable:
        lines.append("### 削除可能な要素（シード論文にマッチしない）")
        lines.append("")
        for name in removable:
            data = results[name]
            lines.append(f"- **{name}**: 削除で {data['reduction']:,}件削減可能 ({data['reduction_pct']:.1f}%)")
        lines.append("")
    else:
        lines.append("> すべての要素がシード論文にマッチしています。単純な削除は推奨されません。")
        lines.append("")

    # 次のステップ
    lines.append("---")
    lines.append("")
    lines.append("## 次のステップ")
    lines.append("")
    lines.append("1. 削除可能な要素を確認し、削除版#2で再テスト")
    lines.append("2. シード論文を個別に確認し、削除要素が本当に不要か確認")
    lines.append("3. 修正版#3で最終件数確認")
    lines.append("")

    return "\n".join(lines)


if __name__ == '__main__':
    main()
