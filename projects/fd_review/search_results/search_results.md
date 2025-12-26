# Search Strategy and Results Summary

## Systematic Review: Faculty Development for Physicians

本ドキュメントは、医師向けFaculty Development（FD）プログラムに関するスコーピングレビューの検索戦略と結果をまとめたものです。

---

## Summary Table

| Database | Search Date | Number of Results |
|----------|-------------|-------------------|
| PubMed/MEDLINE | 2025-12-26 | 2,832 |
| ERIC | 2025-12-26 | 225 |
| ProQuest (Dialog) | 2025-12-25 | 2,144 |
| CENTRAL (Cochrane Library) | 2025-12-25 | 22 |
| **Total (before deduplication)** | - | **5,223** |

---

## PubMed/MEDLINE

### Search Date
2025-12-26

### Search Strategy

```
#1 "Faculty, Medical"[Majr] OR medical faculty[tiab] OR clinical educator*[tiab] OR clinician educator*[tiab] OR medical educator*[tiab] OR clinical teacher*[tiab] OR clinical teaching[tiab]

#2 "Staff Development"[Mesh] OR "Program Development"[Mesh] OR faculty development*[tiab] OR professional development*[tiab] OR teaching skill*[tiab] OR "program design"[tiab]

#3 #1 AND #2
```

### Results
2,832 records

---

## ERIC (Education Resources Information Center)

### Search Date
2025-12-26

### Search Strategy

```
#1 (subject:"Medical School Faculty" OR title:"medical faculty" OR title:"clinical educator" OR title:"clinician educator" OR title:"medical educator" OR title:"clinical teacher" OR title:"clinical teaching")

#2 (subject:"Faculty Development" OR subject:"Professional Development" OR subject:"Staff Development" OR subject:"Program Development" OR subject:"Program Design" OR title:"faculty development" OR title:"professional development" OR title:"teaching skill" OR title:"program design")

#3 #1 AND #2
```

### Results
225 records

---

## ProQuest (Dialog)

### Search Date
2025-12-25

### Search Strategy

| Line | Search Terms | Hits |
|------|--------------|------|
| S1 | MJEMB.EXACT("medical school") OR TI("medical faculty" OR "clinical educator*" OR "clinician educator*" OR "medical educator*" OR "clinical teacher*" OR "clinical teaching") OR AB("medical faculty" OR "clinical educator*" OR "clinician educator*" OR "medical educator*" OR "clinical teacher*" OR "clinical teaching") | 39,042 |
| S2 | EMB.EXACT.EXPLODE("personnel management") OR EMB.EXACT.EXPLODE("program development") OR TI("faculty development*" OR "professional development*" OR "staff development" OR "program development" OR "teaching skill*" OR "program design") OR AB("faculty development*" OR "professional development*" OR "staff development" OR "program development" OR "teaching skill*" OR "program design") | 169,712 |
| S3 | S1 AND S2 | 2,964 |
| S4 | (S1 AND S2) AND (fdb(embase) AND (rtype.exact("Article" OR "Article in Press"))) | 2,144 |

### Results
2,144 records

---

## CENTRAL (Cochrane Library)

### Search Date
2025-12-25 22:13:43

### Search Strategy

| Line | Search Terms | Hits |
|------|--------------|------|
| #1 | (medical NEXT faculty):ti,ab,kw OR (clinical NEXT educator*):ti,ab,kw OR (clinician NEXT educator*):ti,ab,kw OR (medical NEXT educator*):ti,ab,kw OR (clinical NEXT teacher*):ti,ab,kw OR (clinical NEXT teaching):ti,ab,kw | 744 |
| #2 | [mh "Staff Development"] | 108 |
| #3 | [mh "Program Development"] | 960 |
| #4 | (faculty NEXT development*):ti,ab,kw OR (professional NEXT development*):ti,ab,kw OR (staff NEXT development):ti,ab,kw OR (program NEXT development):ti,ab,kw OR (teaching NEXT skill*):ti,ab,kw OR (program NEXT design):ti,ab,kw | 3,105 |
| #5 | #2 OR #3 OR #4 | 3,105 |
| #6 | #1 AND #5 | 22 |

### Results
22 records

---

## Notes

- **Language restriction**: None (all languages with English abstracts included)
- **Date restriction**: None (all publication years included)
- **Study design restriction**: None (all study designs included for scoping review)

---

## Deduplication Results

重複削除処理（タイトルのExact Match）を実行し、以下の結果を得た。

| 項目 | 件数 |
|------|------|
| 入力レコード総数 | 5,223 |
| 重複タイトル | 184 |
| **ユニークレコード数** | **5,039** |

### 処理詳細

- **実行日時**: 2025-12-26
- **正規化処理**: 小文字化、空白正規化、角括弧`[]`削除
- **戦略**: keep-first（最初に出現したレコードを保持）
- **ログファイル**: `dedup_log.txt`

---

## Source Files

| Database | Export File |
|----------|-------------|
| PubMed/MEDLINE | `20251226_2832_pubmed.ris` |
| ERIC | `20251226_225_eric.ris` |
| ProQuest (Dialog) | `ProQuestDocuments-2025-12-25.ris` |
| CENTRAL | `citation-export.ris` |
| **Merged (deduplicated)** | **`merged_deduplicated.ris`** |

