# 検索式ブラッシュアップ結果サマリー

## 概要
膵臓がんとサルコペニアに関する検索式を、MeSH用語を追加することで強化しました。

## 元の検索式
```
1. ((pancreas OR pancreatic) AND (cancer* OR carcinoma* OR neoplas* OR tumo* OR cyst* OR growth* OR adenocarcinoma* OR adenoma* OR malig* OR mass* OR pancreatoblastoma* OR "intraductal papillary mucinous neoplasm" OR IPMN OR IPMNs)) AND (chemoradio* OR chemotherapy OR Fluoropyrimidine OR adriamycin* OR doxorubicin OR fluorouracil OR gemcitabine OR irinotecan OR Camptosar OR Campto OR camptothecin OR oxaliplatin OR paclitaxel OR mitomycin* OR "5-FU" OR FOLFIRINOX OR leucovorin OR FOLFOX OR FOLFIRI OR GEMOX OR S-1 OR SN-38 OR Capecitabine OR Onivyde)

2. (sarcopen* OR "muscle mass" OR "skeletal muscle" OR "muscle wasting" OR "muscular atrophy" OR "body composition" OR cachexia)

3. #1 AND #2
```

## 強化された検索式の主な改善点

### 1. 膵臓がん関連MeSH用語の追加
- **"Pancreatic Neoplasms"[Mesh]**: 膵臓腫瘍の包括的なMeSH用語
- **"Adenocarcinoma"[Mesh]**: 膵臓がんの最も一般的な組織型
- **"Carcinoma, Pancreatic Ductal"[Mesh]**: 膵管腺癌の特異的MeSH用語

### 2. 化学療法関連MeSH用語の追加
- **"Antineoplastic Combined Chemotherapy Protocols"[Mesh]**: 併用化学療法プロトコル
- **個別薬剤のMeSH用語**: "Fluorouracil"[Mesh], "Gemcitabine"[Mesh], "Irinotecan"[Mesh], "Oxaliplatin"[Mesh], "Paclitaxel"[Mesh], "Mitomycin"[Mesh], "Doxorubicin"[Mesh], "Leucovorin"[Mesh], "Capecitabine"[Mesh]

### 3. サルコペニア・筋萎縮関連MeSH用語の追加
- **"Sarcopenia"[Mesh]**: サルコペニアの主要MeSH用語
- **"Muscular Atrophy"[Mesh]**: 筋萎縮の一般的用語
- **"Muscle, Skeletal"[Mesh]**: 骨格筋の解剖学的用語
- **"Body Composition"[Mesh]**: 体組成測定を含む用語
- **"Cachexia"[Mesh]**: がん関連消耗症候群

## 検索戦略の利点

### 1. 感度の向上
- MeSH用語により、フリーテキストでは捕捉できない文献も検索可能
- 統制語彙により、同義語や表記ゆれに対応

### 2. 精度の維持
- 元のフリーテキスト用語をすべて保持
- 論理構造（#1 AND #2 AND #3）を維持

### 3. データベース横断対応
- PubMed/MEDLINE形式
- Cochrane CENTRAL形式
- Embase Dialog形式
- ClinicalTrials.gov形式
- ICTRP形式

## 生成されたファイル

1. **search_formula.md**: 強化された検索式（PubMed形式）
2. **all_database_search.md**: 全データベース対応版
3. **pico_definition.md**: PICO構造の詳細定義
4. **validation_report.md**: 検索式の検証結果
5. **original_search_formula.md**: 元の検索式の記録
6. **enhancement_summary.md**: 本サマリー

## 推奨事項

1. **検索実行前の確認**
   - 各データベースでの検索結果数を確認
   - 必要に応じて検索式の調整を検討

2. **継続的な改善**
   - 新しいMeSH用語の追加を定期的に確認
   - シード論文による検索式の妥当性検証

3. **文献管理**
   - 重複除去処理の実施
   - Rayyan等のスクリーニングツールとの連携

## 技術的詳細

- **SRWS システム使用**: 検索式開発支援システムを活用
- **MeSH階層分析**: extract_mesh.pyによる自動MeSH抽出機能
- **検証機能**: check_search_lines.pyによる行別検証
- **変換機能**: generate_all_database_search.pyによる自動変換

この強化により、膵臓がんとサルコペニアに関する包括的で精度の高い文献検索が可能になりました。
