# システマティックレビュー検索式開発支援システム（SRWS）

## 1. はじめに

### 1.1 目的と概要

このシステムは、以下の機能を提供することでシステマティックレビューのための検索式開発を支援します：

- **検索式の構造化**: ユーザーがコピペした検索式をMarkdownファイルとして構造化
- **検索結果件数の確認**: PubMedを検索して、各検索行の件数を確認
- **MeSH用語分析**: 確定論文のPMIDからMeSH情報を抽出し、階層性を図示して最適なMeSH用語を選定
- **検索式の実行**: 全体の検索式を実行して結果を評価
- **データベース間変換**: PubMed検索式をCochrane CENTRAL、Embase(Dialog)、ClinicalTrials.gov、ICTRP形式に変換
- **Ovid→PubMed変換**: MEDLINE via Ovidの検索式をPubMed形式に変換し、既存のチェックフローへ取り込む

### 1.2 対象読者

- システマティックレビューを実施する研究者
- 医学図書館司書・情報専門家
- 臨床研究支援者

## 2. 準備

### 2.1 必要な環境

- **Python 3.7以上**: 各種スクリプトの実行に必要
- **必要パッケージ**: requests, datetime, time など（`pip install requests` でインストール）

### 2.2 推奨ディレクトリ構造

システムは以下のディレクトリ構造で運用することを推奨します：

```
search-formula-developper/
├── Readme.md                       # 本ドキュメント
├── scripts/                         # 検索式評価用スクリプト群
│   ├── search/                      # 検索関連スクリプト
│   ├── conversion/                  # 変換関連スクリプト
│   └── ... 
└── search_formula/                  # 検索式プロジェクト用ディレクトリ
    ├── project1/                    # プロジェクト1のディレクトリ
    │   ├── pico_definition.md       # PICOの定義
    │   ├── search_formula.md        # 構造化された検索式
    │   ├── mesh_analysis.md         # MeSH用語分析結果
    │   ├── central_search.md        # CENTRAL用検索式
    │   ├── dialog_search.md         # Dialog(Embase)用検索式
    │   └── final_report.md          # 最終報告書
    └── project2/                    # プロジェクト2のディレクトリ
        └── ...
```

各検索プロジェクトは `search_formula` ディレクトリの下に専用のサブディレクトリを作成し管理します。ログや検索結果（RISファイルなど）もプロジェクトディレクトリ直下に保存します。

### 2.3 既存ファイル群の概要と役割

- **テンプレートファイル**:
  - `pico_definition.md`: PICOフレームワークの定義シート
  - `search_formula_template.md`: データベース別の検索式テンプレート
  - `mesh_analysis.md`: MeSH用語の分析と検索式の最終形

- **Pythonスクリプト**:
  - `check_search_lines.py`: 各検索行のヒット件数確認
  - `check_mesh.py`: MeSH用語の存在確認と文献数取得
  - `check_final_query.py`: 最終検索式の評価とRISファイル出力
  - `check_specific_papers.py`: 特定論文の検索条件分析
  - `check_mesh_overlap.py`: MeSH用語間の重複分析
  - その他の補助スクリプト

## 3. 検索式開発ワークフローと使用方法

### 3.1 プロジェクトディレクトリの準備

新しい検索プロジェクトを開始する際は、まず専用のディレクトリを作成します。

```bash
# search_formulaディレクトリがなければ作成
mkdir -p search_formula

# プロジェクト用ディレクトリを作成（例：乳がん放射線療法）
mkdir -p search_formula/乳がん放射線療法

# 必要なサブディレクトリを作成
mkdir -p search_formula/乳がん放射線療法/log
```

### 3.2 検索式の初期入力と構造化

#### 3.2.1 PICOフレームワークの定義

まず、PICOフレームワークを定義します。既存の `pico_definition.md` を参考に、プロジェクトの PICO 定義ファイルを作成します。

1. `pico_definition.md` をテンプレートとして新しいファイルを作成：
```bash
cp templates/pico_definition.md search_formula/プロジェクト名/pico_definition.md
```

2. プロジェクトの要件に合わせて PICO 定義ファイルを編集します。

#### 3.2.2 検索式の構造化

ユーザーが用意した検索式（テキスト形式）を構造化します：

1. **保存先の確認**: まず、どの検索プロジェクトに属する検索式かを確認します。対応するプロジェクトディレクトリ（例: `search_formula/プロジェクト名/`）が存在しない場合は、作成を促します。
2. **ファイルへの保存**: 確認したプロジェクトディレクトリ配下に `search_formula.md` というファイル名で検索式を保存します。
3. **構文の初期チェック**: 保存された `search_formula.md` の内容について、PubMedの標準的な検索構文と比較し、特に以下の点を確認します。
    *   セミコロン（`;`）やコンマ（`,`）が意図しない箇所で使用されていないか。セミコロンを使用する場合は、PubMedでは通常ORとして解釈されない点に注意します。
    *   **論理演算子（AND, OR, NOT）が適切に使用されているか**。論理演算子の適切な使用は、スクリプトによる解析や実行時の正確さに直接影響します。
    *   **括弧 `()` の対応が取れているか、また意図した優先順位でグループ化されているか**。括弧は検索式の階層と優先順位を決定する重要な要素です。
    *   複数の検索条件がある場合、適切な論理演算子で接続されているか。
    *   1行内に複数のOR条件や括弧でグループ化された複雑な条件がある場合も、正しく構造化されているか確認します。
    *   もし構文に曖昧さや、PubMedで直接実行した際に意図しない結果を生む可能性のある記述が見つかった場合は、ユーザーに確認し、必要に応じて修正を提案します。
4. **構造化**: (構文チェック後) 保存された `search_formula.md` の内容を元に、検索式をブロックごとに分割し（Population, Intervention, Comparison, Outcome など）、各ブロック内の検索語をMeSH用語とフリーテキスト用語に分類します。
5. `templates/blocks/search_formula_template.md` を参考に、Markdownフォーマットで構造化します。

例：
```markdown
# プロジェクト名の検索式

## PubMed/MEDLINE

### 基本構造
```
#1 Population（対象集団）
    "Disease"[Mesh] OR
    disease[tiab] OR
    condition[tiab]

#2 Intervention（介入）
    "Therapy"[Mesh] OR
    treatment[tiab] OR
    therapy[tiab]

#3 最終検索式
    #1 AND #2
    Filters: Language
```
```

### 3.3 各検索行（ブロック）のヒット数確認

構造化した検索式の各行（またはブロック）のPubMedでのヒット件数を確認します。改良版では、各検索行を構成する個別のキーワード（OR演算子で区切られた要素）のヒット件数も確認できるようになりました。

#### 3.3.1 `check_search_lines.py` の使用方法

1. スクリプトにコマンドライン引数として入力ファイルと出力ファイルを指定して実行します：

```bash
python scripts/search/term_validator/check_search_lines.py --input-formula search_formula/プロジェクト名/search_formula.md --output search_formula/プロジェクト名/search_lines_results.md
```

2. 出力される `search_lines_results.md` には以下の情報が含まれます：
   - 各検索行のオリジナルクエリ
   - 行内の個別キーワード（ORで区切られた要素）とそれぞれのヒット件数
   - 行全体（すべての要素をORで結合）のヒット件数
   - 最終検索式の構造と展開後の検索式、およびその検索結果

3. 出力された結果を分析し、必要に応じて検索式を調整します。

### 3.4 MeSH用語自動分析システム

#### 3.4.1 概要と機能

システマティックレビューのための検索式開発において、MeSH用語の適切な選定は極めて重要です。このシステムは論文PMIDリストから自動的にMeSH用語を抽出し、その階層構造を可視化、分析するツールです。

主な機能：
- PMIDリストからMeSH用語の自動抽出・集計
- MeSH用語の階層構造の取得と可視化（Mermaidダイアグラム）
- カテゴリ別のMeSH用語分析
- 詳細なMarkdownレポート生成

#### 3.4.2 使用方法

##### 必要なファイル構成

各RQの作業ディレクトリ（例：`search_formula/RQ1/`）に以下のファイルを配置します。

```
search_formula/RQ名/
└── seed_pmids.txt     # 分析対象論文のPMIDリスト（1行に1 PMID）
```

MeSH分析スクリプト `extract_mesh.py` はプロジェクトのトップディレクトリに配置されています。

##### seed_pmids.txtの準備

分析対象とする論文のPMIDを1行に1つずつ記載したテキストファイルを準備します。コメント行は `#` で始めることで無視されます。

例 (`search_formula/RQ名/seed_pmids.txt`):
```
# シード論文リスト
18442104
10675426
39073822
# 以下続く
```

##### 実行コマンド

RQの作業ディレクトリ（例：`search_formula/RQ1/`）に移動してから、以下のコマンドを実行します。

```bash
# 例：search_formula/RQ1/ ディレクトリで実行
python ../../scripts/search/extract_mesh.py --pmid-file ./seed_pmids.txt --output-dir ./
```

または、プロジェクトのトップディレクトリから実行する場合：

```bash
python scripts/search/extract_mesh.py --pmid-file ./search_formula/RQ名/seed_pmids.txt --output-dir ./search_formula/RQ名/
```

これにより、指定した`seed_pmids.txt`を読み込み、結果（`mesh_analysis.md`と`mesh_analysis_results.json`）を指定した出力ディレクトリに保存します。

#### 3.4.3 `extract_mesh.py` スクリプトの概要

このスクリプト (`scripts/search/extract_mesh.py`) は以下の主要な処理を行います：

- **PMIDからの情報取得**: `get_paper_details`関数でPubMed APIを叩き、論文のXMLデータを取得します。
- **MeSH用語抽出**: `extract_mesh_terms`関数でXMLからMeSH記述子、UI、修飾語、主要トピック情報を抽出します。
- **タイトル・抄録抽出**: `extract_title_abstract`関数で論文のタイトルと抄録を抽出します。
- **出版情報抽出**: `extract_publication_info`関数でジャーナル名、出版年、著者情報を抽出します。
- **MeSH階層取得**: `get_mesh_hierarchy`関数でMeSH UIを基にNCBIのMeSHブラウザやE-utilities APIを利用してツリー番号を取得します。
- **ツリー番号からのMeSH情報取得**: `fetch_mesh_term_by_tree_number`関数でSPARQLクエリを使用し、ツリー番号から対応するMeSH用語名やUIを補完します。
- **Mermaid図生成**: `generate_mermaid_diagram`関数で収集したMeSH階層情報からカテゴリ別のMermaid図を生成します。
- **レポート生成**: `main`関数全体でこれらの処理を統括し、最終的にMarkdown形式の分析レポート (`mesh_analysis.md`) とJSON形式のデータ (`mesh_analysis_results.json`) を出力します。

#### 3.4.4 分析結果の解釈と活用

生成される `mesh_analysis.md` には以下の情報が含まれます。

- **分析サマリー**: 分析対象となった論文数、ユニークMeSH用語数。
- **主要なMeSH用語**: 出現頻度順の上位MeSH用語リスト。
- **MeSH用語の階層構造**: カテゴリ別にMermaid図で可視化された階層構造。シード論文に含まれる用語は強調表示されます。
- **論文別MeSH用語**: 各論文に付与されたMeSH用語の詳細リスト。

これらの情報を基に、検索式に含めるべきMeSH用語の選定や、検索戦略の妥当性評価を行います。

#### 3.4.5 検索式へのMeSH用語採用の判断基準

以下の基準でMeSH用語を検索式に採用するかを判断します：

1. 複数の論文で共通して使用されているMeSH用語を優先
2. 階層構造の上位にあるMeSH用語はより広い概念をカバーするため、展開（explode）して使用するか検討
3. 階層構造の下位にあるMeSH用語は特異度が高いため、必要に応じて追加
4. 各MeSH用語の検索結果件数を `scripts/search/mesh_analyzer/check_mesh.py` で確認し、適切な粒度を選択

### 3.5 全体検索式の実行と評価

構造化・最適化された最終検索式を作成し、評価します。

#### 3.5.1 最終検索式の作成

ブロックごとの検索式を `AND` で結合して最終検索式を作成します：

```
(Population) AND (Intervention) AND (Optional filters)
```

#### 3.5.2 `check_final_query.py` による検索式の実行と評価

このスクリプトは、指定された検索式ファイルとPMIDリストファイルに基づき、最終検索式を実行し、シード論文が検索結果に含まれるかを確認します。

1. コマンドライン引数を使用してスクリプトを実行します。
   - `--formula-file`: 検索式が記述されたMarkdownファイルのパス (例: `search_formula/プロジェクト名/search_formula.md`)
   - `--pmid-file`: シード論文のPMIDが記述されたテキストファイルのパス (例: `search_formula/プロジェクト名/seed_pmids.txt`)
   - `--output-dir` (任意): 生成されるRISファイルなどの出力先ディレクトリ。

```bash
python scripts/search/query_executor/check_final_query.py --formula-file search_formula/プロジェクト名/search_formula.md --pmid-file search_formula/プロジェクト名/seed_pmids.txt
```

2. 実行結果を確認：
   - 検索結果の総件数
   - シードスタディの包含状況
   - RISファイルの出力（log/search_results_*.ris）

#### 3.5.3 検索結果の解釈と評価

1. **検索結果数の評価**:
   - 検索結果数の目安は条件によって2,000〜5,000件程度が一般的ですが、これはあくまで目安であり、研究テーマの特性や目的によって適切な件数は大きく異なります。
   - 件数が多すぎる場合は、より具体的な用語の追加や絞り込み条件の検討が必要です。
   - 件数が少なすぎる場合は、同義語の追加や用語の上位概念への拡張を検討します。

2. **シード論文の包含確認**:
   - すべてのシードPMIDが検索結果に含まれることは検索式の妥当性を示す重要な指標です。
   - シードPMIDが検索結果に含まれない場合は、以下の対応を検討します：
     - 検索されなかった論文のMeSH用語と使用されている用語を確認
     - 検索式に不足している用語やMeSH用語の追加
     - 検索構造（AND/OR条件）の見直し

### 3.6 他データベースへの検索式変換

#### 3.6.1 CENTRALへの変換

PubMed検索式をCochrane CENTRAL形式に変換します。

主な変換ルール：
- `[Mesh]` → `MeSH descriptor: [用語] explode all trees`
- `[tiab]` → `:ti,ab,kw`
- PubMedの演算子の調整（特に近接演算子）

例：
```
# PubMed形式
"Breast Neoplasms"[Mesh] OR breast cancer[tiab]

# CENTRAL形式
MeSH descriptor: [Breast Neoplasms] explode all trees OR (breast NEXT cancer):ti,ab,kw
```

詳細は `templates/database/central_search.md` を参照してください。

#### 3.6.2 Dialog (Embase)への変換

PubMed検索式をDialog形式に変換します。

主な変換ルール：
- `[Title/Abstract]` または `[tiab]` → `TI() OR AB()`
- `[MeSH Terms]` または `[Mesh]` → `EMB.EXACT.EXPLODE()`
- 行番号 `#1` → `S1`
- 日付制限 `2018/12/1:2024/9/30[DP]` → `PD(20181201-20240930)`

例：
```
# PubMed形式
"Breast Neoplasms"[Mesh] OR breast cancer[tiab]

# Dialog形式
EMB.EXACT.EXPLODE("breast cancer") OR (TI(breast cancer) OR AB(breast cancer))
```

詳細は `templates/database/Embase(Dialog)_search.md` を参照してください。

#### 3.6.3 ClinicalTrials.govへの変換

PubMed検索式をClinicalTrials.gov形式に変換します。

主な変換ルール：
- MeSH用語は同義語リストに展開: `"Essential Tremor"[Mesh]` → `"essential tremor" OR "benign tremor" OR "familial tremor"`
- 検索フィールドの変換: タグに基づいてCondition/Intervention/Other Termsに分類
- 近接演算子はANDに変換: `"tremor therapy"[tiab:~2]` → `(tremor AND therapy)`

例：
```
# PubMed形式
"Essential Tremor"[Mesh] OR "tremor therapy"[tiab:~2]

# ClinicalTrials.gov形式
Condition: "essential tremor" OR "benign tremor" OR "familial tremor"
Intervention: (tremor AND therapy)
```

#### 3.6.4 ICTRPへの変換

PubMed検索式をICTRP形式に変換します。

主な変換ルール：
- MeSH用語は同義語に展開
- すべての検索フィールドタグを削除
- 近接演算子はANDに変換
- 括弧の深さを制限（ICTRPでは浅い括弧構造が推奨）

例：
```
# PubMed形式
"Essential Tremor"[Mesh] OR "tremor therapy"[tiab:~2]

# ICTRP形式
("essential tremor" OR "benign tremor" OR "familial tremor") OR (tremor AND therapy)
```

### 3.7 Ovid検索式のPubMed形式への変換

#### 3.7.1 概要

- `scripts/conversion/ovid/converter.py` には、MEDLINE via Ovid の検索式をPubMed形式へ変換するユーティリティが含まれています。
- フィールドタグ、MeSH展開（`exp`）、フォーカス指定（`*`）、サブヘッディング、近接演算子（`adjN`）、主要なワイルドカードに対応し、PubMedで表現できない構文は警告として通知します。
- 変換結果は既存のPubMedチェックフロー（ヒット件数確認、MeSH分析、他データベース変換など）へそのまま組み込めます。

#### 3.7.2 使用方法

Python REPL あるいはスクリプトから `convert_ovid_to_pubmed` 関数を呼び出します。

```python
from scripts.conversion.ovid.converter import convert_ovid_to_pubmed

ovid_query = '(heart adj3 failure).ti,ab. OR exp Cardiomyopathies/.'
pubmed_query, warnings = convert_ovid_to_pubmed(ovid_query)
print(pubmed_query)
# => "heart failure"[tiab:~3] OR Cardiomyopathies[mh]
print(warnings)
# => 変換時の注意点（必要な場合のみ）
```

#### 3.7.3 自動テスト

- 変換ロジックは `tests/test_ovid_to_pubmed.py` で網羅的に検証しています。
- ユニットテストのみ実行する場合は `pytest tests/test_ovid_to_pubmed.py -q` を利用してください。
- プロジェクト全体のテストは `pytest -q` で実行でき、外部依存パッケージが未インストールの場合は該当テストが自動的にスキップされます。

## 4. 既存Pythonスクリプトの詳細と利用ガイド

### 4.1 `check_search_lines.py`

**機能**: 指定された検索クエリ（個別の検索語や検索ブロック）のPubMedでのヒット件数を取得します。また、各検索行を構成する個別の検索語（ORで区切られた要素）のヒット件数も表示します。

**使用方法**:
1. コマンドライン引数として入力ファイルと出力ファイルを指定して実行します：
   ```
   python scripts/search/term_validator/check_search_lines.py --input-formula 入力ファイル --output 出力ファイル
   ```

2. 結果を確認：
   - 各検索行内の個別キーワード（ORで区切られた要素）のヒット件数
   - 各検索語の個別ヒット数、ブロックごとのOR検索結果
   - 最終的な検索式の構造と展開後の検索式、およびその検索結果

### 4.2 `check_mesh.py`

**機能**: 指定されたMeSH用語の存在確認とPubMedでの文献数を取得します。

**使用方法**:
1. コマンドライン引数を使用してスクリプトを実行します：
   ```
   python scripts/search/mesh_analyzer/check_mesh.py --terms "Term1,Term2,Term3"
   ```
   または、ファイル内の `mesh_terms` リストを編集して実行：
   ```
   python scripts/search/mesh_analyzer/check_mesh.py
   ```

2. 結果を確認：各MeSH用語の存在有無、MeSHデータベースでの出現数、PubMedでの文献数

### 4.3 `check_final_query.py`

**機能**: 最終検索式を実行し、総ヒット件数、PMIDリストを取得。シードスタディの包含確認とRISファイル出力も行います。

**使用方法**:
```bash
python scripts/search/query_executor/check_final_query.py --formula-file search_formula/プロジェクト名/search_formula.md --pmid-file search_formula/プロジェクト名/seed_pmids.txt --output-dir search_formula/プロジェクト名/
```

結果を確認：検索結果件数、シードスタディの包含状況、RISファイルの出力

### 4.4 その他の有用なスクリプト

- `check_specific_papers.py`: 特定論文が検索式のどの部分に一致するかを分析します
  ```bash
  python scripts/validation/seed_analyzer/check_specific_papers.py --formula-file 検索式ファイル --pmid-file PMIDリストファイル
  ```

- `check_mesh_overlap.py`: 複数のMeSH用語間の重複を分析します
  ```bash
  python scripts/search/mesh_analyzer/check_mesh_overlap.py --terms "Term1,Term2,Term3"
  ```

- `check_modified_search.py`: 修正後の検索式の評価を行います
  ```bash
  python scripts/validation/result_validator/check_modified_search.py --original 元の検索式ファイル --modified 修正後の検索式ファイル --pmids PMIDリストファイル
  ```

- `analyze_papers.py`: 検索結果の詳細分析を行います
  ```bash
  python scripts/utils/analyze_papers.py --input 検索結果RISファイル --output 出力先ディレクトリ
  ```

### 4.5 `search_results_processor.py`

**機能**: 複数のデータベースから取得した検索結果ファイル（RIS, NBIB, ClinicalTrials.gov RIS, ICTRP XML）を処理し、Rayyanでレビュー可能なCSVファイルに変換します。データの統合、重複排除、PRISMAフローチャート用統計の生成も行います。

**主な特徴**:
- 複数のデータソース（PubMed, Embase, CENTRAL, ClinicalTrials.gov, ICTRP）から検索結果を処理
- ファイル形式の自動認識と適切な処理
- DOIとタイトルベースの重複排除
- Rayyan互換CSV形式への変換
- PRISMAフローチャート用の統計情報生成
- 大量の文献を効率的に処理するための分割出力

**使用方法**:
```bash
python scripts/search_results_to_review/search_results_processor.py --input-dir search_formula/プロジェクト名/ --output-dir search_formula/プロジェクト名/processed/ [--verbose]
```

**入力ファイル**:
- RISファイル（.ris, .txt拡張子）: PubMed, Embase, CENTRALなどからエクスポート
- NBIBファイル（.nbib拡張子）: PubMedからのエクスポート
- ClinicalTrials.gov RISファイル
- ICTRP XMLファイル（.xml拡張子）

**出力**:
- テストレビュー用CSV（50件）
- 本レビュー用CSV（500件ごとに分割）
- 圧縮ZIPファイル（全CSVを含む）
- 統計情報レポート

**出力例**:
```
総レコード数: 8,768件
重複排除後のレコード数: 5,807件
重複率: 33.77%
```

詳細なオプションや使用方法は `scripts/search_results_to_review/README.md` を参照してください。

## 5. 付録

### 5.1 PubMed API利用時の注意点

- **APIキー**: 多数のリクエストを行う場合はNCBIのAPIキーを取得して使用（1秒あたり10リクエストまで可能）
- **リクエスト制限**: APIキーなしの場合は1秒あたり3リクエストまで。スクリプト内の `time.sleep()` で調整
- **エラー処理**: 一時的なAPIエラーに対応するため、リトライ機能を実装することを推奨

### 5.2 トラブルシューティング

1. **APIリクエストエラー**:
   - `time.sleep()` の値を大きくしてリクエスト間隔を延長
   - 一時的なサーバーエラーの場合は再試行

2. **検索結果が多すぎる場合**:
   - より特異的な用語を追加
   - フィルターを追加（出版年、言語、研究タイプなど）

3. **シードスタディが検索結果に含まれない場合**:
   - 各論文のMeSH用語とフリーテキストを確認
   - 検索式に不足している用語を追加

4. **RISファイルのエクスポートエラー**:
   - APIからの応答データを確認
   - フォーマット変換処理を見直し

## 6. ファイル構成とガイドライン

### 6.1 ファイル構成

- **Pythonスクリプト群** (`scripts/`)
  - 検索関連スクリプト: `scripts/search/`
  - 変換関連スクリプト: `scripts/conversion/`
  - 検証スクリプト: `scripts/validation/`
  - ユーティリティスクリプト: `scripts/utils/`

- **検索式プロジェクト用ディレクトリ** (`search_formula/`)
  - 各検索プロジェクトは専用ディレクトリで管理
  - 検索結果や分析レポートもプロジェクトディレクトリ内に保存

- **テンプレート** (`templates/`)
  - PICO定義テンプレート: `templates/pico_definition.md`
  - 検索式ブロックテンプレート: `templates/blocks/search_formula_template.md`
  - データベース別テンプレート: `templates/database/`

### 6.2 ファイル命名規則

- データベース名は小文字（pubmed, central, embase）
- 日付形式：YYYYMMDD（例：20250328）
- ステータス接頭辞：draft_, final_, validated_
- 複数バージョンはv1, v2等の接尾辞で管理

### 6.3 コーディングスタイルと開発ガイドライン

- Pythonコードは PEP 8 に準拠
- 分析スクリプトは明確な命名規則に従う
- 各スクリプトは明確な役割と責任を持つよう設計
- 個人情報を含むデータは取り扱わない
- API キーなどの認証情報は環境変数で管理

## 7. 検証と品質保証

自動化された検証ツールを使用して検索式の品質を確保します。主な検証ポイント：

- 各検索用語の妥当性と検索結果
- シード論文の包含確認
- 検索式の構造的問題の特定
- データベース間変換の正確性
- 最終検索結果の評価

詳細な検証レポートを生成し、検索式の改善に役立てることができます。
