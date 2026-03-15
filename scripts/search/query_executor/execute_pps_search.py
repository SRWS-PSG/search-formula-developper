import requests
import time
from typing import Dict, List, Tuple
import os
from datetime import datetime

def get_pubmed_results(query: str, retmax: int = 100000) -> Dict:
    """
    PubMed E-utilities APIを使用して検索クエリの結果件数とPMIDを取得する
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    search_url = f"{base_url}/esearch.fcgi"

    params = {
        'db': 'pubmed',
        'term': query,
        'retmode': 'json',
        'retmax': retmax,
        'usehistory': 'y'
    }

    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()

        return {
            'count': int(data['esearchresult'].get('count', 0)),
            'ids': data['esearchresult'].get('idlist', []),
            'query': query,
            'message': 'Success',
            'webenv': data['esearchresult'].get('webenv', ''),
            'querykey': data['esearchresult'].get('querykey', '')
        }

    except requests.exceptions.RequestException as e:
        return {
            'count': 0,
            'ids': [],
            'query': query,
            'message': f'Error: {str(e)}',
            'webenv': '',
            'querykey': ''
        }

def fetch_all_records_medline(pmids: List[str]) -> List[str]:
    """
    PMIDリストから全レコードをMEDLINE形式で取得
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    all_records = []

    # PMIDを100件ずつ処理
    batch_size = 100
    total_batches = (len(pmids) + batch_size - 1) // batch_size

    for i in range(0, len(pmids), batch_size):
        batch_num = i // batch_size + 1
        batch_pmids = pmids[i:i + batch_size]
        print(f"  Batch {batch_num}/{total_batches}: {len(batch_pmids)} records...")

        params = {
            'db': 'pubmed',
            'id': ','.join(batch_pmids),
            'rettype': 'medline',
            'retmode': 'text'
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            medline_data = response.text

            # MEDLINEフォーマットを個別レコードに分割
            entries = medline_data.split('\n\n')
            for entry in entries:
                if entry.strip() and 'PMID-' in entry:
                    all_records.append(entry)

        except requests.exceptions.RequestException as e:
            print(f"    Error fetching batch {batch_num}: {str(e)}")

        # API制限を考慮して待機
        time.sleep(0.4)

    return all_records

def export_to_ris(records: List[str], filename: str, output_dir: str) -> None:
    """
    MEDLINEレコードをRISファイルに変換して保存（抄録を含む）
    """
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        for entry in records:
            if not entry.strip():
                continue

            # RISエントリの開始
            f.write('TY  - JOUR\n')

            # タイトルとアブストラクトを蓄積
            title = []
            in_title = False
            abstract = []
            in_abstract = False

            for line in entry.split('\n'):
                if not line.strip():
                    continue

                # タイトル開始
                if line.startswith('TI  -'):
                    # 前のタイトルがあれば出力
                    if title:
                        f.write(f'T1  - {" ".join(title)}\n')
                        title = []
                    in_title = True
                    title.append(line.split('- ', 1)[1] if '- ' in line else '')
                    continue

                # タイトル継続行（先頭がスペースのみ）
                if in_title:
                    if line[:4].strip() and not line.startswith('TI'):
                        # 新しいフィールド開始 = タイトル終了
                        if title:
                            f.write(f'T1  - {" ".join(title)}\n')
                            title = []
                        in_title = False
                    else:
                        # タイトル継続
                        title.append(line.strip())
                        continue

                # アブストラクト開始
                if line.startswith('AB  -'):
                    in_abstract = True
                    abstract.append(line.split('- ', 1)[1] if '- ' in line else '')
                    continue

                # アブストラクト継続行
                if in_abstract:
                    if line[:4].strip() and not line.startswith('AB'):
                        # 新しいフィールド開始 = アブストラクト終了
                        if abstract:
                            f.write(f'AB  - {" ".join(abstract)}\n')
                            abstract = []
                        in_abstract = False
                    else:
                        # アブストラクト継続
                        abstract.append(line.strip())
                        continue

                # その他のフィールド変換
                if line.startswith('PMID-'):
                    f.write(f'ID  - {line.split("- ", 1)[1]}\n')
                elif line.startswith('AU  -'):
                    f.write(f'A1  - {line.split("- ", 1)[1]}\n')
                elif line.startswith('JT  -'):
                    f.write(f'JF  - {line.split("- ", 1)[1]}\n')
                elif line.startswith('DP  -'):
                    f.write(f'Y1  - {line.split("- ", 1)[1]}\n')
                elif line.startswith('VI  -'):
                    f.write(f'VL  - {line.split("- ", 1)[1]}\n')
                elif line.startswith('IP  -'):
                    f.write(f'IS  - {line.split("- ", 1)[1]}\n')
                elif line.startswith('PG  -'):
                    f.write(f'SP  - {line.split("- ", 1)[1]}\n')
                elif line.startswith('DOI -'):
                    f.write(f'DO  - {line.split("- ", 1)[1]}\n')

            # 残っているタイトルを書き込み
            if title:
                f.write(f'T1  - {" ".join(title)}\n')

            # 残っているアブストラクトを書き込み
            if abstract:
                f.write(f'AB  - {" ".join(abstract)}\n')

            # RISエントリの終了
            f.write('ER  -\n\n')

def main():
    # PPS Project の最終検索式
    query_p = '''("Medically Unexplained Symptoms"[Mesh] OR "Somatoform Disorders"[Mesh] OR "Psychophysiologic Disorders"[Mesh] OR "chronic pain"[Mesh] OR "Central Nervous System Sensitization"[Mesh] OR "Nociplastic Pain"[Mesh] OR "Polydipsia, Psychogenic"[Mesh] OR "Psychogenic Nonepileptic Seizures"[Mesh] OR "Hearing Loss, Functional"[Mesh] OR "psychogenic syncope"[Supplementary Concept] OR "Orthostatic Intolerance"[Mesh] OR "somatic cough syndrome"[Supplementary Concept] OR "Fibromyalgia"[Mesh] OR "Fatigue Syndrome, Chronic"[Mesh] OR "Colonic Diseases, Functional"[Mesh] OR "Temporomandibular Joint Dysfunction Syndrome"[Mesh] OR "Cystitis, Interstitial"[Mesh] OR "Multiple Chemical Sensitivity"[Mesh] OR "persistent somatic symptom*"[tiab] OR "persistent physical symptom*"[tiab] OR "medically unexplained symptom*"[tiab] OR "Medically Unexplained Physical Symptom*"[tiab] OR "functional somatic disorder*"[tiab] OR "Somatic symptom disorder*"[tiab] OR "functional somatic syndrome*"[tiab] OR "somatisation"[tiab] OR "somatization"[tiab] OR "bodily distress syndrome*"[tiab] OR "chronic pain"[tiab] OR "Chronic primary pain"[tiab] OR "Chronic widespread pain"[tiab] OR "Functional Pain"[tiab] OR "Central Nervous System Sensitization"[tiab] OR "Nociplastic Pain"[tiab] OR "Psychogenic Polydipsia"[tiab] OR "Psychogenic Nonepileptic Seizure*"[tiab] OR "Functional Hearing Loss"[tiab] OR "psychogenic syncope"[tiab] OR "Orthostatic Intolerance"[tiab] OR "Postural Orthostatic Tachycardia Syndrome"[tiab] OR "somatic cough syndrome*"[tiab] OR "Fibromyalgia"[tiab] OR "Chronic Fatigue Syndrome*"[tiab] OR "Chronic fatigue"[tiab] OR "Irritable bowel syndrome"[tiab] OR "Functional Neurological Disorder*"[tiab] OR "Temporomandibular Joint Dysfunction Syndrome"[tiab] OR "interstitial cystitis"[tiab] OR "dyspareunia"[tiab] OR "Multiple Chemical Sensitivity"[tiab] OR "Disorders of gut brain interaction"[tiab] OR "Myalgic Encephalopathy"[tiab] OR "Myalgic Encephalomyelitis"[tiab] OR "Non-organic"[tiab] OR "Persistent symptoms"[tiab:~2] OR "Functional symptoms"[tiab:~2] OR "Functional syndrome"[tiab:~2] OR "Functional gut"[tiab:~2])'''

    query_c = '''("Narrative Medicine"[Mesh] OR "Narration"[Mesh] OR "Patient-Centered Care"[Mesh] OR "narrative approach*"[tiab] OR "narrative medicine"[tiab] OR "narrative based medicine"[tiab] OR "illness narrative*"[tiab] OR "storytelling"[tiab] OR "meaning making"[tiab] OR "Patient-Centered Care"[tiab] OR "re-authoring"[tiab] OR "expert generalist"[tiab] OR "narrative construction"[tiab] OR "illness experience*"[tiab])'''

    query_context = '''("Primary Health Care"[Mesh] OR "General Practice"[Mesh] OR "Physicians, Family"[Mesh] OR "primary care"[tiab] OR "general practice"[tiab] OR "family practice"[tiab] OR "family medicine"[tiab] OR "general practitioner*"[tiab])'''

    final_query = f"{query_p} AND {query_c} AND {query_context}"

    output_dir = "projects/pps/log"

    print("\n=== PubMed検索式の実行 ===")
    print(f"プロジェクト: PPS Narrative Approach")
    print(f"出力先: {output_dir}\n")

    # 検索実行
    print("検索を実行中...")
    result = get_pubmed_results(final_query, retmax=10000)

    if result['message'] != 'Success':
        print(f"エラー: {result['message']}")
        return

    total_count = result['count']
    pmids = result['ids']

    print(f"[OK] 検索結果総数: {total_count:,}件")
    print(f"[OK] 取得PMID数: {len(pmids):,}件\n")

    # 全レコードを取得（抄録含む）
    print("全レコードを取得中（抄録を含む）...")
    all_records = fetch_all_records_medline(pmids)

    print(f"\n[OK] 総レコード数: {len(all_records):,}件")

    # RISファイルにエクスポート
    if all_records:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        ris_filename = f'pps_pubmed_results_{timestamp}.ris'

        print(f"\nRISファイルを作成中（抄録を含む）...")
        export_to_ris(all_records, ris_filename, output_dir)

        output_path = os.path.join(output_dir, ris_filename)
        print(f"[OK] 保存完了: {output_path}")
        print(f"     レコード数: {len(all_records):,}件")
    else:
        print("\n[WARNING] レコードが見つかりませんでした")

    # サマリーファイルの作成
    summary_filename = f'search_summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
    summary_path = os.path.join(output_dir, summary_filename)

    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(f"# PubMed検索結果サマリー - PPS Narrative Approach\n\n")
        f.write(f"<!--\n")
        f.write(f"Generated by: scripts/search/query_executor/execute_pps_search.py\n")
        f.write(f"Project: Persistent Physical Symptoms and Narrative Approach in Primary Care\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"-->\n\n")
        f.write(f"**検索日時:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**検索式:**\n\n")
        f.write(f"#1 Patient (PPS):\n```\n{query_p}\n```\n\n")
        f.write(f"#2 Concept (Narrative):\n```\n{query_c}\n```\n\n")
        f.write(f"#3 Context (Primary Care):\n```\n{query_context}\n```\n\n")
        f.write(f"**Final Query:** #1 AND #2 AND #3\n\n")
        f.write(f"**結果:**\n")
        f.write(f"- 総ヒット数: {total_count:,}件\n")
        f.write(f"- 取得レコード数: {len(pmids):,}件\n")
        f.write(f"- RISエクスポート数: {len(all_records):,}件\n\n")
        f.write(f"**出力ファイル:**\n")
        f.write(f"- RIS (抄録含む): `{ris_filename}`\n\n")
        f.write(f"**注意:**\n")
        f.write(f"- 抄録はRISファイルに含まれています（AB フィールド）\n")
        f.write(f"- 'sage consultation'[tiab] は削除済み（0ヒット）\n")

    print(f"[OK] サマリー保存完了: {summary_path}\n")
    print("=== 検索完了 ===")

if __name__ == "__main__":
    main()
