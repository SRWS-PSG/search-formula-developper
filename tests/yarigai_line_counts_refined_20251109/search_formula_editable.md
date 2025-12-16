# やりがい検索式 - ブロック別編集用

Population条件: `"Physicians"[Mesh] OR physician*[tiab]`

---

## #1 Population

```
"Physicians"[Mesh] OR
physician*[tiab]
```

**検索数データ**:
- Line 1: `"Physicians"[Mesh]` → 個別: 0, 累積: 194,632
- Line 2: `physician*[tiab]` → 個別: 510,299, 累積: 625,518
- **累積総数**: 625,518

---

## #2A MeSH用語（やりがい関連）

```
(("Physicians"[Mesh] OR physician*[tiab]) AND "Personal Satisfaction"[Mesh]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "Job Satisfaction"[Mesh]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "Motivation"[Mesh]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "Work Engagement"[Mesh]) OR


---

## #2B Meaningful Work関連

```
(("Physicians"[Mesh] OR physician*[tiab]) AND "meaningful work"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "work meaningfulness"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "meaningfulness of work"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "meaning in work"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "work meaning"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "sense of meaning"[tiab])
```

**検索数データ**:
- Line 1: `"meaningful work"[tiab]` → 個別: 0
- Line 2: `"work meaningfulness"[tiab]` → 個別: 0
- Line 3: `"meaningfulness of work"[tiab]` → 個別: 11
- Line 4: `"meaning in work"[tiab]` → 個別: 0
- Line 5: `"work meaning"[tiab]` → 個別: 0
- Line 6: `"sense of meaning"[tiab]` → 個別: 0
- **累積総数**: 0 (API不安定)

---

## #2C Work Engagement関連

```
(("Physicians"[Mesh] OR physician*[tiab]) AND "work engagement"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND vigor[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND dedication[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "engaged at work"[tiab])
```

**検索数データ**:
- Line 1: `"work engagement"[tiab]` → 個別: 0
- Line 2: `vigor[tiab]` → 個別: 0
- Line 3: `dedication[tiab]` → 個別: 0
- Line 4: `absorption[tiab]` → 個別: 0
- Line 5: `"engaged at work"[tiab]` → 個別: 0
- **累積総数**: 0 (API不安定)

---

## #2D Calling/Vocation関連

```
(("Physicians"[Mesh] OR physician*[tiab]) AND calling[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "career calling"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "vocational calling"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND vocation*[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "calling orientation"[tiab])
```

**検索数データ**:
- Line 1: `calling[tiab]` → 個別: 0
- Line 2: `"career calling"[tiab]` → 個別: 0
- Line 3: `"vocational calling"[tiab]` → 個別: 0
- Line 4: `vocation*[tiab]` → 個別: 0
- Line 5: `"calling orientation"[tiab]` → 個別: 0
- **累積総数**: 0 (API不安定)

---

## #2E Motivation関連

```
(("Physicians"[Mesh] OR physician*[tiab]) AND "prosocial motivation"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "intrinsic motivation"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "work motivation"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND (motivat*[tiab] AND (work*[tiab] OR job*[tiab] OR career*[tiab] OR professional*[tiab] OR workplace[tiab])))
```

**検索数データ**:
- Line 1: `"prosocial motivation"[tiab]` → 個別: 0
- Line 2: `"intrinsic motivation"[tiab]` → 個別: 0
- Line 3: `"work motivation"[tiab]` → 個別: 0
- Line 4: `(motivat*[tiab] AND (work*[tiab] OR job*[tiab] OR career*[tiab] OR professional*[tiab] OR workplace[tiab]))` → 個別: 4,081
- **累積総数**: 4,133

---

## #2F Satisfaction関連

```
(("Physicians"[Mesh] OR physician*[tiab]) AND "job satisfaction"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "work satisfaction"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "career satisfaction"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "professional satisfaction"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "compassion satisfaction"[tiab])
```

**検索数データ**:
- Line 1: `"job satisfaction"[tiab]` → 個別: 0
- Line 2: `"work satisfaction"[tiab]` → 個別: 248
- Line 3: `"career satisfaction"[tiab]` → 個別: 0
- Line 4: `"professional satisfaction"[tiab]` → 個別: 0
- Line 5: `"compassion satisfaction"[tiab]` → 個別: 0
- **累積総数**: 0 (API不安定)

---

## #2G Professional Fulfillment/Quality of Life

```
(("Physicians"[Mesh] OR physician*[tiab]) AND "professional fulfillment"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "professional quality of life"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "quality of professional life"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND fulfillment*[tiab])
```

**検索数データ**:
- Line 1: `"professional fulfillment"[tiab]` → 個別: 0
- Line 2: `"professional quality of life"[tiab]` → 個別: 108
- Line 3: `"quality of professional life"[tiab]` → 個別: 15
- Line 4: `fulfillment[tiab]` → 個別: 0
- Line 5: `fulfilment[tiab]` → 個別: 0
- **累積総数**: 0 (API不安定)

---

## #2H 日本語概念（ローマ字表記）

```
(("Physicians"[Mesh] OR physician*[tiab]) AND yarigai[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND ikigai[tiab])
```

**検索数データ**:
- Line 1: `yarigai[tiab]` → 個別: 0
- Line 2: `ikigai[tiab]` → 個別: 0
- **累積総数**: 3

---

## #2I 心理的ニーズ/Thriving

```
(("Physicians"[Mesh] OR physician*[tiab]) AND "psychological need*"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND ((autonomy[tiab] OR competence[tiab] OR relatedness[tiab]) AND (work*[tiab] OR job*[tiab] OR professional*[tiab] OR workplace[tiab]))) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "thriving at work"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "workplace thriving"[tiab])
```

**検索数データ**:
- Line 1: `"psychological need*"[tiab]` → 個別: 0
- Line 2: `((autonomy[tiab] OR competence[tiab] OR relatedness[tiab]) AND (work*[tiab] OR job*[tiab] OR professional*[tiab] OR workplace[tiab]))` → 個別: 5,640
- Line 3: `"thriving at work"[tiab]` → 個別: 2
- Line 4: `"workplace thriving"[tiab]` → 個別: 0
- **累積総数**: 0 (API不安定)

---

## #2J Task Significance

```
(("Physicians"[Mesh] OR physician*[tiab]) AND "task significance"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "meaningful task*"[tiab]) OR
(("Physicians"[Mesh] OR physician*[tiab]) AND "work significance"[tiab])
```

**検索数データ**:
- Line 1: `"task significance"[tiab]` → 個別: 1
- Line 2: `"meaningful task*"[tiab]` → 個別: 0
- Line 3: `"work significance"[tiab]` → 個別: 0
- **累積総数**: 0 (API不安定)

---

## 注意事項

- 各ブロックの検索式を直接編集できます
- 個別ヒット数が0のものは削除候補です
- 修正後は新しいファイル名で保存してください
