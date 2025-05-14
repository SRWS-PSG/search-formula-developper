#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path
from datetime import datetime
from rq_processor import RQProcessor

def create_rq_file(template_path: str, output_path: str) -> None:
    """RQテンプレートから新しいRQファイルを作成"""
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(template_content)

def process_rq(rq_file_path: str) -> None:
    """RQファイルを処理し、構造化データを生成"""
    processor = RQProcessor()
    
    try:
        # RQファイルの処理
        structured_data = processor.process_rq_file(rq_file_path)
        
        # 結果の保存
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"rq_analysis_{timestamp}.json"
        saved_path = processor.save_structured_data(structured_data, output_file)
        
        print(f"RQ分析結果を保存しました: {saved_path}")
        
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("使用方法:")
        print("1. 新規RQファイル作成:")
        print("   python main.py create <output_path>")
        print("2. 既存RQファイルの処理:")
        print("   python main.py process <rq_file_path>")
        sys.exit(1)

    command = sys.argv[1]
    
    if command == "create":
        if len(sys.argv) != 3:
            print("出力パスを指定してください")
            sys.exit(1)
            
        template_path = "templates/rq_template.md"
        output_path = sys.argv[2]
        create_rq_file(template_path, output_path)
        print(f"新しいRQファイルを作成しました: {output_path}")
        
    elif command == "process":
        if len(sys.argv) != 3:
            print("RQファイルのパスを指定してください")
            sys.exit(1)
            
        rq_file_path = sys.argv[2]
        process_rq(rq_file_path)
        
    else:
        print(f"不明なコマンドです: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
