# Database Converter Skill

このスキルは、PubMed検索式を他のデータベース形式(CENTRAL, Embase/Dialog, ClinicalTrials.gov, ICTRP)に変換します。

## 発動条件

ユーザーが以下のような自然言語で要求した場合に、このスキルを実行してください:

- 「他のデータベース形式に変換」
- 「CENTRAL形式に変換して」
- 「Embaseの検索式を作成」
- 「ClinicalTrials.govの検索式を生成」
- 「全データベース形式に変換」
- 「データベース変換を実行」

## 入力パラメータ

### 必須パラメータ
- **project_dir**: プロジェクトディレクトリのパス (例: `projects/pps/`)

### オプションパラメータ
- **target_db**: 変換先データベース (デフォルト: `all`)
  - `all` - 全データベース (CENTRAL, Embase/Dialog, ClinicalTrials.gov, ICTRP)
  - `central` - Cochrane CENTRAL
  - `embase` または `dialog` - Embase (Dialog形式)
  - `clinicaltrials` - ClinicalTrials.gov
  - `ictrp` - WHO ICTRP

### 自動検出されるファイル
- `search_formula.md` - PubMed検索式ファイル

## 実行手順

### 1. プロジェクトディレクトリの確認

```python
import os

project_dir = "projects/{project_name}/"
formula_file = os.path.join(project_dir, "search_formula.md")

if not os.path.exists(formula_file):
    print(f"❌ エラー: 検索式ファイルが見つかりません")
    print(f"   期待されるパス: {formula_file}")
    print(f"   → search_formula.md を作成してください")
    return
```

### 2. 変換モードの決定

ユーザーの要求から変換先データベースを判定:
- "全て" / "all databases" → `target_db = "all"`
- "CENTRAL" → `target_db = "central"`
- "Embase" / "Dialog" → `target_db = "dialog"`
- "ClinicalTrials" / "trials registry" → `target_db = "clinicaltrials"`
- "ICTRP" → `target_db = "ictrp"`

### 3A. 全データベース変換 (target_db = "all")

```bash
python scripts/conversion/generate_all_database_search.py \
  --input {formula_file} \
  --output {project_dir}/search_all_databases.md
```

**出力ファイル**: `{project_dir}/search_all_databases.md`

### 3B. 個別データベース変換

```bash
python scripts/conversion/search_converter.py \
  --input {formula_file} \
  --output {project_dir}/search_{target_db}.md \
  --target-db {target_db}
```

**出力ファイル**: `{project_dir}/search_{target_db}.md`

### 4. 結果の整形と表示

**全データベース変換の場合**:
```markdown
## 🔄 データベース形式変換完了

### プロジェクト情報
- **プロジェクト**: pps
- **元の検索式**: projects/pps/search_formula.md
- **変換日時**: 2025-12-31 12:34:56

### 生成されたファイル
以下のデータベース形式に変換されました:

#### ✅ Cochrane CENTRAL
- **ファイル**: [projects/pps/search_central.md](projects/pps/search_central.md)
- **特徴**:
  - MeSH指定: `[mh "term"]`
  - フィールドタグ: `:ti,ab,kw` (Title, Abstract, Keywords)
  - 検索例: `[mh "physicians"]`

#### ✅ Embase (Dialog形式)
- **ファイル**: [projects/pps/search_embase.md](projects/pps/search_embase.md)
- **特徴**:
  - EMTREE形式: `EMB.EXACT.EXPLODE("Term")`
  - 検索行参照: `S1`, `S2`, `S3`
  - コマンドライン版も含む

#### ✅ ClinicalTrials.gov
- **ファイル**: [projects/pps/search_clinicaltrials.md](projects/pps/search_clinicaltrials.md)
- **特徴**:
  - 3つのカテゴリに分類:
    - Condition: 疾患・病態
    - Intervention: 介入・治療
    - Other Terms: その他のキーワード
  - MeSH用語は同義語展開される

#### ✅ WHO ICTRP
- **ファイル**: [projects/pps/search_ictrp.md](projects/pps/search_ictrp.md)
- **特徴**:
  - シンプルなOR/AND構造
  - MeSH用語は同義語展開
  - ネストは浅く保つ

### 変換内容サマリー

| データベース | 総検索ブロック数 | 主な変換内容 |
|-------------|-----------------|--------------|
| CENTRAL | 3ブロック | MeSH → descriptor形式 |
| Embase | 3ブロック | MeSH → EMTREE |
| ClinicalTrials.gov | 3カテゴリ | MeSH展開+カテゴリ分類 |
| ICTRP | 3ブロック | MeSH展開+単純化 |

### 次のステップ
1. 各データベースの検索式ファイルを確認
2. 必要に応じて手動調整
3. 各データベースで検索実行
4. 結果をsearch_results_to_reviewで統合

### 注意事項
⚠️  自動変換には以下の制限があります:
- MeSH同義語展開は基本的なもののみ
- データベース固有の制限(文字数、ネスト深度)は未考慮
- 検索式の論理構造が複雑な場合、手動調整が必要な場合があります
```

**個別データベース変換の場合**:
```markdown
## 🔄 CENTRAL形式への変換完了

### プロジェクト情報
- **プロジェクト**: pps
- **元の検索式**: projects/pps/search_formula.md
- **変換先データベース**: Cochrane CENTRAL

### 生成されたファイル
- **ファイル**: [projects/pps/search_central.md](projects/pps/search_central.md)

### 変換例

**PubMed形式**:
```
"Physicians"[Mesh] OR physician*[tiab]
```

**CENTRAL形式**:
```
[mh "physicians"] OR physician*:ti,ab,kw
```

### 変換ルール
1. **MeSH用語**: `"Term"[Mesh]` → `[mh "term"]` (CENTRAL Advanced Search)
2. **Title/Abstract**: `term[tiab]` → `term:ti,ab,kw`
3. **Title only**: `term[ti]` → `term:ti`
4. **ワイルドカード**: `*` は単語末で使用可。**引用符内ワイルドカードは漏れが出るため避ける**
5. **フレーズ+ワイルドカード**: `"heart transplant*"` → `(heart NEXT transplant*):ti,ab,kw`
6. **近接演算子**: `"persistent symptoms"[tiab:~2]` → `(persistent NEAR/2 symptom*):ti,ab,kw`
7. **論理演算子**: AND/OR/NOT はそのまま使用可能

### 次のステップ
1. search_central.md の内容を確認
2. Cochrane Libraryで検索実行
3. 結果をRIS/CSV形式でダウンロード
```

---

## データベース別変換仕様

### 1. Cochrane CENTRAL

**特徴**:
- Cochrane Libraryで使用される検索インターフェース
- MeSH指定は `[mh "term"]` を使用
- フィールドタグ: `:ti`, `:ab`, `:kw`, `:ti,ab,kw`
- **Warning**: 引用符内のワイルドカードは漏れが出るため、`NEXT`でネストする

**変換例**:
| PubMed | CENTRAL |
|--------|---------|
| `"Physicians"[Mesh]` | `[mh "physicians"]` |
| `physician*[tiab]` | `physician*:ti,ab,kw` |
| `burnout[ti]` | `burnout:ti` |
| `#1 AND #2` | `#1 AND #2` |

**生成ファイル形式**:
```markdown
# Cochrane CENTRAL検索式

## Block 1: Population
[mh "physicians"] OR
physician*:ti,ab,kw OR
doctor*:ti,ab,kw

## Block 2: Outcome
[mh "burnout, professional"] OR
burnout:ti,ab,kw

## Final Query
#1 AND #2
```

---

### 2. Embase (Dialog形式)

**特徴**:
- Dialogコマンドライン形式
- EMTREE統制語彙
- 検索行参照: S1, S2, S3...

**変換例**:
| PubMed | Embase (Dialog) |
|--------|-----------------|
| `"Physicians"[Mesh]` | `EMB.EXACT.EXPLODE("physician")` |
| `physician*[tiab]` | `physician*` |
| `#1 AND #2` | `S1 AND S2` |

**生成ファイル形式**:
```markdown
# Embase (Dialog) 検索式

## Block 1: Population
S1  EMB.EXACT.EXPLODE("physician")
S2  physician* OR doctor*
S3  S1 OR S2

## Block 2: Outcome
S4  EMB.EXACT.EXPLODE("burnout")
S5  burnout
S6  S4 OR S5

## Final Query
S7  S3 AND S6

## Command-line version
EMB.EXACT.EXPLODE("physician")
physician* OR doctor*
S1 OR S2
...
```

---

### 3. ClinicalTrials.gov

**特徴**:
- 3つの検索カテゴリに分類
  - **Condition**: 疾患・病態 (例: 疾患名、症状)
  - **Intervention**: 介入 (例: 薬剤、治療法)
  - **Other Terms**: その他 (例: 対象者、アウトカム)
- MeSH用語は同義語に展開される
- シンプルなOR/AND構造

**カテゴリ分類ルール**:
- 疾患・症状 → Condition
- 薬剤・治療・手術 → Intervention
- 対象者・職業・その他 → Other Terms

**変換例**:
| PubMed | ClinicalTrials.gov |
|--------|--------------------|
| `"Physicians"[Mesh]` | **Other Terms**: `Physicians OR physician OR doctors` |
| `"Burnout, Professional"[Mesh]` | **Condition**: `Burnout, Professional OR burnout OR occupational stress` |
| `"Drug Therapy"[Mesh]` | **Intervention**: `Drug Therapy OR pharmacotherapy` |

**生成ファイル形式**:
```markdown
# ClinicalTrials.gov 検索式

## Condition (疾患・病態)
Burnout, Professional OR burnout OR occupational stress

## Intervention (介入)
(なし)

## Other Terms (その他)
Physicians OR physician OR doctors

## 検索方法
1. Advanced Searchを開く
2. 各カテゴリに対応する検索語を入力
3. すべてのカテゴリをANDで結合して検索
```

---

### 4. WHO ICTRP

**特徴**:
- WHOの国際臨床試験登録プラットフォーム
- シンプルなキーワード検索
- MeSH用語は同義語展開
- ネストは最小限

**変換例**:
| PubMed | ICTRP |
|--------|-------|
| `"Physicians"[Mesh]` | `Physicians OR physician OR doctors` |
| `physician* AND burnout` | `(Physicians OR physician OR doctors) AND burnout` |

**生成ファイル形式**:
```markdown
# WHO ICTRP 検索式

## 検索語
(Physicians OR physician OR doctors) AND (Burnout OR occupational stress)

## 検索方法
1. ICTRP Advanced Searchにアクセス
2. 上記の検索式をコピー&ペースト
3. 検索実行
```

---

## エラーハンドリング

### エラーケース1: search_formula.md が存在しない

```markdown
❌ エラー: 検索式ファイルが見つかりません

期待されるパス: {project_dir}/search_formula.md

**対処方法**:
1. search_formula.md を作成してください
2. 外部AIアシスタントを使用して検索式を作成することを推奨
3. テンプレートを使用する場合:
   ```bash
   cp templates/search_formula_template.md {project_dir}/search_formula.md
   ```
```

### エラーケース2: 検索式の構造が解析できない

```markdown
⚠️  警告: 検索式の構造を完全に解析できませんでした

**影響**:
- 基本的な変換は実行されますが、一部の複雑な論理構造が正しく変換されない可能性があります

**対処方法**:
1. 生成されたファイルを手動で確認
2. 各データベースの公式ドキュメントを参照
3. 必要に応じて手動調整

**推奨リンク**:
- CENTRAL: https://www.cochranelibrary.com/advanced-search
- Embase: https://www.embase.com/
```

### エラーケース3: MeSH同義語展開の制限

```markdown
ℹ️  情報: MeSH同義語の展開は基本的なもののみです

**影響**:
- ClinicalTrials.govとICTRPの検索で、一部の同義語が含まれない可能性

**対処方法**:
1. 生成されたファイルを確認
2. 必要に応じて追加の同義語を手動で追加
3. MeSH Browserで公式の同義語を確認:
   - https://www.ncbi.nlm.nih.gov/mesh/

**例**:
- "Physicians" → "physician", "doctors", "medical doctors" (手動追加推奨: "clinicians")
```

### エラーケース4: 出力ディレクトリへの書き込み失敗

```markdown
❌ エラー: 出力ファイルを保存できませんでした

**対処方法**:
1. ディレクトリの書き込み権限を確認
2. ディスク容量を確認
3. 別のディレクトリを指定して再実行
```

---

## 技術的詳細

### 使用スクリプト
1. `scripts/conversion/generate_all_database_search.py` - 全データベース変換
2. `scripts/conversion/search_converter.py` - 個別データベース変換
3. `scripts/conversion/clinicaltrials/converter.py` - ClinicalTrials.gov変換
4. `scripts/conversion/ictrp/converter.py` - ICTRP変換

### 変換アルゴリズム

**1. PubMed → CENTRAL**:
- MeSH tag正規化: `[Mesh]` → `[MeSH Terms]`
- MeSH変換: `"Term"[Mesh]` → `[mh "term"]`
- Field tag変換: `[tiab]` → `:ti,ab,kw`
- 引用符内ワイルドカード回避: `"phrase*"` → `(word NEXT word*):ti,ab,kw`

**2. PubMed → Embase (Dialog)**:
- MeSH → EMTREE変換
- 検索行番号の自動割り当て (S1, S2, ...)
- EXACT.EXPLODE()関数の適用

**3. PubMed → ClinicalTrials.gov**:
- MeSH termの同義語展開
- 3カテゴリへの自動分類
- シンプルなOR構造への変換

**4. PubMed → ICTRP**:
- MeSH termの同義語展開
- 単純なAND/OR構造への変換
- ネスト深度の削減

### 制限事項

1. **MeSH同義語展開**:
   - 基本的な同義語のみ (完全なMeSH Entry Termsは含まない)
   - 手動での同義語追加を推奨

2. **論理構造の複雑さ**:
   - 深いネスト構造は一部のデータベースで制限される
   - 手動での簡略化が必要な場合あり

3. **データベース固有の機能**:
   - 各データベースの高度な機能 (近接演算子、フィールド制限など) は未対応
   - 手動での調整が必要

4. **文字数制限**:
   - 一部のデータベースには検索式の文字数制限あり
   - 超過する場合は手動で分割

---

## プロンプト例

### 全データベース変換
```
User: PPSプロジェクトの検索式を全データベース形式に変換して

Claude: database-converterスキルを実行します。
[projects/pps/search_formula.md を読み込み...]
[全データベース形式に変換中...]
[結果を表示]
```

### 特定データベース変換
```
User: PPSの検索式をCENTRAL形式に変換

Claude: database-converterスキルをCENTRAL変換モードで実行します。
[projects/pps/search_formula.md を読み込み...]
[CENTRAL形式に変換中...]
[結果を表示]
```

### プロジェクト名から推論
```
User: greenICUをEmbase形式に

Claude: database-converterスキルをEmbase変換モードで実行します。
プロジェクトディレクトリ: projects/greenICU/
[変換中...]
```

---

## 実装時の注意事項

1. **データベース名の正規化**:
   - "CENTRAL" / "Cochrane" / "cochrane library" → `target_db = "central"`
   - "Embase" / "Dialog" / "embase.com" → `target_db = "dialog"`
   - "ClinicalTrials" / "trials" / "ct.gov" → `target_db = "clinicaltrials"`
   - "ICTRP" / "WHO ICTRP" → `target_db = "ictrp"`

2. **出力ファイル名の規則**:
   - 全データベース: `search_all_databases.md`
   - 個別: `search_{target_db}.md` (例: `search_central.md`)

3. **変換後の確認推奨**:
   - 必ず生成ファイルの内容を確認するようユーザーに促す
   - 各データベースの公式ドキュメントへのリンクを提供

4. **次のステップ提案**:
   - 変換完了 → 各データベースで検索実行を提案
   - 検索結果取得 → search_results_to_reviewスキルを提案

---

## 関連スキル

- **search-validator**: 元のPubMed検索式の検証
- **project-initializer**: プロジェクト構造の初期化

## 参考リンク

- [Cochrane Library Advanced Search](https://www.cochranelibrary.com/advanced-search)
- [Embase.com](https://www.embase.com/)
- [ClinicalTrials.gov Advanced Search](https://clinicaltrials.gov/search/advanced)
- [WHO ICTRP Search](https://trialsearch.who.int/)
- [PubMed E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
