# Term Counter Skill

このスキルは、検索式の各検索語やブロックの件数を確認し、重複分析を行って検索式の最適化を支援します。

## 発動条件

ユーザーが以下のような自然言語で要求した場合に、このスキルを実行してください:

- 「各キーワードの件数を調べて」
- 「検索語のヒット数を確認」
- 「ブロックの重複を分析」
- 「各行の件数をチェック」
- 「検索語の効果を確認」
- 「どの検索語が効いているか調べて」
- 「term countを実行」

## 入力パラメータ

### パターン1: 検索式全体の各行件数確認
- **project_dir**: プロジェクトディレクトリのパス (例: `projects/pps/`)
- **mode**: `lines` (デフォルト)
- 自動検出ファイル: `search_formula.md`

### パターン2: 特定ブロックの重複分析
- **project_dir**: プロジェクトディレクトリのパス
- **block_input**: ブロックテキスト (ファイルまたは直接入力)
- **block_name**: ブロック名 (例: "Population", "#2A MeSH")
- **mode**: `overlap`

## 実行モード

### モード1: 各行の件数確認 (check_search_lines.py)

**発動例**:
- "PPSの検索式で各キーワードの件数を確認"
- "各行のヒット数を調べて"

**実行手順**:

1. プロジェクトディレクトリ確認
```python
import os

project_dir = "projects/{project_name}/"
formula_file = os.path.join(project_dir, "search_formula.md")
output_dir = os.path.join(project_dir, "log")

if not os.path.exists(formula_file):
    print(f"❌ エラー: 検索式ファイルが見つかりません")
    print(f"   期待されるパス: {formula_file}")
    return
```

2. 件数確認スクリプト実行
```bash
python scripts/search/term_validator/check_search_lines.py \
  --input-formula {formula_file} \
  --output {output_dir}/search_lines_results_{timestamp}.md
```

3. 結果の整形と表示

**出力例**:
```markdown
## 📊 検索語別ヒット数分析

### プロジェクト情報
- **プロジェクト**: pps
- **検索式ファイル**: projects/pps/search_formula.md
- **分析日時**: 2025-12-31 12:34:56

### 検索行別ヒット数

#### Block #1: Population
| 行番号 | 検索語 | ヒット数 |
|--------|--------|----------|
| #1 | "Physicians"[Mesh] | 234,567件 |
| #2 | "Medical Staff, Hospital"[Mesh] | 45,678件 |
| #3 | physician*[tiab] | 456,789件 |
| #4 | doctor*[tiab] | 678,901件 |

**#1 OR #2 OR #3 OR #4**: 987,654件

#### Block #2: Outcome
| 行番号 | 検索語 | ヒット数 |
|--------|--------|----------|
| #5 | "Burnout, Professional"[Mesh] | 12,345件 |
| #6 | burnout[tiab] | 23,456件 |
| #7 | "occupational stress"[tiab] | 34,567件 |

**#5 OR #6 OR #7**: 56,789件

### 最終検索式
**#1-4 AND #5-7**: 1,234件

### 分析結果
- ✅ 全ての検索語がヒットしています
- ⚠️  #4 (doctor*[tiab]) が最も多くのヒット (678,901件)
- ℹ️  MeSH termsと自由語の組み合わせにより、適度な感度が確保されています

### 推奨事項
1. 非常に広い検索語 (#3, #4) の必要性を再検討
2. より限定的な検索が必要な場合、MeSH termsのみ使用を検討
3. term-counterの重複分析モードで、各検索語の貢献度を確認

### 詳細レポート
- 📄 {output_dir}/search_lines_results_{timestamp}.md に保存しました
```

---

### モード2: ブロック重複分析 (check_block_overlap.py)

**発動例**:
- "Populationブロックの重複を分析"
- "このブロックの各検索語の貢献度を確認"

**実行手順**:

1. ブロック入力の取得
   - **方法A**: ユーザーがブロックテキストを直接提供
   - **方法B**: search_formula.mdから特定ブロックを抽出

2. 重複分析スクリプト実行

**方法A (直接入力)**:
```bash
# 一時ファイルにブロックテキストを保存
echo '{block_text}' > /tmp/temp_block.txt

python scripts/search/term_validator/check_block_overlap.py \
  --input /tmp/temp_block.txt \
  --output {output_dir}/block_overlap_{timestamp}.md \
  --block-name "{block_name}"
```

**方法B (標準入力)**:
```bash
python scripts/search/term_validator/check_block_overlap.py \
  --output {output_dir}/block_overlap_{timestamp}.md \
  --block-name "{block_name}" <<EOF
{block_text}
EOF
```

3. 結果の整形と表示

**出力例**:
```markdown
## 🔄 検索ブロック重複分析

### ブロック情報
- **ブロック名**: #2A Population (MeSH)
- **分析日時**: 2025-12-31 12:34:56

### 個別検索語のヒット数

| # | 検索語 | ヒット数 |
|---|--------|----------|
| 1 | "Physicians"[Mesh] | 234,567件 |
| 2 | "Medical Staff, Hospital"[Mesh] | 45,678件 |
| 3 | "Health Personnel"[Mesh] | 567,890件 |
| 4 | "Nurses"[Mesh] | 345,678件 |

### 累積OR結果 (重複分析)

| ステップ | 検索式 | ヒット数 | 新規追加 | 貢献率 |
|----------|--------|----------|----------|--------|
| 1 | "Physicians"[Mesh] | 234,567件 | - | - |
| 2 | #1 OR "Medical Staff, Hospital"[Mesh] | 256,789件 | +22,222件 | 8.6% |
| 3 | #2 OR "Health Personnel"[Mesh] | 567,890件 | +311,101件 | 54.8% |
| 4 | #3 OR "Nurses"[Mesh] | 678,901件 | +111,011件 | 16.4% |

### 分析結果

#### ✅ 高貢献度の検索語 (>10%新規追加)
1. **"Health Personnel"[Mesh]** - 311,101件追加 (54.8%)
   - 最も多くの新規文献を追加
   - 推奨: 必須

2. **"Nurses"[Mesh]** - 111,011件追加 (16.4%)
   - 重要な追加文献あり
   - 推奨: 必須

#### ⚠️  低貢献度の検索語 (<10%新規追加)
3. **"Medical Staff, Hospital"[Mesh]** - 22,222件追加 (8.6%)
   - 新規追加が少ない
   - 推奨: オプション (感度重視の場合は維持)

#### 🔍 重複の詳細
- **"Physicians"[Mesh]** は **"Health Personnel"[Mesh]** に完全に含まれます
  - Health Personnelの下位概念
  - より広いHealth Personnelのみ使用すれば、Physiciansは不要

### 最適化案

#### オプション1: 最大感度 (現状維持)
```
"Physicians"[Mesh] OR
"Medical Staff, Hospital"[Mesh] OR
"Health Personnel"[Mesh] OR
"Nurses"[Mesh]
```
- **総ヒット数**: 678,901件

#### オプション2: 高効率 (低貢献度除外)
```
"Health Personnel"[Mesh] OR
"Nurses"[Mesh]
```
- **総ヒット数**: 656,789件 (96.7%カバー)
- **削減**: 22,112件 (3.3%)

#### オプション3: 単純化 (上位概念のみ)
```
"Health Personnel"[Mesh]
```
- **総ヒット数**: 567,890件 (83.7%カバー)
- **削減**: 111,011件 (16.4%)
- **注意**: Nursesの独自文献が失われる

### 推奨
✅ **オプション2 (高効率)** を推奨します

**理由**:
- 96.7%のカバレッジを維持
- 低貢献度のMedical Staff, Hospitalを除外
- Health PersonnelがPhysiciansを包含

### 次のステップ
1. search-validatorでseed paper捕捉率を再確認
2. 最適化した検索式で総件数が許容範囲か確認
3. 必要に応じて、除外した検索語を復活

### 詳細レポート
- 📄 {output_dir}/block_overlap_{timestamp}.md に保存しました
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
```

### エラーケース2: 検索式の構造が解析できない

```markdown
⚠️  警告: 検索式の一部の行を解析できませんでした

解析失敗: 2/10行

**影響**:
- 解析できた行のみヒット数を表示します

**対処方法**:
1. search_formula.mdの形式を確認
2. 各行が `#番号 検索式` の形式になっているか確認
3. 例:
   ```
   #1 "Physicians"[Mesh]
   #2 physician*[tiab]
   ```
```

### エラーケース3: API rate limit超過

```markdown
❌ エラー: PubMed APIのレート制限に達しました

**対処方法**:
1. 30秒ほど待ってから再実行
2. 環境変数 `NCBI_RATE_LIMIT_RPS` を調整 (デフォルト: 3リクエスト/秒)
3. NCBI API keyを設定してレート制限を緩和
   - https://www.ncbi.nlm.nih.gov/account/
   - 環境変数: `export NCBI_API_KEY=your_key_here`
```

### エラーケース4: 検索語が0件

```markdown
⚠️  警告: ヒット数が0件の検索語があります

ヒット0件の検索語:
- #5: "Invalid Term"[Mesh]
- #8: xyz123[tiab]

**対処方法**:
1. スペルミスを確認
2. MeSH termの場合、mesh-analyzerスキルで検証
3. 不要な検索語は削除を検討
```

### エラーケース5: ブロック入力が空

```markdown
❌ エラー: ブロックテキストが空です

**対処方法**:
1. 正しいブロックテキストを提供してください
2. 形式例:
   ```
   #### #2A Block Name
   "Term1"[Mesh] OR
   "Term2"[Mesh] OR
   term3[tiab]
   ```
```

---

## 技術的詳細

### 使用スクリプト
1. `scripts/search/term_validator/check_search_lines.py` - 各行の件数確認
2. `scripts/search/term_validator/check_block_overlap.py` - ブロック重複分析

### ヒット数取得ロジック

**check_search_lines.py**:
1. search_formula.mdをパースして各行を抽出
2. 各行のクエリをPubMed E-utilities APIで実行 (retmax=0で件数のみ)
3. 結果を集計してマークダウンレポート生成

**check_block_overlap.py**:
1. ブロック内の各検索語を抽出
2. 個別にヒット数取得
3. 累積OR演算でヒット数取得 (Term1, Term1 OR Term2, Term1 OR Term2 OR Term3, ...)
4. 各ステップの新規追加件数を計算
5. 貢献率を算出 (新規追加 / 総ヒット数)

### API使用効率化
- レート制限遵守: `NCBI_RATE_LIMIT_RPS` 環境変数で制御
- リトライロジック: 最大5回、指数バックオフ
- POST送信: 長いURLの場合は自動的にPOSTメソッド使用

### 重複分析の閾値

**貢献率による分類**:
- **高貢献度**: 10%以上の新規追加 → 必須
- **中貢献度**: 1-10%の新規追加 → オプション
- **低貢献度**: 1%未満の新規追加 → 削除検討

### 出力ファイル

**check_search_lines.py**:
- `{project_dir}/log/search_lines_results_{YYYYMMDD_HHMMSS}.md`

**check_block_overlap.py**:
- `{project_dir}/log/block_overlap_{YYYYMMDD_HHMMSS}.md`
- または指定した出力パス

---

## プロンプト例

### 各行の件数確認
```
User: PPSプロジェクトの各キーワードの件数を調べて

Claude: term-counterスキルを実行します。
[projects/pps/search_formula.md を解析...]
[各行のヒット数を取得中...]
[結果を表示]
```

### ブロック重複分析 (方法1: ブロックテキスト直接提供)
```
User: このブロックの重複を分析して:
#### #2A Population
"Physicians"[Mesh] OR
"Health Personnel"[Mesh] OR
"Nurses"[Mesh]

Claude: term-counterスキルを重複分析モードで実行します。
[ブロック "#2A Population" を分析中...]
[結果を表示]
```

### ブロック重複分析 (方法2: ファイルから抽出)
```
User: PPSのPopulationブロックの重複をチェック

Claude: term-counterスキルを重複分析モードで実行します。
[projects/pps/search_formula.md から "Population" ブロックを抽出...]
[重複分析中...]
[結果を表示]
```

---

## 実装時の注意事項

1. **モード自動判定**:
   - "各行" / "全体" / "ヒット数" → `mode = "lines"`
   - "重複" / "overlap" / "貢献度" → `mode = "overlap"`

2. **ブロック抽出**:
   - ユーザーがブロックテキストを提供 → 直接使用
   - ブロック名のみ指定 → search_formula.mdから該当セクションを抽出

3. **数値フォーマット**:
   - 3桁カンマ区切り (1,234件)
   - パーセント表示 (12.3%)

4. **貢献率の計算**:
   - 新規追加件数 / 累積総ヒット数 × 100

5. **次のステップ提案**:
   - 低貢献度検索語あり → 削除を提案
   - 高重複あり → 上位概念のみ使用を提案
   - 最適化案作成後 → search-validatorで再検証を提案

6. **出力ファイルの組織化**:
   - タイムスタンプ付きファイル名で履歴管理
   - 一時ファイル (.txt) は .gitignore 対象
   - レポート (.md) はコミット推奨

---

## 関連スキル

- **search-validator**: 検索式全体の検証
- **mesh-analyzer**: MeSH termの階層・重複分析
- **database-converter**: 最適化後の検索式を他DB形式に変換

## 参考リンク

- [PubMed E-utilities API](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- [NCBI API Keys](https://www.ncbi.nlm.nih.gov/account/)

## 使用例の詳細

### 例1: 各行の件数確認の典型的なワークフロー

```
1. User: "PPSの検索式で各キーワードの件数を確認"

2. Claude (term-counter skill実行):
   - projects/pps/search_formula.md を読み込み
   - 各行 (#1, #2, #3...) を抽出
   - PubMed APIで個別にヒット数取得
   - 結果をテーブル形式で表示

3. User: "#3のキーワードが多すぎる。どうすべき?"

4. Claude: "term-counterの重複分析モードで、#3を含むブロックを分析しましょう"
   - (重複分析モードに切り替え)
```

### 例2: ブロック重複分析の典型的なワークフロー

```
1. User: "Populationブロックの各検索語がどれくらい貢献しているか知りたい"

2. Claude (term-counter skill - overlap mode):
   - search_formula.md から "Population" ブロックを抽出
   - 各検索語の個別ヒット数取得
   - 累積OR演算で新規追加件数を計算
   - 貢献率を算出
   - 最適化案を提示

3. User: "オプション2で試してみたい"

4. Claude: "search_formula.md を更新して、search-validatorで検証しましょう"
   - (search_formula.md編集 → search-validator実行)
```
