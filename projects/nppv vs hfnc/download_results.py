#!/usr/bin/env python3
"""PubMed検索結果をRIS形式でダウンロード"""

import requests
import time
import os
import re
from datetime import datetime

def get_pubmed_results(query: str, retmax: int = 100000):
    """PubMed E-utilities APIを使用して検索クエリの結果を取得"""
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
    """WebEnvとQueryKeyを使って全レコードをMEDLINE形式で取得"""
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
        
        time.sleep(0.4)
    
    return '\n'.join(all_records)


def convert_medline_to_ris(medline_data: str) -> str:
    """MEDLINEフォーマットをRISフォーマットに変換"""
    ris_output = []
    records = re.split(r'\n(?=PMID-)', medline_data)
    
    field_mapping = {
        'PMID': 'ID', 'TI': 'T1', 'AB': 'AB', 'AU': 'AU', 'FAU': 'A1',
        'JT': 'JF', 'TA': 'JA', 'DP': 'Y1', 'VI': 'VL', 'IP': 'IS',
        'PG': 'SP', 'LID': 'DO', 'MH': 'KW', 'OT': 'KW', 'PT': 'M3', 'LA': 'LA'
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
                            value = value.replace('[doi]', '').strip()
                            ris_entry.append(f'{field_mapping[current_field]}  - {value}')
                    else:
                        ris_entry.append(f'{field_mapping[current_field]}  - {value}')
                
                current_field = line[:4].strip()
                current_value = [line[6:]]
            elif line.startswith('      '):
                current_value.append(line.strip())
            elif line.strip() and current_field:
                current_value.append(line.strip())
        
        if current_field and current_field in field_mapping:
            value = ' '.join(current_value).strip()
            if current_field == 'LID':
                if '[doi]' in value:
                    value = value.replace('[doi]', '').strip()
                    ris_entry.append(f'{field_mapping[current_field]}  - {value}')
            else:
                ris_entry.append(f'{field_mapping[current_field]}  - {value}')
        
        ris_entry.append('ER  -')
        ris_entry.append('')
        ris_output.append('\n'.join(ris_entry))
    
    return '\n'.join(ris_output)


def main():
    # 検索式
    query = '''(("high flow nasal cannula"[tiab] OR "high flow oxygen therapy"[tiab] OR "nasal high flow therapy"[tiab] OR "nasal high flow"[tiab] OR hfnc[tiab] OR hfno[tiab] OR "heated humidified high flow"[tiab] OR "Precision Flow"[tiab] OR "HVT"[tiab] OR ProSoft[tiab] OR Optiflow[tiab] OR AIRVO[tiab]) AND ("Respiratory Insufficiency"[Mesh] OR "Respiratory Failure"[tiab] OR "Acute respiratory failure"[tiab] OR hypercapnia[Mesh] OR hypercapnia[tiab] OR hypercapnic[tiab])) AND ((randomized controlled trial[pt] OR controlled clinical trial[pt] OR randomized[tiab] OR placebo[tiab] OR drug therapy[sh] OR randomly[tiab] OR trial[tiab] OR groups[tiab]) NOT (animals[mh] NOT humans[mh]))'''
    
    output_dir = "projects/nppv vs hfnc"
    
    print("=" * 60)
    print("PubMed Search Results Download")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 検索実行
    print("\nExecuting search...")
    result = get_pubmed_results(query)
    total_count = result['count']
    
    print(f"Total results: {total_count:,}")
    
    if total_count == 0:
        print("No results found.")
        return
    
    if not result['webenv']:
        print("Error: Could not obtain WebEnv for batch download.")
        return
    
    # 全レコードを取得
    print("\nRetrieving all records with abstracts...")
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
    filepath = os.path.join(output_dir, filename)
    
    # ファイルに保存
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(ris_data)
    
    print(f"\n{'='*60}")
    print(f"✅ Download complete!")
    print(f"   File: {filepath}")
    print(f"   Records: {total_count:,}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
