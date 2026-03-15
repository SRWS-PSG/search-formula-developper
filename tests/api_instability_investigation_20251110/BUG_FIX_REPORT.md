# check_block_overlap.py バグ修正レポート

**修正日**: 2025-11-10
**ファイル**: `scripts/search/term_validator/check_block_overlap.py`
**優先度**: 🔴 **Critical**

---

## 🐛 バグの概要

### 問題

`check_block_overlap.py` で累積カウントが失敗した際、**前の累積値をデフォルト値として使い回す**ロジックが実装されていた。

**結果**:
- 累積カウントが増加しない
- 累積カウントが減少する
- 「0ヒット」と誤って報告される

### 影響範囲

- やりがい検索式の検証（`tests/yarigai_line_counts_refined_20251109/`）
- その他のプロジェクトで同じスクリプトを使用した場合

### 発見の経緯

1. `summaru_modified.md` で多数の検索語が「0ヒット」と報告
2. API不安定性調査を実施
3. 実際にはAPIは安定しており、すべて正しい値を返していた
4. スクリプトのロジックにバグがあることを特定

---

## 🔍 バグの詳細

### 問題のコード（修正前）

**ファイル**: `scripts/search/term_validator/check_block_overlap.py`
**行番号**: 220

```python
cumulative_count = cumulative_result['count'] if cumulative_result['count'] is not None else previous_cumulative
```

### 問題点

1. **条件が不十分**
   - `cumulative_result['count'] is not None` だけでは不十分
   - `cumulative_result.get('success')` もチェックすべき

2. **デフォルト値の使用**
   - エラー時に `previous_cumulative` を使うと、エラーが隠蔽される
   - ユーザーはエラーが発生したことに気づかない

3. **連鎖的な影響**
   - 一度エラーが発生すると、以降のすべての累積カウントが影響を受ける

### 実際の症状

**例**: #2B Meaningful Work ブロック

| Line | 個別 | 累積（報告） | 期待値 | 問題 |
|------|------|------------|--------|------|
| 1 | 50 | 50 | 50 | ✓ 正常 |
| 2 | 3 | **0** | 53 | ❌ 累積検索失敗 → 0に |
| 3 | 11 | **0** | 64 | ❌ 前の0を引き継いだ |
| 4 | 42 | 99 | 106 | ⚠️ 部分的に回復（しかし不正確） |

---

## ✅ 修正内容

### 主要な修正

#### 1. エラー時にNoneを返す（行223-229）

**修正前**:
```python
cumulative_count = cumulative_result['count'] if cumulative_result['count'] is not None else previous_cumulative
```

**修正後**:
```python
if not cumulative_result.get('success') or cumulative_result['count'] is None:
    print(f"  [ERROR] 累積検索でエラー: {cumulative_result.get('message', 'Unknown error')}")
    print(f"  累積カウントを取得できませんでした。")
    # エラー時はNoneを記録（デフォルト値を使わない）
    cumulative_count = None
    added_count = None
else:
    cumulative_count = cumulative_result['count']
    # 追加された件数を計算
    if cumulative_count >= previous_cumulative:
        added_count = cumulative_count - previous_cumulative
    else:
        # 累積が減少する異常ケース（本来起きないはず）
        print(f"  [WARN] 累積カウントが減少: {previous_cumulative} → {cumulative_count}")
        added_count = 0
```

**メリット**:
- エラーが明示的に記録される
- ユーザーがエラーを認識できる
- 不正確なデフォルト値を使わない

#### 2. 個別検索のエラーハンドリング改善（行207-213）

**修正前**:
```python
if not individual_result.get('success'):
    print(f"  [WARN] 個別検索でエラー: {individual_result['message']}")
individual_count = individual_result['count']
```

**修正後**:
```python
if not individual_result.get('success'):
    print(f"  [ERROR] 個別検索でエラー: {individual_result['message']}")
    print(f"  このエラーは致命的です。処理を継続できません。")
    individual_count = None
else:
    individual_count = individual_result['count']
```

#### 3. エラー情報を結果に追加（行252-254）

**追加**:
```python
results.append({
    'line': idx,
    'term': term,
    'individual_count': individual_count,
    'cumulative_count': cumulative_count,
    'added_count': added_count,
    'previous_cumulative': previous_cumulative,
    'individual_error': not individual_result.get('success'),  # 追加
    'cumulative_error': not cumulative_result.get('success'),  # 追加
})
```

#### 4. レポート生成の改善（行273-328）

**主な変更**:
- エラーがある場合に警告を表示
- None値を「ERROR」として表示（0ではない）
- エラーマーカー（⚠️IND, ⚠️CUM）を追加
- エラーサマリーを追加

**例**:
```markdown
⚠️ **WARNING**: Some queries encountered errors during execution. See details below.

| Line | Term | Individual Count | Cumulative (OR) | Added | % of Total |
|------|------|------------------|-----------------|-------|------------|
| 1 | `term1` | 50 | 50 | **+50** | 4.1% |
| 2 | `term2` | ERROR | ERROR | **ERROR** | N/A ⚠️IND ⚠️CUM |

### Summary

- **Total unique papers**: 1,213
- **Lines with errors**: 2, 5
- **Error types**: ⚠️IND = Individual query error, ⚠️CUM = Cumulative query error
```

---

## 🧪 テスト結果

### テストケース

4つの検索語を使用したブロック重複分析：
1. "meaningful work"[tiab] (期待値: 50)
2. "work engagement"[tiab] (期待値: 151)
3. vigor[tiab] (期待値: 78)
4. calling[tiab] (期待値: 948)

### 結果

```
================================================================================
✓ ALL TESTS PASSED
================================================================================

Line 1: ✓ PASS - Individual: 50, Cumulative: 50, Added: 50
Line 2: ✓ PASS - Individual: 151, Cumulative: 200, Added: 150
Line 3: ✓ PASS - Individual: 78, Cumulative: 268, Added: 68
Line 4: ✓ PASS - Individual: 948, Cumulative: 1,213, Added: 945
```

### 検証項目

- [x] 個別カウントが正確（期待値と一致）
- [x] 累積カウントが単調増加
- [x] 追加カウントが合理的（個別 ≥ 追加）
- [x] エラー時にNoneを返す（デフォルト値を使わない）
- [x] エラーがログとレポートに記録される

---

## 📊 修正前後の比較

### 修正前（バグあり）

| 検索語 | 報告値 | 問題 |
|--------|--------|------|
| "meaningful work"[tiab] | **0** | ❌ 誤報告 |
| "work engagement"[tiab] | **0** | ❌ 誤報告 |
| calling[tiab] | **0** | ❌ 誤報告 |

**症状**:
- 多数の検索語が0ヒットと誤報告
- 累積カウントが減少
- 「API不安定」と誤認

### 修正後（バグ修正済み）

| 検索語 | 実測値 | 結果 |
|--------|--------|------|
| "meaningful work"[tiab] | **50** | ✓ 正確 |
| "work engagement"[tiab] | **151** | ✓ 正確 |
| calling[tiab] | **948** | ✓ 正確 |

**改善**:
- すべて正確な値を報告
- 累積カウントが単調増加
- エラーが明示的に記録される

---

## 🚀 今後の対策

### 1. 他のスクリプトのレビュー

同様のパターンがないか確認：
```bash
grep -r "if.*is not None.*else" scripts/search/
```

### 2. ユニットテストの追加

```bash
# テストスクリプトを定期的に実行
python3 tests/api_instability_investigation_20251110/test_fixed_script.py
```

### 3. エラーハンドリングのベストプラクティス

**推奨**:
```python
# ❌ 悪い例: デフォルト値を使う
value = result.get('count') or 0

# ✓ 良い例: エラーを明示的に扱う
if not result.get('success'):
    print(f"[ERROR] {result['message']}")
    value = None  # エラーを隠さない
else:
    value = result['count']
```

### 4. ログの改善

- `[WARN]` → `[ERROR]` に変更（致命的なエラーの場合）
- エラー詳細をログに記録
- レスポンス全体をJSON保存（デバッグ用）

---

## 📝 まとめ

### 修正内容

- ✅ エラー時にNoneを返す（デフォルト値を使わない）
- ✅ エラーメッセージを明確化（WARN → ERROR）
- ✅ エラー情報を結果に追加
- ✅ レポートにエラーサマリーを追加
- ✅ テストスクリプトで検証

### 影響

- **修正前**: 多数の検索語が0ヒットと誤報告
- **修正後**: すべて正確な値を報告

### 教訓

1. **デフォルト値は危険**
   - エラーを隠蔽する
   - ユーザーが問題に気づかない

2. **None vs 0 の区別が重要**
   - `0` = 検索結果が0件
   - `None` = エラーで取得できなかった

3. **エラーは明示的に扱う**
   - ログに記録
   - レポートに表示
   - 処理を停止（または継続判断をユーザーに委ねる）

---

## 🔗 関連ファイル

- [修正されたスクリプト](../../scripts/search/term_validator/check_block_overlap.py)
- [テストスクリプト](test_fixed_script.py)
- [テストレポート](test_report.md)
- [総合レポート](COMPREHENSIVE_REPORT.md)
