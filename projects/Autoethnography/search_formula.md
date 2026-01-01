# Autoethnography in Medical Education - Multi-Database Search Formula

## Research Question

What autoethnographic approaches are conducted by research groups that include medical students, physicians, and medical education scholars?

## Target Databases

1. **PubMed/MEDLINE** ✅ (136 hits)
2. **Embase (ProQuest Dialog)** - Pending (manual verification)
3. **ERIC** ✅ (3 hits) - verified 2025-12-29
4. **Anthropological Index Online (RAI)** ✅ (71 hits) - verified 2025-12-29
5. **PsycINFO** - Pending (manual verification)

---

## 1. PubMed/MEDLINE

### Search Strategy

#### #1 Autoethnography Concept

```
"autoethnography"[tiab] OR
"autoethnographic"[tiab] OR
"auto-ethnography"[tiab] OR
"auto-ethnographic"[tiab]
```

**Block #1 hits: 598** (text words only)
**Block #1 hits with MeSH: [To be verified]**

**Removed terms (0 additional papers):**

- "collaborative autoethnography"[tiab] - 59 papers (100% overlap)
- "collective autoethnography"[tiab] - 7 papers (100% overlap)
- "analytic autoethnography"[tiab] - 12 papers (100% overlap)
- "evocative autoethnography"[tiab] - 4 papers (100% overlap)

#### #2 Medical Students, Physicians, and Health Professionals

```
"Physicians"[Mesh] OR
"Students, Medical"[Mesh] OR
"Education, Medical"[Mesh] OR
"Faculty, Medical"[Mesh] OR
physician[tiab] OR
physicians[tiab] OR
doctor[tiab] OR
doctors[tiab] OR
clinician[tiab] OR
clinicians[tiab] OR
practitioner[tiab] OR
practitioners[tiab] OR
resident[tiab] OR
residents[tiab] OR
"medical student"[tiab] OR
"medical students"[tiab] OR
"medical education"[tiab] OR
"medical educator"[tiab] OR
"medical educators"[tiab] OR
"medical faculty"[tiab] OR
psychiatry[tiab] OR
psychiatric[tiab] OR
psychiatrist[tiab] OR
psychiatrists[tiab]
```

**Block #2 hits: ~2.4M** (focused on physicians, medical students, medical education, and mental health contexts)

**Key additions for sensitivity:**

- `clinician/clinicians`, `practitioner/practitioners`, `resident/residents` - Health professionals not explicitly labeled as physicians
- `psychiatry/psychiatric/psychiatrist`, `"mental health"[tiab]` - Mental health contexts

#### #3 Final Query

```
#1 AND #2
```

**Final query hits: 136**

**Seed paper validation: 39/46 (excluded 7 target papers)** ✅

**Filters:**

- Language: English (optional - consider removing to maximize sensitivity)
- Publication Type: No filters (to capture all study types including essays, commentaries, research articles)

---

## Notes

**Search Development Rationale:**

1. **Block #1 (Autoethnography)**:

   - Includes "Anthropology, Cultural"[Mesh] to capture indexed cultural anthropology literature
   - Includes hyphenated variants (auto-ethnography)
   - Covers collaborative and collective autoethnography variants
   - Includes analytic and evocative subtypes
   - Uses [tiab] for autoethnography terms as "autoethnography" is not a standalone MeSH term
2. **Block #2 (Population)**:

   - Combines MeSH terms with text word variants for sensitivity
   - Includes "Faculty, Medical"[Mesh] and "Education, Medical"[Mesh] to capture medical education scholars
   - Captures both singular and plural forms
   - Includes mental health context terms (psychiatry)
3. **Current approach** (based on protocol line 38): 96 hits in MEDLINE

   - This appears to be a reasonable result set for manual screening
   - High sensitivity is prioritized given the scoping review methodology

**Exclusion Criteria** (to be applied during screening, not in search):

- Studies focusing on narrative/reflective writing NOT explicitly described as autoethnographic
- Autoethnographies conducted by patients (without medical student/physician involvement)

**Next Steps:**

1. Validate search with seed papers (if available)
2. Consider testing with/without language filters
3. Consider expanding to include "intern"[tiab], "resident"[tiab] if needed
4. Plan searches for complementary databases: CINAHL, PsycINFO, Scopus, ERIC, Anthropology Plus

---

**Search History:**

- Formula created: 2025-12-17
- Based on: protocol.md lines 30-39
- Validated: 2025-12-17
  - Block #1: 598 hits
  - Block #2: Focused population block (removed health professions/general medical anthropology/bioethics terms)
  - Final query: **136 hits**
  - **Seed paper capture: 39/46 (excluded 7 target papers)** ✅
- Optimization iterations:
  - v1 (narrow): 52 hits, 29/46 seed capture (63%)
  - v2 (expanded): 165 hits, 40/46 seed capture (86%)
  - v3 (final): 136 hits, 39/46 seed capture (excluded 7 target papers)

---

## Appendix: Copy-Paste Format for Protocol

### PubMed/MEDLINE Search Strategy (Validated 2025-12-17)

**Database:** PubMed/MEDLINE
**Search Date:** [To be filled at execution]
**Results:** 136 citations
**Seed Paper Validation:** 39/46 (excluded 7 target papers) ✅

**Search Strategy:**

```
#1 Autoethnography Concept
"autoethnography"[tiab] OR "autoethnographic"[tiab] OR "auto-ethnography"[tiab] OR "auto-ethnographic"[tiab]

#2 Medical Students, Physicians, and Health Professionals
"Physicians"[Mesh] OR "Students, Medical"[Mesh] OR "Education, Medical"[Mesh] OR "Faculty, Medical"[Mesh] OR physician[tiab] OR physicians[tiab] OR doctor[tiab] OR doctors[tiab] OR clinician[tiab] OR clinicians[tiab] OR practitioner[tiab] OR practitioners[tiab] OR resident[tiab] OR residents[tiab] OR "medical student"[tiab] OR "medical students"[tiab] OR "medical education"[tiab] OR "medical educator"[tiab] OR "medical educators"[tiab] OR "medical faculty"[tiab] OR psychiatry[tiab] OR psychiatric[tiab] OR psychiatrist[tiab] OR psychiatrists[tiab]

#3 Final Query
#1 AND #2
```

**Filters Applied:** None (to maximize sensitivity for scoping review)

**Search Rationale:**

- Block #1 captures autoethnography and autoethnographic approaches, including hyphenated variants
- Block #2 expanded beyond physicians/medical students to include:
  - Health professionals (clinicians, practitioners, residents)
  - Mental health contexts (psychiatry, mental health)
  - Excludes general medical anthropology/bioethics and broader health professions terms

**Validation:**

- Seed paper validation: 39/46 papers captured (excluded 7 target papers)
- Overlap analysis performed on 2025-12-17
- Iterative expansion from 52 hits (63% capture) → 136 hits (excluded 7 target papers)
- Nursing-related terms excluded per protocol inclusion criteria (physicians/medical students/medical educators only)

---

## 2. Embase (ProQuest Dialog)

### Search Strategy

#### #1 Autoethnography Concept

```
TI,AB(autoethnography OR autoethnographic OR "auto-ethnography" OR "auto-ethnographic")
```

#### #2 Population (Emtree + Free text)

```
EMB.EXACT.EXPLODE("physician") OR EMB.EXACT.EXPLODE("medical student") OR EMB.EXACT.EXPLODE("medical education") OR EMB.EXACT.EXPLODE("medical school") OR TI,AB(physician OR physicians OR doctor OR doctors OR clinician* OR 
      practitioner* OR resident OR residents OR "medical student*" OR 
      "medical education" OR psychiatr*)
```

#### #3 Final Query

```
#1 AND #2
```

**Results:** [To be verified]

### Syntax Notes

| Element                | Dialog Syntax                 |
| ---------------------- | ----------------------------- |
| Title/Abstract         | `TI,AB(term)`               |
| Emtree Subject Heading | `EMB(term)` or `term/exp` |
| Truncation             | `*`                         |
| Proximity              | `NEAR/n`, `PRE/n`         |

---

## 3. ERIC

### Search Strategy

#### #1 Autoethnography Concept

```
autoethnography OR autoethnographic
```

**Block #1 hits: 1,159** (verified 2025-12-29)

> Note: ERIC uses auto-stemming, truncation `*` not required for title/abstract fields

#### #2 Population (ERIC Descriptors + Free text)

```
subject:"Medical Education" OR subject:"Medical Students" OR subject:"Physicians" OR
physician OR
doctor OR
clinician OR
practitioner OR
resident OR
psychiatry
```

**Block #2 hits: [To be verified]**

> Note: ERICのフリーテキスト検索では引用符なしで自動ステミングが適用されるため、単数形のみで複数形もカバーされます。

#### #3 Final Query

```
(autoethnography OR autoethnographic) AND (subject:"Medical Education" OR subject:"Medical Students" OR subject:"Physicians" OR physician OR doctor OR clinician OR practitioner OR resident OR psychiatry)
```

**Final query hits: 65** (verified 2026-01-01)

**Note:** 最初のカウント確認では40件でしたが、実際のダウンロード時には65件取得されました。ERIC APIの仕様により、カウントと実際の取得件数に差異が生じる場合があります。

### Verification Script

```bash
python projects/Autoethnography/verify_eric_search.py
```

---

## 4. Anthropological Index Online (RAI)

### Search Strategy

**Quick Search:**

```
Keyword 1: autoethnography (71 hits)
Keyword 2: autoethnographic (28 hits)
Combined (deduplicated): 99 hits
```

**Results: 99** (verified 2026-01-01)

### Notes

- URL: https://aio.therai.org.uk/
- RIS download available for all results
- Rate limiting recommended (100 searches/year free tier)

### Verification Script

```bash
# Download both searches
python scripts/search/aio/search_aio.py --keyword "autoethnography" --output log/aio_autoethnography.ris
python scripts/search/aio/search_aio.py --keyword "autoethnographic" --output log/aio_autoethnographic.ris

# Merge and deduplicate
python scripts/utils/merge_ris_files.py log/aio_autoethnography.ris log/aio_autoethnographic.ris -o log/aio_merged.ris
```

**Note:** AIOは単一キーワード検索のみサポートするため、2つの検索を個別実行し、後で統合・重複除去します。

---

## 5. PsycINFO

### Search Strategy

#### #1 Autoethnography Concept

```
TI ( autoethnography OR autoethnographic OR "auto-ethnography" OR "auto-ethnographic" ) OR
AB ( autoethnography OR autoethnographic OR "auto-ethnography" OR "auto-ethnographic" )
```

#### #2 Population (APA Thesaurus + Free text)

```
DE "Physicians" OR DE "Medical Students" OR DE "Medical Education" OR DE "Psychiatrists" OR
TI ( physician* OR doctor* OR clinician* OR practitioner* OR resident* OR 
     "medical student*" OR "medical education" OR psychiatr* ) OR
AB ( physician* OR doctor* OR clinician* OR practitioner* OR resident* OR 
     "medical student*" OR "medical education" OR psychiatr* )
```

#### #3 Final Query

```
S1 AND S2
```

**Results:** [To be verified manually]

### Syntax Notes

| Element       | PsycINFO Syntax |
| ------------- | --------------- |
| Title         | `TI (term)`   |
| Abstract      | `AB (term)`   |
| APA Thesaurus | `DE "term"`   |
| Truncation    | `*`           |
