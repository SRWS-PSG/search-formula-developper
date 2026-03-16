import requests
import time
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional


def fetch_mesh_descriptor_name(term: str) -> Optional[str]:
    """
    MeSHデータベースから用語を検索し、正式なDescriptorName（優先用語）を取得する。

    Entry Term（同義語）で検索した場合でも、対応する正式なDescriptorNameを返す。
    例: "Respiratory Distress Syndrome, Adult" → "Respiratory Distress Syndrome"

    Args:
        term: 検索するMeSH用語

    Returns:
        正式なDescriptorName。見つからない場合はNone。
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    search_url = f"{base_url}/esearch.fcgi"
    fetch_url = f"{base_url}/efetch.fcgi"

    # Step 1: MeSHデータベースでUIDを検索
    search_params = {
        'db': 'mesh',
        'term': term,
        'retmode': 'json'
    }

    try:
        response = requests.get(search_url, params=search_params, timeout=30)
        response.raise_for_status()
        data = response.json()

        id_list = data.get('esearchresult', {}).get('idlist', [])
        if not id_list:
            return None

        # Step 2: efetchでDescriptorレコードのXMLを取得
        time.sleep(0.34)  # API rate limit
        fetch_params = {
            'db': 'mesh',
            'id': id_list[0],
            'retmode': 'xml'
        }

        fetch_resp = requests.get(fetch_url, params=fetch_params, timeout=30)
        fetch_resp.raise_for_status()

        root = ET.fromstring(fetch_resp.content)
        descriptor_name_elem = root.find('.//DescriptorName/String')
        if descriptor_name_elem is not None and descriptor_name_elem.text:
            return descriptor_name_elem.text

        return None

    except (requests.exceptions.RequestException, ET.ParseError):
        return None


def check_mesh_term(term: str) -> Dict:
    """
    PubMed E-utilities APIを使用してMeSH用語の存在をexact matchで確認する。

    MeSHデータベースを検索し、指定された用語が正式なDescriptorName（優先用語）と
    一致するかを検証する。Entry Term（同義語）のみの一致の場合は、
    is_preferred=Falseとして正しいDescriptorNameを提示する。

    Args:
        term: 確認するMeSH用語（例: "Leukemia, Myeloid, Acute"）

    Returns:
        Dict: {
            'exists': bool,           # MeSHデータベースに存在するか（Entry Term含む）
            'is_preferred': bool,     # 正式なDescriptorNameと一致するか
            'preferred_term': str,    # 正式なDescriptorName（不一致時に参照用）
            'term': str,              # 入力された用語
            'mesh_count': int,        # MeSHデータベースでのヒット数
            'pubmed_count': int,      # PubMedでの文献数
            'message': str            # ステータスメッセージ
        }
    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    # MeSH用語の検索
    search_url = f"{base_url}/esearch.fcgi"
    params = {
        'db': 'mesh',
        'term': term,
        'retmode': 'json'
    }

    try:
        response = requests.get(search_url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        count = int(data['esearchresult'].get('count', 0))
        exists = count > 0

        # Exact match検証: DescriptorNameを取得して照合
        preferred_term = ''
        is_preferred = False
        if exists:
            descriptor_name = fetch_mesh_descriptor_name(term)
            if descriptor_name:
                preferred_term = descriptor_name
                # 大文字小文字を無視して完全一致を確認
                is_preferred = (term.lower() == descriptor_name.lower())

        # PubMedでの文献数も確認（exact [Mesh] tagで検索）
        time.sleep(0.34)  # API rate limit
        pubmed_params = {
            'db': 'pubmed',
            'term': f'"{term}"[Mesh]',
            'retmode': 'json'
        }
        pubmed_response = requests.get(search_url, params=pubmed_params, timeout=30)
        pubmed_response.raise_for_status()
        pubmed_data = pubmed_response.json()
        pubmed_count = int(pubmed_data['esearchresult'].get('count', 0))

        # メッセージの構築
        if not exists:
            message = 'MeSH用語が見つかりませんでした。'
        elif is_preferred:
            message = 'Success: 正式なMeSH Descriptor Nameです。'
        else:
            message = (
                f'Warning: "{term}" はEntry Term（同義語）です。'
                f'正式なDescriptorNameは "{preferred_term}" です。'
                f'[Mesh]タグでは "{preferred_term}"[Mesh] を使用してください。'
            )

        return {
            'exists': exists,
            'is_preferred': is_preferred,
            'preferred_term': preferred_term,
            'term': term,
            'mesh_count': count,
            'pubmed_count': pubmed_count,
            'message': message
        }

    except requests.exceptions.RequestException as e:
        return {
            'exists': False,
            'is_preferred': False,
            'preferred_term': '',
            'term': term,
            'mesh_count': 0,
            'pubmed_count': 0,
            'message': f'Error: {str(e)}'
        }

def main():
    # 確認するMeSH用語のリスト（exact match検証のデモ）
    mesh_terms = [
        "Leukemia, Myeloid, Acute",
        "Myelodysplastic Syndromes",
        "Induction Chemotherapy",
        "Remission Induction",
        "Immunocompromised Host",
        "Agranulocytosis",
        # exact match検証用: Entry Termの例
        "Respiratory Distress Syndrome, Adult",  # Entry Term → "Respiratory Distress Syndrome"
        "Respiratory Distress Syndrome",          # 正式なDescriptorName
    ]

    print("MeSH用語の確認を開始します（exact match検証付き）...\n")

    for term in mesh_terms:
        # APIの制限を考慮して少し待機
        time.sleep(1)

        result = check_mesh_term(term)

        print(f"用語: {result['term']}")
        print(f"存在: {'はい' if result['exists'] else 'いいえ'}")
        print(f"正式DescriptorName一致: {'はい' if result['is_preferred'] else 'いいえ'}")
        if result['preferred_term'] and not result['is_preferred']:
            print(f"正式なDescriptorName: {result['preferred_term']}")
        print(f"MeSHデータベースでの出現数: {result['mesh_count']}")
        print(f"PubMedでの文献数: {result['pubmed_count']}")
        print(f"メッセージ: {result['message']}")
        print("-" * 50)

if __name__ == "__main__":
    main()
