#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# .envファイルから環境変数を読み込む
load_dotenv()

def test_gemini_api():
    # APIキーの設定
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEYが設定されていません")
        return
    
    print(f"Using API key: {api_key[:5]}...{api_key[-5:]}")
    
    # APIの設定
    genai.configure(api_key=api_key)
    
    # 簡単なプロンプト
    prompt = """JSONで応答してください:
{
  "mesh_p": ["Diabetes Mellitus", "Obesity"],
  "keyword_p": ["diabetes", "obese"],
  "mesh_i": ["Diet, Reducing", "Exercise"],
  "keyword_i": ["diet therapy", "physical activity"],
  "pmids": ["12345678", "23456789"]
}"""
    
    print("=== 送信するプロンプト ===")
    print(prompt)
    
    # モデルの設定
    print("\n=== モデルの設定 ===")
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-pro-exp-03-25",
            generation_config={"temperature": 0}
        )
        print("モデル設定完了")
    except Exception as e:
        print(f"モデル設定エラー: {e}")
        import traceback
        traceback.print_exc()
        return
    
    try:
        # API呼び出し
        print("\n=== API呼び出し開始 ===")
        response = model.generate_content(prompt)
        print("API呼び出し完了")
        
        # レスポンスの詳細を出力
        print("\n=== API Response Details ===")
        print(f"Response type: {type(response)}")
        print(f"Has 'text' attribute: {hasattr(response, 'text')}")
        if hasattr(response, 'text'):
            print(f"Text value: '{response.text}'")
            print(f"Text type: {type(response.text)}")
        
        # より詳細なレスポンス情報
        if hasattr(response, 'candidates'):
            print("\n=== Candidates ===")
            for i, candidate in enumerate(response.candidates):
                print(f"Candidate {i}:")
                print(f"  content: {candidate.content if hasattr(candidate, 'content') else 'N/A'}")
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    for j, part in enumerate(candidate.content.parts):
                        print(f"    Part {j}: {part}")
                        if hasattr(part, 'text'):
                            print(f"      Text: {part.text[:100]}...")
        
        # 利用可能な属性をすべて表示
        print("\n=== All Available Attributes ===")
        for attr in dir(response):
            if not attr.startswith('_'):  # 内部/プライベート属性を除外
                try:
                    value = getattr(response, attr)
                    if not callable(value):  # メソッドを除外
                        print(f"{attr}: {value}")
                except Exception as e:
                    print(f"{attr}: Error accessing - {e}")
        
        # JSONとして解析してみる
        try:
            if hasattr(response, 'text') and response.text:
                json_data = json.loads(response.text)
                print("\n=== Successfully parsed as JSON ===")
                print(json_data)
        except json.JSONDecodeError as e:
            print(f"\n=== JSON parse error: {e} ===")
            
    except Exception as e:
        print(f"APIエラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gemini_api()
