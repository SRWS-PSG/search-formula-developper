# ERIC Searcher Skill

このスキルは、ERIC (Education Resources Information Center) 教育データベースの検索とシソーラス用語の確認を行います。

## 発動条件

ユーザーが以下のような自然言語で要求した場合に、このスキルを実行してください:

- 「ERICで検索」
- 「ERIC databaseを検索して」
- 「ERICシソーラスを確認」
- 「ERIC thesaurusで検証」
- 「教育データベースを検索」
- 「medical educationをERICで調べて」

## 入力パラメータ

### パターン1: ERIC検索
- **query**: 検索クエリ (例: "medical education", "faculty development")
- **filters** (オプション):
  - `peer_reviewed`: Peer-reviewedのみ (デフォルト: False)
  - `year_min`: 最小出版年 (例: 2020)
  - `year_max`: 最大出版年 (例: 2025)
  - `fulltext`: Full text利用可能のみ (デフォルト: False)
  - `ies_funded`: IES助成研究のみ (デフォルト: False)
  - `wwc_reviewed`: WWCレビュー済み ("y", "r", "n")
- **output_format** (オプション): `count_only` | `summary` | `ris` (デフォルト: summary)

### パターン2: ERICシソーラス検証
- **term**: シソーラス用語 (例: "Medical School Faculty")
- **mode**: `thesaurus` (シソーラス確認モード)
- **build_query**: 関連語を含む検索式を生成 (デフォルト: False)

## 実行モード

### モード1: ERIC検索 (search_eric.py)

**発動例**:
- "ERICでmedical educationを検索"
- "faculty developmentをERICで調べて、peer-reviewedのみ"

**実行手順**:

1. クエリとフィルターの解析
```python
query = "medical education"
filters = {
    "peer_reviewed": True,  # ユーザーが "peer-reviewed" を指定
    "year_min": 2020,        # ユーザーが "2020年以降" を指定
}
```

2. ERIC検索スクリプト実行

**件数のみ確認**:
```bash
python scripts/search/eric/search_eric.py \
  --query "{query}" \
  --count-only \
  --peer-reviewed \
  --year-min {year_min}
```

**サマリー表示**:
```bash
python scripts/search/eric/search_eric.py \
  --query "{query}" \
  --rows 20 \
  --peer-reviewed \
  --year-min {year_min}
```

**RIS出力**:
```bash
python scripts/search/eric/search_eric.py \
  --query "{query}" \
  --output {output_file} \
  --peer-reviewed \
  --year-min {year_min}
```

3. 結果の整形と表示

**出力例 (件数のみ)**:
```markdown
## 🔍 ERIC検索結果

### 検索情報
- **クエリ**: `medical education`
- **フィルター**:
  - ✅ Peer-reviewed のみ
  - 📅 出版年: 2020年以降

### 検索結果
- **総ヒット数**: 1,234件

### 次のステップ
- 結果を詳しく見る場合: `--rows 50` で再実行
- RIS形式でエクスポート: `--output results.ris`
```

**出力例 (サマリー表示)**:
```markdown
## 🔍 ERIC検索結果

### 検索情報
- **クエリ**: `medical education`
- **総ヒット数**: 1,234件
- **表示件数**: 20件

### トップ結果

#### 1. Faculty Development Programs in Medical Education: A Systematic Review
- **著者**: Smith, J., Johnson, A.
- **出版年**: 2023
- **ERIC ID**: EJ1234567
- **シソーラス**: Medical School Faculty, Faculty Development, Medical Education
- **抄録**: This systematic review examines faculty development programs...

#### 2. Burnout Among Medical School Faculty: Prevalence and Interventions
- **著者**: Brown, K., Lee, M.
- **出版年**: 2022
- **ERIC ID**: EJ2345678
- **シソーラス**: Medical School Faculty, Burnout, Occupational Stress
- **抄録**: This study investigates the prevalence of burnout...

(以下、18件省略)

### 詳細レポート
- 📄 全結果をRIS形式でエクスポートする場合:
  ```bash
  python scripts/search/eric/search_eric.py -q "medical education" -o results.ris
  ```
```

**出力例 (RIS出力)**:
```markdown
## 📥 ERIC検索結果エクスポート完了

### 検索情報
- **クエリ**: `medical education`
- **総ヒット数**: 1,234件
- **出力ファイル**: [projects/current/eric_results.ris](projects/current/eric_results.ris)

### 次のステップ
1. RISファイルをRayyanやEndNoteにインポート
2. タイトル・抄録スクリーニング実施
3. 必要に応じて検索式を調整
```

---

### モード2: ERICシソーラス確認 (check_eric_thesaurus.py)

**発動例**:
- "Medical School FacultyがERICシソーラスに存在するか確認"
- "Faculty DevelopmentのERIC thesaurusを調べて"

**実行手順**:

1. シソーラス用語の検証
```bash
python scripts/search/eric/check_eric_thesaurus.py \
  --term "{term}"
```

2. 関連語を含む検索式生成 (オプション)
```bash
python scripts/search/eric/check_eric_thesaurus.py \
  --term "{term}" \
  --build-query
```

3. 結果の整形と表示

**出力例 (用語確認)**:
```markdown
## 📚 ERICシソーラス確認結果

### 用語情報
- **検索用語**: Medical School Faculty
- **ステータス**: ✅ ERICシソーラスに登録されています

### シソーラス詳細

#### カテゴリ
- **Descriptor**: Medical School Faculty
- **Scope Note**: Faculty members employed by medical schools to teach, conduct research, and provide clinical services.

#### 関連語 (Related Terms)
- Faculty (broader)
- Medical Schools (related)
- Medical Education (related)
- Clinical Faculty (narrower)
- Preclinical Faculty (narrower)

#### 使用統計
- **ERIC内の文献数**: 3,456件
- **追加された年**: 1966

### 検索での使用例
```
subject:"Medical School Faculty"
```

### 推奨事項
- ✅ このシソーラス用語をメインクエリとして使用可能
- 関連語も検索に含める場合、下記の検索式生成を参照
```

**出力例 (検索式生成)**:
```markdown
## 🔧 ERIC検索式生成結果

### 基本用語
- **メイン用語**: Faculty Development

### 生成された検索式

#### オプション1: メイン用語のみ
```
subject:"Faculty Development"
```
- **推定ヒット数**: ~2,500件

#### オプション2: 関連語を含む (高感度)
```
subject:"Faculty Development" OR subject:"Professional Development" OR subject:"Staff Development"
```
- **推定ヒット数**: ~5,000件
- **理由**: 関連するシソーラス用語を網羅

#### オプション3: フリーワードも含む (最高感度)
```
(subject:"Faculty Development" OR subject:"Professional Development") OR (faculty AND development)
```
- **推定ヒット数**: ~8,000件
- **理由**: シソーラス + フリーワード

### 推奨
✅ **オプション2** を推奨します

**理由**:
- 高い感度を維持しながら、シソーラス統制語で精度を確保
- 関連する概念を包括的にカバー

### 次のステップ
1. eric-searcherスキルで実際に検索実行
2. ヒット数を確認して、必要に応じてオプション調整
```

---

## ERIC検索の高度な機能

### 1. シソーラス + フリーワード複合検索

**例**: "Medical School Faculty (シソーラス) + burnout (フリーワード)"

```bash
python scripts/search/eric/search_eric.py \
  --query 'subject:"Medical School Faculty" AND burnout' \
  --count-only
```

**Claude Codeでの実行**:
```
User: ERICでMedical School Facultyのシソーラスとburnoutのフリーワードで検索

Claude: eric-searcherスキルを実行します。
クエリ: subject:"Medical School Faculty" AND burnout
[検索中...]
```

### 2. 複数フィルターの組み合わせ

**例**: "Peer-reviewed + 2020年以降 + Full text利用可能"

```bash
python scripts/search/eric/search_eric.py \
  --query "faculty development" \
  --peer-reviewed \
  --year-min 2020 \
  --fulltext \
  --count-only
```

### 3. WWC (What Works Clearinghouse) レビュー済み

**WWCレベル**:
- `y` - Meets Standards (基準を満たす)
- `r` - Meets Standards with Reservations (条件付きで基準を満たす)
- `n` - Does Not Meet Standards (基準を満たさない)

```bash
python scripts/search/eric/search_eric.py \
  --query "reading intervention" \
  --wwc-reviewed y \
  --count-only
```

### 4. IES助成研究のみ

```bash
python scripts/search/eric/search_eric.py \
  --query "reading" \
  --ies-funded \
  --count-only
```

---

## エラーハンドリング

### エラーケース1: ERIC APIアクセスエラー

```markdown
❌ エラー: ERIC APIにアクセスできませんでした

**対処方法**:
1. インターネット接続を確認
2. 少し時間をおいて再試行
3. ERIC API が一時的にダウンしている可能性 (https://eric.ed.gov/)
```

### エラーケース2: シソーラス用語が見つからない

```markdown
❌ エラー: 指定されたシソーラス用語が見つかりません

検索用語: "{term}"

**対処方法**:
1. スペルミスを確認
2. ERICシソーラスブラウザで検索:
   - https://eric.ed.gov/?ti=all
3. 類似の用語を検索:
   - 例: "Faculty" → "Medical School Faculty"
   - 例: "Burnout" → "Occupational Stress" (ERICではBurnoutは登録なし)
```

### エラーケース3: 検索結果が0件

```markdown
⚠️  警告: 検索結果が0件です

**原因の可能性**:
1. フィルターが厳しすぎる (peer-reviewed + year range + fulltext)
2. シソーラス用語が適切でない
3. 検索クエリの構文エラー

**対処方法**:
1. フィルターを緩和して再検索
2. フリーワード検索で試してみる
3. シソーラス用語を再確認
```

### エラーケース4: RISファイル出力失敗

```markdown
❌ エラー: RISファイルを保存できませんでした

**対処方法**:
1. 出力ディレクトリの書き込み権限を確認
2. ディスク容量を確認
3. 別のディレクトリを指定して再実行
```

---

## 技術的詳細

### 使用スクリプト
1. `scripts/search/eric/search_eric.py` - ERIC検索
2. `scripts/search/eric/check_eric_thesaurus.py` - シソーラス確認
3. `scripts/search/eric/eric_api.py` - ERIC API client (内部)
4. `scripts/search/eric/eric_thesaurus.py` - シソーラススクレイパー (内部)

### ERIC API仕様

**ベースURL**: `https://api.ies.ed.gov/eric/`

**主要パラメータ**:
- `search`: 検索クエリ
- `format`: レスポンス形式 (json, xml, csv)
- `start`: 開始レコード番号
- `rows`: 取得件数 (最大2000)
- `fields`: 取得フィールド

**フィルターパラメータ**:
- `fq=peerreviewed:T` - Peer-reviewed
- `fq=publicationdateyear:[2020 TO 2025]` - 年代範囲
- `fq=e_fulltextauth:Y` - Full text利用可能
- `fq=iesgrantcontractnum:*` - IES助成
- `fq=e_wwcreviewstatus:{y|r|n}` - WWCレビュー

### ERICシソーラス構造

**Descriptor (統制語)**:
- ERIC独自のシソーラス用語
- 階層構造あり (broader, narrower, related)
- Scope Noteで用語の定義を提供

**検索構文**:
- `subject:"Term"` - シソーラス検索 (完全一致)
- `title:"Term"` - タイトル検索
- `author:"Name"` - 著者検索
- `AND`, `OR`, `NOT` - 論理演算子

### RIS出力フォーマット

```ris
TY  - JOUR
TI  - Faculty Development Programs in Medical Education
AU  - Smith, John
PY  - 2023
AB  - This systematic review examines...
UR  - https://eric.ed.gov/?id=EJ1234567
ID  - EJ1234567
ER  -
```

---

## プロンプト例

### 基本検索
```
User: ERICでmedical educationを検索して

Claude: eric-searcherスキルを実行します。
クエリ: "medical education"
[検索中...]
[結果を表示]
```

### フィルター付き検索
```
User: faculty developmentをERICで検索、peer-reviewedのみ、2020年以降

Claude: eric-searcherスキルを実行します。
クエリ: "faculty development"
フィルター: peer-reviewed, 2020年以降
[検索中...]
```

### シソーラス確認
```
User: Medical School FacultyがERICシソーラスに存在するか確認

Claude: eric-searcherスキルをシソーラス確認モードで実行します。
用語: "Medical School Faculty"
[確認中...]
```

### 検索式生成
```
User: Faculty DevelopmentのERIC検索式を関連語も含めて生成

Claude: eric-searcherスキルを検索式生成モードで実行します。
用語: "Faculty Development"
[関連語を取得中...]
[検索式を生成...]
```

---

## 実装時の注意事項

1. **クエリ構文の自動判定**:
   - ユーザーが `subject:` を明示 → そのまま使用
   - シソーラス用語と判定 → `subject:"Term"` に変換
   - フリーワード → そのまま使用

2. **フィルターの自動適用**:
   - "peer-reviewed" / "査読済み" → `--peer-reviewed`
   - "2020年以降" / "since 2020" → `--year-min 2020`
   - "full text" → `--fulltext`

3. **出力形式の判定**:
   - "件数だけ" / "count" → `--count-only`
   - "詳細" / "summary" → `--rows 20`
   - "エクスポート" / "RIS" → `--output {file}.ris`

4. **ERICとPubMedの違いを説明**:
   - ERIC: 教育分野専門
   - PubMed: 医学・生命科学専門
   - 医学教育は両方に関連 → 両方検索を推奨

5. **次のステップ提案**:
   - ERIC検索完了 → PubMed検索も提案
   - シソーラス確認完了 → 実際の検索を提案
   - 検索式生成完了 → 実際に検索実行を提案

---

## 関連スキル

- **search-validator**: PubMed検索式の検証
- **mesh-analyzer**: PubMed MeSH term分析 (ERICシソーラスとは異なる)
- **database-converter**: データベース形式変換 (ERICは未対応)

## 参考リンク

- [ERIC Official Site](https://eric.ed.gov/)
- [ERIC Thesaurus Browser](https://eric.ed.gov/?ti=all)
- [ERIC API Documentation](https://ies.ed.gov/ncee/projects/eric/api.asp)
- [What Works Clearinghouse](https://ies.ed.gov/ncee/wwc/)

## ERIC検索の特徴

### PubMedとの違い

| 項目 | ERIC | PubMed |
|------|------|--------|
| 専門分野 | 教育学 | 医学・生命科学 |
| 統制語彙 | ERICシソーラス | MeSH |
| 文献タイプ | 論文、報告書、会議録 | 主に学術論文 |
| Peer-review | 一部のみ | 大部分 |
| 対象地域 | 主に米国 | 国際的 |

### 医学教育研究での活用

**ERICとPubMedの併用を推奨**:
- ERIC: 教育手法、カリキュラム、教員開発
- PubMed: 臨床教育、医学的アウトカム、健康関連

**検索戦略**:
1. PubMedで医学的観点から検索
2. ERICで教育的観点から検索
3. 結果を統合してスクリーニング
