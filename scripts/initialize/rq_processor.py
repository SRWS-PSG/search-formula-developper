#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class RQProcessor:
    def __init__(self, output_dir: str = "docs/analysis"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def process_rq_file(self, rq_file_path: str) -> Dict:
        """RQのmdファイルを読み込んで構造化データを生成"""
        with open(rq_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 構造化データの初期化
        structured_data = {
            'pico': self._extract_pico(content),
            'criteria': self._extract_criteria(content),
            'restrictions': self._extract_restrictions(content),
            'seed_studies': self._extract_seed_studies(content),
            'notes': self._extract_notes(content),
            'metadata': {
                'processed_at': datetime.now().isoformat(),
                'source_file': rq_file_path
            }
        }
        
        return structured_data

    def _extract_pico(self, content: str) -> Dict[str, str]:
        """PICO要素を抽出"""
        pico = {}
        
        # Population
        pop_match = re.search(r'### Population（対象集団）\n(.*?)\n\n', content, re.DOTALL)
        pico['population'] = pop_match.group(1).strip() if pop_match else None

        # Intervention
        int_match = re.search(r'### Intervention（介入）\n(.*?)\n\n', content, re.DOTALL)
        pico['intervention'] = int_match.group(1).strip() if int_match else None

        # Comparison
        comp_match = re.search(r'### Comparison（比較対照）\n(.*?)(?=\n\n### |$)', content, re.DOTALL)
        pico['comparison'] = comp_match.group(1).strip() if comp_match else None

        # Outcome
        out_match = re.search(r'### Outcome（アウトカム）\n(.*?)\n\n', content, re.DOTALL)
        pico['outcome'] = out_match.group(1).strip() if out_match else None

        return pico

    def _extract_criteria(self, content: str) -> Dict[str, List[str]]:
        """組み入れ基準と除外基準を抽出"""
        criteria = {
            'inclusion': [],
            'exclusion': []
        }
        
        # 組み入れ基準
        inclusion_section = re.search(r'## 2\. 組み入れ基準\n(.*?)\n\n', content, re.DOTALL)
        if inclusion_section:
            criteria['inclusion'] = [
                line.strip('- ').strip()
                for line in inclusion_section.group(1).split('\n')
                if line.strip().startswith('-')
            ]

        # 除外基準
        exclusion_section = re.search(r'## 3\. 除外基準\n(.*?)\n\n', content, re.DOTALL)
        if exclusion_section:
            criteria['exclusion'] = [
                line.strip('- ').strip()
                for line in exclusion_section.group(1).split('\n')
                if line.strip().startswith('-')
            ]

        return criteria

    def _extract_restrictions(self, content: str) -> Dict[str, str]:
        """追加の制限事項を抽出"""
        restrictions = {}
        
        restrictions_section = re.search(r'## 4\. 追加の制限事項\n(.*?)\n\n', content, re.DOTALL)
        if restrictions_section:
            for line in restrictions_section.group(1).split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip('- ').strip()
                    restrictions[key] = value.strip()

        return restrictions

    def _extract_seed_studies(self, content: str) -> List[str]:
        """シード研究を抽出"""
        studies = []
        
        studies_section = re.search(r'## 5\. シード研究（代表的な関連論文）\n(.*?)\n\n', content, re.DOTALL)
        if studies_section:
            studies = [
                line.strip('0123456789. ').strip()
                for line in studies_section.group(1).split('\n')
                if line.strip() and not line.strip().startswith('#')
            ]

        return studies

    def _extract_notes(self, content: str) -> str:
        """備考を抽出"""
        notes_match = re.search(r'## 6\. 備考\n(.*?)(?=\n\n|$)', content, re.DOTALL)
        return notes_match.group(1).strip() if notes_match else ""

    def save_structured_data(self, data: Dict, output_filename: str) -> str:
        """構造化データをJSONファイルとして保存"""
        output_path = self.output_dir / output_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        return str(output_path)

def main():
    # 使用例
    processor = RQProcessor()
    
    # RQファイルのパス
    rq_file = "path/to/your/rq_file.md"
    
    # RQの処理
    structured_data = processor.process_rq_file(rq_file)
    
    # 結果の保存
    output_file = f"rq_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    saved_path = processor.save_structured_data(structured_data, output_file)
    print(f"構造化データを保存しました: {saved_path}")

if __name__ == "__main__":
    main()
