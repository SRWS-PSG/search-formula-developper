#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
19の医療専門領域のMeSH term存在確認スクリプト
"""
import time
from typing import Dict, List

from scripts.search.mesh_analyzer.check_mesh import check_mesh_term  # noqa: F401

def main():
    # 19の医療専門領域と候補MeSH term
    specialty_terms = [
        # (テキスト語, 候補MeSH term)
        ("medical specialties", "Medicine"),
        ("internal medicine", "Internal Medicine"),
        ("surgery", "General Surgery"),
        ("pediatrics", "Pediatrics"),
        ("psychiatry", "Psychiatry"),
        ("anesthesiology", "Anesthesiology"),
        ("urology", "Urology"),
        ("family medicine", "Family Practice"),
        ("emergency medicine", "Emergency Medicine"),
        ("general medicine", "General Practice"),
        ("orthopedic surgery", "Orthopedics"),
        ("obstetrics and gynecology", "Obstetrics and Gynecology Department, Hospital"),
        ("neurology", "Neurology"),
        ("dermatology", "Dermatology"),
        ("ophthalmology", "Ophthalmology"),
        ("otolaryngology", "Otolaryngology"),
        ("radiology", "Radiology"),
        ("rehabilitation", "Rehabilitation"),
    ]
    
    # 追加の候補MeSH term（別名確認用）
    alternative_terms = [
        ("obstetrics and gynecology", "Gynecology"),
        ("obstetrics and gynecology", "Obstetrics"),
        ("surgery", "Surgery"),
        ("surgery", "Surgical Procedures, Operative"),
        ("orthopedic surgery", "Orthopedic Procedures"),
        ("medical specialties", "Medical Specialty"),
        ("medical specialties", "Specialties, Medical"),
    ]
    
    print("=" * 80)
    print("19の医療専門領域 MeSH Term 存在確認")
    print("=" * 80)
    print()
    
    results = []
    
    # メイン候補の確認
    print("### 主要候補MeSH Terms ###\n")
    print(f"{'テキスト語':<30} | {'候補MeSH':<45} | {'存在':<5} | {'PubMed件数'}")
    print("-" * 100)
    
    for text_term, mesh_term in specialty_terms:
        time.sleep(0.5)  # API制限対策
        result = check_mesh_term(mesh_term)
        results.append((text_term, mesh_term, result))
        
        exists_str = "✓" if result['exists'] else "✗"
        print(f"{text_term:<30} | {mesh_term:<45} | {exists_str:<5} | {result['pubmed_count']:,}")
    
    print("\n")
    print("### 代替候補MeSH Terms ###\n")
    print(f"{'テキスト語':<30} | {'代替MeSH':<45} | {'存在':<5} | {'PubMed件数'}")
    print("-" * 100)
    
    alt_results = []
    for text_term, mesh_term in alternative_terms:
        time.sleep(0.5)
        result = check_mesh_term(mesh_term)
        alt_results.append((text_term, mesh_term, result))
        
        exists_str = "✓" if result['exists'] else "✗"
        print(f"{text_term:<30} | {mesh_term:<45} | {exists_str:<5} | {result['pubmed_count']:,}")
    
    # Markdown出力用サマリー
    print("\n")
    print("=" * 80)
    print("### Markdown Table for Report ###")
    print("=" * 80)
    print()
    print("| テキスト語 | 推奨MeSH Term | 存在 | PubMed件数 |")
    print("|---|---|---|---|")
    
    for text_term, mesh_term, result in results:
        exists_str = "✓" if result['exists'] else "✗"
        print(f"| {text_term} | {mesh_term} | {exists_str} | {result['pubmed_count']:,} |")
    
    return results, alt_results

def save_results_to_markdown(results, alt_results, output_path):
    """結果をMarkdownファイルに保存"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# MeSH Term 存在確認結果\n\n")
        f.write("## 主要候補MeSH Terms\n\n")
        f.write("| テキスト語 | 候補MeSH Term | 存在 | PubMed件数 |\n")
        f.write("|---|---|---|---|\n")
        
        for text_term, mesh_term, result in results:
            exists_str = "✓" if result['exists'] else "✗"
            f.write(f"| {text_term} | {mesh_term} | {exists_str} | {result['pubmed_count']:,} |\n")
        
        f.write("\n## 代替候補MeSH Terms\n\n")
        f.write("| テキスト語 | 代替MeSH Term | 存在 | PubMed件数 |\n")
        f.write("|---|---|---|---|\n")
        
        for text_term, mesh_term, result in alt_results:
            exists_str = "✓" if result['exists'] else "✗"
            f.write(f"| {text_term} | {mesh_term} | {exists_str} | {result['pubmed_count']:,} |\n")
        
        # 推奨検索式ブロック
        f.write("\n## 推奨 Specialty Block 検索式\n\n")
        f.write("```\n")
        
        mesh_terms_for_block = []
        text_terms_for_block = []
        
        for text_term, mesh_term, result in results:
            if result['exists']:
                mesh_terms_for_block.append(f'"{mesh_term}"[mh]')
            text_terms_for_block.append(f'"{text_term}"[tiab]')
        
        all_terms = mesh_terms_for_block + text_terms_for_block
        f.write("#3 " + " OR ".join(all_terms))
        f.write("\n```\n")
    
    print(f"Results saved to: {output_path}")

if __name__ == "__main__":
    import sys
    results, alt_results = main()
    
    # 結果をファイルに保存
    output_path = "projects/fd_review/mesh_specialty_results.md"
    save_results_to_markdown(results, alt_results, output_path)
