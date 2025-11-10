# やりがい検索式 全ブロック行ごと件数 再集計計画

**作成日**: 2025-11-10
**目的**: バグ修正後のスクリプトで全ブロックの正確な行ごと件数を取得し、1つのmdファイルにまとめる

---

## 背景

### 問題点
- `tests/yarigai_line_counts_refined_20251109/` の結果は、バグのある `check_block_overlap.py` で生成された
- 多くの検索語が「0ヒット」と誤報告された
- 累積カウントが減少する異常が報告された

### 修正内容
- `scripts/search/term_validator/check_block_overlap.py` のバグを修正（2025-11-10）
- エラー時に前の値を使わず、`None` を返すように変更
- エラーを明示的に記録・表示するように改善

### 信頼できるデータ
- `tests/yarigai_line_counts_refined_20251109/five_year_counts_2021plus.md` は正確だった
- API調査の結果、PubMed API自体は100%安定していることを確認

---

## 対象ブロック

### 1. Population（医師ブロック）
- **#1 Population (Physicians only)**
  - 入力ファイル: `search_block_population.txt`
  - 出力ファイル: `analysis_population.md`

### 2. Concept（それ以外のブロック）
- **#2A MeSH Terms**
  - 入力: `search_block_2a_mesh.txt`
  - 出力: `analysis_2a_mesh.md`

- **#2B Meaningful Work**
  - 入力: `search_block_2b_meaningful.txt`
  - 出力: `analysis_2b_meaningful.md`

- **#2C Work Engagement**
  - 入力: `search_block_2c_engagement.txt`
  - 出力: `analysis_2c_engagement.md`

- **#2D Calling/Vocation**
  - 入力: `search_block_2d_calling.txt`
  - 出力: `analysis_2d_calling.md`

- **#2E Motivation**
  - 入力: `search_block_2e_motivation.txt`
  - 出力: `analysis_2e_motivation.md`

- **#2F Satisfaction**
  - 入力: `search_block_2f_satisfaction.txt`
  - 出力: `analysis_2f_satisfaction.md`

- **#2G Fulfillment**
  - 入力: `search_block_2g_fulfillment.txt`
  - 出力: `analysis_2g_fulfillment.md`

- **#2H Japanese Concepts**
  - 入力: `search_block_2h_japanese.txt`
  - 出力: `analysis_2h_japanese.md`

- **#2I Psychological Needs**
  - 入力: `search_block_2i_needs.txt`
  - 出力: `analysis_2i_needs.md`

- **#2J Task Significance**
  - 入力: `search_block_2j_task.txt`
  - 出力: `analysis_2j_task.md`

**合計**: 11ブロック

---

## 実行手順

**選択**: オプションA（全ブロック再実行）

### Phase 1: 全ブロック再実行
1. 修正済みスクリプトで全11ブロックを再実行
2. API rate limitを考慮して各ブロック間に5秒待機
3. **個別の分析レポート（`analysis_*.md`）は生成しない**
4. すべてのデータを直接メモリに保持して統合

### Phase 2: データの統合（リアルタイム）
1. 各ブロック分析時にデータをメモリに蓄積
2. 全ブロック完了後、1つの統合レポートを生成
3. **個別の `analysis_*.md` ファイルは作成しない**

### Phase 3: 統合レポート生成
1つのmdファイルに全ブロックのデータを統合：
```markdown
# やりがい検索式 全ブロック行ごと件数レポート

生成日: YYYY-MM-DD
使用スクリプト: check_block_overlap.py (バグ修正版)

## #1 Population (Physicians only)
| Line | Term | Individual Count | Cumulative Count | Added | % of Total |
|------|------|------------------|------------------|-------|------------|
| ... | ... | ... | ... | ... | ... |

**Total**: XXX papers

## #2A MeSH Terms
| Line | Term | Individual Count | Cumulative Count | Added | % of Total |
|------|------|------------------|------------------|-------|------------|
| ... | ... | ... | ... | ... | ... |

**Total**: XXX papers

...（以下同様）
```

### Phase 4: サマリー作成
レポート末尾に以下のサマリーを追加：

1. **各ブロックの総ヒット数**
   ```markdown
   | Block | Total Hits | Notes |
   |-------|------------|-------|
   | #1 Population | XXX | - |
   | #2A MeSH | XXX | - |
   | ... | ... | ... |
   ```

2. **高価値検索語トップ10**
   - 寄与度が高い検索語をリスト

3. **低価値検索語リスト**
   - 寄与度 < 1% の検索語
   - 削除候補として検討

4. **修正が必要な検索語**
   - 以前「0ヒット」と誤報告されたが、実際はヒットがある検索語
   - 例: "job satisfaction"[tiab] (2,141件)

---

## 出力ファイル

**統合レポートのみ（1ファイル）**:
- `tests/yarigai_comprehensive_line_counts_20251110.md`
  - 全ブロックの行ごと件数統合レポート
  - サマリーと分析含む
  - **個別のブロックレポート（`analysis_*.md`）は生成しない**

---

## 推定実行時間

### オプションA（全ブロック再実行 - 統合レポートのみ生成）
- 分析実行: 15-20分
  - 11ブロック × 平均10-20行/ブロック
  - API待機時間（5秒/ブロック）: 55秒
- 統合レポート生成: 1分（メモリ内データから直接生成）
- **合計**: 約15-20分

---

## 技術的詳細

### 実装アプローチ

**新しい統合スクリプトを作成**:
- `tests/recount_all_blocks_unified.py`
- 全ブロックをループ処理
- 各ブロックの結果をメモリに蓄積
- 最後に1つの統合レポートを生成

**スクリプト構造**:
```python
# 1. 全ブロック定義を読み込み
blocks = [
    {"name": "#1 Population", "file": "search_block_population.txt"},
    {"name": "#2A MeSH", "file": "search_block_2a_mesh.txt"},
    # ... 以下同様
]

# 2. 各ブロックをループ処理
all_results = []
for block in blocks:
    results = analyze_block(block['file'], block['name'])
    all_results.append({
        'block_name': block['name'],
        'results': results
    })
    time.sleep(5)  # API rate limit対策

# 3. 統合レポート生成
generate_unified_report(all_results, output_path)
```

### 既存スクリプトの活用
```bash
# check_block_overlap.py の analyze_block_overlap() 関数を利用
# ただし、mdファイル出力は行わず、データのみ返す
```

### API制限対策
- Rate limit: 3 requests/second (API key無し)
- インターバル: 0.5秒/リクエスト（余裕を持った設定）
- ブロック間待機: 5秒
- リトライロジック: 最大5回、指数バックオフ

### エラーハンドリング
- API エラー → `None` を返す（デフォルト値を使わない）
- タイムアウト → リトライ
- HTTP 429 → 指数バックオフでリトライ
- すべてのエラーをログとレポートに記録

---

## 実行確認事項

### 実行前チェックリスト
- [ ] `check_block_overlap.py` のバグ修正が完了している
- [ ] `tests/yarigai_line_counts_refined_20251109/` に全ブロックの入力ファイル（`.txt`）が存在する
- [ ] インターネット接続が安定している
- [ ] 実行時間の余裕がある（15-25分）

### 実行後チェックリスト
- [ ] すべてのブロックで分析が成功した（エラーマーカー⚠️がない）
- [ ] 累積カウントが単調増加している
- [ ] 「0ヒット」の誤報告がない
- [ ] 統合レポートが生成された
- [ ] サマリーの数値が妥当である

---

## 次のステップ

1. **この計画を実行**
   - 全ブロックの正確な件数を取得

2. **検索式の更新**
   - 正確な件数をもとに `search_formula_editable.md` を更新
   - 「削除候補」だった検索語を復活

3. **最終検証**
   - `check_final_query.py` で総ヒット数を確認
   - Seed PMIDが100%捕捉されるか検証

4. **検索式の確定**
   - 最終版の検索式を `search_formula.md` として確定
   - 全データベース形式に変換（CENTRAL, Embase, etc.）

---

## 備考

### 既知の問題
- 以前の `summaru_modified.md` は信頼できない（バグのあるスクリプトで生成）
- `five_year_counts_2021plus.md` は正確だった

### 重要な発見
- API は100%安定（調査済み）
- すべての「0ヒット」は誤報告だった
- 特に重要: "job satisfaction"[tiab] = 2,141件（0ではない）

### 参照ドキュメント
- [バグ修正レポート](../tests/api_instability_investigation_20251110/BUG_FIX_REPORT.md)
- [調査結果](../tests/api_instability_investigation_20251110/FINDINGS.md)
- [総合レポート](../tests/api_instability_investigation_20251110/COMPREHENSIVE_REPORT.md)
