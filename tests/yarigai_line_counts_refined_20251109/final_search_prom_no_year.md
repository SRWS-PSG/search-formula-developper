# やりがい検索式（PROMフィルター併用・年次制限なし）

## ブロック定義

- **#1 Population**: `( "Physicians"[Mesh] OR physician*[tiab] )`
- **#2 やりがい概念ブロック**: 既存の満足度・意味づけ・動機づけ・呼びかけ等の用語（下記最終式参照）
- **#3 PROMフィルター**: `templates/PROM_search_filter.md` に記載のPubMed版フィルター全文

## PubMed件数（2025-11-10, esearch）

| 条件 | 件数 |
|---|---|
| #1 Population | 625,538 |
| #3 PROMフィルター | 4,202,671 |
| (#1) AND (#3) | 170,382 |

※ #2との組み合わせ件数は概念ブロック構築後に分解検証済（`five_year_counts_2021plus.md` 参照）。PROMフィルターは患者報告アウトカムに関する記述を担保する追加感度層として適用する。

## 年次フィルター追加時（2021年以降）

2021年1月1日以降（`("2021/01/01"[PDAT] : "3000"[PDAT])`）を加えた場合の同日付カウント:

| 条件 | PubMed件数 |
|---|---|
| #1 Population AND 年次 | 135,710 |
| PROMフィルター AND 年次 | 1,405,142 |
| (#1 AND PROM) AND 年次 | 49,609 |
| 最終式 (#1 AND #2 AND PROM AND 年次) | 2,787 |

→ 年次フィルターの追加で `#1 AND PROM` は170,382件 → 49,609件（▲70.9%）、最終式は2,787件となり最新5年近辺に焦点が当たる。

## 最終検索式案（PubMed）

```
("Physicians"[Mesh] OR physician*[tiab])
AND
(
    "Personal Satisfaction"[Mesh] OR
    "Job Satisfaction"[Mesh] OR
    "Motivation"[Mesh] OR
    "Work Engagement"[Mesh] OR
    "meaningful work"[tiab] OR
    "work meaningfulness"[tiab] OR
    "meaningfulness of work"[tiab] OR
    "meaning in work"[tiab] OR
    "work meaning"[tiab] OR
    "sense of meaning"[tiab] OR
    "work engagement"[tiab] OR
    vigor[tiab] OR
    dedication[tiab] OR
    calling[tiab] OR
    "career calling"[tiab] OR
    "vocational calling"[tiab] OR
    vocation*[tiab] OR
    "prosocial motivation"[tiab] OR
    "intrinsic motivation"[tiab] OR
    "work motivation"[tiab] OR
    (motivat*[tiab] AND (work*[tiab] OR job*[tiab] OR career*[tiab] OR professional*[tiab] OR workplace[tiab])) OR
    "job satisfaction"[tiab] OR
    "work satisfaction"[tiab] OR
    "career satisfaction"[tiab] OR
    "professional satisfaction"[tiab] OR
    "compassion satisfaction"[tiab] OR
    "professional fulfillment"[tiab] OR
    "professional quality of life"[tiab] OR
    "quality of professional life"[tiab] OR
    fulfillment*[tiab] OR
    yarigai[tiab] OR
    ikigai[tiab] OR
    "psychological need*"[tiab] OR
    ((autonomy[tiab] OR competence[tiab] OR relatedness[tiab]) AND (work*[tiab] OR job*[tiab] OR career*[tiab] OR professional*[tiab] OR workplace[tiab])) OR
    "thriving at work"[tiab] OR
    "task significance"[tiab] OR
    "meaningful task*"[tiab] OR
    "work significance"[tiab]
)
AND
(
    HR-PRO[tiab] OR HRPRO[tiab] OR HRQL[tiab] OR HRQoL[tiab] OR QL[tiab] OR
    QoL[tiab] OR "quality of life"[tw] OR "life quality"[tw] OR "health index"*[tiab] OR
    "health indices"[tiab] OR "health profile"*[tiab] OR "health status"[tw] OR
    ((patient[tiab] OR self[tiab] OR child[tiab] OR parent[tiab] OR carer[tiab] OR proxy[tiab])
        AND ((report[tiab] OR reported[tiab] OR reporting[tiab]) OR (rated[tiab] OR rating[tiab] OR ratings[tiab])
        OR based[tiab] OR (assessed[tiab] OR assessment[tiab] OR assessments[tiab]))) OR
    ((disability[tiab] OR function[tiab] OR functional[tiab] OR functions[tiab] OR subjective[tiab] OR utility[tiab]
        OR utilities[tiab] OR wellbeing[tiab] OR "well being"[tiab]) AND (index[tiab] OR indices[tiab] OR instrument[tiab]
        OR instruments[tiab] OR measure[tiab] OR measures[tiab] OR questionnaire[tiab] OR questionnaires[tiab] OR
        profile[tiab] OR profiles[tiab] OR scale[tiab] OR scales[tiab] OR score[tiab] OR scores[tiab] OR status[tiab]
        OR survey[tiab] OR surveys[tiab]))
)
```

## 運用メモ

- PROMフィルターにより患者報告アウトカム視点を担保。必要に応じて `quality of life[tw]` など既存概念と重複する語が含まれるため、重複排除は不要（PubMedは自動で重複論文をマージ）。
- 今後年次や言語フィルターを追加する場合は AND で別ブロックを追加して管理する。例: 上式に `AND ("2021/01/01"[PDAT] : "3000"[PDAT])` を付与して最新5年のみに絞る。
