# tests/yarigai_sr_filter_counts_20251110

Systematic Reviewフィルター（`templates/SR_filter.md`）と #2 Concept Block 統合クエリを掛け合わせた件数を取得するための補助フォルダー。

## ファイル一覧
- `run_sr_filtered_counts.py` — PubMed API から全期間／5年／3年のヒット数を取得し、Markdownレポートを生成するスクリプト
- `plan_sr_filter_counts_20251110.md` — 実行計画と検証手順
- `sr_filtered_counts_20251110.md` — スクリプト実行後に生成されるレポート（まだ未作成の場合あり）

## 使い方
```bash
python tests/yarigai_sr_filter_counts_20251110/run_sr_filtered_counts.py
```
出力は同フォルダー内の `sr_filtered_counts_20251110.md` に保存される。今回はブロック行ごとのテーブルは生成しない。
