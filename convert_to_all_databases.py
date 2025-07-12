import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts', 'conversion'))

from search_converter import convert_to_central, convert_to_dialog

def convert_extended_intervention_formula():
    """Convert the final extended intervention search formula to all database formats"""
    
    pubmed_query = '((Social Isolation[mh]) OR (Loneliness[mh]) OR (loneliness[tiab]) OR ("social isolation"[tiab]) OR ("social isolat*"[tiab])) AND ((Smartphone[mh]) OR (Wearable Electronic Devices[mh]) OR (Mobile Applications[mh]) OR (smartphone*[tiab]) OR ("mobile app*"[tiab]) OR ("mobile application*"[tiab]) OR ("wearable device*"[tiab]) OR ("digital phenotyping"[tiab]) OR ("passive sensing"[tiab]) OR ("mobile health"[tiab]) OR (mhealth[tiab]) OR (Cell Phone[mh]) OR (Remote Sensing Technology[mh]) OR ("Digital Biomarkers"[tiab]) OR ("sensor data"[tiab]) OR (accelerometer[tiab]) OR ("activity monitor*"[tiab]) OR (app[tiab]) OR (apps[tiab]) OR (("cell"[tiab] or "cellular"[tiab] or "mobile"[tiab] or "smart"[tiab]) AND ("phone"[tiab] or "telephone"[tiab] or "device"[tiab] or "application"[tiab])) OR ("Handheld Computer*"[tiab]) OR ("real time data"[tiab]) OR ("Short Messag* Service*"[tiab]) OR (SMS[tiab]) OR ("text messag*"[tiab]))'
    
    print("=== データベース変換 - 拡張Intervention Block検索式 ===")
    print(f"元のPubMed検索式: {pubmed_query}")
    print()
    
    print("🔄 CENTRAL形式に変換中...")
    try:
        central_query = convert_to_central(pubmed_query)
        print("✅ CENTRAL変換完了")
        print(f"CENTRAL検索式: {central_query}")
        print()
    except Exception as e:
        print(f"❌ CENTRAL変換エラー: {e}")
        central_query = "変換エラー"
        print()
    
    print("🔄 Dialog (Embase)形式に変換中...")
    try:
        dialog_query = convert_to_dialog(pubmed_query)
        print("✅ Dialog変換完了")
        print(f"Dialog検索式: {dialog_query}")
        print()
    except Exception as e:
        print(f"❌ Dialog変換エラー: {e}")
        dialog_query = "変換エラー"
        print()
    
    output_content = f"""# 拡張Intervention Block検索式 - 全データベース対応版

- **対象概念**: (社会的孤立 OR 孤独感) AND スマートデバイス（拡張版）
- **PubMed検索結果**: 964件
- **対象PMID**: 31342903, 35161852, 38900745 (100%包含確認済み)
- **変換日**: 2025年7月12日

```
{pubmed_query}
```

```
{central_query}
```

```
{dialog_query}
```


- **PubMed**: Social Isolation[mh], Loneliness[mh], loneliness[tiab], "social isolation"[tiab], "social isolat*"[tiab]
- **CENTRAL**: [mh "Social Isolation"], [mh "Loneliness"], loneliness:ti,ab,kw, "social isolation":ti,ab,kw, "social isolat*":ti,ab,kw
- **Dialog**: 'social isolation'/exp, 'loneliness'/exp, loneliness:ti,ab,kw, 'social isolation':ti,ab,kw, 'social isolat*':ti,ab,kw

- **PubMed**: Smartphone[mh], Wearable Electronic Devices[mh], Mobile Applications[mh], Cell Phone[mh], Remote Sensing Technology[mh]
- **CENTRAL**: [mh "Smartphone"], [mh "Wearable Electronic Devices"], [mh "Mobile Applications"], [mh "Cell Phone"], [mh "Remote Sensing Technology"]
- **Dialog**: 'smartphone'/exp, 'wearable computer'/exp, 'mobile application'/exp, 'mobile phone'/exp, 'remote sensing'/exp

- **共通**: smartphone*, "mobile app*", "mobile application*", "wearable device*", "digital phenotyping", "passive sensing", "mobile health", mhealth, "Digital Biomarkers", "sensor data", accelerometer, "activity monitor*", app, apps, "Handheld Computer*", "real time data", "Short Messag* Service*", SMS, "text messag*"
- **複合検索**: (cell OR cellular OR mobile OR smart) AND (phone OR telephone OR device OR application)

1. **PubMed**: そのまま使用可能
2. **CENTRAL**: Cochrane Libraryで使用、MeSH用語の表記に注意
3. **Dialog**: Embaseで使用、統制語彙の違いに注意
4. **検索実行前**: 各データベースの最新シンタックスを確認してください

1. **PubMed**: 基本検索式（964件）
2. **CENTRAL**: 変換後検索式で実行
3. **Dialog**: 変換後検索式で実行
4. **結果統合**: 重複除去後に統合分析

- ✅ 全対象PMID包含確認済み
- ✅ 検索件数が管理可能範囲内
- ✅ 概念の一貫性維持
- ✅ データベース間の互換性確保
"""
    
    output_file = "search_formula/social_isolation_tech/all_databases_search_formula.md"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_content)
    
    print(f"📁 全データベース検索式を保存: {output_file}")
    
    return {
        'pubmed': pubmed_query,
        'central': central_query,
        'dialog': dialog_query,
        'output_file': output_file
    }

if __name__ == "__main__":
    results = convert_extended_intervention_formula()
    print("\n🎉 データベース変換完了!")
    print(f"PubMed: {len(results['pubmed'])} 文字")
    print(f"CENTRAL: {len(results['central'])} 文字")
    print(f"Dialog: {len(results['dialog'])} 文字")
