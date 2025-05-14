#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import json
import os
import re
import argparse # 追加
from datetime import datetime
from typing import Dict, List, Set, Optional, Any
from bs4 import BeautifulSoup

def get_paper_details(pmid: str) -> Dict:
    """
    PubMed E-utilities APIを使用して論文の詳細情報を取得する
    
    Args:
        pmid: 論文のPMID
        
    Returns:
        Dict: 論文の詳細情報
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    fetch_url = f"{base_url}/efetch.fcgi"
    
    api_key = os.getenv("NCBI_API_KEY")
    params = {
        'db': 'pubmed',
        'id': pmid,
        'retmode': 'xml'
    }
    if api_key:
        params['api_key'] = api_key
    
    try:
        response = requests.get(fetch_url, params=params)
        response.raise_for_status()
        return {
            'pmid': pmid,
            'xml': response.text,
            'status': 'success'
        }
    except requests.exceptions.RequestException as e:
        return {
            'pmid': pmid,
            'xml': None,
            'status': 'error',
            'message': str(e)
        }

def extract_mesh_terms(xml_data: str) -> List[Dict]:
    """
    XMLデータからMeSH用語を抽出する
    
    Args:
        xml_data: PubMed論文のXMLデータ
        
    Returns:
        List[Dict]: MeSH用語のリスト
    """
    mesh_terms = []
    
    if not xml_data:
        return mesh_terms
    
    soup = BeautifulSoup(xml_data, 'lxml')
    
    # MeSH用語の抽出
    mesh_headings = soup.find_all('meshheading')
    
    for heading in mesh_headings:
        descriptor = heading.find('descriptorname')
        
        if descriptor:
            # MeSH UIの取得
            mesh_ui = descriptor.get('ui', '')
            
            # 修飾語の抽出
            qualifiers = []
            for qualifier in heading.find_all('qualifiername'):
                qualifier_name = qualifier.text
                qualifier_ui = qualifier.get('ui', '')
                major_topic = qualifier.get('majortopicyn', 'N') == 'Y'
                qualifiers.append({
                    'name': qualifier_name,
                    'ui': qualifier_ui,
                    'major_topic': major_topic
                })
            
            # 主要トピックかどうか
            major_topic = descriptor.get('majortopicyn', 'N') == 'Y'
            
            mesh_terms.append({
                'descriptor': descriptor.text,
                'ui': mesh_ui,
                'major_topic': major_topic,
                'qualifiers': qualifiers
            })
    
    return mesh_terms

def extract_title_abstract(xml_data: str) -> Dict:
    """
    XMLデータからタイトルと抄録を抽出する
    
    Args:
        xml_data: PubMed論文のXMLデータ
        
    Returns:
        Dict: タイトルと抄録
    """
    if not xml_data:
        return {'title': '', 'abstract': ''}
    
    soup = BeautifulSoup(xml_data, 'lxml')
    
    # タイトルの抽出
    title_element = soup.find('articletitle')
    title = title_element.text if title_element else ''
    
    # 抄録の抽出
    abstract_texts = soup.find_all('abstracttext')
    abstract = ' '.join([text.text for text in abstract_texts]) if abstract_texts else ''
    
    return {
        'title': title,
        'abstract': abstract
    }

def extract_publication_info(xml_data: str) -> Dict:
    """
    XMLデータから出版情報を抽出する
    
    Args:
        xml_data: PubMed論文のXMLデータ
        
    Returns:
        Dict: 出版情報
    """
    if not xml_data:
        return {
            'journal': '',
            'year': '',
            'authors': []
        }
    
    soup = BeautifulSoup(xml_data, 'lxml')
    
    # ジャーナル名の抽出
    journal_element = soup.find('journal')
    journal = journal_element.find('title').text if journal_element and journal_element.find('title') else ''
    
    # 出版年の抽出
    pub_date = soup.find('pubdate')
    year = pub_date.find('year').text if pub_date and pub_date.find('year') else ''
    
    # 著者の抽出
    authors = []
    author_list = soup.find('authorlist')
    
    if author_list:
        for author in author_list.find_all('author'):
            last_name = author.find('lastname')
            fore_name = author.find('forename')
            
            if last_name and fore_name:
                authors.append(f"{last_name.text} {fore_name.text}")
            elif last_name:
                authors.append(last_name.text)
    
    return {
        'journal': journal,
        'year': year,
        'authors': authors
    }

def get_mesh_hierarchy(mesh_ui: str, mesh_name: Optional[str] = None) -> List[str]:
    """
    指定した MeSH Descriptor UI からツリー番号（Tree Number）の一覧を取得して返す。

    - まず NCBI MeSH Browser の HTML をスクレイピングして「Tree Number(s):」行を探す。
    - 見つからない場合は <div id="maincontent"> 直下のツリー構造リストを解析する。
    - それでも取得できなければ E-utilities efetch (db=mesh, retmode=xml) を試す。
    - すべて失敗した場合は 'Unknown.<UI>' だけを返す（手動カテゴリ推測や basic_hierarchy は廃止）。

    Args:
        mesh_ui (str): MeSH Descriptor UI（例 "D009103"）
        mesh_name (Optional[str]): 参照用の見出し語（ログ出力のため。処理には必須ではない）

    Returns:
        List[str]: 取得したツリー番号のリスト。取得失敗時は ["Unknown.<UI>"]。
    """
    import requests, re, time
    from bs4 import BeautifulSoup

    # --- 1. MeSH Browser を直接スクレイピング ---------------------------------
    browser_url = f"https://www.ncbi.nlm.nih.gov/mesh/?term={mesh_ui}"
    print(f"[get_mesh_hierarchy] '{mesh_name or mesh_ui}' のツリー番号取得: {browser_url}")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36"
        )
    }

    try:
        resp = requests.get(browser_url, headers=headers, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        main = soup.find(id="maincontent")
        if main:
            # --- (a) <p> タグに "Tree Number(s):" があるパターン ------------
            p_tree = next(
                (p for p in main.find_all("p") if "Tree Number" in p.get_text()),
                None,
            )
            if p_tree:
                txt = (
                    p_tree.get_text()
                    .replace("Tree Number(s):", "")
                    .replace("Tree Number:", "")
                    .strip()
                )
                if txt:
                    numbers = [s.strip() for s in re.split(r"[, ]+", txt) if s.strip()]
                    if numbers:
                        print(f" → 取得成功 (MeSH Browser pタグ): {numbers}")
                        return numbers

            # --- (b) ツリー構造リスト (<ul>/<li>) を辿るパターン ----------
            tree_numbers = []
            for b_tag in main.find_all("b"): # Renamed b to b_tag to avoid conflict
                li = b_tag.find_parent("li")
                if not li:
                    continue
                m = re.search(r"([A-Z]\d+(?:\.\d+)+)", li.get_text())
                if m:
                    tree_numbers.append(m.group(1))
            if tree_numbers:
                print(f" → 取得成功 (MeSH Browser list): {tree_numbers}")
                return list(dict.fromkeys(tree_numbers))  # 重複除去

    except Exception as e:
        print(f"[get_mesh_hierarchy] MeSH Browser 取得失敗: {e}")

    # --- 2. efetch (db=mesh, retmode=xml) ----------------------------------------
    try:
        efetch_response = requests.get( # Renamed efetch to efetch_response
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi",
            params={"db": "mesh", "id": mesh_ui, "retmode": "xml"},
            timeout=20,
        )
        efetch_response.raise_for_status()
        soup = BeautifulSoup(efetch_response.text, "lxml")

        # <TreeNumber> または <treenumber>
        numbers = [t.get_text() for t in soup.find_all(["TreeNumber", "treenumber"])]
        if numbers:
            print(f" → 取得成功 (efetch xml): {numbers}")
            return numbers

    except Exception as e:
        print(f"[get_mesh_hierarchy] efetch 取得失敗: {e}")

    # --- 3. どの方法でも取れなかった場合 ----------------------------------------
    print(f"[get_mesh_hierarchy] ツリー番号取得不能 → Unknown.{mesh_ui}")
    return [f"Unknown.{mesh_ui}"]

def fetch_mesh_term_by_tree_number(tree_number: str) -> Optional[Dict[str, str]]:
    """
    ツリー番号から MeSH 見出し語名・Descriptor UI を取得する。
    NLM Linked Data SPARQLエンドポイントを使用。
    
    デバッグ結果に基づく改善版：
    1. 正規表現を使用して年度に依存しないマッチング
    2. 複数の検索パターンを試行（多段階フォールバック）
    
    Args:
        tree_number: 検索するMeSHツリー番号（例："C10.228.140.079.862"）
        
    Returns:
        Optional[Dict[str, str]]: 見つかった場合はMeSH UIと名前の辞書、見つからない場合はNone
    """
    print(f"ツリー番号 '{tree_number}' のMeSH用語をSPARQLで検索中...")
    
    # FROMステートメントを削除し、年度非依存の正規表現検索に変更したSPARQLクエリ
    sparql_query = f"""
    PREFIX mesh:  <http://id.nlm.nih.gov/mesh/>
    PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>
    PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?d ?uid ?label
    WHERE {{
      ?tn a meshv:TreeNumber ;
          rdfs:label ?tnl .
      FILTER(REGEX(?tnl, "^{tree_number}$", "i"))
      ?d meshv:treeNumber ?tn ;
         meshv:identifier ?uid ;
         rdfs:label ?label .
    }}
    LIMIT 5
    """
    
    # エンドポイントURLとパラメータ
    endpoint_url = "https://id.nlm.nih.gov/mesh/sparql"
    params = {
        "query": sparql_query,
        "format": "json",
        "offset": 0, # 取得開始位置
        "limit": 10 # 取得件数上限 (通常は1件で十分)
    }
    
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(endpoint_url, params=params, headers=headers, timeout=30) # timeoutを延長
        response.raise_for_status()
        results = response.json()
        
        bindings = results.get("results", {}).get("bindings", [])
        if not bindings:
            print(f"ツリー番号 '{tree_number}' に対応するMeSH用語が見つかりませんでした (SPARQL)。レスポンス: {response.text}")
            return None
        
        first_result = bindings[0]
        uid_uri = first_result.get("uid", {}).get("value", "")
        label = first_result.get("label", {}).get("value", "")
        
        # UIDはURI形式 (例: http://id.nlm.nih.gov/mesh/D000001) で返ってくるので、末尾のD番号を抽出
        uid = uid_uri.split("/")[-1] if uid_uri else ""
        
        if not uid or not label:
            print(f"ツリー番号 '{tree_number}' からUIDまたはラベルが取得できませんでした (SPARQL)。UID URI: {uid_uri}, Label: {label}")
            return None

        print(f"ツリー番号 '{tree_number}' -> MeSH UI: {uid}, Name: {label}")
        return {
            "ui": uid,
            "name": label,
            "tree_number": tree_number
        }
            
    except requests.exceptions.Timeout:
        print(f"ツリー番号 '{tree_number}' のSPARQL検索中にタイムアウトエラーが発生しました。")
        return None
    except requests.exceptions.RequestException as e:
        print(f"ツリー番号 '{tree_number}' のSPARQL検索中にエラー: {str(e)}。レスポンス: {response.text if 'response' in locals() else 'N/A'}")
        return None
    except json.JSONDecodeError:
        print(f"ツリー番号 '{tree_number}' のSPARQL検索結果のJSONデコードエラー。レスポンス: {response.text}")
        return None
    except Exception as e: # その他の予期せぬエラー
        print(f"ツリー番号 '{tree_number}' のSPARQL結果処理中に予期せぬエラー: {str(e)}")
        return None
    finally:
        time.sleep(0.1) # NLMの推奨に従い、リクエスト間隔を調整 (1秒あたり10リクエスト以内)

def generate_mermaid_diagram(mesh_hierarchies: Dict, all_collected_tree_numbers: Set[str]) -> str:
    """
    MeSH階層構造からMermaid図を生成する。
    カテゴリごとに完全に独立した複数のMermaid図を作成し、
    実際のMeSH用語名を表示し、seed論文に付与されていたMeSH用語のみを強調表示する。
    
    Args:
        mesh_hierarchies: MeSH階層構造の辞書
        all_collected_tree_numbers: 収集された全ツリー番号のセット
        
    Returns:
        str: 複数のMermaid図を含むテキスト
    """
    
    # ヘルパー関数
    def create_safe_node_id(tree_path: str) -> str:
        """ツリーパスから安全なノードIDを生成する"""
        return f"node_{tree_path.replace('.', '_').replace('-', '_')}"
    
    def create_safe_label(name: str) -> str:
        """Mermaid用に文字列を安全にエスケープする"""
        return name.replace("\"", "'").replace("\\", "")
    # MeSHカテゴリ（トップレベル）の定義
    mesh_categories: Dict[str, str] = {
        'A': '解剖学 (Anatomy)',
        'B': '生物 (Organisms)',
        'C': '疾患 (Diseases)',
        'D': '化学物質と医薬品 (Chemicals and Drugs)',
        'E': '分析・診断・治療技術と装置 (Techniques and Equipment)',
        'F': '精神医学と心理学 (Psychiatry and Psychology)',
        'G': '生物学・物理学 (Biological Sciences)',
        'H': '自然科学 (Physical Sciences)',
        'I': '人類学・教育・社会・社会現象 (Social Phenomena)',
        'J': '技術・産業・農業 (Technology, Industry, Agriculture)',
        'K': '人文科学 (Humanities)',
        'L': '情報科学 (Information Science)',
        'M': '人物 (Named Groups)',
        'N': '健康管理 (Health Care)',
        'V': '出版物の種類 (Publication Characteristics)',
        'Z': '地理的な位置 (Geographic Locations)',
        'Unknown': '不明なカテゴリ (Unknown)'
    }
    
    # カテゴリごとの階層データ
    category_hierarchies: Dict[str, Set[str]] = {}
    
    # カテゴリごとに、既に追加したMeSH IDを追跡するセット
    category_added_ids: Dict[str, Set[str]] = {}
    for category in mesh_categories.keys():
        category_added_ids[category] = set()

    # ツリー番号からMeSH名へのマッピングを作成 (初期状態)
    tree_number_to_name_map: Dict[str, str] = {}
    for mesh_id, info in mesh_hierarchies.items():
        for tn in info.get("tree_numbers", []):
            if tn:
                tree_number_to_name_map[tn] = info["name"]

    # all_collected_tree_numbers に含まれるが、tree_number_to_name_map にまだ名前がないものを検索
    # (mesh_hierarchies には論文から直接抽出されたMeSHの情報しかないため、親ノードの名前は別途取得が必要)
    print("\n=== 未知のツリー番号に対応するMeSH用語を検索します ===")
    unknown_tree_numbers_to_fetch = all_collected_tree_numbers - set(tree_number_to_name_map.keys())
    
    fetched_terms_count = 0
    for tn_to_fetch in sorted(list(unknown_tree_numbers_to_fetch)): # Sort for deterministic behavior
        if not tn_to_fetch or tn_to_fetch.startswith("Unknown"): # "Unknown.DXXXX"のようなものは検索しない
            continue
        try:
            fetched_info = fetch_mesh_term_by_tree_number(tn_to_fetch)
            if fetched_info:
                tree_number_to_name_map[fetched_info['tree_number']] = fetched_info['name']
                # Optionally, update mesh_hierarchies if the fetched term is new
                if fetched_info['ui'] not in mesh_hierarchies:
                    mesh_hierarchies[fetched_info['ui']] = {
                        'name': fetched_info['name'],
                        'ui': fetched_info['ui'],
                        'tree_numbers': [fetched_info['tree_number']],
                        'count': 0, # Not directly from a paper's MeSH list
                        'major_topic': False
                    }
                fetched_terms_count += 1
                # Limit API calls if necessary, e.g., for testing
                # if fetched_terms_count >= 10:
                #     print("一度の検索上限に達しました。残りは次回以降に検索されます。")
                #     break
        except Exception as e:
            print(f"ツリー番号 {tn_to_fetch} の取得中にエラー発生: {str(e)}")
            continue
    print(f"未知のツリー番号から {fetched_terms_count} 件のMeSH用語情報を取得・補完しました。")


    # カテゴリごとのMeSH用語リスト
    category_terms: Dict[str, List[tuple[str, Dict]]] = {}
    
    # 各MeSH用語の階層構造を処理し、カテゴリごとに分類
    for mesh_id, info in mesh_hierarchies.items(): 
        name = info.get("name", "")
        if not name:  # 名前がない場合はスキップ
            continue
            
        tree_numbers = info.get("tree_numbers", [])
        
        if not tree_numbers or all(tn.startswith('Unknown') for tn in tree_numbers):
            if 'Unknown' not in category_terms:
                category_terms['Unknown'] = []
                category_added_ids['Unknown'] = set()
            if mesh_id not in category_added_ids['Unknown']:
                category_terms['Unknown'].append((mesh_id, info))
                category_added_ids['Unknown'].add(mesh_id)
            continue
        
        for tree_number in tree_numbers:
            if not tree_number or not tree_number[0].isalpha() or tree_number.startswith("Unknown"):
                continue
            category = tree_number[0]
            
            if category not in category_hierarchies:
                category_hierarchies[category] = set() 
            if category not in category_terms:
                category_terms[category] = []
                category_added_ids[category] = set()
                
            category_hierarchies[category].add(tree_number)
            
            if mesh_id not in category_added_ids[category]:
                category_terms[category].append((mesh_id, info))
                category_added_ids[category].add(mesh_id)

    used_in_papers = {mesh_id for mesh_id, info in mesh_hierarchies.items() if info.get("count", 0) > 0}
    
    # 結果用のテキスト行リスト
    result_lines = []
    
    for category, terms_in_category in sorted(category_terms.items()):
        if not terms_in_category:
            continue
            
        category_desc = mesh_categories.get(category, f'カテゴリ {category}')
        result_lines.append(f"## カテゴリ {category}: {category_desc}\n")
        result_lines.append("```mermaid\nflowchart TD\n")
        
        node_ids_for_mermaid: Dict[str, str] = {} 
        paths_for_mermaid: Dict[str, str] = {}  
        
        # 階層構造データの構築方法を根本的に改善
        # 先に全ノードを定義してから、エッジを構築する二段階アプローチ
        
        # ステップ1: 各ノードを一度だけ定義する
        nodes_defined = set()
        
        # すべてのツリーパスを収集（部分パスを含む）
        current_category_tree_paths: Set[str] = set()
        
        # カテゴリに関連するツリー番号を収集
        if category in category_hierarchies:
            for tn_full in category_hierarchies[category]:
                # 完全なパスを追加
                current_category_tree_paths.add(tn_full)
                # 部分パスも追加
                parts = tn_full.split('.')
                path_segment = ""
                for i, part in enumerate(parts):
                    path_segment = f"{path_segment}.{part}" if i > 0 else part
                    current_category_tree_paths.add(path_segment)
        
        # このカテゴリ内の用語から直接ツリー番号を追加
        for _, term_info in terms_in_category:
            for tree_num in term_info.get("tree_numbers", []):
                if tree_num.startswith(category):
                    current_category_tree_paths.add(tree_num)
        
        # すべてのノードを定義
        for tree_path in sorted(list(current_category_tree_paths)):
            if tree_path not in paths_for_mermaid:
                node_id = create_safe_node_id(tree_path)
                paths_for_mermaid[tree_path] = node_id
                
                # ノードラベルの決定
                parts = tree_path.split('.')
                last_part = parts[-1] if parts else ""
                
                if tree_path in tree_number_to_name_map:
                    mesh_name = tree_number_to_name_map[tree_path]
                    safe_name = create_safe_label(mesh_name)
                    # 用語名を主体とし、末尾の番号部分のみ表示
                    node_label = f"{safe_name} [{last_part}]"
                elif len(parts) == 1 and category != "Unknown":
                    # トップレベルカテゴリノード
                    node_label = f"{mesh_categories.get(category, '')}"
                else:
                    # それ以外の場合は末尾の番号のみ表示
                    node_label = f"Tree #{last_part}"
                
                result_lines.append(f"    {node_id}[\"{node_label}\"]\n")
                nodes_defined.add(tree_path)
        
        # ステップ2: エッジを一度だけ定義する
        edges_defined = set()
        
        for tree_path in sorted(list(current_category_tree_paths)):
            parts = tree_path.split('.')
            if len(parts) <= 1:  # ルートノードはスキップ
                continue
                
            # 親パスを構築
            parent_parts = parts[:-1]
            parent_path = '.'.join(parent_parts)
            
            # カテゴリパスの場合（最初の要素がカテゴリ文字）
            if len(parent_parts) == 0:
                parent_path = category
            
            # 親ノードと子ノードの両方が定義されている場合のみエッジを追加
            if parent_path in paths_for_mermaid and tree_path in paths_for_mermaid:
                parent_id = paths_for_mermaid[parent_path]
                child_id = paths_for_mermaid[tree_path]
                edge_key = f"{parent_id}_to_{child_id}"
                
                if edge_key not in edges_defined:
                    result_lines.append(f"    {parent_id} --> {child_id}\n")
                    edges_defined.add(edge_key)

        # MeSH用語ノードは既に階層構造内に統合されているため、別途追加する必要はない
        
        # ノードのスタイル設定
        for mesh_ui_style, _ in terms_in_category:
            # パスのツリー番号から対応するノードIDを見つける
            for tn in mesh_hierarchies.get(mesh_ui_style, {}).get("tree_numbers", []):
                if tn in paths_for_mermaid and mesh_ui_style in used_in_papers:
                    node_id_to_style = paths_for_mermaid[tn]
                    result_lines.append(f"    style {node_id_to_style} fill:#ff8c00,stroke:#333,stroke-width:2px\n")
        
        result_lines.append("```\n\n")
        result_lines.append("| MeSH UI | MeSH 用語 | 出現数 | ツリー番号 (カテゴリ内) |\n")
        result_lines.append("|---------|----------|-------|-----------------------|\n")
        
        for mesh_id_table, info_table in terms_in_category: 
            category_specific_tree_numbers = [tn for tn in info_table.get("tree_numbers", []) if tn.startswith(category)]
            if category_specific_tree_numbers: 
                tree_numbers_text_table = ", ".join(sorted(list(set(category_specific_tree_numbers))))
                result_lines.append(f"| {mesh_id_table} | {info_table['name']} | {info_table.get('count', 0)} | {tree_numbers_text_table} |\n")
        result_lines.append("\n")
    
    return "".join(result_lines)

def ensure_directory_exists(path: str) -> None:
    """
    ディレクトリが存在しない場合は作成する
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

def main() -> None:
    """
    seed_pmids.txt で与えられた PubMed ID 群を対象に
    * MeSH 用語抽出
    * ツリー番号取得（get_mesh_hierarchy）
    * Mermaid 図＆ Markdown／JSON レポート生成
    を実行するメイン関数。
    """
    parser = argparse.ArgumentParser(description="PubMedのPMIDリストからMeSH用語を抽出し、階層分析レポートを生成します。")
    parser.add_argument(
        "--pmid-file",
        type=str,
        default="seed_pmids.txt",
        help="PMIDが1行に1つ記載された入力ファイルのパス (デフォルト: seed_pmids.txt)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="結果を出力するディレクトリのパス (デフォルト: カレントディレクトリ)"
    )
    args = parser.parse_args()

    # ------------------------------------------------------------------
    # 0. 入力ファイル（seed_pmids.txt）取得
    # ------------------------------------------------------------------
    seed_path = args.pmid_file
    output_dir = args.output_dir

    # 出力ディレクトリが存在しない場合は作成
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        with open(seed_path, "r", encoding="utf-8") as f: # Added encoding
            pmids = [ln.strip() for ln in f if ln.strip() and not ln.startswith('#')] # コメント行を無視
    except FileNotFoundError:
        print(f"エラー: PMIDファイルが見つかりません。パス: {seed_path}")
        return


    # 結果を保持する大きな辞書
    results: Dict[str, Any] = {
        "papers": [],
        "mesh_terms": {}, # Stores aggregated info for each MeSH UI
        "mesh_hierarchies": {} # Stores detailed hierarchy info for top terms
    }

    print(f"\n=== {len(pmids)} 件の論文について MeSH 解析開始 ===")

    # ------------------------------------------------------------------
    # 1. 各 PMID → 論文詳細取得 → MeSH 用語抽出
    # ------------------------------------------------------------------
    for pmid in pmids:
        print(f"\n[main] PMID {pmid} 処理開始")
        paper = get_paper_details(pmid)
        if paper["status"] == "error":
            print(f"  ↳ 取得失敗: {paper['message']}")
            continue

        mesh_list_for_paper = extract_mesh_terms(paper["xml"]) # Renamed to avoid conflict
        meta      = extract_title_abstract(paper["xml"])
        pubinfo   = extract_publication_info(paper["xml"])

        # ログ出力
        print(f"  タイトル : {meta['title'][:80]}…")
        print(f"  Journal : {pubinfo['journal']} ({pubinfo['year']})")
        print(f"  MeSH 用語数 : {len(mesh_list_for_paper)}")

        results["papers"].append(
            {
                "pmid": pmid,
                "title": meta["title"],
                "journal": pubinfo["journal"],
                "year": pubinfo["year"],
                "authors": pubinfo["authors"],
                "mesh_terms": mesh_list_for_paper # Use renamed variable
            }
        )

        # term 出現回数カウント
        for term in mesh_list_for_paper: # Use renamed variable
            ui = term["ui"]
            if not ui: continue # Skip if UI is empty

            if ui not in results["mesh_terms"]:
                results["mesh_terms"][ui] = {
                    "name": term["descriptor"],
                    "ui": ui,
                    "count": 0,
                    "papers": [],
                    "major_topic_count": 0
                }
            results["mesh_terms"][ui]["count"] += 1
            if pmid not in results["mesh_terms"][ui]["papers"]:
                 results["mesh_terms"][ui]["papers"].append(pmid)
            if term["major_topic"]:
                results["mesh_terms"][ui]["major_topic_count"] += 1

        time.sleep(0.34)   # PubMed API レート制限 (adjust as needed)

    # ------------------------------------------------------------------
    # 2. 上位 MeSH 用語のツリー番号取得と全ツリー番号収集
    # ------------------------------------------------------------------
    print("\n=== 上位MeSH用語の階層構造を取得し、全ツリー番号を収集します ===")
    sorted_terms_list = sorted( # Renamed to avoid conflict
        results["mesh_terms"].items(),
        key=lambda x: (x[1]["count"], x[1]["major_topic_count"]),
        reverse=True
    )
    top_n_terms = sorted_terms_list[:20] # Consider making N configurable
    
    all_tree_numbers_collected: Set[str] = set() # To be passed to generate_mermaid_diagram

    for ui, info in top_n_terms:
        if not ui: continue # Skip if UI is somehow empty
        print(f"\n[main] 上位MeSH用語 '{info['name']}' (UI: {ui}) の階層処理...")
        # get_mesh_hierarchy is now more robust and primarily uses MeSH Browser / efetch for Descriptor UI
        tree_numbers_for_term = get_mesh_hierarchy(ui, info["name"]) 
        
        # Store in mesh_hierarchies (this dict is used by generate_mermaid_diagram)
        results["mesh_hierarchies"][ui] = {
            "name": info["name"],
            "ui": ui, # Ensure UI is stored here as well
            "tree_numbers": tree_numbers_for_term,
            "count": info["count"], # Keep original count from papers
            "major_topic": info["major_topic_count"] > 0
        }
        
        # Collect all parts of the tree numbers for later lookup if needed
        for tn in tree_numbers_for_term:
            if tn and not tn.startswith("Unknown"):
                parts = tn.split('.')
                current_path = ""
                for i_part, part_val in enumerate(parts):
                    current_path = f"{current_path}.{part_val}" if i_part > 0 else part_val
                    all_tree_numbers_collected.add(current_path)
        time.sleep(0.34)  # API rate limit

    # Fallback for basic hierarchy (might be less necessary now)
    # print("MeSH階層構造の取得に失敗しました。基本的な階層構造を手動で設定します。")
    # basic_hierarchy = { ... }
    # for ui, info in results['mesh_hierarchies'].items(): ...

    # ------------------------------------------------------------------
    # 3. Mermaid 図生成 & ファイル出力
    # ------------------------------------------------------------------
    print("\n=== Mermaid図とレポートを生成します ===")
    mermaid_diagram_text_content = generate_mermaid_diagram( # Renamed variable
        results["mesh_hierarchies"], # This now contains top N terms with their hierarchies
        all_tree_numbers_collected  # All unique tree number paths found
    )

    print(f"\n出力ディレクトリ: {output_dir}")
    
    # ディレクトリ存在確認 (dummy.txtは生成しない)
    os.makedirs(output_dir, exist_ok=True)

    # 既存のXが付いたファイルがあれば削除
    for filename in ["mesh_analysis.mdX", "mesh_hierarchy.mdX", "debug_mesh_sparql.pyX"]:
        bad_file = os.path.join(output_dir, filename)
        if os.path.exists(bad_file):
            try:
                os.remove(bad_file)
                print(f"不正なファイル '{filename}' を削除しました")
            except Exception as e:
                print(f"ファイル削除エラー '{filename}': {str(e)}")

    # JSON形式で結果を保存
    output_file_json = os.path.join(output_dir, "mesh_analysis_results.json")
    with open(output_file_json, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # Markdown形式のレポートも生成
    md_output_file_analysis = os.path.join(output_dir, "mesh_analysis.md")
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(md_output_file_analysis, 'w', encoding='utf-8') as f:
        f.write(f"# シードスタディのMeSH用語分析\n")
        f.write(f"生成日時: {now_str}\n\n")
        
        f.write("## 分析サマリー\n\n")
        f.write(f"- 分析論文数: {len(pmids)}件\n")
        f.write(f"- 抽出されたユニークMeSH用語数: {len(results['mesh_terms'])}個\n\n") # Changed to unique
        
        f.write("## 主要なMeSH用語（出現頻度順 - 上位20件）\n\n") # Clarified top 20
        f.write("| MeSH UI | MeSH 用語 | 出現数 | 主要トピック論文数 |\n") # Clarified column
        f.write("|---------|----------|-------|------------------|\n")
        
        for ui, term_info_detail in top_n_terms: # Use top_n_terms for this table
            f.write(f"| {ui} | {term_info_detail['name']} | {term_info_detail['count']} | {term_info_detail['major_topic_count']} |\n")
        
        f.write("\n## MeSH用語の階層構造 (上位用語ベース)\n\n") # Clarified based on top terms
        f.write("以下のMermaid図は、論文から抽出された主要なMeSH用語とその階層構造をカテゴリ別に示しています。\n")
        f.write("未知の親階層の用語名も可能な限り補完しています。\n\n")
        f.write(mermaid_diagram_text_content) 
        
        f.write("### 凡例\n\n")
        f.write("- オレンジ色のノード: Seed論文に実際に付与されていたMeSH用語 (上位20件に含まれるもの)\n")
        f.write("- 通常のノード: 上記MeSH用語の階層を構成する親ノード (可能な場合、用語名を補完)\n\n")
        
        f.write("## 論文別MeSH用語\n\n")
        for paper_data_item in results['papers']: # Renamed variable
            f.write(f"### PMID: {paper_data_item['pmid']}\n\n")
            f.write(f"- タイトル: {paper_data_item['title']}\n")
            f.write(f"- ジャーナル: {paper_data_item['journal']} ({paper_data_item['year']})\n")
            f.write(f"- 著者: {', '.join(paper_data_item['authors'])}\n")
            f.write(f"- MeSH用語数: {len(paper_data_item['mesh_terms'])}\n\n")
            
            f.write("| MeSH UI | MeSH 用語 | 主要トピック | 修飾語 |\n")
            f.write("|---------|----------|------------|-------|\n")
            
            for term_detail in paper_data_item['mesh_terms']: # Renamed variable
                major_indicator = "Yes" if term_detail['major_topic'] else "No"
                
                qualifier_text = ""
                if term_detail['qualifiers']:
                    qualifier_list = []
                    for qualifier in term_detail['qualifiers']:
                        q_indicator = "*" if qualifier['major_topic'] else ""
                        qualifier_list.append(f"{qualifier['name']}{q_indicator}")
                    qualifier_text = ", ".join(qualifier_list)
                
                f.write(f"| {term_detail['ui']} | {term_detail['descriptor']} | {major_indicator} | {qualifier_text} |\n")
            f.write("\n---\n\n")
    
    print(f"\n分析が完了しました。")
    print(f"結果を次のファイルに保存しました：")
    print(f"- JSON形式: {output_file_json}")
    print(f"- 分析レポート: {md_output_file_analysis}")

if __name__ == "__main__":
    main()
