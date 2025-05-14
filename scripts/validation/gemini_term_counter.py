#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import time
import argparse
import requests
import re
from datetime import datetime
from dotenv import load_dotenv
from google import genai

# .envファイルから環境変数を読み込む
load_dotenv()

def read_file(file_path):
    """ファイルを読み込む関数"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_search_formula_with_gemini(content, api_key):
    """Gemini APIを使って検索式を抽出する関数"""
    # プロンプトの作成
    prompt = f"""
以下の検索式ファイル（Markdown形式）から、検索式のコンポーネントと組入論文の情報を抽出してください。
以下のJSON形式で返してください:

```json
{{
  "mesh_p": ["用語1", "用語2", ...],  // Population MeSH用語（統制語P）: [mh]または[Mesh]タグを持つ用語
  "keyword_p": ["用語1", "用語2", ...],  // Population フリーワード（フリーワードP）: [tiab]タグを持つ用語
  "mesh_i": ["用語1", "用語2", ...],  // Intervention MeSH用語（統制語I）: [mh]または[Mesh]タグを持つ用語
  "keyword_i": ["用語1", "用語2", ...],  // Intervention フリーワード（フリーワードI）: [tiab]タグを持つ用語
  "pmids": ["PMID1", "PMID2", ...]  // 組入論文のPMID: PMID:の後に続く数字
}}
```

検索式ファイルから抽出すべき情報:
1. Population MeSH用語（統制語P）: [mh]または[Mesh]タグを持つ用語
2. Population フリーワード（フリーワードP）: [tiab]タグを持つ用語
3. Intervention MeSH用語（統制語I）: [mh]または[Mesh]タグを持つ用語
4. Intervention フリーワード（フリーワードI）: [tiab]タグを持つ用語
5. 組入論文のPMID: PMID:の後に続く数字

ファイル内容:
{content}
"""

    try:
        
        # JSONスキーマを定義
        response_schema = {
            "type": "object",
            "properties": {
                "mesh_p": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Population MeSH terms (統制語P)"
                },
                "keyword_p": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Population keywords (フリーワードP)"
                },
                "mesh_i": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Intervention MeSH terms (統制語I)"
                },
                "keyword_i": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Intervention keywords (フリーワードI)"
                },
                "pmids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "PMIDs from the included papers (組入論文)"
                }
            },
            "required": ["mesh_p", "keyword_p", "mesh_i", "keyword_i", "pmids"]
        }
        
        # APIリクエスト (genai.Clientを使用)
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content( 
            model="gemini-2.5-pro-exp-03-25", # モデル名を 'models/' プレフィックス付きで指定
            contents=prompt, # promptをcontentsパラメータに渡す
            config={
                'response_mime_type': 'application/json',
                'response_schema': response_schema,
            }
        )
        
        print("Gemini API response received")
        
        # JSONレスポンスの解析
        try:
            # Client APIでは .parsed 属性で直接パース済みオブジェクトを取得できる場合がある
            if hasattr(response, 'parsed') and response.parsed:
                 result = response.parsed
                 print("Successfully got parsed response")
                 # Pydanticモデルなどからdictに変換する必要があればここで行う
                 if not isinstance(result, dict):
                     # 簡単なdictへの変換を試みる (必要に応じて調整)
                     try:
                         result = json.loads(json.dumps(result)) # 一度JSON文字列にしてからdictに戻す
                     except Exception:
                         print("Warning: Could not convert parsed response to dict.")
                 return result
            elif hasattr(response, 'text') and response.text:
                # .text 属性からJSONをパース
                text = response.text
                # Markdown記法（```json〜```）を削除
                if text.startswith('```') and '```' in text[3:]:
                    start_idx = text.find('\n', 3) + 1
                    end_idx = text.rfind('```')
                    if start_idx > 0 and end_idx > start_idx:
                        text = text[start_idx:end_idx].strip()
                
                print(f"Attempting to parse text: {text[:100]}...")
                result = json.loads(text)
                print("Successfully parsed JSON response from text")
                return result
            else:
                 print("Response does not contain 'parsed' or 'text' attribute.")
                 print("Falling back to manual extraction...")

        except Exception as parsing_error:
            print(f"Error parsing response: {parsing_error}")
            import traceback
            traceback.print_exc()
            print("Falling back to manual extraction...")

        # --- フォールバック処理 (変更なし) ---
        # メッシュとフリーワードを手動で抽出
        mesh_p = re.findall(r'"([^"]+)"(?:\s*)\[(?:mh|Mesh)\]', content)
        keyword_p = []
        mesh_i = []
        keyword_i = []
        
        # フリーワードPセクションの抽出
        p_keyword_section = re.search(r'フリーワード\(Pにまつわるもの\)(.*?)(?:統制語|$)', content, re.DOTALL)
        if p_keyword_section:
            keyword_p = re.findall(r'"([^"]+)"(?:\s*)\[tiab\]', p_keyword_section.group(1))
        
        # 統制語Iセクションの抽出
        i_mesh_section = re.search(r'統制語\(\s*I[^)]*\)(.*?)(?:フリーワード|$)', content, re.DOTALL)
        if i_mesh_section:
            mesh_i = re.findall(r'"([^"]+)"(?:\s*)\[(?:mh|Mesh)\]', i_mesh_section.group(1))
        
        # フリーワードIセクションの抽出
        i_keyword_section = re.search(r'フリーワード\(\s*I[^)]*\)(.*?)(?:#|$)', content, re.DOTALL)
        if i_keyword_section:
            keyword_i = re.findall(r'"([^"]+)"(?:\s*)\[tiab\]', i_keyword_section.group(1))
        
        # PMIDsの抽出 - パターンを改善
        pmids = re.findall(r'PMID:\s*(\d+)(?:;|\s|$)', content)
        
        fallback_result = {
            "mesh_p": mesh_p,
            "keyword_p": keyword_p,
            "mesh_i": mesh_i,
            "keyword_i": keyword_i,
            "pmids": pmids
        }
        
        print("Created fallback result from regex extraction:")
        print(f"- mesh_p: {len(mesh_p)} items")
        print(f"- keyword_p: {len(keyword_p)} items")
        print(f"- mesh_i: {len(mesh_i)} items")
        print(f"- keyword_i: {len(keyword_i)} items")
        print(f"- pmids: {len(pmids)} items ({pmids})")
        
        return fallback_result

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        import traceback
        traceback.print_exc()
        
        # --- APIエラー時のフォールバック処理 (変更なし) ---
        print("Falling back to regex extraction after API error...")
        try:
            mesh_p = re.findall(r'"([^"]+)"(?:\s*)\[(?:mh|Mesh)\]', content)
            keyword_p = []
            mesh_i = []
            keyword_i = []
            
            p_keyword_section = re.search(r'フリーワード\(Pにまつわるもの\)(.*?)(?:統制語|$)', content, re.DOTALL)
            if p_keyword_section:
                keyword_p = re.findall(r'"([^"]+)"(?:\s*)\[tiab\]', p_keyword_section.group(1))
            
            i_mesh_section = re.search(r'統制語\(\s*I[^)]*\)(.*?)(?:フリーワード|$)', content, re.DOTALL)
            if i_mesh_section:
                mesh_i = re.findall(r'"([^"]+)"(?:\s*)\[(?:mh|Mesh)\]', i_mesh_section.group(1))
            
            i_keyword_section = re.search(r'フリーワード\(\s*I[^)]*\)(.*?)(?:#|$)', content, re.DOTALL)
            if i_keyword_section:
                keyword_i = re.findall(r'"([^"]+)"(?:\s*)\[tiab\]', i_keyword_section.group(1))
            
            pmids = re.findall(r'PMID:\s*(\d+)(?:;|\s|$)', content)
            
            fallback_result = {
                "mesh_p": mesh_p,
                "keyword_p": keyword_p,
                "mesh_i": mesh_i,
                "keyword_i": keyword_i,
                "pmids": pmids
            }
            
            print("Created fallback result from regex extraction after API error")
            return fallback_result
        except Exception as regex_error:
            print(f"Error in regex extraction: {regex_error}")
            return None

def count_pubmed_results(terms, field_tag):
    """PubMed APIを使って検索キーの検索結果数を取得する関数"""
    results = {}
    total_count = 0

    if not terms:
        return {"terms": {}, "total": 0}

    # ORで結合した全体クエリの構築
    combined_query = " OR ".join([f'"{term}"{field_tag}' for term in terms])

    try:
        # 全体クエリの検索数を取得
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            'db': 'pubmed',
            'term': combined_query,
            'retmode': 'json'
        }
        response = requests.get(search_url, params=params)
        data = response.json()
        total_count = int(data['esearchresult'].get('count', 0))

        # 個別の検索キーの検索数を取得
        for term in terms:
            time.sleep(0.34)  # APIレート制限に配慮 (3リクエスト/秒)
            query = f'"{term}"{field_tag}'
            params = {
                'db': 'pubmed',
                'term': query,
                'retmode': 'json'
            }
            response = requests.get(search_url, params=params)
            data = response.json()
            count = int(data['esearchresult'].get('count', 0))
            results[term] = count
            print(f"Term: {term}{field_tag} - Count: {count}")

    except Exception as e:
        print(f"Error querying PubMed API: {e}")

    return {"terms": results, "total": total_count}

def check_included_papers(pmids, search_formula):
    """組入論文が検索式にマッチするか確認する関数"""
    results = {}
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    for pmid in pmids:
        time.sleep(0.34)  # APIレート制限に配慮
        query = f"{search_formula} AND {pmid}[uid]"
        params = {
            'db': 'pubmed',
            'term': query,
            'retmode': 'json'
        }
        
        try:
            response = requests.get(search_url, params=params)
            data = response.json()
            count = int(data['esearchresult'].get('count', 0))
            results[pmid] = count > 0
            match_status = "✓" if count > 0 else "✗"
            print(f"PMID {pmid}: {match_status}")
        except Exception as e:
            print(f"Error checking PMID {pmid}: {e}")
            results[pmid] = False

    return results

def generate_report(filename, search_data, pmid_results):
    """検索結果のレポートを生成する関数"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_path = f"logs/validation/gemini_search_report_{timestamp}.md"
    
    # サマリーの集計
    mesh_p_total = search_data.get('mesh_p', {}).get('total', 0)
    keyword_p_total = search_data.get('keyword_p', {}).get('total', 0)
    p_combined_total = search_data.get('p_combined', {}).get('total', 0)
    
    mesh_i_total = search_data.get('mesh_i', {}).get('total', 0)
    keyword_i_total = search_data.get('keyword_i', {}).get('total', 0)
    i_combined_total = search_data.get('i_combined', {}).get('total', 0)
    
    full_formula_total = search_data.get('full_formula', {}).get('total', 0)
    
    included_count = sum(1 for status in pmid_results.values() if status)
    total_pmids = len(pmid_results)
    inclusion_rate = included_count / total_pmids if total_pmids > 0 else 0
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# 検索式カウントレポート\n")
        f.write(f"日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"対象ファイル: {filename}\n\n")
        
        # サマリー部分
        f.write("## サマリー\n\n")
        f.write(f"- Population合計: {p_combined_total:,}件\n")
        f.write(f"- Intervention合計: {i_combined_total:,}件\n")
        f.write(f"- 完全な検索式(P AND I): {full_formula_total:,}件\n")
        f.write(f"- 組入論文の包含率: {included_count}/{total_pmids} ({inclusion_rate:.2%})\n\n")
        
        # Population MeSH用語
        f.write("## Population MeSH用語 [Mesh]\n\n")
        f.write(f"合計: {mesh_p_total:,}件\n\n")
        f.write("| 用語 | 検索数 |\n")
        f.write("|------|-------:|\n")
        
        mesh_p_terms = search_data.get('mesh_p', {}).get('terms', {})
        for term, count in mesh_p_terms.items():
            f.write(f"| {term} | {count:,} |\n")
        
        # Population フリーワード
        f.write("\n## Population フリーワード [tiab]\n\n")
        f.write(f"合計: {keyword_p_total:,}件\n\n")
        f.write("| 用語 | 検索数 |\n")
        f.write("|------|-------:|\n")
        
        keyword_p_terms = search_data.get('keyword_p', {}).get('terms', {})
        for term, count in keyword_p_terms.items():
            f.write(f"| {term} | {count:,} |\n")
        
        # Intervention MeSH用語
        f.write("\n## Intervention MeSH用語 [Mesh]\n\n")
        f.write(f"合計: {mesh_i_total:,}件\n\n")
        f.write("| 用語 | 検索数 |\n")
        f.write("|------|-------:|\n")
        
        mesh_i_terms = search_data.get('mesh_i', {}).get('terms', {})
        for term, count in mesh_i_terms.items():
            f.write(f"| {term} | {count:,} |\n")
        
        # Intervention フリーワード
        f.write("\n## Intervention フリーワード [tiab]\n\n")
        f.write(f"合計: {keyword_i_total:,}件\n\n")
        f.write("| 用語 | 検索数 |\n")
        f.write("|------|-------:|\n")
        
        keyword_i_terms = search_data.get('keyword_i', {}).get('terms', {})
        for term, count in keyword_i_terms.items():
            f.write(f"| {term} | {count:,} |\n")
        
        # 組入論文の包含確認
        f.write("\n## 組入論文の包含確認\n\n")
        f.write("| PMID | 検索式に包含 |\n")
        f.write("|------|:------------:|\n")
        
        for pmid, status in pmid_results.items():
            status_mark = "✓" if status else "✗"
            f.write(f"| {pmid} | {status_mark} |\n")
        
        # 検索式の詳細
        f.write("\n## 使用した検索式\n\n")
        f.write("### Population (P)\n")
        f.write("```\n")
        
        p_parts = []
        if mesh_p_terms:
            mesh_p_part = " OR ".join([f'"{term}"[Mesh]' for term in mesh_p_terms.keys()])
            p_parts.append(f"({mesh_p_part})")
        
        if keyword_p_terms:
            keyword_p_part = " OR ".join([f'"{term}"[tiab]' for term in keyword_p_terms.keys()])
            p_parts.append(f"({keyword_p_part})")
        
        p_formula = " OR ".join(p_parts)
        f.write(p_formula + "\n")
        f.write("```\n\n")
        
        f.write("### Intervention (I)\n")
        f.write("```\n")
        
        i_parts = []
        if mesh_i_terms:
            mesh_i_part = " OR ".join([f'"{term}"[Mesh]' for term in mesh_i_terms.keys()])
            i_parts.append(f"({mesh_i_part})")
        
        if keyword_i_terms:
            keyword_i_part = " OR ".join([f'"{term}"[tiab]' for term in keyword_i_terms.keys()])
            i_parts.append(f"({keyword_i_part})")
        
        i_formula = " OR ".join(i_parts)
        f.write(i_formula + "\n")
        f.write("```\n\n")
        
        f.write("### 完全な検索式 (P AND I)\n")
        f.write("```\n")
        full_formula = f"({p_formula}) AND ({i_formula})"
        f.write(full_formula + "\n")
        f.write("```\n")
    
    print(f"\nレポートを {report_path} に保存しました。")
    return report_path

def main():
    parser = argparse.ArgumentParser(description='Gemini APIを使用して検索式を抽出し、PubMedの検索数をカウントするスクリプト')
    parser.add_argument('--input', required=True, help='検索式ファイルのパス')
    parser.add_argument('--api-key', help='Gemini APIキー (未指定の場合は環境変数GEMINI_API_KEYを使用)')
    
    args = parser.parse_args()
    input_file = args.input
    api_key = args.api_key or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("ERROR: Gemini APIキーが指定されていません。--api-keyオプションまたは環境変数GEMINI_API_KEYで指定してください。")
        return
    
    # ファイルの読み込み
    file_content = read_file(input_file)
    
    # Gemini APIを使って検索式を抽出
    print("Gemini APIを使用して検索式を抽出中...")
    search_components = extract_search_formula_with_gemini(file_content, api_key)
    
    if not search_components:
        print("ERROR: 検索式の抽出に失敗しました。")
        return
    
    # 各コンポーネントを取得
    mesh_p = search_components.get('mesh_p', [])
    keyword_p = search_components.get('keyword_p', [])
    mesh_i = search_components.get('mesh_i', [])
    keyword_i = search_components.get('keyword_i', [])
    pmids = search_components.get('pmids', [])
    
    print(f"\n抽出された検索キー:")
    print(f"- Population MeSH用語: {len(mesh_p)}個")
    print(f"- Population フリーワード: {len(keyword_p)}個")
    print(f"- Intervention MeSH用語: {len(mesh_i)}個")
    print(f"- Intervention フリーワード: {len(keyword_i)}個")
    print(f"- 組入論文PMID: {len(pmids)}個")
    
    # PubMedの検索数を取得
    print("\nPubMedの検索数を取得中...")
    
    search_data = {}
    
    print("\n=== Population MeSH用語の検索件数確認中... ===")
    search_data['mesh_p'] = count_pubmed_results(mesh_p, "[Mesh]")
    
    print("\n=== Population フリーワードの検索件数確認中... ===")
    search_data['keyword_p'] = count_pubmed_results(keyword_p, "[tiab]")
    
    print("\n=== Intervention MeSH用語の検索件数確認中... ===")
    search_data['mesh_i'] = count_pubmed_results(mesh_i, "[Mesh]")
    
    print("\n=== Intervention フリーワードの検索件数確認中... ===")
    search_data['keyword_i'] = count_pubmed_results(keyword_i, "[tiab]")
    
    # Population全体 (MeSH OR キーワード)
    p_formula = ""
    p_parts = []
    
    if mesh_p:
        mesh_p_part = " OR ".join([f'"{term}"[Mesh]' for term in mesh_p])
        p_parts.append(f"({mesh_p_part})")
    
    if keyword_p:
        keyword_p_part = " OR ".join([f'"{term}"[tiab]' for term in keyword_p])
        p_parts.append(f"({keyword_p_part})")
    
    p_formula = " OR ".join(p_parts)
    
    # Intervention全体 (MeSH OR キーワード)
    i_formula = ""
    i_parts = []
    
    if mesh_i:
        mesh_i_part = " OR ".join([f'"{term}"[Mesh]' for term in mesh_i])
        i_parts.append(f"({mesh_i_part})")
    
    if keyword_i:
        keyword_i_part = " OR ".join([f'"{term}"[tiab]' for term in keyword_i])
        i_parts.append(f"({keyword_i_part})")
    
    i_formula = " OR ".join(i_parts)
    
    # Population全体の検索数
    print("\n=== Population全体 (MeSH OR フリーワード) の検索件数確認中... ===")
    try:
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            'db': 'pubmed',
            'term': p_formula,
            'retmode': 'json'
        }
        response = requests.get(search_url, params=params)
        data = response.json()
        p_total = int(data['esearchresult'].get('count', 0))
        search_data['p_combined'] = {"total": p_total}
        print(f"Population全体: {p_total:,}件")
    except Exception as e:
        print(f"Error: {e}")
        search_data['p_combined'] = {"total": 0}
    
    # Intervention全体の検索数
    print("\n=== Intervention全体 (MeSH OR フリーワード) の検索件数確認中... ===")
    try:
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            'db': 'pubmed',
            'term': i_formula,
            'retmode': 'json'
        }
        response = requests.get(search_url, params=params)
        data = response.json()
        i_total = int(data['esearchresult'].get('count', 0))
        search_data['i_combined'] = {"total": i_total}
        print(f"Intervention全体: {i_total:,}件")
    except Exception as e:
        print(f"Error: {e}")
        search_data['i_combined'] = {"total": 0}
    
    # 完全な検索式 (P AND I) の検索数
    print("\n=== 完全な検索式 (P AND I) の検索件数確認中... ===")
    full_formula = f"({p_formula}) AND ({i_formula})"
    try:
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            'db': 'pubmed',
            'term': full_formula,
            'retmode': 'json'
        }
        response = requests.get(search_url, params=params)
        data = response.json()
        full_total = int(data['esearchresult'].get('count', 0))
        search_data['full_formula'] = {"total": full_total}
        print(f"完全な検索式 (P AND I): {full_total:,}件")
    except Exception as e:
        print(f"Error: {e}")
        search_data['full_formula'] = {"total": 0}
    
    # 組入論文の検証
    print("\n=== 組入論文の検索式包含確認中... ===")
    pmid_results = check_included_papers(pmids, full_formula)
    
    # レポート生成
    print("\nレポートを生成中...")
    report_path = generate_report(input_file, search_data, pmid_results)
    
    print(f"\n検証が完了しました。")

if __name__ == "__main__":
    main()
