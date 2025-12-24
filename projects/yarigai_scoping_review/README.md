# 日本の医師における「やりがい」：スコーピングレビュー（プロトコル）

## プロジェクト概要

**研究者**: 島尻大輝
**所属**: 名古屋大学医学部医学科
**連絡先**: daiki20041213@gmail.com
**科研費**: 25K13585
**プロジェクト作成日**: 2025-11-05

## リサーチクエスチョン

1. **RQ1**: 日本の医師における仕事のやりがいとは何か？
2. **RQ2**: 日本国外の医師における仕事のやりがいとは何か？

## 背景

医師は日々多くの業務に追われ、長時間労働や重い責任の中で働いている。それでも多くの医師は、患者の回復や感謝の言葉、仲間との協力、専門的な知識を生かせることなどに「やりがい」を感じながら仕事を続けている。

しかし、医師がどのようなときにやりがいを感じ、どんな要因がそれを支えているのかについては、まだ十分に整理されていない。このスコーピングレビューでは、医師の「やりがい」に関する研究を幅広く調べ、どのように定義され、どんな要素や背景が関係しているのかを明らかにすることを目的とする。

## 実施済み作業

### 1. リポジトリのセットアップ
- [x] プライベートリポジトリの作成（youkiti/search-formula-developper-yarigai）
- [x] リモート設定の変更（originをyoukitiリポジトリに設定）
- [x] プロジェクトディレクトリの作成（`search_formula/yarigai_scoping_review/`）

### 2. CLAUDE.mdの作成
- [x] システムアーキテクチャの文書化
- [x] 主要コマンドの一覧作成
- [x] 検索式開発ワークフローの説明
- [x] データベース変換ルールの記載

**ファイル**: [../../CLAUDE.md](../../CLAUDE.md)

### 3. 検索式の開発（PubMed/MEDLINE）
- [x] PCCフレームワークに基づく検索式設計
- [x] Population（医師）ブロックの構築
- [x] Concept（やりがい）ブロックの構築（10サブカテゴリー）
- [x] Context（日本）ブロックの構築
- [x] 最終検索式の統合（RQ1, RQ2）

**ファイル**: [search_formula.md](search_formula.md)

#### 検索式の構造

```
#1 Population (医師)
├── MeSH用語: "Physicians"[Mesh], "General Practitioners"[Mesh]
└── フリーテキスト: physician*, doctor*, clinician*, etc.

#2 Concept (やりがい関連概念)
├── #2A: MeSH用語（8つの統制語彙）
├── #2B: Meaningful Work（有意義な仕事）
├── #2C: Work Engagement（ワークエンゲージメント）
├── #2D: Calling/Vocation（天職・召命）
├── #2E: Motivation（動機付け）
├── #2F: Satisfaction（満足感）
├── #2G: Professional Fulfillment（専門職としての充足感）
├── #2H: 日本語概念（yarigai, ikigai）
├── #2I: 心理的ニーズ/Thriving
└── #2J: Task Significance（仕事の重要性）

#3 測定尺度（オプション）
└── WAMI, CVQ, PFI, UWES, BPNSWS, etc.

#4 日本関連（RQ1用）
└── Japan[Mesh], Japan[tiab], Japanese[tiab], etc.

最終検索式:
- RQ1: #1 AND #2 AND #4
- RQ2: #1 AND #2
```

### 4. PICO定義の作成
- [x] PCCフレームワークの詳細定義
- [x] 組み入れ基準・除外基準の明確化
- [x] シード論文の特定（Nishigori et al. 2024）
- [x] 検索データベースの選定（6データベース）

**ファイル**: [pico_definition.md](pico_definition.md)

### 5. 検索戦略の詳細説明
- [x] 検索戦略の設計原則の説明
- [x] 各検索ブロックの設計意図の文書化
- [x] 妥当性検証手順の記載
- [x] 想定される課題と対応策の整理

**ファイル**: [search_strategy_explanation.md](search_strategy_explanation.md)

## プロジェクトファイル一覧

```
search_formula/yarigai_scoping_review/
├── README.md                          # 本ファイル（プロジェクト概要）
├── pico_definition.md                 # PICO/PCC定義と組み入れ基準
├── search_formula.md                  # PubMed検索式（実行可能形式）
└── search_strategy_explanation.md     # 検索戦略の詳細説明
```

## 次のステップ

### ステップ1: シード論文の特定と準備
- [ ] Nishigori et al. (2024)のPMIDを取得
- [ ] 追加のシード論文（4-9本）を文献検索で特定
- [ ] `seed_pmids.txt`ファイルを作成（1行に1 PMID）

### ステップ2: 検索式の検証
- [ ] 各検索行のヒット件数を確認
  ```bash
  python scripts/search/term_validator/check_search_lines.py \
    --input-formula search_formula/yarigai_scoping_review/search_formula.md \
    --output search_formula/yarigai_scoping_review/search_lines_results.md
  ```

- [ ] シード論文のMeSH用語を分析
  ```bash
  python scripts/search/extract_mesh.py \
    --pmid-file search_formula/yarigai_scoping_review/seed_pmids.txt \
    --output-dir search_formula/yarigai_scoping_review/
  ```

- [ ] 最終検索式を実行してシード論文の包含を確認
  ```bash
  python scripts/search/query_executor/check_final_query.py \
    --formula-file search_formula/yarigai_scoping_review/search_formula.md \
    --pmid-file search_formula/yarigai_scoping_review/seed_pmids.txt \
    --output-dir search_formula/yarigai_scoping_review/
  ```

### ステップ3: 検索式の調整
- [ ] MeSH分析結果に基づいて不足している用語を追加
- [ ] ヒット件数が適切か評価（RQ1: 2,000-5,000件を想定）
- [ ] シード論文が全て捕捉されているか確認
- [ ] 必要に応じて検索式を修正

### ステップ4: 他データベースへの変換
- [ ] Embase (Dialog形式)への変換
- [ ] CENTRAL (Cochrane)への変換
- [ ] ClinicalTrials.govへの変換
- [ ] ICTRPへの変換
- [ ] PsycInfoへの適応（手動調整）
- [ ] ERICへの適応（手動調整）
- [ ] 医中誌（ICHUSHI）への変換（日本語キーワード）

**コマンド例（全データベース一括変換）**:
```bash
python scripts/conversion/generate_all_database_search.py \
  --input search_formula/yarigai_scoping_review/search_formula.md \
  --output-dir search_formula/yarigai_scoping_review/
```

### ステップ5: 実際の検索実行
- [ ] PubMedで検索実行、結果をRISファイルでエクスポート
- [ ] Embaseで検索実行、結果をエクスポート
- [ ] CENTRALで検索実行、結果をエクスポート
- [ ] PsycInfoで検索実行、結果をエクスポート
- [ ] ERICで検索実行、結果をエクスポート
- [ ] CINAHLで検索実行、結果をエクスポート
- [ ] 医中誌で検索実行、結果をエクスポート
- [ ] ClinicalTrials.govで検索実行、結果をエクスポート
- [ ] ICTRPで検索実行、結果をエクスポート

### ステップ6: 検索結果の処理
- [ ] 全データベースの結果を統合
- [ ] 重複を除外
- [ ] Rayyan用CSVファイルを作成
- [ ] PRISMAフローチャート用統計を生成

**コマンド**:
```bash
python scripts/search_results_to_review/search_results_processor.py \
  --input-dir search_formula/yarigai_scoping_review/ \
  --output-dir search_formula/yarigai_scoping_review/processed/
```

### ステップ7: スクリーニング
- [ ] Rayyanにアップロード
- [ ] タイトル・抄録スクリーニング（二人レビュアー）
- [ ] フルテキストレビュー（二人レビュアー）
- [ ] データ抽出

### ステップ8: データ統合と報告
- [ ] 質的統合（テーマ別分類）
- [ ] 表と図の作成
- [ ] PRISMAフローチャートの作成
- [ ] 論文執筆

## 検索データベース

| データベース | 主な特徴 | 検索予定日 | ステータス |
|------------|---------|----------|----------|
| **MEDLINE (PubMed)** | 医学文献の中心的DB | 未定 | 検索式完成 |
| **Embase** | 欧州中心、薬学文献 | 未定 | 変換予定 |
| **APA PsycInfo** | 心理学関連文献 | 未定 | 変換予定 |
| **ERIC** | 教育関連文献 | 未定 | 変換予定 |
| **CINAHL** | 看護・医療専門職 | 未定 | 変換予定 |
| **医中誌 (ICHUSHI)** | 日本語医学文献 | 未定 | 変換予定 |

**補助的検索**:
- ClinicalTrials.gov（臨床試験登録）
- ICTRP（WHO国際臨床試験登録）
- 総説論文の引用・被引用文献

## キーワードと概念

### 主要概念（Concept）
- Meaningful work / work meaningfulness
- Work engagement (vigor, dedication, absorption)
- Calling orientation / vocational calling
- Prosocial motivation / intrinsic motivation
- Job satisfaction / professional satisfaction
- Professional fulfillment
- Compassion satisfaction
- Thriving at work
- Psychological need satisfaction
- Task significance

### 測定尺度
- Work and Meaning Inventory (WAMI)
- Calling and Vocation Questionnaire (CVQ)
- Professional Fulfillment Index (PFI)
- Utrecht Work Engagement Scale (UWES)
- Basic Psychological Need Satisfaction at Work Scale (BPNSWS)
- Thriving at Work Scale
- Job Diagnostic Survey (JDS)
- Professional Quality of Life (ProQOL)

### 日本語概念
- やりがい (yarigai)
- 生きがい (ikigai)

## 方法論的枠組み

### スコーピングレビューの枠組み
- **PRISMA-ScR**: PRISMA extension for scoping reviews
- **JBI Framework**: Joanna Briggs Institute の5ステージフレームワーク

### レビュープロセス
1. リサーチクエスチョンの特定 ✓
2. 関連する研究の特定（検索式開発） ✓
3. 研究の選択（スクリーニング）
4. データのチャーティング（抽出）
5. 結果の整理、要約、報告

### 二人レビュー体制
- タイトル・抄録スクリーニング: 独立した二人のレビュアー
- フルテキストレビュー: 独立した二人のレビュアー
- データ抽出: 独立した二人のレビュアー
- 不一致の解決: 議論、必要に応じて第三レビュアー

## 参考文献

### 主要シード論文
Nishigori H, Shimazono Y, Busari J, Dornan T. Exploring yarigai: The meaning of working as a physician in teaching medical professionalism. Med Teach. 2024 Nov;46(11):1486–93. Available from: http://dx.doi.org/10.1080/0142159X.2024.2316227

### 方法論的参考文献
- PRISMA-ScR: Tricco AC, et al. PRISMA Extension for Scoping Reviews (PRISMA-ScR): Checklist and Explanation. Ann Intern Med. 2018;169(7):467-473.
- JBI Methodology: Peters MDJ, et al. Chapter 11: Scoping Reviews. JBI Manual for Evidence Synthesis. 2020.

## 連絡先

**研究責任者**: 島尻大輝
**所属**: 名古屋大学医学部医学科
**Email**: daiki20041213@gmail.com

## ライセンスと利益相反

**科研費**: 25K13585
**利益相反**: なし

---

**最終更新日**: 2025-11-05
**バージョン**: 1.0
**ステータス**: 検索式開発完了、検証待ち
