<!--
Created by: Codex CLI (GPT-5.2)
Purpose: ERIC(無料)アクセス用スクリプト確認 / Anthropological Index Online(AIO) 検索実装の開発計画
Created on: 2025-12-29
-->

# ERIC（無料）アクセス用スクリプト確認 / AIO検索実装計画

## 1) ERIC（無料）アクセス用スクリプトの確認結果

### 対象スクリプト（リポジトリ内）
- APIクライアント: `scripts/search/eric/eric_api.py`
- CLI: `scripts/search/eric/search_eric.py`
- 一括DL（特定クエリ用）: `scripts/search/eric/download_eric_results.py`（※最大2000件の制限あり）

### ERIC「無料版」アクセス観点の結論
- `scripts/search/eric/eric_api.py` は ERIC公式の IES API エンドポイント `https://api.ies.ed.gov/eric/` を叩いており、現状の実装に **APIキー設定やログインは不要**。
- ローカル環境から実際に疎通できることを確認（`--count-only` / 結果取得ともに成功）。

### 動作確認コマンド例
```bash
# 件数確認
python scripts/search/eric/search_eric.py --query "medical education" --count-only

# 取得（表示）
python scripts/search/eric/search_eric.py --query "medical education" --rows 2

# シソーラス + フリーワード
python scripts/search/eric/search_eric.py --query 'subject:"Medical School Faculty" AND burnout' --count-only
```

### 実装上の重要ポイント（ERIC側）
- 1リクエストあたりの取得上限: `rows` は最大2000（`eric_api.py` の `MAX_ROWS = 2000`）
  - 2000件を超える場合は `start` を使ったページネーション（繰り返し取得）が必要
- CLIはJSON以外（`xml`/`csv`）も指定可能（ただし現状は“生レスポンス”扱い）
- RIS出力は `export_results_to_ris()` で実装済み

---

## 2) Anthropological Index Online（AIO）を同様のやり方で検索するための開発計画

> 方針: まず「最小の検索→結果ID取得→RIS一括DL」までをMVPとして実装し、挙動が不明な部分（上限、細かいフィールド挙動等）は **実装しながら確認** する。

### 2.1 事前調査（こちらで確認できた範囲）

#### AIOサイトとページ
- ベースURL: `https://aio.therai.org.uk/`
- 検索UI:
  - Quick search: `GET /quick-search` → `POST /quick-search`
  - Advanced search: `GET /advanced-search` → `POST /advanced-search`
- Browse（補助）:
  - Browse keywords: `GET /keywords/search`
  - Browse journals: `GET /journals/search`

#### CSRFトークンとセッション
- `GET /quick-search` / `GET /advanced-search` で HTML内に hidden `_token` が埋め込まれ、Cookie（`PHPSESSID`）も付与される
- `POST` 時は `_token` を送る（Cookieも同一セッションで維持する想定）

#### Quick search（フォーム仕様の要点）
- `POST /quick-search` の主パラメータ例:
  - `_token`
  - `qs_keyword`（検索語）
  - `qs_decades[]`（例: `recent` / `all` / `1950` ...）
  - `qs_resultsmode`（`bib`/`full`/`fullkeywords`）
  - `qs_sort`（`year_d`/`year_a`/`title_a`/`title_d`）
  - `qs_filter`（`*` / `Film` / `Article`）
- `POST` 後の遷移例（結果IDがURLに入る）:
  - `/quick-search/<results_id>/<mode>?page=1`

#### Advanced search（フォーム仕様の要点）
- `POST /advanced-search` の主パラメータ例:
  - `_token`
  - `cw`（条件の結合: `AND` / `OR`）
  - `as_resultsmode`（`bib`/`full`/`fullkeywords`）
  - `filter`（`*` / `Film` / `Article`）
  - `sort`（`year_d`/`year_a`/`title_a`/`title_d`）
  - 条件（インデックス付き）:
    - `f0`/`o0`/`v0`, `f1`/`o1`/`v1`, ...
    - 例: 「Title contains autoethnography」→ `f0=title`, `o0=CT`, `v0=autoethnography`
- `POST` 後の遷移例:
  - `/advanced-search/<results_id>/<mode>?page=1`

#### 結果の一括ダウンロード（RIS等）
- 結果画面にダウンロードフォームがあり、エンドポイントは次の形:
  - `GET /results/<results_id>/download?action=downloadresults&resultsid=<results_id>&mimetype=ris&charset=UTF-8`
  - `mimetype`: `html` / `csv` / `endnote` / `ris`
  - `charset`: `DEFAULT` / `UTF-8` / `Latin1` / `ASCII`
- **確認できた挙動**: `mimetype=ris` のレスポンスは「表示ページ分」ではなく **検索結果全件** を返す（ページネーション不要で一括DL可能）
  - 件数はRIS内の `TY  -` 行数などで算出可能

#### キーワード・ジャーナルの補助エンドポイント（プレーンテキスト）
UIのオートコンプリート用に、プレーンテキストを返すAPIが露出している（こちらはCSRF不要で応答することを確認）。
- キーワード候補: `GET /keywords/legacy/by-prefix?prefix=<text>`
- ジャーナル候補: `GET /journal/lookup/names-by-prefix?prefix=<text>`

#### 利用条件（重要）
- `https://aio.therai.org.uk/conditions.shtml` より:
  - 「限定的利用（年100検索未満）」は多くのケースで無料、頻繁な利用や非教育機関はサブスク対象
- したがって実装は **過剰な自動化を避ける設計（キャッシュ・レート制限）** を前提にする

---

### 2.2 実装ゴール（ERICと“同様”にする範囲）
- CLIで検索を実行し、結果を `RIS`（優先）で保存できる
- 可能なら `--count-only` 相当（ただしAIOは「検索→結果ID→DL」で最小2リクエストになり得る）
- 検索条件（Advanced search）をコードで組み立て可能（field/operator/value + AND/OR）

---

### 2.3 実装案（リポジトリの既存構造に寄せる）

#### 追加する想定パス（案）
- `scripts/search/aio/aio_client.py`
  - `AIOClient`（`requests.Session`）
  - `_get_csrf_token(path)`（`/quick-search` or `/advanced-search` をGETして `_token` 抽出）
  - `quick_search(...) -> results_id`
  - `advanced_search(criteria, combine, ...) -> results_id`
  - `download_results(results_id, mimetype, charset) -> bytes/str`
- `scripts/search/aio/search_aio.py`
  - `search_eric.py` と同じ体裁のCLI（`--query` に相当する引数設計）
  - `--output` で `.ris` 保存、`--format`（ris/csv/html/endnote）も任意
- （必要なら）`scripts/search/aio/aio_ris.py`
  - RISの最小パース（件数計算、1件目の表示など）

---

### 2.4 開発ステップ（実装しながら不明点を潰す）

#### Phase 0: 最小の疎通（スモーク）
- `GET /quick-search` → `_token` 抽出
- `POST /quick-search` → `results_id` 抽出（リダイレクトURLから）
- `GET /results/<id>/download?...mimetype=ris` → ファイル保存

#### Phase 1: MVP（Quick search対応）
- CLI:
  - `--quick --keyword "<text>"`
  - `--decades recent|all|1950|...`（複数指定可）
  - `--filter *|Article|Film`
  - `--sort year_d|year_a|title_a|title_d`
  - `--mode bib|full|fullkeywords`（結果表示のHTMLモードに合わせるだけ。DL自体はRIS優先）
  - `--output out.ris`
- 取得後に件数を表示（RISの `TY  -` 行数など）

#### Phase 2: Advanced search対応（本命）
- `criteria` を `[(field, op, value), ...]` として受け取り、`f0/o0/v0` を組み立て
- `cw=AND|OR` を指定できるようにする（全条件一致 / いずれか一致）
- field候補は、UIに存在するものを列挙（title/author/year/keyword/subject/.../journal/issn等）
- operator候補（UI準拠）:
  - `==`, `!=`, `>`, `<`, `>=`, `<=`, `LI`(matches), `NL`(does not match), `CT`(contains), `NC`(does not contain)

#### Phase 3: 省リクエスト化（利用制限に配慮）
- キャッシュ（強く推奨）:
  - `--cache-dir` を設け、クエリ+条件のハッシュでRISを保存（同一条件の再実行はネットワークを叩かない）
  - キャッシュにメタ情報（日時、条件、results_id、URL）をJSONで添付
- レート制限:
  - 少なくとも連続実行時は `sleep` を入れる（例: 1〜2秒、指数バックオフ）
  - User-Agent を明示し、失敗時のリトライ回数を抑制

#### Phase 4: 追加機能（必要になったら）
- キーワード/ジャーナルの補助コマンド
  - `aio_lookup_keyword --prefix auto`
  - `aio_lookup_journal --prefix American`
  - 既存の露出エンドポイントを利用（`/keywords/legacy/by-prefix` 等）
- HTML結果の軽量表示（RISを保存しない場合でも、上位N件だけ表示）

---

### 2.5 不明点（実装しながら確認する項目）
- ダウンロード上限（結果が非常に多い場合にRISが何件まで返るか）
- 無料利用（100検索/年など）の実際の制限のかかり方（IP/セッション/その他）
- Advanced search の複数条件で、未指定スロット（例: `f1`未指定）の扱いとエラー条件
- 非ローマ字・特殊文字のRISエンコーディング最適解（UTF-8/Latin1 など）

