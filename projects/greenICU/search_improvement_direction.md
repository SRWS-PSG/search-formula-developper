# Green ICU 検索式改善の方向性

> **作成日**: 2025-12-28  
> **ステータス**: 分析・改善中  
> **現状の問題**: 検索件数が多すぎる（約22,000件 → 理想は10,000件以下）

---

## 1. 現状の課題サマリー

### 検索件数の問題
| 検索式バージョン | 件数 | 評価 |
|-----------------|------|------|
| 初期版（改善前） | 35,033件 | ❌ 多すぎる |
| 高頻度語削除後 | 21,661件 | ⚠️ まだ多い |
| 目標 | 5,000〜10,000件 | ✅ 適切な範囲 |

### 検証対象PMID（18件）の捕捉率
| 段階 | 捕捉率 | 備考 |
|------|--------|------|
| 初期 | 61.1% (11/18件) | 7件漏れ |
| 改善後 | 88.2% (15/17件) | ICUスコープ外1件を評価対象から除外 |
| 目標 | 90%以上 | |
※ 評価対象は18件中、ICUスコープ外（PMID 39998996）を除いた17件。

---

## 2. 問題の高頻度用語（削除済み）

以下の用語は単独で100万件以上のヒットがあり、検索ノイズの主要原因として**削除済み**：

| 用語 | 件数 | 問題点 |
|------|------|--------|
| `environment*[tiab]` | 1,616,568件 | 環境全般を広くカバーしすぎ |
| `intervention[tiab]` | 973,422件 | 医療全般で使用される一般語 |
| `education[tiab]` | 726,406件 | 医学教育全般をカバー |
| `sustain*[tiab]` | 592,583件 | 持続性全般（環境以外も含む） |

---

## 3. 今後の改善方向

### 3.1 Green関連用語の精緻化

**問題**: `green[tiab]`単独で257,820件

**改善案**: フレーズ中心でICU関連に限定（PubMedの近接非対応を回避）

```
PubMed（フレーズ中心）:
"green ICU"[tiab] OR "green team"[tiab] OR "sustainability team"[tiab] OR
(green[tiab] AND (ICU[tiab] OR "intensive care"[tiab]))

Embase（近接演算子対応）:
green NEAR/3 (ICU OR "intensive care") OR "green team" OR "sustainability team"
```

### 3.2 Planet関連用語の追加（反映済み）

**方針**: `planet*[tiab]`を追加（PMID 39665859 等の捕捉用）

```
planet[tiab] OR "planetary health"[tiab]
```

### 3.3 ICU専門誌の活用（Top 10・反映済み）

以下の高インパクト雑誌を`[Journal]`としてPopulation (P)ブロックに追加：

| 順位 | 雑誌名 | JIF |
|------|--------|-----|
| 1 | Lancet Respiratory Medicine | 32.8 |
| 2 | Intensive Care Medicine | 21.2 |
| 3 | American Journal of Respiratory and Critical Care Medicine | 19.4 |
| 4 | Critical Care | 9.3 |
| 5 | Chest | 8.6 |
| 6 | Critical Care Medicine | 6.0 |
| 7 | Annals of Intensive Care | 5.5 |
| 8 | Intensive and Critical Care Nursing | 4.7 |
| 9 | Anaesthesia Critical Care & Pain Medicine | 4.7 |
| 10 | Journal of Intensive Care | 4.7 |

### 3.4 構文エラーの修正（完了済み）

- ~~`"Emergencies""[Mesh]`~~ → `"Emergencies"[Mesh]`（二重引用符エラー）
- 括弧バランスの修正

---

## 4. 捕捉できなかった論文の分析

### ICUスコープ外（除外が適切）
| PMID | タイトル | 理由 |
|------|----------|------|
| 39998996 | "The Power of Education to Reduce the Carbon Footprint of Volatile Anesthetics" | 手術室の麻酔薬に関する論文、ICU非特化 |

### ICUスコープ内（捕捉すべき）
| PMID | タイトル | 捕捉に必要な用語 |
|------|----------|------------------|
| 39665859 | "Beta-lactam administration, which one is the best for the planet?" | `"Intensive Care Medicine"[Journal]` + `planet[tiab]` |

---

## 5. 研究の3つの定義とカバレッジ

本レビューにおけるICU環境保全の定義：

| 定義 | 現在のカバレッジ | 改善案 |
|------|-----------------|--------|
| ①カーボンフットプリント定量化 | ✅ 十分 | - |
| ②標的介入プログラム | ⚠️ 部分的 | QI/auditは環境語とのANDで絞り込み（単独は除外） |
| ③Green ICUチーム創設・維持 | ⚠️ 不十分 | `"green team"[tiab]`, `"sustainability team"[tiab]` 追加検討 |

---

## 6. 次のアクション

1. [x] `planet[tiab]`/`"planetary health"[tiab]` をConcept (C)に追加
2. [x] `green`はフレーズ中心（`"green ICU"`, `"green team"`, `"sustainability team"`）に寄せてICU関連に限定
3. [x] Top 10 ICU雑誌をPopulation (P)ブロックに追加
4. [x] QI/auditは環境語とのANDで絞り込み（単独は除外）
5. [ ] 修正後の検索式でPubMed APIを使って件数確認
6. [ ] 18件のPMID捕捉率を再検証（評価対象は17件）
7. [ ] 偽陽性率の確認（サンプル抽出で適合性評価）

---

## 7. 参考：検索式の構造

```
Population (P): ICU患者・医療スタッフ
  └─ MeSH: Intensive Care Units, Critical Care, Critical Illness, etc.
  └─ フリーワード: icu, intensive care, critical care, etc.
  └─ 雑誌: Intensive Care Medicine, Critical Care, etc.

Concept (C): 環境保全措置
  └─ MeSH: Carbon Footprint, Medical Waste, Quality Improvement, etc.
  └─ フリーワード: climate change, carbon footprint, green ICU, etc.
  └─ 組み合わせ: (green AND ICU関連), (waste AND reduction/audit), QI/audit AND 環境語

Final: P AND C
```

---

## 8. 関連ファイル

- 現在の検索式: [`search.md`](./search.md)
- Devinセッション: https://app.devin.ai/sessions/c19f584056c74d67af2f36e75b704ff9 （セッション期限切れ）
