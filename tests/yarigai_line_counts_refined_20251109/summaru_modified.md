# やりがい検索式ブラッシュアップ - 各ブロック検索数データ

生成日時: 2025-11-09
Population条件: `"Physicians"[Mesh] OR physician*[tiab]`
フィルター: なし（後で追加予定）

---

## #1 Population

| Line | 検索語 | 個別ヒット数 | 累積(OR) | 追加 |
|------|--------|-------------|----------|------|
| 1 | `"Physicians"[Mesh]` | 0 | 194,632 | +0 |
| 2 | `physician*[tiab]` | 510,299 | 625,518 | +430,886 |

**累積総数**: 625,518

---

## #2A MeSH用語（やりがい関連・主要テーマ）

| Line | 検索語 | 個別ヒット数 | 累積(OR) | 追加 |
|------|--------|-------------|----------|------|
| 1 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "Personal Satisfaction"[Majr])` | 489 | 0 | +489 |
| 2 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "Job Satisfaction"[Majr])` | 2,314 | 0 | +0 |
| 3 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "Motivation"[Majr:noexp])` | 0 | 0 | +0 |
| 4 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "Work Engagement"[Mesh])` | 95 | 4,032 | +4,032 |

これ、すべて　[mesh]にして

---

## #2B Meaningful Work関連

| Line | 検索語 | 個別ヒット数 | 累積(OR) | 追加 |
|------|--------|-------------|----------|------|
| 1 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "meaningful work"[tiab])` | 0 | 50 | +0 |
| 2 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "work meaningfulness"[tiab])` | 0 | 0 | +-50 |
| 3 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "meaningfulness of work"[tiab])` | 11 | 0 | +0 |
| 4 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "meaning in work"[tiab])` | 0 | 99 | +99 |
| 5 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "work meaning"[tiab])` | 0 | 0 | +-99 |
| 6 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "sense of meaning"[tiab])` | 0 | 0 | +0 |

**累積総数**: 0 (API不安定)

---

## #2C Work Engagement関連

| Line | 検索語 | 個別ヒット数 | 累積(OR) | 追加 |
|------|--------|-------------|----------|------|
| 1 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "work engagement"[tiab])` | 0 | 0 | +0 |
| 2 | `(("Physicians"[Mesh] OR physician*[tiab]) AND vigor[tiab])` | 0 | 219 | +219 |
| 3 | `(("Physicians"[Mesh] OR physician*[tiab]) AND dedication[tiab])` | 0 | 0 | +-219 |
| 4 | `(("Physicians"[Mesh] OR physician*[tiab]) AND absorption[tiab])` | 0 | 0 | +0 |
| 5 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "engaged at work"[tiab])` | 0 | 0 | +0 |

**累積総数**: 0 (API不安定)

---

## #2D Calling/Vocation関連

| Line | 検索語 | 個別ヒット数 | 累積(OR) | 追加 |
|------|--------|-------------|----------|------|
| 1 | `(("Physicians"[Mesh] OR physician*[tiab]) AND calling[tiab])` | 0 | 948 | +0 |
| 2 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "career calling"[tiab])` | 0 | 948 | +0 |
| 3 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "vocational calling"[tiab])` | 0 | 0 | +-948 |
| 4 | `(("Physicians"[Mesh] OR physician*[tiab]) AND vocation*[tiab])` | 0 | 0 | +0 |
| 5 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "calling orientation"[tiab])` | 0 | 0 | +0 |

**累積総数**: 0 (API不安定)

---

## #2E Motivation関連

| Line | 検索語 | 個別ヒット数 | 累積(OR) | 追加 |
|------|--------|-------------|----------|------|
| 1 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "prosocial motivation"[tiab])` | 0 | 3 | +0 |
| 2 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "intrinsic motivation"[tiab])` | 0 | 0 | +-3 |
| 3 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "work motivation"[tiab])` | 0 | 184 | +184 |
| 4 | `(("Physicians"[Mesh] OR physician*[tiab]) AND (motivat*[tiab] AND (work*[tiab] OR job*[tiab] OR career*[tiab] OR professional*[tiab] OR workplace[tiab])))` | 4,081 | 4,133 | +3,949 |

**累積総数**: 4,133

---

## #2F Satisfaction関連

| Line | 検索語 | 個別ヒット数 | 累積(OR) | 追加 |
|------|--------|-------------|----------|------|
| 1 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "job satisfaction"[tiab])` | 0 | 0 | +0 |
| 2 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "work satisfaction"[tiab])` | 248 | 0 | +0 |
| 3 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "career satisfaction"[tiab])` | 0 | 2,761 | +2,761 |
| 4 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "professional satisfaction"[tiab])` | 0 | 0 | +-2,761 |
| 5 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "compassion satisfaction"[tiab])` | 0 | 0 | +0 |

**累積総数**: 0 (API不安定)

---

## #2G Professional Fulfillment/Quality of Life

| Line | 検索語 | 個別ヒット数 | 累積(OR) | 追加 |
|------|--------|-------------|----------|------|
| 1 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "professional fulfillment"[tiab])` | 0 | 0 | +0 |
| 2 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "professional quality of life"[tiab])` | 108 | 306 | +306 |
| 3 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "quality of professional life"[tiab])` | 15 | 0 | +-306 |
| 4 | `(("Physicians"[Mesh] OR physician*[tiab]) AND fulfillment[tiab])` | 0 | 771 | +771 |
| 5 | `(("Physicians"[Mesh] OR physician*[tiab]) AND fulfilment[tiab])` | 0 | 0 | +-771 |

**累積総数**: 0 (API不安定)

---

## #2H 日本語概念（ローマ字表記）

| Line | 検索語 | 個別ヒット数 | 累積(OR) | 追加 |
|------|--------|-------------|----------|------|
| 1 | `(("Physicians"[Mesh] OR physician*[tiab]) AND yarigai[tiab])` | 0 | 1 | +0 |
| 2 | `(("Physicians"[Mesh] OR physician*[tiab]) AND ikigai[tiab])` | 0 | 3 | +2 |

**累積総数**: 3

---

## #2I 心理的ニーズ/Thriving

| Line | 検索語 | 個別ヒット数 | 累積(OR) | 追加 |
|------|--------|-------------|----------|------|
| 1 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "psychological need*"[tiab])` | 0 | 0 | +0 |
| 2 | `(("Physicians"[Mesh] OR physician*[tiab]) AND ((autonomy[tiab] OR competence[tiab] OR relatedness[tiab]) AND (work*[tiab] OR job*[tiab] OR professional*[tiab] OR workplace[tiab])))` | 5,640 | 5,758 | +5,758 |
| 3 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "thriving at work"[tiab])` | 2 | 5,760 | +2 |
| 4 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "workplace thriving"[tiab])` | 0 | 0 | +-5,760 |

**累積総数**: 0 (API不安定)

---

## #2J Task Significance

| Line | 検索語 | 個別ヒット数 | 累積(OR) | 追加 |
|------|--------|-------------|----------|------|
| 1 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "task significance"[tiab])` | 1 | 1 | +1 |
| 2 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "meaningful task*"[tiab])` | 0 | 8 | +7 |
| 3 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "work significance"[tiab])` | 0 | 0 | +-8 |

**累積総数**: 0 (API不安定)

---

## 注意事項

- **個別ヒット数が0**: PubMed APIの返り値が0と表示されているが、実際にはヒットしている可能性がある（API不安定性）
- **累積数の異常**: 累積数が正しく計算されていないケースが多数（APIレスポンスの不安定性）
- **マイナスの追加数**: 累積カウントが前の行より減っているケース（API不安定性）

### 個別検索での実測値を再確認すべきブロック

累積カウントが信頼できないため、各検索語を単独でPubMedで手動確認することを推奨：

1. #2A MeSH Terms: 個別カウント有り (489, 2,314, 0, 95, 0)
2. #2B Meaningful Work: 個別カウント有り (0, 0, 11, 0, 0, 0)
3. #2E Motivation: 個別カウント信頼できる (0, 0, 0, 4,081)
4. #2F Satisfaction: 個別カウント有り (0, 248, 0, 0, 0)
5. #2G Fulfillment: 個別カウント有り (0, 108, 15, 0, 0)
6. #2I Psychological Needs: 個別カウント有り (0, 5,640, 2, 0)
7. #2J Task Significance: 個別カウント有り (1, 0, 0)
