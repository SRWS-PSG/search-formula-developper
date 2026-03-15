---
description: PowerShellでPythonコードを実行する際のクォーテーション問題を回避する
---

# PowerShell + Python クォーテーション問題の回避ルール

## 問題
PowerShellでダブルクォーテーション `"` やシングルクォーテーション `'` を含むPythonコードを `python -c "..."` で実行すると、エスケープ問題でエラーになることが多い。

特に以下のケースで問題が発生しやすい：
- 検索クエリ（例: `subject:"Faculty Development"`）
- JSONデータ
- 複数行の文字列
- ネストしたクォート

## ルール

### ❌ やってはいけない
```powershell
# 複雑なクォートを含むone-liner
python -c "from module import func; print(func('subject:\"Term\"'))"
```

### ✅ 正しい方法

**1. 簡単なコード（クォートなし）のみone-linerで実行**
```powershell
# OK: シンプルなコード
python -c "print(1+1)"
python -c "from module import func; print(func(123))"
```

**2. クォートを含む場合は必ずスクリプトファイルを作成**
```python
# scripts/search/eric/test_query.py を作成
from eric_api import get_eric_record_count
query = 'subject:"Faculty Development"'
print(get_eric_record_count(query))
```

```powershell
# スクリプトを実行
python scripts/search/eric/test_query.py
```

**3. デバッグ用の汎用テストスクリプトを用意する**
プロジェクトに `scripts/debug_query.py` のようなテンプレートを用意しておき、クエリ部分だけを書き換えて使用する。

## 判断基準

| コード内容 | 推奨方法 |
|-----------|---------|
| `"` や `'` を含まない | one-liner OK |
| `"` または `'` を1つ含む | one-liner 可能だが注意 |
| `"` と `'` を両方含む | **必ずスクリプトファイル** |
| 複数行のロジック | **必ずスクリプトファイル** |

## メリット
1. クォーテーションエスケープのデバッグ時間を節約
2. コードが読みやすく、再利用しやすい
3. 結果をファイルに保存しやすい
4. Git履歴に残せる
