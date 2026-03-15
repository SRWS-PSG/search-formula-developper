# システマティックレビュー検索式開発支援システム（SRWS）

## 1. はじめに

### 1.1 目的と概要

このシステムは、システマティックレビュー・スコーピングレビューのための検索式開発を支援するツール群です。以下の機能を提供します：

- **検索式の構造化**: 検索式をMarkdownファイルとして構造化・管理
- **検索結果件数の確認**: PubMedを検索して各検索行の件数を確認
- **MeSH用語分析**: 確定論文のPMIDからMeSH情報を抽出し、階層構造を可視化して最適なMeSH用語を選定
- **検索式の検証**: シード論文の捕捉率を確認して検索式の妥当性を評価
- **データベース間変換**: PubMed検索式をCochrane CENTRAL、Embase（Dialog）、ClinicalTrials.gov、ICTRP形式に変換
- **Ovid→PubMed変換**: MEDLINE via Ovidの検索式をPubMed形式に変換
- **ブロック重複分析**: OR接続された検索語の貢献度を分析し、冗長な用語を特定
- **ERIC検索**: 教育研究データベースERICでの検索・シソーラス確認
- **検索結果処理**: 複数データベースの結果を統合し、Rayyan互換CSVに変換

### 1.2 リポジトリの役割

このリポジトリは**検証・変換・分析ツール**を提供します。検索式の作成自体は外部のAIアシスタント（ChatGPT、Claude、GitHub Copilotなど）との対話で行い、本ツールで検証・最適化することを想定しています。

- ✅ 検索式の検証（シード論文捕捉率、MeSH確認）
- ✅ データベース形式変換（PubMed ↔ CENTRAL ↔ Embase等）
- ✅ 分析ユーティリティ（用語重複、ブロック最適化）
- ❌ 検索式の自動生成（外部AIを推奨）

### 1.3 対象読者

- システマティックレビューを実施する研究者
- 医学図書館司書・情報専門家
- 臨床研究支援者

## 2. 準備

### 2.1 必要な環境

- **Python 3.7以上**
- **必要パッケージ**:

```bash
pip install -r requirements.txt
```

主な依存パッケージ:
| パッケージ | 用途 |
|-----------|------|
| requests | HTTP通信（PubMed API等） |
| beautifulsoup4 | HTMLパース（ERICシソーラス等） |
| lxml | XMLパース |
| pandas | データ分析 |
| python-dotenv | 環境変数管理 |
| loguru | ログ管理 |
| pytest | テストフレームワーク |

### 2.2 環境変数の設定

`.env.example` を `.env` にコピーし、必要なAPIキーを設定します：

```bash
cp .env.example .env
```

```env
# NCBI E-utilities（PubMed）APIキー
NCBI_API_KEY=your_api_key_here
NCBI_TOOL=your_tool_name
NCBI_EMAIL=your_email@example.com
NCBI_RATE_LIMIT_RPS=3  # APIキーなし:3、あり:10

# Gemini APIキー（一部検証スクリプトで使用）
GEMINI_API_KEY=
```

### 2.3 ディレクトリ構造

```
search-formula-developper/
├── Readme.md                       # 本ドキュメント
├── CLAUDE.md                       # Claude Code用ガイド
├── requirements.txt                # Python依存パッケージ
├── .env.example                    # 環境変数テンプレート
├── scripts/                        # ツール群
│   ├── search/                     # 検索・検証関連スクリプト
│   │   ├── term_validator/         # 検索語・検索行の検証
│   │   ├── mesh_analyzer/          # MeSH用語分析
│   │   ├── query_executor/         # 最終クエリ実行・評価
│   │   ├── eric/                   # ERIC検索連携
│   │   ├── validation/             # 高度な検証ツール
│   │   └── extract_mesh.py         # MeSH抽出
│   ├── conversion/                 # データベース変換
│   │   ├── ovid/                   # Ovid → PubMed変換
│   │   ├── clinicaltrials/         # ClinicalTrials.gov変換
│   │   ├── ictrp/                  # ICTRP変換
│   │   ├── search_converter.py     # 汎用コンバータ
│   │   └── generate_all_database_search.py  # 全DB一括変換
│   ├── initialize/                 # プロジェクト初期化
│   ├── validation/                 # 包括的検証
│   │   ├── seed_analyzer/          # シード論文分析
│   │   └── result_validator/       # 結果検証
│   ├── search_results_to_review/   # 検索結果処理（Rayyan用）
│   ├── ris/                        # RISファイル処理
│   └── utils/                      # ユーティリティ
├── projects/                       # プロジェクト作業ディレクトリ
│   └── PROJECT_NAME/
│       ├── protocol.md             # 研究プロトコル（RQ・PICO定義）
│       ├── seed_papers/            # キー論文の書誌情報
│       ├── seed_pmids.txt          # シード論文PMID一覧
│       ├── search_formula.md       # 検索式
│       ├── mesh_analysis.md        # MeSH分析結果
│       └── log/                    # 検証結果・検索ログ
├── templates/                      # テンプレート
│   ├── rq_template.md              # リサーチクエスチョンテンプレート
│   ├── pico_definition.md          # PICO定義テンプレート
│   ├── sr_filter.md                # システマティックレビューフィルタ
│   ├── prom_search_filter.md       # PROMs検索フィルタ
│   ├── blocks/                     # 検索式ブロックテンプレート
│   └── database/                   # DB別テンプレート
├── .claude/skills/                 # Claude Code Skills定義
└── tests/                          # テストスイート
```

## 3. Claude Code Skills統合

Claude Code（VSCode拡張機能またはCLI）を使用する場合、自然言語の対話で以下のSkillsが自動的に発動し、各タスクを効率的に実行できます。

### 利用可能なSkills

| Skill名 | 発動キーワード例 | 主な機能 |
|---------|-----------------|---------|
| **search-validator** | "検索式を検証して" | 検索式検証、seed paper捕捉確認 |
| **mesh-analyzer** | "MeSHを抽出して" | MeSH抽出・階層分析・重複チェック |
| **database-converter** | "全データベース形式に変換" | PubMed → CENTRAL/Embase/ClinicalTrials/ICTRP変換 |
| **term-counter** | "各キーワードの件数を調べて" | 検索語件数確認・ブロック重複分析 |
| **project-initializer** | "新しいプロジェクトを作成" | プロジェクト構造初期化 |
| **eric-searcher** | "ERICで検索" | ERIC検索・シソーラス確認 |
| **search-formula-reviewer** | "検索式をレビューして" | Protocol対応確認・Pearl Growing・MeSH検証一括実行 |

### Skills使用例

```
User: "ppsプロジェクトの検索式を検証して"
Claude: search-validatorスキルを実行 → 検証結果を表示

User: "全データベース形式に変換"
Claude: database-converterスキルを実行 → CENTRAL/Embase/ClinicalTrials/ICTRP形式を生成
```

詳細は [.claude/skills/README.md](.claude/skills/README.md) を参照してください。

## 4. 検索式開発ワークフロー

### 4.1 推奨ワークフロー

```
1. プロジェクト初期化     → project-initializer Skill or 手動
2. プロトコル作成         → protocol.md にRQ・PICOを定義（手動）
3. シード論文登録         → seed_pmids.txt にPMIDを記載（手動）
4. MeSH分析             → mesh-analyzer Skill
5. 検索式作成            → 外部AI（ChatGPT、Claude等）で対話的に作成
6. 検索式包括レビュー     → search-formula-reviewer Skill
7. 検索式検証            → search-validator Skill
8. 検索語最適化          → term-counter Skill
9. データベース変換       → database-converter Skill
10. ERIC検索             → eric-searcher Skill（教育研究の場合）
11. 検索結果処理          → search_results_processor.py
```

### 4.2 プロジェクトの準備

#### Step 1: プロジェクトフォルダ作成

```bash
mkdir -p projects/PROJECT_NAME/seed_papers
```

または Claude Code Skills で:
```
User: "PROJECT_NAMEという新しいプロジェクトを作成"
```

#### Step 2: プロトコル作成

```bash
cp templates/rq_template.md projects/PROJECT_NAME/protocol.md
# protocol.md を編集してRQとPICOを定義
```

#### Step 3: シード論文の準備

- キー論文の書誌情報を `seed_papers/` に配置（RIS, NBIB, RTF等）
- PMIDを `seed_pmids.txt` に記載（1行1 PMID、`#` でコメント可）

```
# シード論文リスト
18442104
10675426
39073822
```

#### Step 4: 検索式の開発

外部AIアシスタントと対話的に検索式を開発し、`search_formula.md` に保存します。

**推奨フォーマット（スクリプト互換）**:

```markdown
# プロジェクト名

## PubMed/MEDLINE

\```
#1 ("Disease"[Mesh] OR disease[tiab] OR condition[tiab])
#2 ("Therapy"[Mesh] OR treatment[tiab])
#3 #1 AND #2
\```
```

**パース要件**:
- `## PubMed/MEDLINE` セクションヘッダーが必要
- 検索式はコードブロック内に記述
- 各行は `#N ` で始まる（Nは行番号）
- 最終行は `#N AND #M` 形式の組み合わせ式

#### Step 5: 検証・最適化

本リポジトリのツール群で検索式を検証・最適化します（詳細は以下のセクション参照）。

## 5. スクリプト使用ガイド

### 5.1 検索式のヒット件数確認

各検索行のPubMedでのヒット件数を確認します。行内の個別キーワード（ORで区切られた要素）のヒット件数も表示されます。

```bash
python scripts/search/term_validator/check_search_lines.py \
  --input-formula projects/PROJECT_NAME/search_formula.md \
  --output projects/PROJECT_NAME/log/search_lines_results.md
```

### 5.2 最終検索式の実行とシード論文検証

最終検索式を実行し、シード論文が検索結果に含まれるかを確認します。各PMIDを個別に `query AND pmid[PMID]` で検証するため、大規模な検索結果（>10,000件）でも正確に検証できます。

```bash
python scripts/search/query_executor/check_final_query.py \
  --formula-file projects/PROJECT_NAME/search_formula.md \
  --pmid-file projects/PROJECT_NAME/seed_pmids.txt \
  --output-dir projects/PROJECT_NAME/
```

**出力内容**:
- 検索結果の総件数
- 各シード論文の捕捉状況（✅ captured / ❌ missed）
- 全体の捕捉率（例: 5/5 = 100%）

### 5.3 MeSH用語分析

シード論文からMeSH用語を抽出し、階層構造をMermaidダイアグラムで可視化します。

```bash
python scripts/search/extract_mesh.py \
  --pmid-file projects/PROJECT_NAME/seed_pmids.txt \
  --output-dir projects/PROJECT_NAME/
```

出力: `mesh_analysis.md`（分析レポート）、`mesh_analysis_results.json`（構造化データ）

#### MeSH用語の個別確認

```bash
# MeSH用語の存在確認と文献数取得
python scripts/search/mesh_analyzer/check_mesh.py --terms "Term1,Term2,Term3"

# MeSH用語間の重複分析
python scripts/search/mesh_analyzer/check_mesh_overlap.py --terms "Term1,Term2,Term3"
```

### 5.4 ブロック重複分析

ORで接続された検索語の個別貢献度を分析し、冗長な用語を特定します。

```bash
python scripts/search/term_validator/check_block_overlap.py \
  -i block_input.txt \
  -o projects/PROJECT_NAME/log/block_analysis.md \
  --block-name "Block Description"
```

**入力フォーマット**（テキストファイル）:
```
#### #2A Block Name
"Term1"[Mesh] OR
"Term2"[Mesh] OR
term3[tiab] OR
term4[tiab]
```

**出力**: 各用語のヒット件数、累積ヒット数、追加文献数、貢献率、低寄与用語（< 1%）・高重複用語（> 80%）の識別

### 5.5 データベース変換

#### 全データベース一括変換

```bash
python scripts/conversion/generate_all_database_search.py \
  --input projects/PROJECT_NAME/search_formula.md \
  --output-dir projects/PROJECT_NAME/
```

#### 個別フォーマット変換

```bash
python scripts/conversion/search_converter.py \
  --input search_formula.md \
  --output output.md \
  --target-db [central|dialog|clinicaltrials|ictrp]
```

#### 変換ルール概要

| 変換先 | MeSH変換 | フィールドタグ | 行番号 |
|-------|----------|-------------|--------|
| CENTRAL | `MeSH descriptor: [Term] explode all trees` | `:ti,ab,kw` | — |
| Dialog/Embase | `EMB.EXACT.EXPLODE()` | `TI() OR AB()` | `S1, S2...` |
| ClinicalTrials.gov | 同義語に展開 | Condition/Intervention/Other分類 | — |
| ICTRP | 同義語に展開、タグ削除 | — | — |

#### Ovid → PubMed変換

```python
from scripts.conversion.ovid.converter import convert_ovid_to_pubmed

ovid_query = '(heart adj3 failure).ti,ab. OR exp Cardiomyopathies/.'
pubmed_query, warnings = convert_ovid_to_pubmed(ovid_query)
print(pubmed_query)
# => "heart failure"[tiab:~3] OR Cardiomyopathies[mh]
```

### 5.6 ERIC検索（教育データベース）

教育研究データベースERICでの検索をサポートします。

```bash
# 基本検索
python scripts/search/eric/search_eric.py -q "medical education" -r 20

# シソーラス（descriptor）+ フリーワード検索
python scripts/search/eric/search_eric.py -q "subject:\"Medical School Faculty\" AND burnout"

# 査読済みのみ + 年範囲フィルタ
python scripts/search/eric/search_eric.py -q "faculty development" \
  --peer-reviewed --year-min 2020 --count-only

# RISエクスポート
python scripts/search/eric/search_eric.py -q "medical education" -o results.ris
```

**CLIフィルタオプション**:

| オプション | 説明 |
|-----------|------|
| `--peer-reviewed` | 査読済み論文のみ |
| `--year-min YYYY` | 最小出版年 |
| `--year-max YYYY` | 最大出版年 |
| `--fulltext` | 全文利用可能のみ |
| `--ies-funded` | IES助成研究のみ |
| `--wwc-reviewed [y/r/n]` | WWCレビュー済み |

**ERICシソーラス確認**:

```bash
# 用語情報の取得（カテゴリ、関連語）
python scripts/search/eric/check_eric_thesaurus.py -t "Medical School Faculty"

# 関連語を含む検索クエリ生成
python scripts/search/eric/check_eric_thesaurus.py -t "Faculty Development" --build-query

# 用語の存在確認
python scripts/search/eric/check_eric_thesaurus.py -t "Some Term" --check-only
```

### 5.7 検索結果処理

複数データベースの検索結果を統合し、Rayyanでスクリーニング可能なCSVに変換します。

```bash
python scripts/search_results_to_review/search_results_processor.py \
  --input-dir projects/PROJECT_NAME/ \
  --output-dir projects/PROJECT_NAME/processed/
```

**対応入力フォーマット**: RIS (.ris)、NBIB (.nbib)、ClinicalTrials.gov RIS、ICTRP XML (.xml)

**出力**:
- テストレビュー用CSV（50件）
- 本レビュー用CSV（500件ごとに分割）
- 圧縮ZIPファイル
- PRISMAフローチャート用統計情報

### 5.8 その他のツール

```bash
# 特定論文が検索式のどの部分に一致するかを分析
python scripts/validation/seed_analyzer/check_specific_papers.py \
  --formula-file projects/PROJECT_NAME/search_formula.md \
  --pmid-file projects/PROJECT_NAME/seed_pmids.txt

# 修正前後の検索式を比較
python scripts/validation/result_validator/check_modified_search.py \
  --original original.md --modified modified.md --pmids seed_pmids.txt
```

## 6. 検索式フォーマット

### フィールドタグ

| タグ | 説明 |
|-----|------|
| `[Mesh]` / `[MeSH Terms]` | MeSH記述子 |
| `[tiab]` | Title/Abstract |
| `[ti]` | Titleのみ |
| `[ab]` | Abstractのみ |
| `[tw]` | Text Word |

### 近接演算子

PubMedでは指定語数以内に出現する用語の検索が可能です：

```
"hip pain"[Title/Abstract:~2]
# → "hip"と"pain"が2語以内に出現する文献
```

### ブロック構造の例

```markdown
# プロジェクト名

## PubMed/MEDLINE

\```
#1 ("Disease"[Mesh] OR disease[tiab] OR condition[tiab])
#2 ("Therapy"[Mesh] OR treatment[tiab])
#3 #1 AND #2
Filters: Humans, English
\```
```

## 7. テスト

```bash
# 全テスト実行
pytest -q

# 特定テスト実行
pytest tests/test_ovid_to_pubmed.py -q
```

## 8. 技術詳細

### API利用

- NCBI E-utilities API（PubMed）を使用
- レート制限: APIキーなし3 req/s、APIキーあり10 req/s
- `NCBI_API_KEY` 環境変数で設定

### MeSH階層取得の仕組み

1. PubMed APIで論文詳細取得
2. MeSH記述子・修飾語を抽出
3. NCBI MeSHブラウザからツリー番号取得
4. RDFエンドポイントで階層情報照会
5. Mermaidダイアグラム生成

### レポートファイルのメタデータ

すべての分析レポートには再現性のため以下のメタデータを含めます：

```markdown
<!--
Generated by: scripts/path/to/script.py
Command: python scripts/path/to/script.py --arg1 value1
Input data: path/to/input/data.txt
Generated on: YYYY-MM-DD HH:MM:SS
-->
```

## 9. ライセンス

MIT License
