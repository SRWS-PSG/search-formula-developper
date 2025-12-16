# SRフィルター併用テスト計画（2025-11-10）

## 目的
- `tests/yarigai_comprehensive_line_counts_20251110.md` で用いた #2 Concept Block（医師×やりがい関連語 46行OR）に対し、`templates/SR_filter.md` の Systematic Review フィルターを AND で適用したヒット数（全期間／5年／3年）を取得する
- 個別行単位のテーブルは生成せず、統合カウントのみを確認する

## 入力ソース
- コンセプトクエリ: `run_sr_filtered_counts.py` 内の `FULL_CONCEPT_QUERY`
- SRフィルター: `templates/SR_filter.md`（説明文＋フィルター本体＋参照URL。スクリプトでクエリ段落のみ抽出）

## 出力
1. `tests/yarigai_sr_filter_counts_20251110/sr_filtered_counts_20251110.md`
   - 期間別ヒット数表（全期間／5年／3年）
   - 使用クエリ概要とSRフィルター全文
   - 行別ブロック表は含めない
2. ターミナルログ
   - PubMed API 呼び出しごとのヒット数

## 実行手順
1. **準備**
   - `.env` もしくは環境変数で `NCBI_API_KEY`, `NCBI_EMAIL`, `NCBI_TOOL`（任意）を設定してAPI制限を緩和
   - `templates/SR_filter.md` のフォーマット（説明文→注意書き→クエリ→URL）が崩れていないか確認
2. **スクリプト実行**
   ```bash
   python tests/yarigai_sr_filter_counts_20251110/run_sr_filtered_counts.py
   ```
   - 3回（全期間・5年・3年）の `get_pubmed_count` を順次実行
   - レート制限は `check_block_overlap.py` に準拠
3. **結果確認**
   - `sr_filtered_counts_20251110.md` を開き、ヒット数が `NA` ではなく数値で出力されていることを確認
   - 必要に応じて同ファイル内のクエリ抜粋をコピーし、PubMed UIでスポットチェック

## 検証チェックリスト
- [ ] Markdownに全3期間の値が記録されている
- [ ] SRフィルター全文が添付されている
- [ ] ブロック行テーブルが出力されていない（要件準拠）
- [ ] エラー時は再実行し、APIレスポンスの安定性を確認

## 所要時間（目安）
- 入力確認: 2分
- スクリプト実行: 5〜10分（APIレスポンスに依存）
- 結果確認: 3分
