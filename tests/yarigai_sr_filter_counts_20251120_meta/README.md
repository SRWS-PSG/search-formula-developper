# tests/yarigai_sr_filter_counts_20251120_meta

HSLS LibGuides Ovid MEDLINE Systematic Review フィルターと #2 Concept Block を掛け合わせた件数を取得するための補助フォルダー。

## ファイル一覧
- `run_sr_filtered_counts.py` — PubMed API から全期間／5年／3年のヒット数を取得し、Markdownレポートを生成するスクリプト
- `plan_sr_filter_counts_20251110.md` — 旧フォルダーからのコピー（更新予定）
- `sr_filtered_counts_20251120_hsls.md` — スクリプト実行後に生成されるレポート（HSLSフィルター版）

## 使い方
```bash
python tests/yarigai_sr_filter_counts_20251120_meta/run_sr_filtered_counts.py
```
出力は同フォルダー内の `sr_filtered_counts_20251120_hsls.md` に保存される。ブロック行ごとのテーブルは生成しない。
