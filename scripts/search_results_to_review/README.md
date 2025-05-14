# 検索結果処理ツール（Search Results Processor）

このツールは、システマティックレビューにおいて複数のデータベースから収集した検索結果を効率的に処理し、Rayyanなどのスクリーニングツールで利用可能な形式に変換するためのコマンドラインユーティリティです。

## 機能概要

- 複数のデータソース（PubMed, Embase, CENTRAL, ClinicalTrials.gov, ICTRP）から検索結果を一括処理
- 多様なファイル形式（RIS, NBIB, XML）の自動認識と処理
- DOIとタイトルベースの重複排除機能
- Rayyan互換CSVフォーマットへの変換
- 大量の文献を効率的に処理するための分割出力（デフォルト: 500件/ファイル単位）
- PRISMAフローチャート用の統計情報生成

## 依存ライブラリ

以下のPythonパッケージが必要です：

```bash
pip install pandas rispy nbib lxml
```

- `pandas`: データ処理とCSV出力
- `rispy`: RISファイルの解析
- `nbib`: NBIBファイルの解析
- `lxml`: XMLファイルの解析

## 使用方法

### 基本的な使用方法

```bash
python search_results_processor.py --input-dir <検索結果ファイルのあるディレクトリ> --output-dir <出力先ディレクトリ>
```

### オプション

- `--input-dir` (必須): 検索結果ファイルが保存されているディレクトリのパス
- `--output-dir` (任意): 処理結果の出力先ディレクトリ。指定がない場合は `<input-dir>/processed` が使用されます
- `--verbose` (任意): 詳細な処理情報を表示します

### 例

```bash
# 基本的な使用例
python search_results_processor.py --input-dir search_formula/project1 --output-dir search_formula/project1/processed

# 詳細な処理情報を表示
python search_results_processor.py --input-dir search_formula/project1 --output-dir search_formula/project1/processed --verbose
```

## 入力ファイル形式

以下のファイル形式を自動認識して処理します：

1. **RISファイル** (`.ris`, `.txt`拡張子)
   - PubMed, Embase, CENTRAL等からのエクスポートファイル
   - プロバイダー別（ProQuest, Ovid, Mendeley, Endnote, Zotero, Paperpile, Rayyan, CENTRAL等）の形式に対応

2. **NBIBファイル** (`.nbib`拡張子)
   - PubMedからのエクスポートファイル

3. **ClinicalTrials.gov RISファイル**
   - ClinicalTrials.govからのエクスポートファイル

4. **ICTRP XMLファイル** (`.xml`拡張子)
   - ICTRPからのエクスポートファイル

## 出力ファイル

以下のファイルが出力されます：

1. **テストレビュー用CSV** (`0_testreview.csv`)
   - 最初の50件のレコードを含むCSVファイル

2. **レビュー用CSV** (`1_search.csv`, `2_search.csv`, ...)
   - 残りのレコードを500件ごとに分割したCSVファイル
   - 大量の文献を効率的にスクリーニングするために分割

3. **圧縮ZIPファイル** (`rayyan_csv_files.zip`)
   - すべてのCSVファイルをまとめた圧縮ファイル

4. **統計情報レポート** (`summary_report_YYYYMMDD_HHMMSS.txt`)
   - 各データソースの件数
   - 重複排除前後のレコード数
   - 重複率
   - PRISMAフローチャート用の書式化された統計情報

## 処理フロー

```mermaid
flowchart TD
    A[検索結果ファイル\n検出] --> B[ファイルタイプ\n自動認識]
    B --> C[ファイル読み込み\nと処理]
    C --> D[データの統合]
    D --> E[重複排除]
    E --> F[CSV形式に変換]
    F --> G[分割出力]
    G --> H[統計情報生成]
```

## ファイル形式ごとの処理の詳細

### RISファイル処理

- 複数のRISフォーマット（ProQuest, Ovid, Mendeley, Endnote, Zotero, Paperpile, Rayyan, CENTRAL）に対応
- データ抽出パターンに基づいてファイルタイプを自動判別
- 各フィールドを標準化して統一的なスキーマに変換

### NBIBファイル処理

- PubMedからエクスポートされたNBIBファイルを解析
- 著者情報、ジャーナル情報、抄録などの詳細情報を抽出
- 標準化されたスキーマに変換

### ClinicalTrials.gov処理

- ClinicalTrials.govのRISまたはCSVファイルから情報を抽出
- 研究デザイン、介入、条件などの重要な情報を抄録として結合
- ジャーナル名に "ClinicalTrials.gov" を設定

### ICTRP XML処理

- ICTRPからのXMLファイルを解析
- 研究ID、タイトル、条件、介入などの情報を抽出
- プロジェクト情報を構造化して標準フォーマットに変換

## 重複排除アルゴリズム

重複の検出と排除は以下の優先順位で行われます：

1. **DOIの完全一致**: 同一DOIを持つレコードは重複と判定
2. **タイトルの類似性**: 大文字小文字を無視してタイトルが完全一致するレコードは重複と判定
3. **初出優先**: 重複が検出された場合、最初に出現したレコードを保持

## トラブルシューティング

### よくある問題

1. **文字化けが発生する場合**
   - 出力ファイルがUTF-8 with BOM形式で保存されるため、日本語環境でも通常は問題ありません
   - CSVファイルをExcelで開く場合は、文字コードを指定してインポートしてください

2. **特定のファイルが処理されない**
   - サポートされていないファイル形式である可能性があります
   - ファイルが破損していないか確認してください
   - `--verbose` オプションを使用して詳細なエラーメッセージを確認してください

3. **重複排除の精度に問題がある**
   - 一部のデータベースでは論文のタイトルが若干異なる場合があります
   - 同一論文が異なるDOIを持つケースではタイトルベースの重複検出に依存します

## モジュール構成

このツールは以下のモジュールから構成されています：

- `file_handlers.py`: 各ファイル形式の読み込みと初期処理
- `data_processing.py`: データ統合、スキーマ統一、重複排除
- `output_generator.py`: CSV出力、統計情報生成
- `search_results_processor.py`: メインの実行ファイル

## 今後の開発計画

1. **さらなるファイル形式のサポート**
   - 各種書誌情報形式（BibTeX, RDF等）への対応拡大
   - さらに多くのデータベース固有フォーマットのサポート

2. **インタラクティブモード**
   - GUIインターフェースの追加
   - ウェブインターフェースの開発

3. **分析機能の強化**
   - 検索結果の自動カテゴリ分類
   - キーワード分析と可視化

## ライセンス

本ツールはMITライセンスの下で提供されています。
