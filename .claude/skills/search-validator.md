# Search Validator Skill

このスキルは、systematic reviewプロジェクトの検索式を検証し、seed paperが正しく捕捉されているかを確認します。

## 発動条件

ユーザーが以下のような自然言語で要求した場合に、このスキルを実行してください:

- 「検索式を検証して」
- 「seed paperを確認」
- 「validationを実行」
- 「最終検索式をチェック」
- 「seed PMIDが捕捉されているか確認」
- 「検索式が正しいか調べて」

## 入力パラメータ

### 必須パラメータ
- **project_dir**: プロジェクトディレクトリのパス (例: `projects/pps/`)

### 自動検出されるファイル
スキル実行時に、以下のファイルをproject_dir内から自動検出します:
- `search_formula.md` - 検索式ファイル
- `seed_pmids.txt` - Seed PMID一覧ファイル

いずれかのファイルが存在しない場合は、ユーザーにエラーメッセージを表示してください。

## 実行手順

### 1. プロジェクトディレクトリの確認

```python
import os

# プロジェクトディレクトリの存在確認
if not os.path.exists(project_dir):
    print(f"エラー: プロジェクトディレクトリが見つかりません: {project_dir}")
    return
```

### 2. 必要なファイルの存在確認

```python
formula_file = os.path.join(project_dir, "search_formula.md")
pmid_file = os.path.join(project_dir, "seed_pmids.txt")

if not os.path.exists(formula_file):
    print(f"❌ エラー: 検索式ファイルが見つかりません")
    print(f"   期待されるパス: {formula_file}")
    print(f"   → search_formula.md を作成してください")
    return

if not os.path.exists(pmid_file):
    print(f"⚠️  警告: Seed PMIDファイルが見つかりません")
    print(f"   期待されるパス: {pmid_file}")
    print(f"   → seed_pmids.txt を作成するか、検索式の総件数のみ確認します")
    pmid_file = None  # PMIDファイルなしで続行
```

### 3. 検証スクリプトの実行

```bash
python scripts/search/query_executor/check_final_query.py \
  --formula-file {formula_file} \
  --pmid-file {pmid_file} \
  --output-dir {project_dir}
```

### 4. 結果の整形と表示

スクリプトの出力を解析して、以下の形式でマークダウンレポートを表示:

```markdown
## 🔍 検索式検証結果

### プロジェクト情報
- **プロジェクト**: {project_name}
- **検索式ファイル**: {formula_file}
- **Seed PMIDファイル**: {pmid_file}

### 検索結果サマリー
- **総ヒット数**: {total_count:,}件
- **最終検索式**: `{final_query}`

### Seed Paper捕捉状況
- **捕捉率**: {captured}/{total} ({percentage}%)

#### 詳細
{捕捉されたPMIDのリスト}
{捕捉されなかったPMIDのリスト}

### 次のステップ
{推奨されるアクション}
```

### 5. レポートファイルの保存

検証結果を以下のパスに保存:
```
{project_dir}/log/validation_{timestamp}.md
```

## 出力例

```markdown
## 🔍 検索式検証結果

### プロジェクト情報
- **プロジェクト**: pps
- **検索式ファイル**: projects/pps/search_formula.md
- **Seed PMIDファイル**: projects/pps/seed_pmids.txt

### 検索結果サマリー
- **総ヒット数**: 1,234件
- **最終検索式**: `(#1 AND #2 AND #3) AND (Humans[Mesh] AND English[Lang])`

### Seed Paper捕捉状況
- **捕捉率**: 5/5 (100%) ✅

#### 捕捉されたPMID (5件)
- ✅ PMID 12345678: 捕捉されています
- ✅ PMID 23456789: 捕捉されています
- ✅ PMID 34567890: 捕捉されています
- ✅ PMID 45678901: 捕捉されています
- ✅ PMID 56789012: 捕捉されています

#### 捕捉されなかったPMID
なし

### 次のステップ
✅ 全てのseed paperが捕捉されています。次は他のデータベース形式への変換を検討してください。
```

## エラーハンドリング

### エラーケース1: プロジェクトディレクトリが存在しない

```markdown
❌ エラー: プロジェクトディレクトリが見つかりません

指定されたパス: {project_dir}

**対処方法**:
1. パスのスペルミスを確認してください
2. 新規プロジェクトの場合は、project-initializerスキルを使って作成してください
```

### エラーケース2: search_formula.md が存在しない

```markdown
❌ エラー: 検索式ファイルが見つかりません

期待されるパス: {project_dir}/search_formula.md

**対処方法**:
1. 検索式を作成してください (外部AIアシスタントを推奨)
2. テンプレートを使用する場合: `cp templates/search_formula_template.md {project_dir}/search_formula.md`
```

### エラーケース3: seed_pmids.txt が空

```markdown
⚠️  警告: Seed PMIDファイルが空です

ファイルパス: {project_dir}/seed_pmids.txt

**影響**:
- 総件数の確認は可能ですが、seed paper捕捉率は検証できません

**対処方法**:
1. key papersのPMIDを1行に1つずつ記入してください
2. 例:
   ```
   12345678
   23456789
   # コメントは#で始める
   ```
```

### エラーケース4: Seed paperが捕捉されていない (< 100%)

```markdown
⚠️  警告: 一部のseed paperが捕捉されていません

捕捉率: {captured}/{total} ({percentage}%)

**捕捉されなかったPMID**:
- ❌ PMID {pmid1}
- ❌ PMID {pmid2}

**対処方法**:
1. 捕捉されなかったPMIDの論文内容を確認
2. 不足している検索語を特定
3. 検索式を修正して再検証

**推奨ツール**:
- `mesh-analyzer` スキル: 捕捉されなかった論文のMeSH termを抽出
- `check_specific_papers.py`: どのブロックで捕捉されているか詳細分析
```

### エラーケース5: API rate limit超過

```markdown
❌ エラー: PubMed APIのレート制限に達しました

**対処方法**:
1. 30秒ほど待ってから再実行してください
2. 頻繁に発生する場合は、NCBI_API_KEYの設定を検討してください
   - https://www.ncbi.nlm.nih.gov/account/ でAPI keyを取得
   - 環境変数に設定: `export NCBI_API_KEY=your_key_here`
```

## 技術的詳細

### 使用スクリプト
- `scripts/search/query_executor/check_final_query.py`

### 検証ロジック
1. **総件数取得**: 最終検索式をPubMed APIで実行 (retmax=0で件数のみ)
2. **Seed paper捕捉確認**: 各PMIDに対して `(最終検索式) AND {pmid}[PMID]` を実行
3. **個別確認の理由**: 大規模検索(>10,000件)では古い論文が最初のバッチに含まれない可能性があるため

### API使用制限
- レート制限: 3リクエスト/秒 (APIキーなし), 10リクエスト/秒 (APIキーあり)
- スクリプト内で `time.sleep(0.34)` により自動的に制限を遵守

### 出力ファイル
- レポート: `{project_dir}/log/validation_{YYYYMMDD_HHMMSS}.md`
- RISファイル: 出力なし (スクリプトはseed検証のみに最適化)

## プロンプト例

### 基本的な使い方
```
User: PPSプロジェクトの検索式を検証して

Claude: search-validatorスキルを実行します。
[projects/pps/ を確認...]
[検証中...]
[結果を表示]
```

### プロジェクト名から推論
```
User: greenICUの検索式をチェック

Claude: search-validatorスキルを実行します。
プロジェクトディレクトリ: projects/greenICU/
[検証中...]
```

### パスを明示的に指定
```
User: projects/autoethnography/ の検索式を検証

Claude: search-validatorスキルを実行します。
[検証中...]
```

## 実装時の注意事項

1. **プロジェクト名の正規化**:
   - ユーザーが "PPS" と言った場合 → `projects/pps/` に変換
   - ユーザーが "projects/pps" と言った場合 → そのまま使用
   - 末尾の `/` は自動補完

2. **ファイル存在確認の順序**:
   - まずproject_dirの存在確認
   - 次にsearch_formula.mdの存在確認
   - 最後にseed_pmids.txtの存在確認 (オプショナル)

3. **出力の可読性**:
   - 数値は3桁カンマ区切り (1,234件)
   - 捕捉率はパーセント表示 (5/5 = 100%)
   - 絵文字で視覚的にわかりやすく (✅❌⚠️)

4. **次のステップの提案**:
   - 100%捕捉 → database-converterスキルを提案
   - 一部未捕捉 → mesh-analyzerスキルを提案
   - 検索式が見つからない → プロトコル確認と外部AI使用を提案

## 関連スキル

- **mesh-analyzer**: 捕捉されなかった論文のMeSH term分析
- **term-counter**: 各検索語の件数確認
- **database-converter**: 他データベース形式への変換
