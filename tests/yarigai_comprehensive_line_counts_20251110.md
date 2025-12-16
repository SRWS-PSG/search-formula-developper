# やりがい検索式 全ブロック行ごと件数レポート

**生成日**: 2025-11-10 18:22:34
**使用スクリプト**: check_block_overlap.py (バグ修正版)
**実行スクリプト**: tests/recount_all_blocks_unified.py

**表記**: `#1 AND ...` は `("Physicians"[Mesh] OR physician*[tiab]) AND ...` を簡略表記

---

## #1 Population (Physicians only)

| Line | Term | Individual (All) | Individual (3y 2023+) | Individual (5y 2021+) | Cumulative (OR) | Added | % of Total |
|------|------|------------------|----------------------|----------------------|-----------------|-------|------------|
| 1 | [`"Physicians"[Mesh]`](https://pubmed.ncbi.nlm.nih.gov/?term="Physicians"[Mesh]) | 194,632 | 22,611 | 135,710 | 194,632 | **+194,632** | 100.0% |
| 2 | [`physician*[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=physician*[tiab]) | 510,328 | 63,597 | - | 625,547 | **+430,915** | 68.9% |

**Total**: 625,547 papers

---

## #2A MeSH Terms

| Line | Term | Individual (All) | Individual (3y 2023+) | Individual (5y 2021+) | Cumulative (OR) | Added | % of Total |
|------|------|------------------|----------------------|----------------------|-----------------|-------|------------|
| 1 | [`#1 AND "Personal Satisfaction"[Mesh]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"Personal+Satisfaction"[Mesh])) | 1,371 | 142 | 332 | 1,371 | **+1,371** | 100.0% |
| 2 | [`#1 AND "Job Satisfaction"[Mesh]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"Job+Satisfaction"[Mesh])) | 4,968 | 495 | 845 | 6,088 | **+4,717** | 77.5% |
| 3 | [`#1 AND "Motivation"[Mesh]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"Motivation"[Mesh])) | 7,861 | 666 | 1,273 | 13,451 | **+7,363** | 54.7% |
| 4 | [`#1 AND "Work Engagement"[Mesh]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"Work+Engagement"[Mesh])) | 95 | 30 | 47 | 13,511 | **+60** | 0.4% |

**Total**: 13,511 papers

---

## #2B Meaningful Work

| Line | Term | Individual (All) | Individual (3y 2023+) | Individual (5y 2021+) | Cumulative (OR) | Added | % of Total |
|------|------|------------------|----------------------|----------------------|-----------------|-------|------------|
| 1 | [`#1 AND "meaningful work"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"meaningful+work"[tiab])) | 50 | 18 | 26 | 50 | **+50** | 100.0% |
| 2 | [`#1 AND "work meaningfulness"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"work+meaningfulness"[tiab])) | 3 | 0 | 2 | 53 | **+3** | 5.7% |
| 3 | [`#1 AND "meaningfulness of work"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"meaningfulness+of+work"[tiab])) | 11 | 2 | 6 | 62 | **+9** | 14.5% |
| 4 | [`#1 AND "meaning in work"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"meaning+in+work"[tiab])) | 42 | 11 | 21 | 99 | **+37** | 37.4% |
| 5 | [`#1 AND "work meaning"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"work+meaning"[tiab])) | 6 | 1 | 2 | 104 | **+5** | 4.8% |
| 6 | [`#1 AND "sense of meaning"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"sense+of+meaning"[tiab])) | 48 | 12 | 21 | 149 | **+45** | 30.2% |

**Total**: 149 papers

---

## #2C Work Engagement

| Line | Term | Individual (All) | Individual (3y 2023+) | Individual (5y 2021+) | Cumulative (OR) | Added | % of Total |
|------|------|------------------|----------------------|----------------------|-----------------|-------|------------|
| 1 | [`#1 AND "work engagement"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"work+engagement"[tiab])) | 151 | 43 | 70 | 151 | **+151** | 100.0% |
| 2 | [`#1 AND vigor[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+vigor[tiab])) | 78 | 8 | 15 | 219 | **+68** | 31.1% |
| 3 | [`#1 AND dedication[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+dedication[tiab])) | 354 | 80 | 118 | 550 | **+331** | 60.2% |
| 4 | [`#1 AND absorption[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+absorption[tiab])) | 876 | 98 | 170 | 1,412 | **+862** | 61.0% |
| 5 | [`#1 AND "engaged at work"[tiab]`]() | 0 | 0 | 0 | 1,412 | 0 | 0.0% |

**Total**: 1,412 papers

---

## #2D Calling/Vocation

| Line | Term | Individual (All) | Individual (3y 2023+) | Individual (5y 2021+) | Cumulative (OR) | Added | % of Total |
|------|------|------------------|----------------------|----------------------|-----------------|-------|------------|
| 1 | [`#1 AND calling[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+calling[tiab])) | 948 | 123 | 218 | 948 | **+948** | 100.0% |
| 2 | [`#1 AND "career calling"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"career+calling"[tiab])) | 3 | 1 | 2 | 948 | 0 | 0.0% |
| 3 | [`#1 AND "vocational calling"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"vocational+calling"[tiab])) | 4 | 0 | 0 | 948 | 0 | 0.0% |
| 4 | [`#1 AND vocation*[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+vocation*[tiab])) | 1,009 | 106 | 173 | 1,941 | **+993** | 51.2% |
| 5 | [`#1 AND "calling orientation"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"calling+orientation"[tiab])) | 0 | 0 | 0 | 1,941 | 0 | 0.0% |

**Total**: 1,941 papers

---

## #2E Motivation

| Line | Term | Individual (All) | Individual (3y 2023+) | Individual (5y 2021+) | Cumulative (OR) | Added | % of Total |
|------|------|------------------|----------------------|----------------------|-----------------|-------|------------|
| 1 | [`#1 AND "prosocial motivation"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"prosocial+motivation"[tiab])) | 3 | 1 | 1 | 3 | **+3** | 100.0% |
| 2 | [`#1 AND "intrinsic motivation"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"intrinsic+motivation"[tiab])) | 139 | 38 | 67 | 141 | **+138** | 97.9% |
| 3 | [`#1 AND "work motivation"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"work+motivation"[tiab])) | 47 | 13 | 18 | 184 | **+43** | 23.4% |
| 4 | [`#1 AND (motivat*[tiab] AND (work*[tiab] OR job*[tiab] OR career*[tiab] OR professional*[tiab] OR workplace[tiab])`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+(motivat*[tiab]+AND+(work*[tiab]+OR+job*[tiab]+OR+career*[tiab]+OR+professional*[tiab]+OR+workplace[tiab])))) | 4,081 | 852 | 1,436 | 4,133 | **+3,949** | 95.5% |

**Total**: 4,133 papers

---

## #2F Satisfaction

| Line | Term | Individual (All) | Individual (3y 2023+) | Individual (5y 2021+) | Cumulative (OR) | Added | % of Total |
|------|------|------------------|----------------------|----------------------|-----------------|-------|------------|
| 1 | [`#1 AND "job satisfaction"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"job+satisfaction"[tiab])) | 2,141 | 465 | 721 | 2,141 | **+2,141** | 100.0% |
| 2 | [`#1 AND "career satisfaction"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"career+satisfaction"[tiab])) | 519 | 87 | 137 | 2,576 | **+435** | 16.9% |
| 3 | [`#1 AND "professional satisfaction"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"professional+satisfaction"[tiab])) | 313 | 54 | 85 | 2,840 | **+264** | 9.3% |
| 4 | [`#1 AND "work satisfaction"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"work+satisfaction"[tiab])) | 248 | 48 | 86 | 3,018 | **+178** | 5.9% |
| 5 | [`#1 AND "workplace satisfaction"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"workplace+satisfaction"[tiab])) | 34 | 11 | 18 | 3,041 | **+23** | 0.8% |

**Total**: 3,041 papers

---

## #2G Professional Fulfillment

| Line | Term | Individual (All) | Individual (3y 2023+) | Individual (5y 2021+) | Cumulative (OR) | Added | % of Total |
|------|------|------------------|----------------------|----------------------|-----------------|-------|------------|
| 1 | [`#1 AND "professional fulfillment"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"professional+fulfillment"[tiab])) | 199 | 99 | 152 | 199 | **+199** | 100.0% |
| 2 | [`#1 AND "career fulfillment"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"career+fulfillment"[tiab])) | 9 | 4 | 6 | 208 | **+9** | 4.3% |
| 3 | [`#1 AND fulfillment[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+fulfillment[tiab])) | 655 | 183 | 288 | 655 | **+447** | 68.2% |
| 4 | [`#1 AND "professional well-being"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"professional+well-being"[tiab])) | 77 | 43 | 55 | 719 | **+64** | 8.9% |
| 5 | [`#1 AND "professional wellbeing"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"professional+wellbeing"[tiab])) | 15 | 6 | 8 | 733 | **+14** | 1.9% |

**Total**: 733 papers

---

## #2H Japanese Concepts

| Line | Term | Individual (All) | Individual (3y 2023+) | Individual (5y 2021+) | Cumulative (OR) | Added | % of Total |
|------|------|------------------|----------------------|----------------------|-----------------|-------|------------|
| 1 | [`#1 AND ikigai[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+ikigai[tiab])) | 3 | 2 | 3 | 3 | **+3** | 100.0% |
| 2 | [`#1 AND "iki-gai"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"iki-gai"[tiab])) | 0 | 0 | 0 | 3 | 0 | 0.0% |
| 3 | [`#1 AND yarigai[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+yarigai[tiab])) | 1 | 1 | 1 | 3 | 0 | 0.0% |
| 4 | [`#1 AND "yari-gai"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"yari-gai"[tiab])) | 0 | 0 | 0 | 3 | 0 | 0.0% |

**Total**: 3 papers

---

## #2I Psychological Needs

| Line | Term | Individual (All) | Individual (3y 2023+) | Individual (5y 2021+) | Cumulative (OR) | Added | % of Total |
|------|------|------------------|----------------------|----------------------|-----------------|-------|------------|
| 1 | [`#1 AND (autonomy[tiab] AND work*[tiab])`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+(autonomy[tiab]+AND+work*[tiab]))) | 1,411 | 331 | 520 | 1,411 | **+1,411** | 100.0% |
| 2 | [`#1 AND (competence[tiab] AND work*[tiab])`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+(competence[tiab]+AND+work*[tiab]))) | 1,736 | 377 | 588 | 3,084 | **+1,673** | 54.2% |
| 3 | [`#1 AND (relatedness[tiab] AND work*[tiab])`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+(relatedness[tiab]+AND+work*[tiab]))) | 93 | 15 | 26 | 3,155 | **+71** | 2.3% |
| 4 | [`#1 AND "self-determination"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"self-determination"[tiab])) | 588 | 76 | 139 | 3,699 | **+544** | 14.7% |

**Total**: 3,699 papers

---

## #2J Task Significance

| Line | Term | Individual (All) | Individual (3y 2023+) | Individual (5y 2021+) | Cumulative (OR) | Added | % of Total |
|------|------|------------------|----------------------|----------------------|-----------------|-------|------------|
| 1 | [`#1 AND "task significance"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"task+significance"[tiab])) | 1 | 0 | 1 | 1 | **+1** | 100.0% |
| 2 | [`#1 AND "work significance"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"work+significance"[tiab])) | 1 | 0 | 0 | 2 | **+1** | 50.0% |
| 3 | [`#1 AND "job significance"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"job+significance"[tiab])) | 2 | 0 | - | 4 | **+2** | 50.0% |
| 4 | [`#1 AND "meaningful work"[tiab]`](https://pubmed.ncbi.nlm.nih.gov/?term=(("Physicians"[Mesh]+OR+physician*[tiab])+AND+"meaningful+work"[tiab])) | 50 | 18 | 26 | 54 | **+50** | 92.6% |

**Total**: 54 papers

---

# サマリー

## #2 各ブロック総ヒット数（全期間／5年／3年）

| Block | All-time | 5y (2021+) | 3y (2023+) |
|-------|----------|-------------|------------|
| #2A MeSH Terms | 13,511 | 2,339 | 1,242 |
| #2B Meaningful Work | 149 | 70 | 40 |
| #2C Work Engagement | 1,412 | 357 | 218 |
| #2D Calling/Vocation | 1,941 | 390 | 228 |
| #2E Motivation | 4,133 | 1,461 | 865 |
| #2F Satisfaction | 3,041 | 980 | 626 |
| #2G Professional Fulfillment | 733 | 339 | 221 |
| #2H Japanese Concepts | 3 | 3 | 2 |
| #2I Psychological Needs | 3,699 | 1,215 | 763 |
| #2J Task Significance | 54 | 27 | 18 |

※ `tests/get_block_totals_by_period.py` の結果を `tests/block_totals_by_period.md/.json` に保存

## #2 Concept Block 全体（46行をORで結合）

| 期間 | ヒット数 |
|------|----------|
| 全期間 | 24,278 |
| 5年限定 (2021+) | 5,860 |
| 3年限定 (2023+) | 3,401 |

※ `tests/get_final_concept_block_count.py` の結果を `tests/final_concept_block_count_20251110.md` に保存
