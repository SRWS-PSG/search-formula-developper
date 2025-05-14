import re
from typing import List, Dict, Optional
import os
import sys

class ICTRPConverter:
    """PubMed検索式をICTRP形式に変換するクラス"""
    
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
            return '("essential tremor" OR "benign tremor" OR "familial tremor")'
        
        return f'"{clean_term}"'
        
    def _convert_proximity(self, query_part: str) -> str:
        """近接演算子を適切な形式に変換"""
        # 近接演算子パターン（例: "term1 term2"[tiab:~2]）を検出
        prox_pattern = r'"([^"]+)"\[([a-z]+):~(\d+)\]'
        
        def _replace_proximity(match):
            terms = match.group(1).split()
            # ICTRPでは近接演算子をサポートしていないため、ANDに変換
            if len(terms) == 2:
                return f"({terms[0]} AND {terms[1]})"
            else:
                # 3語以上の場合は全てのタームをANDで結合
                return f"({' AND '.join(terms)})"
        
        return re.sub(prox_pattern, _replace_proximity, query_part)
    
    def _convert_term(self, query_part: str) -> str:
        """検索語を適切なICTRP形式に変換"""
        # 近接演算子を含む場合
        if ":~" in query_part:
            # 近接演算子パターン
            prox_pattern = r'"([^"]+)"\[([a-z]+):~(\d+)\]'
            
            match = re.search(prox_pattern, query_part)
            if match:
                terms = match.group(1).split()
                # ICTRPでは近接演算子をサポートしていないため、ANDに変換
                if len(terms) == 2:
                    return f"({terms[0]} AND {terms[1]})"
                else:
                    return f"({' AND '.join(terms)})"
            
            # パターンにマッチしない場合はそのまま
            return query_part
            
        # タグパターン
        mesh_pattern = r'\[Mesh\]|\[MeSH Terms\]|\[mh\]'
        tiab_pattern = r'\[Title/Abstract\]|\[tiab\]'
        title_pattern = r'\[Title\]|\[ti\]'
        ad_pattern = r'\[Affiliation\]|\[ad\]'
        
        # タグに基づいて変換
        if re.search(mesh_pattern, query_part):
            # MeSH用語の展開
            cleaned = self._expand_mesh_terms(query_part)
        elif re.search(title_pattern, query_part) or re.search(tiab_pattern, query_part) or re.search(ad_pattern, query_part):
            # タグの削除
            cleaned = re.sub(r'\[[^\]]+\]', '', query_part).strip()
            
            # 引用符内のスペースで区切られた単語を処理
            if cleaned.startswith('"') and cleaned.endswith('"'):
                terms = cleaned.strip('"').split()
                if len(terms) > 1:
                    # ICTRPではスペースで区切られた複数単語をそのまま使用
                    cleaned = f'"{" ".join(terms)}"'
        else:
            # その他のタグなし検索語
            cleaned = query_part
        
        return cleaned

    def convert_line(self, line_content: str) -> str:
        """単一の検索行をICTRP形式に変換"""
        return self._convert_term(line_content)
    
    def convert(self, pubmed_query: str) -> str:
        """PubMed検索式をICTRP形式に変換
        
        Args:
            pubmed_query: PubMed形式の検索式
            
        Returns:
            str: ICTRP形式の検索文字列
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
        
        # 各ブロックの内容を変換
        converted_blocks = {}
        for block_id, query in query_blocks.items():
            # 他のブロックを参照していない場合のみ変換
            if not any(other_id in query for other_id in query_blocks.keys() if other_id != block_id):
                converted = self.convert_line(query)
                converted_blocks[block_id] = converted
        
        # 最終検索式の構造を解析（例: (#1 OR #2) AND (#3 OR #4)）
        ictrp_query = final_query
        
        # ブロック参照を変換後の内容に置換
        for block_id, converted in converted_blocks.items():
            # 独立したブロック参照のみを置換
            pattern = r'(?<!\w)' + re.escape(block_id) + r'(?!\w)'
            ictrp_query = re.sub(pattern, converted, ictrp_query)
        
        # 括弧の正規化（ICTRP対応）
        ictrp_query = self._normalize_brackets(ictrp_query)
        
        # 大文字のブール演算子に変換
        ictrp_query = re.sub(r'\bAND\b', 'AND', ictrp_query, flags=re.IGNORECASE)
        ictrp_query = re.sub(r'\bOR\b', 'OR', ictrp_query, flags=re.IGNORECASE)
        ictrp_query = re.sub(r'\bNOT\b', 'NOT', ictrp_query, flags=re.IGNORECASE)
        
        return ictrp_query
    
    def _normalize_brackets(self, query: str) -> str:
        """括弧の深さを制限し、ICTRPに適した形式に正規化"""
        # 括弧の深さを確認し、必要に応じて調整
        open_count = 0
        max_depth = 2  # ICTRPでは浅い括弧構造が推奨
        
        chars = list(query)
        for i, char in enumerate(chars):
            if char == '(':
                open_count += 1
                if open_count > max_depth:
                    # 深い括弧を削除して論理演算子に置き換え
                    chars[i] = ' '
            elif char == ')':
                if open_count > max_depth:
                    chars[i] = ' '
                else:
                    open_count = max(0, open_count - 1)
        
        return ''.join(chars)

def convert_to_ictrp(pubmed_query: str) -> str:
    """PubMed検索式をICTRP形式に変換するユーティリティ関数"""
    converter = ICTRPConverter()
    return converter.convert(pubmed_query)

if __name__ == "__main__":
    # 単体テスト用
    test_query = """
    #1 "Essential Tremor"[Mesh]
    #2 "tremor therapy"[tiab:~2]
    #3 "deep brain"[Title:~0]
    #4 "hospital university"[ad:~5]
    #5 (#1 OR #2) AND (#3 OR #4)
    """
    
    ictrp_result = convert_to_ictrp(test_query)
    print("ICTRP Query:")
    print(ictrp_result)
