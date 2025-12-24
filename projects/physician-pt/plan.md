# physician-pt: PubMed検索式 作成計画

## 目的（memo.mdを要約）
- 医師とリハビリテーション専門職（PT/OT/ST等）が関与する患者ケアにおける「多職種協働」を対象に、協働を妨げる要因（barriers）と、障壁の理解に用いられた理論的枠組み（theoretical frameworks）を扱うレビューをPubMedで同定する。
- まずは **Interdisciplinary（= interprofessional / multidisciplinary / teamwork）** と **Barriers（+ facilitators / determinants / frameworks）** の2ブロックで検索式を組む。

## 前提
- 使うDB: PubMedのみ（NCBI E-utilities API）
- まずは感度優先（NOTや過度な限定は入れない）
- 「医師＋リハ専門職が両方含まれる」「教育機関のみの文脈は除外」などの条件は、原則スクリーニングで担保（必要なら後述の追加ブロックで絞る）

## 作業手順（PubMed APIで反復）
1. Seed PMIDsを整備する
   - `projects/physician-pt/seed_pmids.txt` を作り、memo.mdのキー論文PMIDを入れる（まずは“落とさない”ことを最優先の評価軸にする）。
2. 2ブロックの初期検索式を作る
   - `projects/physician-pt/search_formula_validation.md` に `#1`（Interdisciplinary）と `#2`（Barriers）を定義し、`#3 #1 AND #2` を最終式にする。
3. ブロック別ヒット数を確認する（感度/ノイズの把握）
   - 実行: `python scripts/search/term_validator/check_search_lines.py -i projects/physician-pt/search_formula_validation.md -o projects/physician-pt/log/search_lines_YYYYMMDD.md`
4. Seed capture（キー論文の捕捉）を確認する（最重要）
   - 実行: `python scripts/search/query_executor/check_final_query.py --formula-file projects/physician-pt/search_formula_validation.md --pmid-file projects/physician-pt/seed_pmids.txt --output-dir projects/physician-pt/log`
5. 改善を回す
   - Seedが落ちる場合: 落ちたPMIDを確認し、そこに出てくる語（MeSH/tiab）を追加して再検証。
   - ヒットが多すぎる場合（例: >数千〜数万）: 追加ブロックを検討し、追加後も seed capture を維持できるか確認する。
6. 最終成果物を整える
   - 人間向けの説明用として `projects/physician-pt/search_formula.md`（作成日、ブロックの意図、最終クエリ、検証結果）を整備する。

## 追加ブロック案（必要な場合のみ）
- **レビュー限定（任意）**: `review[pt] OR systematic review[pt] OR meta-analysis[pt] OR "scoping review"[tiab] OR "systematic review"[tiab]`
- **職種限定（任意）**: `("Physicians"[Mesh] OR physician*[tiab] OR doctor*[tiab]) AND ("Physical Therapists"[Mesh] OR "Occupational Therapists"[Mesh] OR "Speech-Language Pathology"[Mesh] OR physiotherapist*[tiab] OR "physical therapist*"[tiab] OR "occupational therapist*"[tiab] OR "speech therapist*"[tiab])`

## 現在のドラフト（2ブロック）
- 機械検証用の式は `projects/physician-pt/search_formula_validation.md` に置く（このファイルを起点に改訂していく）。

## 実施結果（2025-02-14）
- ブロック調整後の最終式で seed 5/5 捕捉
- 最終ヒット数: 135,818
- 記録: `projects/physician-pt/log/search_lines_20250214_v2.md`
