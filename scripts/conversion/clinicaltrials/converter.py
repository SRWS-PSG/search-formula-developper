import re
from typing import List, Dict, Tuple
import os
import sys

class ClinicalTrialsConverter:
    """PubMed検索式をClinicalTrials.gov形式に変換するクラス"""
    
    def __init__(self, mesh_synonym_map: Dict[str, List[str]] = None):
        """
        Args:
            mesh_synonym_map: MeSH用語と同義語のマッピング辞書（任意）
        """
        self.mesh_synonym_map = mesh_synonym_map or {}
        
    def _expand_mesh_terms(self, mesh_term: str) -> str:
        """MeSH用語を同義語リストに展開"""
        # MeSH用語から[]タグを除去
        clean_term = re.sub(r'\[Mesh\]|\[MeSH Terms\]|\[mh\]', '', mesh_term).strip().strip('"\'')
        
        # 同義語マップに存在する場合は展開、なければそのまま返す
        if clean_term in self.mesh_synonym_map:
            synonyms = self.mesh_synonym_map.get(clean_term, [clean_term])
            return ' OR '.join([f'"{term}"' for term in synonyms])
        
        # デフォルトの同義語展開（エッセンシャルトレモアの例）
        if "Essential Tremor" in clean_term:
            return '"essential tremor" OR "benign tremor" OR "familial tremor"'
        
        return f'"{clean_term}"'
        
    def _convert_proximity(self, query_part: str) -> str:
        """近接演算子を適切な形式に変換"""
        # 近接演算子パターン（例: "term1 term2"[tiab:~2]）を検出
        prox_pattern = r'"([^"]+)"\[([a-z]+):~(\d+)\]'
        
        def _replace_proximity(match):
            terms = match.group(1).split()
            # ClinicalTrials.govではAND演算子に変換
            if len(terms) == 2:
                return f"({terms[0]} AND {terms[1]})"
            else:
                # 3語以上の場合は全てのタームをANDで結合
                return f"({' AND '.join(terms)})"
        
        return re.sub(prox_pattern, _replace_proximity, query_part)
    
    def _convert_field_tags(self, query_part: str) -> Tuple[str, str]:
        """フィールドタグを適切なClinicalTrials.govフィールドに変換
        
        Returns:
            Tuple[変換後のクエリ, フィールド名（"Condition"/"Intervention"/"Title"/"Other Terms"）]
        """
        # タグパターン
        mesh_pattern = r'\[Mesh\]|\[MeSH Terms\]|\[mh\]'
        tiab_pattern = r'\[Title/Abstract\]|\[tiab\]'
        title_pattern = r'\[Title\]|\[ti\]'
        ad_pattern = r'\[Affiliation\]|\[ad\]'
        
        # タグに基づいてフィールドを決定
        if re.search(mesh_pattern, query_part):
            field = "Condition"  # MeSH疾患名はConditionに
            # MeSH用語の展開
            cleaned = self._expand_mesh_terms(query_part)
        elif re.search(title_pattern, query_part):
            field = "Title"
            # タイトルフィールドの変換
            cleaned = re.sub(title_pattern, '', query_part)
            # 近接演算子の処理
            if ":~" in query_part:
                cleaned = self._convert_proximity(query_part)
            else:
                # 引用符の処理
                cleaned = cleaned.strip()
                if cleaned.startswith('"') and cleaned.endswith('"'):
                    cleaned = cleaned.strip('"')
                cleaned = f'"{cleaned}"'
        elif re.search(tiab_pattern, query_part):
            # 内容によって振り分け
            if any(term in query_part.lower() for term in ["treatment", "therapy", "drug", "medication"]):
                field = "Intervention"
            else:
                field = "Other Terms"
            
            # タグの削除と近接演算子の処理
            if ":~" in query_part:
                cleaned = self._convert_proximity(query_part)
            else:
                cleaned = re.sub(tiab_pattern, '', query_part).strip()
        elif re.search(ad_pattern, query_part):
            field = "Other Terms"
            if ":~" in query_part:
                cleaned = self._convert_proximity(query_part)
            else:
                # 所属機関フィールドはOther Termsとして扱う
                cleaned = re.sub(ad_pattern, '', query_part).strip()
                if cleaned.startswith('"') and cleaned.endswith('"'):
                    # 引用符内のスペースで区切られた単語をANDで結合
                    terms = cleaned.strip('"').split()
                    if len(terms) > 1:
                        cleaned = f"({' AND '.join(terms)})"
                    else:
                        cleaned = f'"{terms[0]}"'
        else:
            field = "Other Terms"
            cleaned = query_part
        
        return cleaned, field

    def convert_line(self, line_content: str) -> Dict[str, str]:
        """単一の検索行をClinicalTrials.gov形式に変換"""
        # 近接演算子を含む場合
        if ":~" in line_content:
            # タグパターン
            mesh_pattern = r'\[Mesh\]|\[MeSH Terms\]|\[mh\]'
            tiab_pattern = r'\[Title/Abstract\]|\[tiab\]'
            title_pattern = r'\[Title\]|\[ti\]'
            ad_pattern = r'\[Affiliation\]|\[ad\]'
            
            # 近接演算子パターン
            prox_pattern = r'"([^"]+)"\[([a-z]+):~(\d+)\]'
            
            match = re.search(prox_pattern, line_content)
            if match:
                terms = match.group(1).split()
                field_tag = match.group(2)
                proximity = match.group(3)
                
                # フィールドタグに基づいてフィールドを決定
                if field_tag in ['Mesh', 'MeSH Terms', 'mh']:
                    field = "Condition"
                elif field_tag in ['Title', 'ti']:
                    field = "Title"
                elif field_tag in ['Title/Abstract', 'tiab']:
                    if any(term in line_content.lower() for term in ["treatment", "therapy", "drug", "medication"]):
                        field = "Intervention"
                    else:
                        field = "Other Terms"
                elif field_tag in ['Affiliation', 'ad']:
                    field = "Other Terms"
                else:
                    field = "Other Terms"
                
                # 近接演算子をANDに変換
                if len(terms) == 2:
                    cleaned = f"({terms[0]} AND {terms[1]})"
                else:
                    cleaned = f"({' AND '.join(terms)})"
                
                return {field: cleaned}
        
        # 標準的な変換ルートを使用
        cleaned, field = self._convert_field_tags(line_content)
        return {field: cleaned}
    
    def convert(self, pubmed_query: str) -> Dict[str, str]:
        """PubMed検索式をClinicalTrials.gov形式に変換
        
        Args:
            pubmed_query: PubMed形式の検索式
            
        Returns:
            Dict[str, str]: フィールド名をキー、検索条件を値とした辞書
        """
        lines = [line.strip() for line in pubmed_query.split('\n') if line.strip()]
        
        # 行番号と実際のクエリを分離
        query_blocks = {}
        for line in lines:
            # #から始まる行番号がある場合
            if line.startswith('#'):
                parts = line.split(' ', 1)
                if len(parts) > 1:
                    query_blocks[parts[0]] = parts[1]
            else:
                # 行番号がない場合はそのまま処理
                query_blocks[f"#{len(query_blocks)+1}"] = line
        
        # 最終行（結合条件）を特定
        final_query = None
        for block_id, query in query_blocks.items():
            if all(other_id in query for other_id in query_blocks.keys() if other_id != block_id):
                final_query = query
                break
        
        # 最終行が見つからない場合は全てを統合
        if not final_query:
            # 単純なAND結合
            final_query = " AND ".join([f"({query})" for query in query_blocks.values()])
        
        # 結合条件を解析（#1 OR #2 AND #3 など）
        block_relations = {}
        
        # 各ブロックの内容をフィールド別に変換
        converted_blocks = {}
        for block_id, query in query_blocks.items():
            # 他のブロックを参照していない場合のみ変換
            if not any(other_id in query for other_id in query_blocks.keys() if other_id != block_id):
                converted = self.convert_line(query)
                converted_blocks[block_id] = converted
        
        # 最終検索式の構造を解析（例: (#1 OR #2) AND (#3 OR #4)）
        final_structure = final_query
        for block_id, converted in converted_blocks.items():
            # block_idが最終構造の中でどのように使われているか特定
            for field, value in converted.items():
                if field not in block_relations:
                    block_relations[field] = []
                block_relations[field].append(value)
        
        # フィールド別に条件をグループ化
        ct_query = {}
        for field, values in block_relations.items():
            # 同じフィールド内の条件をORで結合
            ct_query[field] = " OR ".join(values)
        
        return ct_query

def convert_to_clinicaltrials(pubmed_query: str) -> Dict[str, str]:
    """PubMed検索式をClinicalTrials.gov形式に変換するユーティリティ関数"""
    converter = ClinicalTrialsConverter()
    return converter.convert(pubmed_query)

def format_ct_output(ct_query: Dict[str, str]) -> str:
    """ClinicalTrials.gov変換結果を整形"""
    output = []
    for field, query in ct_query.items():
        output.append(f"{field}: {query}")
    
    result = '\n'.join(output)
    
    # Advanced Search UI表示形式も追加
    ui_parts = []
    for field, query in ct_query.items():
        ui_parts.append(f"( {field}: {query} )")
    
    ui_format = "\n\nAdvanced Search UI表示形式：\n```\n" + " AND\n".join(ui_parts) + "\n```"
    
    return result + ui_format

if __name__ == "__main__":
    # 単体テスト用
    test_query = """
    #1 "Essential Tremor"[Mesh]
    #2 "tremor therapy"[tiab:~2]
    #3 "deep brain"[Title:~0]
    #4 "hospital university"[ad:~5]
    #5 (#1 OR #2) AND (#3 OR #4)
    """
    
    ct_result = convert_to_clinicaltrials(test_query)
    print(format_ct_output(ct_result))
