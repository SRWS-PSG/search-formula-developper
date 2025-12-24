#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Physicians階層下のMeSH term存在確認スクリプト
"""
import requests
import time
from typing import Dict, List, Tuple

def check_mesh_term(term: str) -> Dict:
    """
    PubMed E-utilities APIを使用してMeSH用語の存在を確認する
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    search_url = f"{base_url}/esearch.fcgi"
    
    params = {
        'db': 'mesh',
        'term': term,
        'retmode': 'json'
    }
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        count = int(data['esearchresult'].get('count', 0))
        exists = count > 0
        
        # PubMedでの文献数も確認
        pubmed_params = {
            'db': 'pubmed',
            'term': f'{term}[mh]',
            'retmode': 'json'
        }
        pubmed_response = requests.get(search_url, params=pubmed_params)
        pubmed_response.raise_for_status()
        pubmed_data = pubmed_response.json()
        pubmed_count = int(pubmed_data['esearchresult'].get('count', 0))
        
        return {
            'exists': exists,
            'term': term,
            'mesh_count': count,
            'pubmed_count': pubmed_count,
            'message': 'Success'
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'exists': False,
            'term': term,
            'mesh_count': 0,
            'pubmed_count': 0,
            'message': f'Error: {str(e)}'
        }

def main() -> Tuple[List, List]:
    # ユーザーが指定した19の領域とPhysicians下位MeSH termのマッピング
    # (元のテキスト語, 対応するPhysicians下位MeSH term)
    physician_terms = [
        # 元のテキスト語 -> Physicians下位MeSH
        ("internal medicine", "Physicians"),  # 内科医は汎用
        ("surgery", "Surgeons"),
        ("pediatrics", "Pediatricians"),
        ("psychiatry", "Psychiatrists"),
        ("anesthesiology", "Anesthesiologists"),
        ("urology", "Urologists"),
        ("family medicine", "Physicians, Family"),
        ("emergency medicine", "Physicians"),  # 救急は汎用
        ("general medicine", "General Practitioners"),
        ("orthopedic surgery", "Orthopedic Surgeons"),
        ("obstetrics and gynecology", "Obstetricians"),  # + Gynecologists
        ("neurology", "Neurologists"),
        ("dermatology", "Dermatologists"),
        ("ophthalmology", "Ophthalmologists"),
        ("otolaryngology", "Otolaryngologists"),
        ("radiology", "Radiologists"),
        ("rehabilitation", "Physiatrists"),
    ]
    
    # Physicians下位の全MeSH terms（ユーザー提供リスト）
    all_physician_mesh = [
        "Physicians",
        "Allergists",
        "Anesthesiologists",
        "Cardiologists",
        "Dermatologists",
        "Endocrinologists",
        "Foreign Medical Graduates",
        "Gastroenterologists",
        "General Practitioners",
        "Geriatricians",
        "Gynecologists",
        "Hospitalists",
        "Nephrologists",
        "Neurologists",
        "Obstetricians",
        "Occupational Health Physicians",
        "Oncologists",
        "Radiation Oncologists",
        "Ophthalmologists",
        "Osteopathic Physicians",
        "Otolaryngologists",
        "Pathologists",
        "Pediatricians",
        "Neonatologists",
        "Physiatrists",
        "Physicians, Family",
        "Physicians, Primary Care",
        "Physicians, Women",
        "Psychiatrists",
        "Pulmonologists",
        "Radiologists",
        "Rheumatologists",
        "Surgeons",
        "Barber Surgeons",
        "Neurosurgeons",
        "Oral and Maxillofacial Surgeons",
        "Orthopedic Surgeons",
        "Urologists",
    ]
    
    print("=" * 80)
    print("Physicians階層下 MeSH Term 存在確認")
    print("=" * 80)
    print()
    
    results = []
    
    # 全Physicians下位MeSH termsの確認
    print("### Physicians下位 MeSH Terms ###\n")
    print(f"{'MeSH Term':<40} | {'存在':<5} | {'PubMed件数'}")
    print("-" * 70)
    
    for mesh_term in all_physician_mesh:
        time.sleep(0.4)  # API制限対策
        result = check_mesh_term(mesh_term)
        results.append((mesh_term, result))
        
        exists_str = "✓" if result['exists'] else "✗"
        print(f"{mesh_term:<40} | {exists_str:<5} | {result['pubmed_count']:,}")
    
    return results, []

def save_results_to_markdown(results, output_path):
    """結果をMarkdownファイルに保存"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Physicians階層 MeSH Term 存在確認結果\n\n")
        f.write("## Physicians下位 MeSH Terms\n\n")
        f.write("| MeSH Term | 存在 | PubMed件数 |\n")
        f.write("|---|---|---|\n")
        
        for mesh_term, result in results:
            exists_str = "✓" if result['exists'] else "✗"
            f.write(f"| {mesh_term} | {exists_str} | {result['pubmed_count']:,} |\n")
        
        # 19領域に対応するMeSH terms
        f.write("\n## 19領域対応表\n\n")
        f.write("| 元テキスト語 | 推奨MeSH Term |\n")
        f.write("|---|---|\n")
        
        mapping = [
            ("medical specialties", "Physicians (親term)"),
            ("specialty-specific", "N/A (テキスト語のみ)"),
            ("discipline-specific", "N/A (テキスト語のみ)"),
            ("clinical specialty", "N/A (テキスト語のみ)"),
            ("clinical specialties", "N/A (テキスト語のみ)"),
            ("internal medicine", "Physicians, Primary Care"),
            ("surgery", "Surgeons"),
            ("pediatrics", "Pediatricians"),
            ("psychiatry", "Psychiatrists"),
            ("anesthesiology", "Anesthesiologists"),
            ("urology", "Urologists"),
            ("family medicine", "Physicians, Family"),
            ("emergency medicine", "Hospitalists / Physicians"),
            ("general medicine", "General Practitioners / Physicians, Primary Care"),
            ("orthopedic surgery", "Orthopedic Surgeons"),
            ("obstetrics and gynecology", "Obstetricians OR Gynecologists"),
            ("neurology", "Neurologists"),
            ("dermatology", "Dermatologists"),
            ("ophthalmology", "Ophthalmologists"),
            ("otolaryngology", "Otolaryngologists"),
            ("radiology", "Radiologists"),
            ("rehabilitation", "Physiatrists"),
        ]
        
        for text_term, mesh_term in mapping:
            f.write(f"| {text_term} | {mesh_term} |\n")
        
        # 推奨検索式ブロック
        f.write("\n## 推奨 Specialty Block 検索式\n\n")
        f.write("```\n")
        
        # MeSH terms (Physicians下位で存在するもの)
        mesh_terms = []
        for mesh_term, result in results:
            if result['exists'] and result['pubmed_count'] > 0:
                mesh_terms.append(f'"{mesh_term}"[mh]')
        
        # テキスト語
        text_terms = [
            '"medical specialties"[tiab]',
            '"specialty-specific"[tiab]',
            '"discipline-specific"[tiab]',
            '"clinical specialty"[tiab]',
            '"clinical specialties"[tiab]',
            '"internal medicine"[tiab]',
            '"surgery"[tiab]',
            '"pediatrics"[tiab]',
            '"psychiatry"[tiab]',
            '"anesthesiology"[tiab]',
            '"urology"[tiab]',
            '"family medicine"[tiab]',
            '"emergency medicine"[tiab]',
            '"general medicine"[tiab]',
            '"orthopedic surgery"[tiab]',
            '"obstetrics and gynecology"[tiab]',
            '"neurology"[tiab]',
            '"dermatology"[tiab]',
            '"ophthalmology"[tiab]',
            '"otolaryngology"[tiab]',
            '"radiology"[tiab]',
            '"rehabilitation"[tiab]',
        ]
        
        all_terms = mesh_terms + text_terms
        f.write("#3 " + " OR ".join(all_terms))
        f.write("\n```\n")
    
    print(f"\nResults saved to: {output_path}")

if __name__ == "__main__":
    results, _ = main()
    
    # 結果をファイルに保存
    output_path = "projects/fd_review/mesh_physician_results.md"
    save_results_to_markdown(results, output_path)
