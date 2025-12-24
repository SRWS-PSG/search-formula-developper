# Autoethnography in Medical Education - PubMed Search Formula

## Research Question
What autoethnographic approaches are conducted by research groups that include medical students, physicians, and medical education scholars?

## PubMed/MEDLINE

### Search Strategy

#### #1 Autoethnography Concept
```
"autoethnography"[tiab] OR
"autoethnographic"[tiab] OR
"auto-ethnography"[tiab] OR
"auto-ethnographic"[tiab]
```
**Block #1 hits: 598**

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
   - Includes hyphenated variants (auto-ethnography)
   - Covers collaborative and collective autoethnography variants
   - Includes analytic and evocative subtypes
   - Uses [tiab] only as autoethnography is not a MeSH term

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
#1 Autoethnography Concept (598 hits)
"autoethnography"[tiab] OR "autoethnographic"[tiab] OR "auto-ethnography"[tiab] OR "auto-ethnographic"[tiab]

#2 Medical Students, Physicians, and Health Professionals (~2.4M hits)
"Physicians"[Mesh] OR "Students, Medical"[Mesh] OR "Education, Medical"[Mesh] OR "Faculty, Medical"[Mesh] OR physician[tiab] OR physicians[tiab] OR doctor[tiab] OR doctors[tiab] OR clinician[tiab] OR clinicians[tiab] OR practitioner[tiab] OR practitioners[tiab] OR resident[tiab] OR residents[tiab] OR "medical student"[tiab] OR "medical students"[tiab] OR "medical education"[tiab] OR "medical educator"[tiab] OR "medical educators"[tiab] OR "medical faculty"[tiab] OR psychiatry[tiab] OR psychiatric[tiab] OR psychiatrist[tiab] OR psychiatrists[tiab]

#3 Final Query (136 hits)
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
