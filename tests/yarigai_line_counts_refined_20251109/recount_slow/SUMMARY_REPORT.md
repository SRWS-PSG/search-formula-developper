# 待機時間延長版（5秒） - ブロック別検索数レポート

生成日時: 2025-11-09 15:30:35
Population条件: `"Physicians"[Mesh] OR physician*[tiab]`
待機時間: 各API呼び出し間5秒、ブロック間10秒

---

## #2A MeSH用語（やりがい関連）

| Line | 検索語 | 個別 | 累積 | 追加 | 割合 |
|------|--------|------|------|------|------|
| 1 | `"Personal Satisfaction"[Mesh]` | 1,371 | 1,371 | +1,371 | 10.1% |
| 2 | `"Job Satisfaction"[Mesh]` | NA | 6,088 | +4,717 | 34.9% |
| 3 | `"Motivation"[Mesh]` | 7,861 | 6,088 | +0 | 0.0% |
| 4 | `"Work Engagement"[Mesh]` | NA | 13,511 | +7,423 | 54.9% |

**累積総数**: 13,511
**最も効果的**: Line 4 ("Work Engagement"[Mesh], +7,423件, 54.9%)
**低効率用語** (<1%): Line 3
**高重複用語** (>80%): Line 3
**注**: Line 2, 4 の個別カウントはAPIエラーで取得不可 (NA表示)

---

## #2B Meaningful Work関連

| Line | 検索語 | 個別 | 累積 | 追加 | 割合 |
|------|--------|------|------|------|------|
| 1 | `"meaningful work"[tiab]` | 50 | 50 | +50 | 33.6% |
| 2 | `"work meaningfulness"[tiab]` | 3 | 53 | +3 | 2.0% |
| 3 | `"meaningfulness of work"[tiab]` | 11 | 53 | +0 | 0.0% |
| 4 | `"meaning in work"[tiab]` | 42 | 99 | +46 | 30.9% |
| 5 | `"work meaning"[tiab]` | 6 | 104 | +5 | 3.4% |
| 6 | `"sense of meaning"[tiab]` | 48 | 149 | +45 | 30.2% |

**累積総数**: 149
**最も効果的**: Line 1 ("meaningful work"[tiab], +50件, 33.6%)
**低効率用語** (<1%): Line 3
**高重複用語** (>80%): Line 3

---

## #2C Work Engagement関連

| Line | 検索語 | 個別 | 累積 | 追加 | 割合 |
|------|--------|------|------|------|------|
| 1 | `"work engagement"[tiab]` | 151 | 151 | +151 | 27.5% |
| 2 | `vigor[tiab]` | NA | 219 | +68 | 12.4% |
| 3 | `dedication[tiab]` | 354 | 550 | +331 | 60.2% |
| 4 | `"engaged at work"[tiab]` | 0 | 550 | +0 | 0.0% |

**累積総数**: 550
**最も効果的**: Line 3 (dedication[tiab], +331件, 60.2%)
**低効率用語** (<1%): Line 4
**注**: Line 2 の個別カウントはAPIエラーで取得不可 (NA表示)

---

## #2D Calling/Vocation関連

| Line | 検索語 | 個別 | 累積 | 追加 | 割合 |
|------|--------|------|------|------|------|
| 1 | `calling[tiab]` | 948 | 0 | +0 | 0.0% |
| 2 | `"career calling"[tiab]` | 3 | 948 | +948 | 48.8% |
| 3 | `"vocational calling"[tiab]` | 4 | 948 | +0 | 0.0% |
| 4 | `vocation*[tiab]` | NA | 1,941 | +993 | 51.2% |
| 5 | `"calling orientation"[tiab]` | 0 | 1,941 | +0 | 0.0% |

**累積総数**: 1,941
**最も効果的**: Line 4 (vocation*[tiab], +993件, 51.2%)
**低効率用語** (<1%): Line 1, 3, 5
**高重複用語** (>80%): Line 1, 3
**注**: Line 4 の個別カウントはAPIエラーで取得不可 (NA表示)

---

## #2E Motivation関連

| Line | 検索語 | 個別 | 累積 | 追加 | 割合 |
|------|--------|------|------|------|------|
| 1 | `"prosocial motivation"[tiab]` | 3 | 3 | +3 | 0.1% |
| 2 | `"intrinsic motivation"[tiab]` | 139 | 141 | +138 | 3.3% |
| 3 | `"work motivation"[tiab]` | 47 | 141 | +0 | 0.0% |
| 4 | `(motivat*[tiab] AND (work*[tiab] OR job*[tiab] OR career*[tiab] OR professional*[tiab] OR workplace[tiab]))` | NA | 4,133 | +3,992 | 96.6% |

**累積総数**: 4,133
**最も効果的**: Line 4 ((motivat*[tiab] AND (work*[tiab] OR job*[tiab] OR career*[tiab] OR professional*[tiab] OR workplace[tiab])), +3,992件, 96.6%)
**低効率用語** (<1%): Line 1, 3
**高重複用語** (>80%): Line 3
**注**: Line 4 の個別カウントはAPIエラーで取得不可 (NA表示)

---

## #2F Satisfaction関連

| Line | 検索語 | 個別 | 累積 | 追加 | 割合 |
|------|--------|------|------|------|------|
| 1 | `"job satisfaction"[tiab]` | 2,141 | 2,141 | +2,141 | 68.9% |
| 2 | `"work satisfaction"[tiab]` | 248 | 2,141 | +0 | 0.0% |
| 3 | `"career satisfaction"[tiab]` | 519 | 2,141 | +0 | 0.0% |
| 4 | `"professional satisfaction"[tiab]` | 313 | 3,018 | +877 | 28.2% |
| 5 | `"compassion satisfaction"[tiab]` | 103 | 3,107 | +89 | 2.9% |

**累積総数**: 3,107
**最も効果的**: Line 1 ("job satisfaction"[tiab], +2,141件, 68.9%)
**低効率用語** (<1%): Line 2, 3
**高重複用語** (>80%): Line 2, 3

---

## #2G Professional Fulfillment/Quality of Life

| Line | 検索語 | 個別 | 累積 | 追加 | 割合 |
|------|--------|------|------|------|------|
| 1 | `"professional fulfillment"[tiab]` | 199 | 199 | +199 | 25.8% |
| 2 | `"professional quality of life"[tiab]` | 108 | 306 | +107 | 13.9% |
| 3 | `"quality of professional life"[tiab]` | 15 | 317 | +11 | 1.4% |
| 4 | `fulfillment*[tiab]` | 655 | 771 | +454 | 58.9% |

**累積総数**: 771
**最も効果的**: Line 4 (fulfillment*[tiab], +454件, 58.9%)

---

## #2H 日本語概念（ローマ字表記）

| Line | 検索語 | 個別 | 累積 | 追加 | 割合 |
|------|--------|------|------|------|------|
| 1 | `yarigai[tiab]` | 1 | 1 | +1 | 33.3% |
| 2 | `ikigai[tiab]` | 3 | 3 | +2 | 66.7% |

**累積総数**: 3
**最も効果的**: Line 2 (ikigai[tiab], +2件, 66.7%)

---

## #2I 心理的ニーズ/Thriving

| Line | 検索語 | 個別 | 累積 | 追加 | 割合 |
|------|--------|------|------|------|------|
| 1 | `"psychological need*"[tiab]` | NA | 129 | +129 | 2.2% |
| 2 | `((autonomy[tiab] OR competence[tiab] OR relatedness[tiab]) AND (work*[tiab] OR job*[tiab] OR professional*[tiab] OR workplace[tiab]))` | 5,640 | 5,758 | +5,629 | 97.7% |
| 3 | `"thriving at work"[tiab]` | 2 | 5,760 | +2 | 0.0% |
| 4 | `"workplace thriving"[tiab]` | 0 | 5,760 | +0 | 0.0% |

**累積総数**: 5,760
**最も効果的**: Line 2 (((autonomy[tiab] OR competence[tiab] OR relatedness[tiab]) AND (work*[tiab] OR job*[tiab] OR professional*[tiab] OR workplace[tiab])), +5,629件, 97.7%)
**低効率用語** (<1%): Line 3, 4
**注**: Line 1 の個別カウントはAPIエラーで取得不可 (NA表示)

---

## #2J Task Significance

| Line | 検索語 | 個別 | 累積 | 追加 | 割合 |
|------|--------|------|------|------|------|
| 1 | `"task significance"[tiab]` | NA | 1 | +1 | 11.1% |
| 2 | `"meaningful task*"[tiab]` | 7 | 8 | +7 | 77.8% |
| 3 | `"work significance"[tiab]` | 1 | 9 | +1 | 11.1% |

**累積総数**: 9
**最も効果的**: Line 2 ("meaningful task*"[tiab], +7件, 77.8%)
**注**: Line 1 の個別カウントはAPIエラーで取得不可 (NA表示)

---

## 全体サマリー

### ブロック別累積総数

| ブロック | 累積総数 | 信頼性 |
|----------|----------|--------|
| #2A | 13,511 | ⚠️ 中 |
| #2B | 149 | ✅ 高 |
| #2C | 550 | ⚠️ 中 |
| #2D | 1,941 | ⚠️ 中 |
| #2E | 4,133 | ⚠️ 中 |
| #2F | 3,107 | ✅ 高 |
| #2G | 771 | ✅ 高 |
| #2H | 3 | ✅ 高 |
| #2I | 5,760 | ⚠️ 中 |
| #2J | 9 | ⚠️ 中 |

### 備考

- NA = PubMed APIエラーで個別件数が取得できなかった項目
- 累積カウントはORクエリの最新値。APIエラー時は直前値を引き継ぎ
