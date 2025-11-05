import requests
import time
from typing import Dict, List
import argparse
import os

def get_pubmed_count(query: str) -> Dict[str, any]:
    """
    PubMed E-utilities APIを使用して検索クエリの結果件数を取得する

    Args:
        query: PubMed検索クエリ

    Returns:
        Dict: {
            'count': int,
            'query': str,
            'message': str
        }
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    search_url = f"{base_url}/esearch.fcgi"

    params = {
        'db': 'pubmed',
        'term': query,
        'retmode': 'json'
    }

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()

        return {
            'count': int(data['esearchresult'].get('count', 0)),
            'query': query,
            'message': 'Success'
        }

    except requests.exceptions.RequestException as e:
        return {
            'count': 0,
            'query': query,
            'message': f'Error: {str(e)}'
        }

def main():
    parser = argparse.ArgumentParser(
        description="医師(#1) × 各コンセプトブロック(#2A-#2J)の組み合わせでヒット件数を取得します。"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        required=True,
        help="結果を保存するMarkdownファイルのパス"
    )
    parser.add_argument(
        "--optimized",
        action="store_true",
        help="最適化版の検索式を使用する"
    )

    args = parser.parse_args()

    # 出力ディレクトリが存在しない場合は作成
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # #1 Population (医師)
    if args.optimized:
        physician_block = '("Physicians"[Mesh] OR physician*[tiab] OR doctor*[tiab] OR "general practitioner*"[tiab] OR clinician*[tiab])'
    else:
        physician_block = '("Physicians"[Mesh] OR "General Practitioners"[Mesh] OR physician*[tiab] OR doctor*[tiab] OR "general practitioner*"[tiab] OR clinician*[tiab] OR "medical doctor*"[tiab])'

    # コンセプトブロックの定義
    if args.optimized:
        concept_blocks = {
            "#2A MeSH用語（やりがい関連）": '("Personal Satisfaction"[Mesh] OR "Job Satisfaction"[Mesh] OR "Motivation"[Mesh] OR "Professional Role"[Mesh] OR "Professional Autonomy"[Mesh] OR "Career Choice"[Mesh])',
            "#2B Meaningful Work関連": '("meaningful work"[tiab] OR "work meaningfulness"[tiab] OR "meaningfulness of work"[tiab] OR "meaning in work"[tiab] OR "work meaning"[tiab] OR "sense of meaning"[tiab])',
            "#2C Work Engagement関連": '("work engagement"[tiab] OR vigor[tiab] OR dedication[tiab] OR absorption[tiab])',
            "#2D Calling/Vocation関連": '(calling[tiab] OR vocation*[tiab])',
            "#2E Motivation関連": '("intrinsic motivation"[tiab] OR motivat*[tiab])',
            "#2F Satisfaction関連": '("job satisfaction"[tiab] OR "work satisfaction"[tiab] OR "career satisfaction"[tiab] OR "professional satisfaction"[tiab] OR "compassion satisfaction"[tiab])',
            "#2G Professional Fulfillment/Quality of Life": '("professional fulfillment"[tiab] OR "professional quality of life"[tiab] OR "quality of professional life"[tiab] OR fulfillment[tiab] OR fulfilment[tiab])',
            "#2H 日本語概念": '(ikigai[tiab])',
            "#2I 心理的ニーズ/Thriving": '("psychological need*"[tiab] OR autonomy[tiab] OR competence[tiab] OR relatedness[tiab] OR "thriving at work"[tiab] OR thriving[tiab])',
            "#2J Task Significance": '("task significance"[tiab] OR "meaningful task*"[tiab] OR "work significance"[tiab])'
        }
    else:
        concept_blocks = {
            "#2A MeSH用語（やりがい関連）": '("Personal Satisfaction"[Mesh] OR "Job Satisfaction"[Mesh] OR "Motivation"[Mesh] OR "Work Engagement"[Mesh] OR "Professional Role"[Mesh] OR "Professional Autonomy"[Mesh] OR "Career Choice"[Mesh] OR "Vocation"[Mesh])',
            "#2B Meaningful Work関連": '("meaningful work"[tiab] OR "work meaningfulness"[tiab] OR "meaningfulness of work"[tiab] OR "meaning in work"[tiab] OR "work meaning"[tiab] OR "sense of meaning"[tiab])',
            "#2C Work Engagement関連": '("work engagement"[tiab] OR vigor[tiab] OR dedication[tiab] OR absorption[tiab] OR "engaged at work"[tiab])',
            "#2D Calling/Vocation関連": '(calling[tiab] OR "career calling"[tiab] OR "vocational calling"[tiab] OR vocation*[tiab] OR "calling orientation"[tiab])',
            "#2E Motivation関連": '("prosocial motivation"[tiab] OR "intrinsic motivation"[tiab] OR "work motivation"[tiab] OR motivat*[tiab])',
            "#2F Satisfaction関連": '("job satisfaction"[tiab] OR "work satisfaction"[tiab] OR "career satisfaction"[tiab] OR "professional satisfaction"[tiab] OR "compassion satisfaction"[tiab])',
            "#2G Professional Fulfillment/Quality of Life": '("professional fulfillment"[tiab] OR "professional quality of life"[tiab] OR "quality of professional life"[tiab] OR fulfillment[tiab] OR fulfilment[tiab])',
            "#2H 日本語概念": '(yarigai[tiab] OR ikigai[tiab])',
            "#2I 心理的ニーズ/Thriving": '("psychological need*"[tiab] OR autonomy[tiab] OR competence[tiab] OR relatedness[tiab] OR "thriving at work"[tiab] OR thriving[tiab])',
            "#2J Task Significance": '("task significance"[tiab] OR "meaningful task*"[tiab] OR "work significance"[tiab])'
        }

    print(f"\n医師ブロック × 各コンセプトブロックの検索件数を取得します...")
    print(f"使用する検索式: {'最適化版' if args.optimized else 'オリジナル版'}\n")

    # 医師ブロック単独のヒット件数
    print(f"[0/11] #1 Population (医師) 単独のヒット件数を取得中...")
    time.sleep(0.4)
    physician_only_result = get_pubmed_count(physician_block)
    physician_only_count = physician_only_result['count']
    print(f"  #1のみ: {physician_only_count:,} 件\n")

    results = []

    for idx, (block_name, concept_query) in enumerate(concept_blocks.items(), 1):
        print(f"[{idx}/10] {block_name} を検索中...")

        # #1 AND #2X の件数を取得
        combined_query = f"{physician_block} AND {concept_query}"
        time.sleep(0.4)
        combined_result = get_pubmed_count(combined_query)
        individual_count = combined_result['count']

        results.append({
            'block_name': block_name,
            'individual_count': individual_count
        })

        print(f"  #1 AND {block_name}: {individual_count:,} 件\n")

    # Markdownレポートを生成
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(f"# Physician × Concept Combination Analysis\n\n")
        f.write(f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Search Formula Version: {'Optimized' if args.optimized else 'Original'}\n\n")

        # #1 単独の件数
        f.write(f"## #1 Population (Physicians) - Baseline\n\n")
        f.write(f"Total papers matching physician criteria: **{physician_only_count:,}**\n\n")

        # 組み合わせ結果のテーブル
        f.write(f"## #1 AND Each Concept Block\n\n")
        f.write("| Block | #1 AND Block |\n")
        f.write("|-------|-------------|\n")

        for result in results:
            individual = result['individual_count']
            f.write(f"| {result['block_name']} | {individual:,} |\n")

        # サマリー
        f.write(f"\n## Summary\n\n")

        # 最も効果的なブロック
        if results:
            max_individual = max(results, key=lambda x: x['individual_count'])
            f.write(f"- **Largest block**: {max_individual['block_name']} ({max_individual['individual_count']:,} papers)\n")

            min_individual = min(results, key=lambda x: x['individual_count'])
            f.write(f"- **Smallest block**: {min_individual['block_name']} ({min_individual['individual_count']:,} papers)\n")

            total_individual = sum([r['individual_count'] for r in results])
            f.write(f"- **Sum of all blocks** (with overlap): {total_individual:,} papers\n\n")

        # 注意事項
        f.write(f"## Note\n\n")
        f.write(f"Each count represents **#1 AND [Block]** independently.\n")
        f.write(f"The actual combined query **#1 AND (#2A OR #2B OR ... OR #2J)** will have fewer papers than the sum due to overlap between blocks.\n")

    print(f"\n[OK] 分析完了! 結果を {args.output} に保存しました。")

if __name__ == "__main__":
    main()
