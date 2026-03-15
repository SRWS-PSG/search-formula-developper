# Project Initializer Skill

このスキルは、新しいsystematic reviewプロジェクトの標準的なディレクトリ構造とファイルを自動生成します。

## 発動条件

ユーザーが以下のような自然言語で要求した場合に、このスキルを実行してください:

- 「新しいプロジェクトを作成」
- 「新規プロジェクトの初期化」
- 「プロジェクト構造を作成して」
- 「新しいsystematic reviewを始めたい」
- 「プロジェクトのセットアップ」

## 入力パラメータ

### 必須パラメータ
- **project_name**: プロジェクト名 (例: `burnout-nurses`, `greenICU`, `pps`)

### オプションパラメータ
- **template_type**: 使用するテンプレート (デフォルト: `standard`)
  - `standard` - 標準的なsystematic reviewテンプレート
  - `pico` - PICO frameworkに基づくテンプレート
  - `minimal` - 最小限のファイルのみ

## 実行手順

### 1. プロジェクト名の正規化

```python
import re

# プロジェクト名を小文字・ハイフン区切りに正規化
project_name = project_name.lower()
project_name = re.sub(r'[^a-z0-9\-_]', '-', project_name)
project_name = re.sub(r'-+', '-', project_name)  # 連続ハイフンを1つに
```

例:
- "Burnout Nurses" → `burnout-nurses`
- "Green ICU" → `green-icu`
- "PPS_study" → `pps-study`

### 2. ディレクトリ構造の作成

```bash
mkdir -p projects/{project_name}/seed_papers
mkdir -p projects/{project_name}/log
```

**作成される構造**:
```
projects/
└── {project_name}/
    ├── protocol.md          # 研究プロトコル
    ├── seed_pmids.txt       # Seed PMIDs
    ├── search_formula.md    # 検索式 (空テンプレート)
    ├── seed_papers/         # Seed論文のbibliography
    └── log/                 # 検証結果・ログ
```

### 3. テンプレートファイルのコピー

**標準テンプレート (standard)**:
```bash
cp templates/rq_template.md projects/{project_name}/protocol.md
```

**PICOテンプレート (pico)**:
```bash
cp templates/pico_definition.md projects/{project_name}/protocol.md
```

### 4. 初期ファイルの作成

**seed_pmids.txt** (空ファイル):
```bash
cat > projects/{project_name}/seed_pmids.txt <<EOF
# Seed PMIDs (Key Papers)
# 1行に1つのPMIDを記入してください
# コメント行は#で始めます

# 例:
# 12345678
# 23456789

EOF
```

**search_formula.md** (テンプレート):
```bash
cat > projects/{project_name}/search_formula.md <<EOF
# Search Formula: {project_name}

## PubMed/MEDLINE

### Block #1: Population
<!-- ここに対象集団の検索語を記入 -->

### Block #2: Intervention (or Exposure)
<!-- ここに介入・曝露の検索語を記入 -->

### Block #3: Outcome
<!-- ここにアウトカムの検索語を記入 -->

### Final Query
<!-- 最終的な検索式の組み合わせを記入 -->
<!-- 例: #1 AND #2 AND #3 -->
<!-- Filters: Humans[Mesh], English[Lang] -->

EOF
```

**README.md** (プロジェクト概要):
```bash
cat > projects/{project_name}/README.md <<EOF
# {project_name}

## プロジェクト概要
<!-- このプロジェクトの概要を記入 -->

## 作成日
$(date +%Y-%m-%d)

## ファイル構成

- **protocol.md** - 研究プロトコル (RQ, PICO, 包含/除外基準)
- **seed_pmids.txt** - Seed論文のPMID一覧
- **seed_papers/** - Seed論文のbibliographyファイル (RIS, NBIB等)
- **search_formula.md** - PubMed検索式
- **log/** - 検証結果とログファイル

## ワークフロー

### Step 1: プロトコル作成
\`protocol.md\` にResearch QuestionとPICO frameworkを記入

### Step 2: Seed論文の収集
- Key papersを特定
- \`seed_papers/\` にbibliographyファイルを配置
- \`seed_pmids.txt\` にPMIDを記入

### Step 3: 検索式開発
- 外部AIアシスタント (ChatGPT, Claude等) を使用して検索式を作成
- \`search_formula.md\` に検索式を記入

### Step 4: 検証
\`\`\`bash
# 検索式の検証
python scripts/search/query_executor/check_final_query.py \\
  --formula-file projects/{project_name}/search_formula.md \\
  --pmid-file projects/{project_name}/seed_pmids.txt \\
  --output-dir projects/{project_name}/
\`\`\`

### Step 5: データベース変換
\`\`\`bash
# 全データベース形式に変換
python scripts/conversion/generate_all_database_search.py \\
  --input projects/{project_name}/search_formula.md \\
  --output projects/{project_name}/search_all_databases.md
\`\`\`

## 参考リンク
- [CLAUDE.md](../../CLAUDE.md) - システム全体のドキュメント
- [テンプレート](../../templates/) - 各種テンプレート

EOF
```

### 5. 結果の表示

```markdown
## 🎉 プロジェクト作成完了

### プロジェクト情報
- **プロジェクト名**: {project_name}
- **プロジェクトパス**: projects/{project_name}/
- **作成日時**: {timestamp}
- **テンプレート**: {template_type}

### 作成されたファイル

#### ✅ ディレクトリ構造
```
projects/{project_name}/
├── 📄 protocol.md          # 研究プロトコル
├── 📄 seed_pmids.txt       # Seed PMIDs (空)
├── 📄 search_formula.md    # 検索式テンプレート
├── 📄 README.md            # プロジェクト概要
├── 📁 seed_papers/         # Seed論文フォルダ (空)
└── 📁 log/                 # ログフォルダ (空)
```

#### 📝 次のステップ

##### 1. プロトコルの作成
[protocol.md](projects/{project_name}/protocol.md) を編集して、以下を記入:
- Research Question (RQ)
- PICO framework
  - **P**opulation (対象集団)
  - **I**ntervention (介入)
  - **C**omparison (比較)
  - **O**utcome (アウトカム)
- 包含/除外基準

##### 2. Seed論文の収集
- key papersを5-10件特定
- PMIDを [seed_pmids.txt](projects/{project_name}/seed_pmids.txt) に記入
  ```
  12345678
  23456789
  ```
- (オプション) Bibliography fileを `seed_papers/` に配置

##### 3. 検索式の開発
外部AIアシスタントを使用することを推奨:
- VS Code Copilot Chat
- ChatGPT
- Claude

プロトコルとseed papersを共有して、検索式を作成してもらい、
[search_formula.md](projects/{project_name}/search_formula.md) に保存

##### 4. 検証と最適化
Claude Codeのスキルを活用:
- **search-validator**: 検索式の検証とseed paper捕捉確認
  ```
  "PPSプロジェクトの検索式を検証して"
  ```
- **mesh-analyzer**: MeSH term抽出と階層分析
  ```
  "PPSのMeSHを抽出して"
  ```
- **term-counter**: 各検索語の件数確認
  ```
  "各キーワードの件数を調べて"
  ```

##### 5. データベース変換
- **database-converter**: 他のデータベース形式に変換
  ```
  "全データベース形式に変換して"
  ```

### 便利なコマンド

#### プロジェクトディレクトリに移動
```bash
cd projects/{project_name}/
```

#### ファイル一覧表示
```bash
ls -la
```

#### プロトコルを開く
```bash
code protocol.md  # VS Code
# または
open protocol.md  # macOS
# または
start protocol.md  # Windows
```

### 関連ドキュメント
- 📖 [CLAUDE.md](CLAUDE.md#project-setup-workflow) - プロジェクトセットアップの詳細
- 📖 [templates/rq_template.md](templates/rq_template.md) - RQテンプレートの例
- 📖 [templates/pico_definition.md](templates/pico_definition.md) - PICO定義テンプレート
```

---

## テンプレート種類

### 1. Standard Template (デフォルト)

**使用ファイル**: `templates/rq_template.md`

**含まれる内容**:
- Research Question (RQ)
- PICO framework
- Study design
- Inclusion/Exclusion criteria
- Language restrictions
- Publication date range

**適用例**: 一般的なsystematic review

---

### 2. PICO Template

**使用ファイル**: `templates/pico_definition.md`

**含まれる内容**:
- PICOの詳細定義
- 各要素の具体例
- MeSH terms候補
- 検索戦略のヒント

**適用例**: PICOが明確なclinical question

---

### 3. Minimal Template

**含まれる内容**:
- 基本的なディレクトリ構造のみ
- テンプレートファイルは最小限

**適用例**: 既存のプロトコルがある場合

---

## エラーハンドリング

### エラーケース1: プロジェクト名が既に存在

```markdown
⚠️  警告: プロジェクトが既に存在します

既存のプロジェクト: projects/{project_name}/

**対処方法**:
1. 別のプロジェクト名を使用
2. 既存プロジェクトを削除して再作成 (注意: データが失われます)
   ```bash
   rm -rf projects/{project_name}/
   ```
3. 既存プロジェクトをそのまま使用
```

### エラーケース2: プロジェクト名が無効

```markdown
❌ エラー: プロジェクト名に無効な文字が含まれています

指定されたプロジェクト名: "{invalid_name}"
使用可能な文字: a-z, 0-9, ハイフン(-), アンダースコア(_)

**推奨される名前**:
- "{suggested_name1}"
- "{suggested_name2}"
```

### エラーケース3: ディレクトリ作成失敗

```markdown
❌ エラー: ディレクトリを作成できませんでした

**対処方法**:
1. 書き込み権限を確認
2. ディスク容量を確認
3. パスに無効な文字がないか確認
```

### エラーケース4: テンプレートファイルが見つからない

```markdown
⚠️  警告: テンプレートファイルが見つかりません

期待されるパス: templates/{template_name}.md

**影響**:
- 空のprotocol.mdが作成されます

**対処方法**:
- templates/ディレクトリにテンプレートファイルが存在するか確認
- 手動でprotocol.mdを編集
```

---

## 技術的詳細

### ディレクトリ作成コマンド
```bash
mkdir -p projects/{project_name}/seed_papers
mkdir -p projects/{project_name}/log
```

### ファイルコピー
```bash
cp templates/rq_template.md projects/{project_name}/protocol.md
```

### プロジェクト名の正規化ロジック
```python
import re

def normalize_project_name(name: str) -> str:
    """プロジェクト名を正規化"""
    # 小文字化
    name = name.lower()
    # スペースをハイフンに
    name = name.replace(' ', '-')
    # 無効な文字を削除
    name = re.sub(r'[^a-z0-9\-_]', '', name)
    # 連続ハイフンを1つに
    name = re.sub(r'-+', '-', name)
    # 前後のハイフンを削除
    name = name.strip('-')
    return name
```

### 作成されるファイルのサイズ
- protocol.md: ~2KB (テンプレートによる)
- seed_pmids.txt: ~100B (空)
- search_formula.md: ~500B (テンプレート)
- README.md: ~1.5KB

---

## プロンプト例

### 基本的な使い方
```
User: burnout-nursesという新しいプロジェクトを作成して

Claude: project-initializerスキルを実行します。
プロジェクト名: burnout-nurses
[ディレクトリ作成中...]
[テンプレートファイルコピー中...]
[結果を表示]
```

### テンプレート指定
```
User: Green ICUプロジェクトをPICOテンプレートで作成

Claude: project-initializerスキルをPICOテンプレートで実行します。
プロジェクト名: green-icu
テンプレート: pico
[作成中...]
```

### プロジェクト名の正規化
```
User: 新しいプロジェクト "Autoethnography in Medical Education" を作成

Claude: project-initializerスキルを実行します。
プロジェクト名を正規化: "autoethnography-in-medical-education"
[作成中...]
```

---

## 実装時の注意事項

1. **プロジェクト名の検証**:
   - 既存プロジェクトと重複チェック
   - 無効な文字の自動修正
   - ユーザーに正規化後の名前を確認

2. **テンプレート選択**:
   - デフォルトはstandardテンプレート
   - ユーザーが "PICO" を明示 → picoテンプレート
   - 明示的に "minimal" 指定 → minimalテンプレート

3. **ファイル上書き防止**:
   - 既存プロジェクトがある場合は警告
   - 上書きする場合は明示的な確認を取る

4. **相対パスの使用**:
   - すべてのパスは作業ディレクトリからの相対パス
   - `projects/{project_name}/` として一貫性を保つ

5. **次のステップの明確化**:
   - 作成後、必ず次に何をすべきか提示
   - 他のスキル (search-validator等) への誘導

6. **README.mdの自動生成**:
   - プロジェクト固有のワークフローを含める
   - 実際に使えるコマンド例を記載

---

## 関連スキル

- **search-validator**: プロジェクト作成後の検索式検証
- **mesh-analyzer**: Seed論文のMeSH抽出
- **term-counter**: 検索語の件数確認
- **database-converter**: データベース形式変換

## 参考リンク

- [CLAUDE.md - Project Setup Workflow](../../CLAUDE.md#project-setup-workflow)
- [templates/rq_template.md](../../templates/rq_template.md)
- [templates/pico_definition.md](../../templates/pico_definition.md)
