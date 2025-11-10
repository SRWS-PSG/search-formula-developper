# PubMed API不安定性調査

**作成日**: 2025-11-10
**目的**: やりがい検索式検証で観測されたAPI不安定性の根本原因を特定する

## 背景

`tests/yarigai_line_counts_refined_20251109/` での検証で以下の問題が発生：

- 個別ヒット数が0と表示される（実際にはヒットしている可能性）
- 累積カウントが前の行より減少（マイナスの追加数）
- 一部のブロックで正常、他のブロックで異常

## ファイル構成

```
api_instability_investigation_20251110/
├── README.md (このファイル)
├── investigation_plan.md (詳細な調査計画書)
├── experiment_3a_response_logging.py (実験3A: APIレスポンス構造の詳細ログ)
├── experiment_6a_manual_crosscheck.py (実験6A: 0ヒットの手動クロスチェック)
├── experiment_1a_query_complexity.py (実験1A: クエリ複雑度と成功率の相関)
├── run_all_experiments.sh (全実験の実行スクリプト)
└── results/ (実験結果の出力先)
    ├── exp_3a_report.md
    ├── exp_3a_raw_responses.json
    ├── exp_6a_report.md
    ├── exp_6a_raw_results.json
    ├── exp_1a_report.md
    └── exp_1a_raw_results.json
```

## 主要仮説

1. **仮説1**: クエリの複雑さがタイムアウトを引き起こす
2. **仮説2**: API Rate Limitingによる429エラーの誤処理
3. **仮説3**: APIレスポンスのパースエラー
4. **仮説4**: PubMed側のクエリ検証エラー
5. **仮説5**: 累積クエリの長さ制限
6. **仮説6**: 特定の検索語の実ヒット数が本当に0

詳細は [investigation_plan.md](investigation_plan.md) を参照。

## 実行方法

### すべての実験を実行

```bash
cd tests/api_instability_investigation_20251110
./run_all_experiments.sh
```

### Phase別に実行

```bash
# Phase 1のみ（基礎調査: 実験3A, 6A）
./run_all_experiments.sh 1

# Phase 2のみ（タイミング・Rate制御: 実験1A）
./run_all_experiments.sh 2
```

### 個別の実験を実行

```bash
# 実験3A: APIレスポンス構造の詳細ログ
python experiment_3a_response_logging.py

# 実験6A: 0ヒットの手動クロスチェック
python experiment_6a_manual_crosscheck.py

# 実験1A: クエリ複雑度と成功率の相関
python experiment_1a_query_complexity.py
```

## 実験の概要

### 実験3A: APIレスポンス構造の詳細ログ

**目的**: APIが正常にデータを返しているか、パースエラーが発生しているかを確認

**テスト内容**:
- 問題のあった検索語（#2B～#2F）を再度APIに送信
- 完全なJSONレスポンスをログに記録
- `count` フィールドの位置を確認
- エラーフィールドの有無を確認

**期待される成果**:
- `esearchresult.count` が本当に存在しないのか確認
- 別のフィールド名でカウントが返されているか確認
- エラーレスポンスのパターンを特定

### 実験6A: 0ヒットの手動クロスチェック

**目的**: 報告された「0ヒット」が本当に0なのか、APIエラーなのかを判定

**テスト内容**:
- 0ヒットと報告された検索語を5回ずつ実行
- Population条件あり・なしの両方で検証
- 結果の一貫性をチェック

**期待される成果**:
- 真の0ヒット（医師×その概念の組み合わせが文献に存在しない）
- 偽の0ヒット（APIエラーだが0と報告された）
- を区別できる

### 実験1A: クエリ複雑度と成功率の相関

**目的**: 複雑なクエリがタイムアウトや失敗を引き起こすか検証

**テスト内容**:
- Level 1（単純な単語検索）からLevel 5（入れ子のAND/OR）まで段階的にテスト
- 各クエリを3回ずつ実行
- レスポンス時間と成功率を測定

**期待される成果**:
- クエリの複雑さと失敗率の相関を特定
- タイムアウト発生の閾値を特定
- 最適なクエリ構造を提案

## 結果の確認

実験終了後、`results/` ディレクトリに以下が生成されます：

- **`exp_*_report.md`**: 人間が読みやすい分析レポート（Markdown形式）
- **`exp_*_raw_*.json`**: 生データ（JSON形式、詳細分析用）

各レポートには以下が含まれます：
- 実験サマリー（成功率、エラーパターン）
- 詳細な結果テーブル
- 仮説の評価（確認 / 却下 / 不確定）
- 推奨事項

## 次のステップ

実験完了後：

1. **各レポートを確認** (`results/exp_*_report.md`)
2. **仮説の評価をまとめる** (どの仮説が確認されたか)
3. **根本原因を特定**
4. **既存のスクリプトを修正**:
   - `scripts/search/term_validator/check_block_overlap.py`
   - タイムアウト値の調整
   - エラーハンドリングの改善
   - Rate limit制御の最適化

## 環境変数

以下の環境変数を設定することで、より高速・安定した実行が可能：

```bash
# .env ファイルに記述
NCBI_API_KEY=your_api_key_here  # 10 req/sec に増加
NCBI_EMAIL=your_email@example.com
NCBI_TOOL=yarigai_search_validator
```

API Keyなしでも実行可能（3 req/sec制限）

## トラブルシューティング

### "requests" モジュールが見つからない

```bash
pip install requests python-dotenv
```

### 実行権限エラー

```bash
chmod +x run_all_experiments.sh
chmod +x experiment_*.py
```

### タイムアウトエラーが頻発

`.env` でタイムアウト値を調整：

```bash
# 現在のデフォルト: 30秒
# 必要に応じてスクリプト内の REQUEST_TIMEOUT を変更
```

## 貢献

新しい仮説を追加する場合：

1. `investigation_plan.md` に仮説を追加
2. `experiment_*` スクリプトを作成（既存スクリプトをテンプレートとして使用）
3. `run_all_experiments.sh` に新しいPhaseを追加

## ライセンス

このプロジェクトのライセンスに準拠
