#!/usr/bin/env python3
"""
greenICU PubMed検索実行スクリプト

search.mdの検索式を実行し、結果をRIS形式で保存します。
"""

import requests
import time
import os
import re
from datetime import datetime
from pathlib import Path


def get_pubmed_results(query: str, retmax: int = 100000):
    """PubMed E-utilities APIを使用して検索クエリの結果件数とPMIDを取得する"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    params = {
        'db': 'pubmed',
        'term': query,
        'retmax': retmax,
        'retmode': 'json',
        'usehistory': 'y'
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()
    
    result = data.get('esearchresult', {})
    return {
        'count': int(result.get('count', 0)),
        'pmids': result.get('idlist', []),
        'webenv': result.get('webenv', ''),
        'query_key': result.get('querykey', '')
    }


def fetch_pubmed_records(webenv: str, query_key: str, total: int, batch_size: int = 200) -> str:
    """WebEnvとQueryKeyを使って全レコードをMEDLINE形式で取得する"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    all_records = []
    
    for start in range(0, total, batch_size):
        print(f"  Fetching records {start + 1} - {min(start + batch_size, total)} of {total}...")
        
        params = {
            'db': 'pubmed',
            'query_key': query_key,
            'WebEnv': webenv,
            'retstart': start,
            'retmax': batch_size,
            'rettype': 'medline',
            'retmode': 'text'
        }
        
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        all_records.append(response.text)
        
        time.sleep(0.4)  # API制限を考慮
    
    return '\n'.join(all_records)


def convert_medline_to_ris(medline_data: str) -> str:
    """MEDLINEフォーマットをRISフォーマットに変換する"""
    ris_output = []
    records = re.split(r'\n(?=PMID-)', medline_data)
    
    field_mapping = {
        'PMID': 'ID',
        'TI': 'T1',
        'AB': 'AB',
        'AU': 'AU',
        'FAU': 'A1',
        'JT': 'JF',
        'TA': 'JA',
        'DP': 'Y1',
        'VI': 'VL',
        'IP': 'IS',
        'PG': 'SP',
        'LID': 'DO',
        'MH': 'KW',
        'OT': 'KW',
        'PT': 'M3',
        'LA': 'LA',
    }
    
    for record in records:
        if not record.strip():
            continue
        
        ris_entry = ['TY  - JOUR']
        current_field = None
        current_value = []
        
        for line in record.split('\n'):
            if len(line) >= 4 and line[4:6] == '- ':
                if current_field and current_field in field_mapping:
                    value = ' '.join(current_value).strip()
                    if current_field == 'LID':
                        if '[doi]' in value:
                            doi = value.replace('[doi]', '').strip()
                            ris_entry.append(f'{field_mapping[current_field]}  - {doi}')
                    else:
                        ris_entry.append(f'{field_mapping[current_field]}  - {value}')
                
                current_field = line[:4].strip()
                current_value = [line[6:]]
            elif line.startswith('      '):
                current_value.append(line.strip())
            elif line.strip() and current_field:
                current_value.append(line.strip())
        
        # 最後のフィールドを処理
        if current_field and current_field in field_mapping:
            value = ' '.join(current_value).strip()
            if current_field == 'LID':
                if '[doi]' in value:
                    doi = value.replace('[doi]', '').strip()
                    ris_entry.append(f'{field_mapping[current_field]}  - {doi}')
            else:
                ris_entry.append(f'{field_mapping[current_field]}  - {value}')
        
        ris_entry.append('ER  -')
        ris_entry.append('')
        ris_output.append('\n'.join(ris_entry))
    
    return '\n'.join(ris_output)


def build_query():
    """search.mdの検索式を組み立てる"""
    
    # #1 ICU/critical care
    p1 = '''
    "Intensive Care Units"[Mesh] OR
    "Critical Care"[Mesh] OR
    "Critical Illness"[Mesh] OR
    icu[tiab] OR
    "intensive care"[tiab] OR
    "critical care"[tiab] OR
    perioperative[tiab] OR
    "Lancet Respiratory Medicine"[Journal] OR
    "Intensive Care Medicine"[Journal] OR
    "American Journal of Respiratory and Critical Care Medicine"[Journal] OR
    "Critical Care"[Journal] OR
    "Chest"[Journal] OR
    "Critical Care Medicine"[Journal] OR
    "Annals of Intensive Care"[Journal] OR
    "Intensive and Critical Care Nursing"[Journal] OR
    "Anaesthesia Critical Care & Pain Medicine"[Journal] OR
    "Journal of Intensive Care"[Journal]
    '''.replace('\n', ' ').strip()
    
    # #2 Environmental/quality terms
    p2 = '''
    "Carbon Footprint"[Mesh] OR
    "Medical Waste"[Mesh] OR
    "Recycling"[Mesh] OR "Climate Change"[MeSH] OR 
    "climate change"[tiab] OR
    "carbon footprint"[tiab] OR
    "planetary health"[tiab] OR
    "green ICU"[tiab] OR
    "green team"[tiab] OR
    "sustainability team"[tiab] OR
    "life cycle assessment"[tiab] OR
    "material flow"[tiab] OR
    planet[tiab] OR
    "environmental impact"[tiab] OR
    "waste reduction"[tiab] OR
    "medical waste"[tiab] OR
    (green[tiab] AND (ICU[tiab] OR "intensive care"[tiab])) OR
    (waste[tiab] AND (reduction[tiab] OR audit[tiab])) OR
    (carbon[tiab] AND footprint[tiab]) OR
    (("Quality Improvement"[Mesh] OR "Medical Audit"[Mesh] OR "quality improvement"[tiab] OR audit[tiab]) AND
     (carbon[tiab] OR footprint[tiab] OR waste[tiab] OR environmental[tiab] OR climate[tiab] OR sustainability[tiab]))
    '''.replace('\n', ' ').strip()
    
    # #3 Drug/procedure + planet/audit/reduction
    p3 = '''
    (("Acetaminophen"[Mesh] OR paracetamol[tiab] OR acetaminophen[tiab]) OR
     ("beta-Lactams"[Mesh] OR "beta-lactam"[tiab]) OR
     ("Phlebotomy"[Mesh] OR phlebotomy[tiab])) AND
    (planet[tiab] OR "Quality Improvement"[Mesh] OR "Medical Audit"[Mesh] OR "quality improvement"[tiab] OR audit[tiab] OR reduction[tiab])
    '''.replace('\n', ' ').strip()
    
    # #4 = #1 AND (#2 OR #3)
    return f'({p1}) AND (({p2}) OR ({p3}))'


def main():
    print("=" * 60)
    print("greenICU PubMed Search")
    print("=" * 60)
    
    # 出力ディレクトリ
    script_dir = Path(__file__).parent
    output_dir = script_dir / "pubmed_results"
    output_dir.mkdir(exist_ok=True)
    
    # 検索式を組み立て
    query = build_query()
    print(f"\nQuery length: {len(query)} chars")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 検索実行
    print("\nExecuting search...")
    result = get_pubmed_results(query, retmax=0)
    total_count = result['count']
    
    print(f"Total results: {total_count:,}")
    
    if total_count == 0:
        print("No results found.")
        return 0
    
    # 全件取得
    print("\nRetrieving all records with abstracts...")
    result = get_pubmed_results(query, retmax=total_count)
    
    if not result['webenv']:
        print("Error: Could not obtain WebEnv for batch download.")
        return 1
    
    # レコード取得
    medline_data = fetch_pubmed_records(
        result['webenv'],
        result['query_key'],
        total_count
    )
    
    # RIS形式に変換
    print("\nConverting to RIS format...")
    ris_data = convert_medline_to_ris(medline_data)
    
    # ファイル名を生成
    date_str = datetime.now().strftime('%Y%m%d')
    filename = f"{date_str}_{total_count}_pubmed.ris"
    filepath = output_dir / filename
    
    # 保存
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(ris_data)
    
    print("\n" + "=" * 60)
    print(f"✅ Download complete!")
    print(f"   File: {filepath}")
    print(f"   Records: {total_count:,}")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit(main())
