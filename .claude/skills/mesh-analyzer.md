# MeSH Analyzer Skill

このスキルは、seed paperからMeSH termsを抽出し、階層構造を分析して、検索式の最適化を支援します。

## 発動条件

ユーザーが以下のような自然言語で要求した場合に、このスキルを実行してください:

- 「MeSHを抽出して」
- 「MeSH termsを分析」
- 「MeSH階層を調べて」
- 「seed paperのMeSHを確認」
- 「MeSHツリーを生成」
- 「MeSH termの重複をチェック」
- 「このMeSH termが有効か確認」

## 入力パラメータ

### パターン1: Seed paperからMeSH抽出
- **project_dir**: プロジェクトディレクトリのパス (例: `projects/pps/`)
- 自動検出ファイル: `seed_pmids.txt`

### パターン2: 特定のMeSH termを検証
- **terms**: カンマ区切りのMeSH term一覧 (例: "Physicians, Burnout Professional")

### パターン3: MeSH termの重複分析
- **terms**: カンマ区切りのMeSH term一覧
- **mode**: `overlap` (重複分析モード)

## 実行モード

### モード1: MeSH抽出と階層分析 (extract_mesh.py)

**発動例**:
- "PPSプロジェクトのMeSHを抽出"
- "seed paperからMeSH termsを取得"

**実行手順**:

1. プロジェクトディレクトリ確認
```python
import os

project_dir = "projects/{project_name}/"
pmid_file = os.path.join(project_dir, "seed_pmids.txt")

if not os.path.exists(pmid_file):
    print(f"❌ エラー: Seed PMIDファイルが見つかりません")
    print(f"   期待されるパス: {pmid_file}")
    return
```

2. MeSH抽出スクリプト実行
```bash
python scripts/search/extract_mesh.py \
  --pmid-file {pmid_file} \
  --output-dir {project_dir}
```

3. 結果の整形と表示

**出力例**:
```markdown
## 🧬 MeSH Term抽出結果

### プロジェクト情報
- **プロジェクト**: pps
- **Seed PMID数**: 5件
- **抽出されたMeSH term数**: 45件

### 頻出MeSH Terms (全論文で出現)

#### 出現頻度: 5/5 (100%)
1. **Physicians** [M01.526.702]
   - 文献数: 234,567件
   - Major Topic: 3/5論文
   - 階層: Named Groups > Persons > Health Personnel > Physicians

2. **Burnout, Professional** [F01.145.126.100]
   - 文献数: 12,345件
   - Major Topic: 5/5論文
   - 階層: Psychiatry and Psychology > Behavioral Disciplines and Activities > Burnout, Professional

#### 出現頻度: 4/5 (80%)
3. **Occupational Stress** [F01.145.126.990.500]
   - 文献数: 23,456件
   - Major Topic: 2/5論文

### MeSH階層図
詳細なMermaid形式の階層図は以下に保存されました:
- 📄 {project_dir}/mesh_analysis.md

### 推奨される検索語
以下のMeSH termsを検索式に含めることを推奨します:
- ✅ "Burnout, Professional"[Mesh] - 全論文でMajor Topic
- ✅ "Physicians"[Mesh] - 全論文で出現
- ⚠️  "Occupational Stress"[Mesh] - 4/5論文 (オプション)

### 次のステップ
1. mesh_analysis.md で階層構造を確認
2. 検索式に推奨MeSH termsを追加
3. search-validatorで再検証
```

**生成ファイル**:
- `{project_dir}/mesh_analysis.md` - 詳細レポート (Mermaid階層図含む)
- `{project_dir}/mesh_analysis_results.json` - JSON形式の生データ

---

### モード2: MeSH term検証 (check_mesh.py)

**発動例**:
- "PhysiciansというMeSH termが有効か確認"
- "Burnout, Professional, Occupational StressのMeSHをチェック"

**実行手順**:

1. MeSH termのリストを解析
```python
# ユーザー入力から用語を抽出
terms = [term.strip() for term in user_input.split(",")]
```

2. 各termを検証
```bash
python scripts/search/mesh_analyzer/check_mesh.py --terms "{term1},{term2},{term3}"
```

**出力例**:
```markdown
## 🔍 MeSH Term検証結果

### 検証対象
- Physicians
- Burnout, Professional
- Occupational Stress

### 検証結果

#### ✅ Physicians
- **MeSH Database**: 存在する (1件)
- **PubMed文献数**: 234,567件
- **推奨度**: 高 (大量の文献で使用)

#### ✅ Burnout, Professional
- **MeSH Database**: 存在する (1件)
- **PubMed文献数**: 12,345件
- **推奨度**: 高

#### ❌ Invalid Term Example
- **MeSH Database**: 存在しない
- **エラー**: MeSH termとして登録されていません
- **提案**: PubMed MeSH Browserで正しい用語を確認してください
  - https://www.ncbi.nlm.nih.gov/mesh/

### サマリー
- ✅ 有効なMeSH terms: 2/3
- ❌ 無効なMeSH terms: 1/3
```

---

### モード3: MeSH重複分析 (check_mesh_overlap.py)

**発動例**:
- "PhysiciansとMedical Staffの重複を確認"
- "これらのMeSH termsの重複をチェック"

**実行手順**:

```bash
python scripts/search/mesh_analyzer/check_mesh_overlap.py --terms "{term1},{term2},{term3}"
```

**出力例**:
```markdown
## 🔄 MeSH Term重複分析結果

### 分析対象
- Physicians
- Medical Staff, Hospital
- Health Personnel

### 個別ヒット数
| MeSH Term | ヒット数 |
|-----------|----------|
| Physicians | 234,567件 |
| Medical Staff, Hospital | 45,678件 |
| Health Personnel | 567,890件 |

### 重複分析

#### Physicians OR Medical Staff, Hospital
- **合計ヒット数**: 256,789件
- **重複**: 23,456件 (Physiciansの10%)
- **新規追加**: 22,222件
- **判定**: ✅ 併用推奨 (新規文献が追加される)

#### Physicians OR Health Personnel
- **合計ヒット数**: 567,890件
- **重複**: 234,567件 (Physiciansの100%)
- **新規追加**: 333,323件
- **判定**: ⚠️  Health PersonnelはPhysiciansを完全に含む
  - PhysiciansはHealth Personnelの下位概念
  - Health Personnelのみ使用すれば十分

### 最適化された検索式
```
"Health Personnel"[Mesh]
```

**理由**: Health PersonnelがPhysiciansとMedical Staff, Hospitalの両方を包含

### 推奨事項
- Health Personnelのみ使用 (最大カバレッジ)
- または、より限定的にしたい場合はPhysiciansのみ使用
```

---

## エラーハンドリング

### エラーケース1: seed_pmids.txt が存在しない

```markdown
❌ エラー: Seed PMIDファイルが見つかりません

期待されるパス: {project_dir}/seed_pmids.txt

**対処方法**:
1. seed_pmids.txt を作成して、PMIDを1行に1つずつ記入
2. 例:
   ```
   12345678
   23456789
   # コメント行
   ```
```

### エラーケース2: seed_pmids.txt が空

```markdown
⚠️  警告: Seed PMIDファイルが空です

**対処方法**:
1. key papersのPMIDを追加してください
2. PMIDの探し方:
   - PubMed論文ページで確認
   - DOIからPMID検索: `python scripts/utils/find_pmid_from_doi.py --doi {doi}`
```

### エラーケース3: API rate limit超過

```markdown
❌ エラー: PubMed APIのレート制限に達しました

**対処方法**:
1. 1分ほど待ってから再実行
2. 頻繁に発生する場合:
   - NCBI API keyを取得: https://www.ncbi.nlm.nih.gov/account/
   - 環境変数に設定: `export NCBI_API_KEY=your_key_here`
```

### エラーケース4: MeSH階層の取得失敗

```markdown
⚠️  警告: 一部のMeSH termの階層情報を取得できませんでした

取得失敗: 3/45 terms

**影響**:
- 基本的なMeSH抽出は完了
- 階層図に一部の親ノードが表示されない可能性

**対処方法**:
- 時間をおいて再実行
- NCBI MeSH Browserで手動確認: https://www.ncbi.nlm.nih.gov/mesh/
```

### エラーケース5: 無効なMeSH term指定

```markdown
❌ エラー: 指定されたMeSH termが見つかりません

無効なterm: "Invalid Term Example"

**対処方法**:
1. スペルミスを確認
2. MeSH Browserで正しい用語を検索
   - https://www.ncbi.nlm.nih.gov/mesh/
3. 同義語を確認 (例: "Physician" → "Physicians")
```

---

## 技術的詳細

### 使用スクリプト
1. `scripts/search/extract_mesh.py` - MeSH抽出と階層分析
2. `scripts/search/mesh_analyzer/check_mesh.py` - MeSH term検証
3. `scripts/search/mesh_analyzer/check_mesh_overlap.py` - 重複分析

### MeSH階層の取得ロジック
1. **Paper取得**: PubMed E-utilities APIでXML取得
2. **MeSH抽出**: XMLからMeSH descriptorsとqualifiersを抽出
3. **Tree Number取得**: MeSH UIからTree Numberを取得
4. **階層構築**: Tree Numberの階層構造を解析
5. **親ノード取得**: 不明なTree Numberに対応するMeSH nameを検索
6. **Mermaid生成**: 階層図をMermaid記法で出力

### MeSH Tree Numberの例
- `M01.526.702` → Named Groups > Persons > Health Personnel > Physicians
- `F01.145.126.100` → Psychiatry and Psychology > ... > Burnout, Professional

### 出力フォーマット

**mesh_analysis.md の構造**:
```markdown
# MeSH Term分析結果

## サマリー
- 分析論文数: 5件
- 抽出されたMeSH terms: 45件
- Major Topic指定: 25件

## カテゴリ別MeSH Terms

### Category A: 解剖学 (Anatomy)
(該当termなし)

### Category F: 精神医学・心理学 (Psychiatry and Psychology)
#### Burnout, Professional [F01.145.126.100]
- 出現: 5/5論文 (100%)
- Major Topic: 5/5論文
- PubMed文献数: 12,345件

## MeSH階層図 (Mermaid)
```mermaid
graph TD
    F01[Behavior and Behavior Mechanisms]
    F01.145[Behavioral Disciplines and Activities]
    ...
```
```

---

## プロンプト例

### 基本的な使い方
```
User: PPSプロジェクトのseed paperからMeSHを抽出して

Claude: mesh-analyzerスキルを実行します。
[projects/pps/seed_pmids.txt を確認...]
[5件のPMIDからMeSH抽出中...]
[結果を表示]
```

### MeSH term検証
```
User: Physicians, Burnout Professional, Occupational StressのMeSHが有効か確認

Claude: mesh-analyzerスキルをMeSH検証モードで実行します。
[3つのMeSH termsを検証中...]
[結果を表示]
```

### 重複分析
```
User: PhysiciansとHealth Personnelの重複をチェック

Claude: mesh-analyzerスキルを重複分析モードで実行します。
[2つのMeSH termsの重複を分析中...]
[結果を表示]
```

---

## 実装時の注意事項

1. **モード自動判定**:
   - プロジェクト名のみ → MeSH抽出モード
   - MeSH term列挙 + "検証/確認" → MeSH検証モード
   - MeSH term列挙 + "重複/overlap" → 重複分析モード

2. **MeSH term正規化**:
   - ユーザー入力の大文字小文字は保持
   - カンマ区切りで複数term対応
   - クォーテーション除去 ("Physicians" → Physicians)

3. **階層図の表示制御**:
   - Mermaid図が長い場合は、ファイル保存のみ通知
   - 主要なMeSH termsのみサマリー表示

4. **API使用の効率化**:
   - extract_mesh.pyはキャッシュ機能あり (既存のJSON再利用)
   - 複数回実行しても同じPMIDは再取得しない

5. **次のステップ提案**:
   - MeSH抽出完了 → search-validatorで検索式に組み込んで検証
   - 重複発見 → より広い/狭いMeSH termの選択を提案
   - Major Topicが多いterm → 優先的に検索式に組み込み推奨

---

## 関連スキル

- **search-validator**: MeSH termを含む検索式の検証
- **term-counter**: MeSH termの個別ヒット数確認
- **project-initializer**: seed_pmids.txtの初期化

## 参考リンク

- [NCBI MeSH Browser](https://www.ncbi.nlm.nih.gov/mesh/)
- [MeSH Tree Structures](https://www.nlm.nih.gov/mesh/meshhome.html)
- [PubMed E-utilities API](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
