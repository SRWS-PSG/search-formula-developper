# Search Formula Reviewer Skill

このスキルは、systematic reviewプロジェクトのフォルダを指定すると、protocol（組み入れ基準）と検索式の対応レビュー、seed論文を活用したpearl growing、MeSH実行を含む検索式の包括的レビューを一括で行います。

## 発動条件

ユーザーが以下のような自然言語で要求した場合に、このスキルを実行してください:

- 「検索式をレビューして」
- 「検索式の包括的レビュー」
- 「pearl growingを実行」
- 「組み入れ基準と検索式の対応を確認」
- 「検索式を総合的にチェック」
- 「search formula review」
- 「検索戦略をレビュー」
- 「検索式の妥当性を評価して」
- 「protocolと検索式の整合性を確認」

## 入力パラメータ

### 必須パラメータ
- **project_dir**: プロジェクトディレクトリのパス (例: `projects/yamamoto/`)

### 自動検出されるファイル
スキル実行時に、以下のファイルをproject_dir内から自動検出します:
- `protocol.md` - プロトコルファイル（組み入れ基準・PICO定義）
- `search_formula.md` - 検索式ファイル
- `seed_pmids.txt` または `seed.txt` - Seed論文のPMIDリスト
- `mesh_analysis.md` / `mesh_analysis_results.json` - 既存のMeSH分析結果（あれば再利用）

### オプションパラメータ
- **skip_phases**: スキップするフェーズ番号のリスト (例: `[1]` でフェーズ1をスキップ)
- **focus**: 特定のフェーズのみ実行 (例: `pearl_growing` でフェーズ2のみ)

## 実行概要

このスキルは3つのフェーズで構成されます:

```
Phase 1: 組み入れ基準 ↔ 検索式 対応レビュー（protocol.md ベース）
Phase 2: Pearl Growing（seed論文ベースの検索語拡張提案）
Phase 3: 検索式の技術的レビュー（MeSH実行・ヒット数・構造確認）
```

---

## Phase 1: 組み入れ基準と検索式の対応レビュー

### 目的
protocolに記載された組み入れ基準（PICO/PCC）の各要素が検索式のブロックとして適切にカバーされているかを確認する。

### 実行手順

#### 1-1. protocol.mdの読み込みと要素抽出

protocol.mdから以下の要素を抽出する:

```
- Population/Participants: 対象疾患・患者群
- Intervention/Concept: 介入・コンセプト
- Comparison: 比較対照（該当する場合）
- Outcome: アウトカム（該当する場合）
- Context: コンテキスト（該当する場合）
- 組み入れ基準: 具体的な条件リスト
- 除外基準: 除外条件リスト
- 研究デザイン制限: RCTのみ、Case reportを含む、等
- 言語制限: English only、制限なし、等
- 出版年制限: 2022年以降、等
- 検索対象データベース: MEDLINE, Embase, CENTRAL等
```

#### 1-2. search_formula.mdの読み込みとブロック解析

検索式ファイルから以下を抽出する:

```
- 各ブロック（#1, #2, #3, ...）の名前と内容
- 最終結合式（#N AND #M 形式）
- フィルタ条件（言語、出版年、Humans等）
- 使用されているMeSH terms一覧
- 使用されているフリーワード一覧
```

#### 1-3. 対応マトリクスの作成

protocolの各要素と検索式ブロックの対応関係を表にまとめる。

### Phase 1 出力例

```markdown
## 📋 Phase 1: 組み入れ基準 ↔ 検索式 対応レビュー

### 対応マトリクス

| Protocol要素 | 対応ブロック | カバー状況 | コメント |
|-------------|------------|-----------|---------|
| **Population**: RA, sJIA, AOSD | #1 | ✅ 十分 | RA, JIA, Still's diseaseのMeSH+フリーワードを網羅 |
| **Concept**: Biologics, JAKi | #2 | ⚠️ 一部不足 | Ozoralizumab, Peficitinibのフリーワードなし |
| **Concept**: Paradoxical reactions | #3 | ✅ 十分 | 類義語も広くカバー |
| **言語制限** | - | ❌ 未設定 | Protocolに言語制限の記載なし→フィルタなしで適切 |
| **出版年制限** | - | ❌ 未設定 | Protocolに出版年制限の記載なし→フィルタなしで適切 |
| **研究デザイン**: Case report含む | - | ✅ 適切 | Study design filterなし→Case reportも捕捉可能 |

### 詳細分析

#### ✅ 適切にカバーされている要素
1. **Population (#1)**:
   - "Arthritis, Rheumatoid"[MeSH] → RA
   - "Arthritis, Juvenile"[MeSH] → JIA
   - "Still's Disease"[tiab] → AOSD
   - ✅ Protocolの対象疾患3つすべてをカバー

2. **Paradoxical Reactions (#3)**:
   - Paradoxical reactions/effects → 主概念
   - Drug-induced psoriasis/sarcoidosis/lupus → 具体的PR
   - Immune-mediated adverse events → 広義の定義
   - ✅ Protocolの4.2.2節の用語リストと一致

#### ⚠️ 潜在的なギャップ
1. **Concept (#2) - 薬剤リストの不一致**:
   - Protocolに記載されているがフリーワード未記載:
     - Ozoralizumab (日本のみ承認、MeSH未登録)
     - Peficitinib (日本のみ承認、MeSH未登録)
   - **推奨**: `ozoralizumab[tiab] OR peficitinib[tiab]` を追加

2. **Rituximab**:
   - Protocol記載あり、検索式に rituximab[tiab] は含まれているが "Rituximab"[MeSH]は未確認
   - **推奨**: MeSH termの存在を確認し追加を検討

#### ❌ 未カバーの要素
（該当なし、または該当する場合にリスト表示）

### Protocol ↔ 検索式 整合性スコア
- **カバー率**: 8/9要素 (89%)
- **判定**: ⚠️ 軽微な修正推奨
```

---

## Phase 2: Pearl Growing（seed論文ベースの検索語拡張提案）

### 目的
seed論文の書誌情報・MeSH terms・タイトル/アブストラクトを分析し、現在の検索式に含まれていない有用な検索語を発見する。

### 実行手順

#### 2-1. Seed PMIDsの読み込み

```python
# seed_pmids.txt または seed.txt からPMIDを読み込み
# コメント行（#始まり）と空行を除外
```

#### 2-2. PubMed APIで各seed論文の詳細情報を取得

各PMIDについて以下を取得:
- タイトル
- アブストラクト
- MeSH terms（Major Topic / Minor Topicの区別含む）
- 著者キーワード
- 出版年
- ジャーナル名

**実行方法**: `scripts/search/extract_mesh.py` を使用するか、既存の `mesh_analysis_results.json` があればそれを再利用する。

```bash
# MeSH分析がまだ行われていない場合
python scripts/search/extract_mesh.py \
  --pmid-file {pmid_file} \
  --output-dir {project_dir}
```

#### 2-3. 検索式との差分分析

以下の観点で差分を分析する:

**A. MeSH term差分**
- seed論文に付与されているが検索式に含まれていないMeSH terms
- 特にMajor Topicとして付与されているものを優先
- 頻出度（N/M論文に出現）でランキング

**B. タイトル/アブストラクトからのキーワード候補**
- seed論文のタイトルに含まれるが検索式にないキーワード
- 特に以下のパターンを重視:
  - 疾患の別名・略語
  - 薬剤の一般名・商品名
  - 概念の同義語

**C. 著者キーワード差分**
- 著者が指定したキーワードで検索式にないもの

#### 2-4. Pearl Growing 推奨事項の生成

各候補について以下を評価:
- PubMed単独でのヒット数
- 現在の検索式にANDした場合の追加ヒット数
- seed論文捕捉への影響

### Phase 2 出力例

```markdown
## 🔍 Phase 2: Pearl Growing（検索語拡張提案）

### Seed論文情報
- **分析論文数**: 4件
- **PMID**: 22505694, 17994192, 26965410, 28115268

### Seed論文のMeSH Terms分析

#### 全Seed論文に共通するMeSH Terms
| MeSH Term | 頻度 | Major Topic | 検索式に含まれる? |
|-----------|------|------------|-----------------|
| Arthritis, Rheumatoid | 4/4 | 3/4 | ✅ #1 |
| Tumor Necrosis Factor Inhibitors | 3/4 | 2/4 | ✅ #2 |
| Psoriasis | 3/4 | 2/4 | ❌ |
| Dermatitis | 2/4 | 1/4 | ❌ |
| Drug Eruptions | 2/4 | 2/4 | ❌ |

#### 🆕 検索式に未含のMeSH Terms（追加候補）

| # | MeSH Term | 頻度 | ヒット数 | 追加効果 | 推奨度 |
|---|----------|------|---------|---------|-------|
| 1 | "Psoriasis"[Mesh] | 3/4 | 89,234件 | ⚠️ 広すぎる可能性 | 要検討 |
| 2 | "Drug Eruptions"[Mesh] | 2/4 | 12,456件 | #3ブロックに追加推奨 | ⭐ 高 |
| 3 | "Skin Diseases"[Mesh] | 2/4 | 345,678件 | 広すぎる | ❌ 不要 |

### タイトル/アブストラクトからの追加候補

| # | キーワード候補 | 出現論文 | 現在の検索式 | PubMedヒット数 | 推奨 |
|---|-------------|---------|------------|--------------|------|
| 1 | "TNF-alpha inhibitor"[tiab] | 2/4 | ❌ | 1,234件 | ⭐ 追加推奨 |
| 2 | "anti-TNF"[tiab] | 3/4 | ❌ | 23,456件 | ⭐ 追加推奨 |
| 3 | "biologic therapy"[tiab] | 2/4 | ❌ | 5,678件 | 要検討 |

### Pearl Growing サマリー

#### 優先度高（追加推奨）
1. `"Drug Eruptions"[Mesh]` → #3ブロックに追加
   - 理由: 2/4のseed論文でMajor Topic、PRの上位概念として有用
2. `"anti-TNF"[tiab]` → #2ブロックに追加
   - 理由: 3/4のseed論文に出現、臨床的に広く使われる表現

#### 優先度中（検討推奨）
3. `"Psoriasis"[Mesh]` → #3ブロックに追加検討
   - 注意: 広い概念のため、ノイズ増加の可能性
   - 検証: 追加前後のヒット数比較を推奨

#### 不要（追加非推奨）
4. `"Skin Diseases"[Mesh]` → 広すぎるため不要

### Seed Paper捕捉状況
（search-validatorの結果がある場合は統合表示）
```

---

## Phase 3: 検索式の技術的レビュー

### 目的
検索式の各構成要素について、MeSH termの妥当性、ヒット数、構文エラー、最適化の余地を確認する。

### 実行手順

#### 3-1. MeSH term の妥当性検証

検索式に含まれるすべてのMeSH termについて:
- MeSH Databaseに存在するかを確認
- Entry termではないか（正式名称を使用しているか）
- 階層構造上の位置（Explode時に含まれる下位概念）

```bash
# MeSH検証
python scripts/search/mesh_analyzer/check_mesh.py --terms "{term1},{term2},..."
```

#### 3-2. 各行/ブロックのヒット数確認

```bash
# 検索行ごとのヒット数
python scripts/search/term_validator/check_search_lines.py \
  -i {formula_file} \
  -o {project_dir}/log/search_lines_results_{timestamp}.md
```

#### 3-3. Seed Paper捕捉確認

```bash
# Seed paper検証
python scripts/search/query_executor/check_final_query.py \
  --formula-file {formula_file} \
  --pmid-file {pmid_file} \
  --output-dir {project_dir}
```

#### 3-4. 構文チェック

以下のチェック項目をClaudeが直接検証:
- フィールドタグの正確性 (`[Mesh]` vs `[MeSH Terms]` vs `[MeSH]`)
- 括弧の対応
- OR/AND演算子の正しい使用
- 近接演算子の構文 (`[tiab:~N]`)
- ワイルドカード `*` の適切な使用
- 行番号参照 `#N` の整合性（存在する行を参照しているか）

#### 3-5. MeSH階層と重複分析

同一ブロック内のMeSH termsについて:
- 親子関係にあるterm（Explodeすれば片方で足りるケース）を検出
- 過度に広い/狭いMeSH termの特定

#### 3-6. 総合評価

### Phase 3 出力例

```markdown
## 🔬 Phase 3: 検索式の技術的レビュー

### MeSH Term 妥当性

| # | MeSH Term | 存在 | PubMed件数 | 備考 |
|---|----------|------|-----------|------|
| 1 | Arthritis, Rheumatoid | ✅ | 123,456件 | 正式名称 |
| 2 | Arthritis, Juvenile | ✅ | 34,567件 | 正式名称 |
| 3 | Rheumatic Diseases | ✅ | 45,678件 | 広い概念、explodeで多数の下位含む |
| 4 | Tumor Necrosis Factor Inhibitors | ✅ | 23,456件 | 正式名称 |
| 5 | Sarcoidosis | ✅ | 34,567件 | 正式名称 |

#### MeSH階層の注意点
- ⚠️ "Rheumatic Diseases"[MeSH] は explode で "Arthritis, Rheumatoid" を含む
  - 両方指定は冗長ではあるが、感度を重視する場合は許容される
  - "Rheumatic Diseases" のみで代替可能

### 各ブロック ヒット数

| ブロック | 内容 | ヒット数 |
|---------|------|---------|
| #1 | Population (RA/JIA/AOSD) | 234,567件 |
| #2 | Intervention (Biologics/JAKi) | 456,789件 |
| #3 | Concept (Paradoxical reactions) | 12,345件 |
| #4 | #1 AND #2 AND #3 | 567件 |

### Seed Paper捕捉結果

| # | PMID | タイトル | 捕捉 |
|---|------|--------|------|
| 1 | 22505694 | (タイトル) | ✅ |
| 2 | 17994192 | (タイトル) | ✅ |
| 3 | 26965410 | (タイトル) | ❌ |
| 4 | 28115268 | (タイトル) | ✅ |

- **捕捉率**: 3/4 (75%) ⚠️

#### ❌ 未捕捉論文の分析 (PMID: 26965410)
- **タイトル**: (タイトル)
- **不一致ブロック**: #3 (Paradoxical reactions)
- **原因**: この論文はPRを"adverse cutaneous reaction"と表現
- **対策**: `"adverse cutaneous reaction"[tiab]` を #3 に追加

### 構文チェック

| チェック項目 | 結果 | 詳細 |
|------------|------|------|
| フィールドタグ | ✅ | [MeSH], [tiab] 正しく使用 |
| 括弧の対応 | ✅ | 問題なし |
| OR/AND演算子 | ✅ | 正しく使用 |
| 近接演算子 | ✅ | [tiab:~2] 正しい構文 |
| 行番号参照 | ✅ | #1-#3 存在、#4 = #1 AND #2 AND #3 で整合 |

### 総合評価

| 項目 | 評価 | スコア |
|------|------|-------|
| Protocol対応 | ⚠️ 一部不足 | 89% |
| Seed論文捕捉 | ⚠️ 不完全 | 75% |
| MeSH妥当性 | ✅ 良好 | 100% |
| 構文正確性 | ✅ 問題なし | 100% |
| 検索語の網羅性 | ⚠️ 追加候補あり | - |

### 推奨アクション（優先度順）

1. 🔴 **Seed論文100%捕捉が必須**
   - PMID 26965410 の捕捉のため `"adverse cutaneous reaction"[tiab]` を #3 に追加
   - 追加後に再検証

2. 🟡 **Pearl Growing候補の検討**
   - `"Drug Eruptions"[Mesh]` を #3 に追加（Major Topic 2/4論文）
   - `"anti-TNF"[tiab]` を #2 に追加（3/4論文に出現）

3. 🟢 **Protocol対応の補完**
   - `ozoralizumab[tiab]` を #2 に追加（日本のみ承認薬）
   - `peficitinib[tiab]` を #2 に追加（日本のみ承認薬）

4. ℹ️ **MeSH階層の最適化（任意）**
   - "Rheumatic Diseases"[MeSH] と "Arthritis, Rheumatoid"[MeSH] の重複確認
```

---

## レポートファイルの保存

3フェーズの結果を統合して以下のパスに保存:

```
{project_dir}/log/search_formula_review_{YYYYMMDD_HHMMSS}.md
```

### レポートファイルのメタデータ

```markdown
<!--
Generated by: search-formula-reviewer skill
Project: {project_name}
Protocol file: {project_dir}/protocol.md
Search formula: {project_dir}/search_formula.md
Seed PMIDs: {project_dir}/seed_pmids.txt ({N} PMIDs)
Phases executed: Phase 1 (Protocol mapping), Phase 2 (Pearl growing), Phase 3 (Technical review)
Generated on: YYYY-MM-DD HH:MM:SS
-->
```

---

## エラーハンドリング

### エラーケース1: protocol.mdが存在しない

```markdown
❌ エラー: プロトコルファイルが見つかりません

期待されるパス: {project_dir}/protocol.md

**影響**:
- Phase 1（組み入れ基準レビュー）はスキップされます
- Phase 2, 3 は実行可能

**対処方法**:
1. protocol.md を作成してください
2. テンプレート: `cp templates/rq_template.md {project_dir}/protocol.md`
```

### エラーケース2: search_formula.mdが存在しない

```markdown
❌ エラー: 検索式ファイルが見つかりません

期待されるパス: {project_dir}/search_formula.md

**影響**:
- Phase 1, 3 は実行できません
- Phase 2（Pearl Growing）のみ部分的に実行可能

**対処方法**:
1. 検索式を作成してください（外部AIアシスタント推奨）
2. Protocolの検索式セクション（Appendix等）に検索式がある場合は、それを search_formula.md にコピーしてください
```

### エラーケース3: seed PMIDファイルが存在しない / 空

```markdown
⚠️ 警告: Seed PMIDファイルが見つかりません

検索パス:
- {project_dir}/seed_pmids.txt
- {project_dir}/seed.txt

**影響**:
- Phase 2（Pearl Growing）はスキップされます
- Phase 3 のseed捕捉確認はスキップされます

**対処方法**:
1. seed_pmids.txt を作成して、key papersのPMIDを1行に1つずつ記入
2. protocolのReference節からPMIDを特定可能な場合があります
```

### エラーケース4: Protocol内に検索式が含まれている（search_formula.mdなし）

```markdown
ℹ️ 検出: Protocol内に検索式が含まれています

protocol.md の Appendix セクションに検索式が記載されています。

**推奨**:
1. Protocol内の検索式を `search_formula.md` に転記
2. 転記後にこのスキルを再実行
3. または、Protocol内の検索式を直接レビュー（Phase 1のみ実行）
```

### エラーケース5: API rate limit超過

```markdown
❌ エラー: PubMed APIのレート制限に達しました

**対処方法**:
1. 30秒ほど待ってから再実行してください
2. --skip_phases オプションで完了済みフェーズをスキップ可能
3. NCBI_API_KEY の設定を検討:
   - https://www.ncbi.nlm.nih.gov/account/ でAPI keyを取得
   - 環境変数に設定: `export NCBI_API_KEY=your_key_here`
```

---

## 技術的詳細

### 使用スクリプト
1. `scripts/search/extract_mesh.py` - Seed論文のMeSH抽出（Phase 2）
2. `scripts/search/mesh_analyzer/check_mesh.py` - MeSH term妥当性検証（Phase 3）
3. `scripts/search/mesh_analyzer/check_mesh_overlap.py` - MeSH重複分析（Phase 3）
4. `scripts/search/term_validator/check_search_lines.py` - 検索行ヒット数（Phase 3）
5. `scripts/search/query_executor/check_final_query.py` - Seed捕捉確認（Phase 3）

### Claude自身が実行する分析（スクリプト不要）
- Phase 1: Protocol読解 → 要素抽出 → 検索式との対応マッピング
- Phase 2: Seed論文のタイトル/アブストラクトからのキーワード候補抽出
- Phase 3: 構文チェック、フィールドタグ検証、括弧対応確認

### APIリクエスト概算
- Phase 2（MeSH抽出）: seed論文数 × 3〜5リクエスト
- Phase 3（行ヒット数）: 検索行数 × 1リクエスト
- Phase 3（Seed捕捉）: seed論文数 × 1リクエスト + 1（総件数）
- Phase 3（MeSH検証）: MeSH term数 × 1リクエスト

### 実行時間の目安
- 全フェーズ: 3〜10分（seed論文数・検索行数に依存）
- Phase 1のみ: 即時（API不要、Claude分析のみ）
- Phase 2のみ: 1〜3分
- Phase 3のみ: 2〜5分

---

## プロンプト例

### 基本的な使い方（全フェーズ実行）
```
User: yamamotoプロジェクトの検索式をレビューして

Claude: search-formula-reviewerスキルを実行します。
[projects/yamamoto/ を確認中...]
[Phase 1: 組み入れ基準 ↔ 検索式 対応レビュー]
[Phase 2: Pearl Growing]
[Phase 3: 技術的レビュー]
[統合レポートを表示]
```

### 特定フェーズのみ
```
User: yamamotoのpearl growingをやって

Claude: search-formula-reviewerスキルのPhase 2を実行します。
[projects/yamamoto/ のseed論文を分析中...]
[Pearl Growing結果を表示]
```

### Protocol対応のみ
```
User: yamamotoの組み入れ基準と検索式の対応を確認

Claude: search-formula-reviewerスキルのPhase 1を実行します。
[protocol.mdとsearch_formula.mdを比較中...]
[対応マトリクスを表示]
```

### Protocol内に検索式がある場合
```
User: yamamotoの検索式をレビューして

Claude: search-formula-reviewerスキルを実行します。
[projects/yamamoto/ を確認中...]
ℹ️ search_formula.md が見つかりません。
ℹ️ protocol.md の Appendix に検索式が含まれています。
→ Protocol内の検索式を使用してレビューを実行します。
[レビュー結果を表示]
```

---

## 実装時の注意事項

1. **プロジェクト名の正規化**:
   - ユーザーが "yamamoto" と言った場合 → `projects/yamamoto/` に変換
   - ユーザーが "projects/yamamoto" と言った場合 → そのまま使用
   - 末尾の `/` は自動補完

2. **search_formula.md がない場合の代替**:
   - protocol.md の Appendix セクションに検索式がないか確認
   - あれば `search_formula_from_protocol` として内部的にパースして使用
   - ユーザーに search_formula.md への転記を推奨

3. **seed PMIDの検出順序**:
   - `seed_pmids.txt` → `seed.txt` → protocol.md内の参考文献からPMID抽出を試行
   - いずれもない場合はPhase 2, 3のseed関連をスキップ

4. **既存分析結果の再利用**:
   - `mesh_analysis_results.json` が存在する場合、Phase 2でAPI呼び出しを省略
   - ファイルの更新日時とseed_pmids.txtの更新日時を比較し、古い場合は再実行

5. **出力の段階的表示**:
   - 各Phaseの結果を完了ごとに表示（全Phase完了を待たない）
   - ユーザーが途中で中断・修正したい場合に対応

6. **総合評価の基準**:
   - Seed捕捉100%: ✅（目標値）
   - Seed捕捉80-99%: ⚠️（要改善）
   - Seed捕捉<80%: ❌（大幅な修正必要）
   - Protocol対応90%以上: ✅
   - Protocol対応70-89%: ⚠️
   - Protocol対応<70%: ❌

7. **Phase 2 Pearl Growingの対話的アプローチ**:
   - 候補が多数ある場合は優先度でフィルタして表示
   - ユーザーの判断を仰いでから検索式に反映
   - 追加候補の影響（ヒット数変化）を事前に計算

8. **レポートファイル保存**:
   - 必ずlog/ディレクトリに保存
   - ディレクトリがなければ自動作成
   - タイムスタンプ付きファイル名で上書き防止

9. **Protocol内の検索式検出パターン**:
   - `### Appendix` セクション
   - `#1`, `#2` 等の行番号パターン
   - `[MeSH]`, `[tiab]` 等のフィールドタグ

---

## 関連スキル

- **search-validator**: Phase 3のseed捕捉検証と同等（単独実行用）
- **mesh-analyzer**: Phase 2のMeSH抽出と同等（単独実行用）
- **term-counter**: Phase 3のヒット数確認と同等（単独実行用）
- **database-converter**: レビュー完了後の次ステップとして推奨
- **project-initializer**: protocol.md等が未作成の場合に推奨

## 参考リンク

- [NCBI MeSH Browser](https://www.ncbi.nlm.nih.gov/mesh/)
- [PubMed E-utilities API](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- [PRESS Peer Review Guidelines](https://www.cadth.ca/resources/finding-evidence/press)
- [Cochrane Handbook - Searching for Studies](https://training.cochrane.org/handbook/current/chapter-04)
