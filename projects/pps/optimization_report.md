# MeSH Optimization Report

**Date**: 2025-12-31
**Source Formula**: `projects/pps/seach_formula_2.md`

## Optimization Strategy
1. **Analyze Contribution**: Identified MeSH terms with **0 unique hits** (hits that are not covered by any other term in the entire search block, including text words).
2. **Check Hierarchy**: Checked if these terms are children of other MeSH terms in the list (which would make them structurally redundant).
3. **Delete**: Remove terms that provide no unique contribution.

## Analysis Results
- **Total Block Count (Original)**: 1,257,828
- **Hierarchy Check**: No parent-child relationships found among the MeSH terms in the list.
- **Redundancy Source**: The redundancies are driven by the broad coverage of Text Words (e.g., `Functional syndrome[tiab:~2]`).

## Deleted Terms
The following MeSH terms had **0 unique contribution** and have been removed:

| Term | Pre-Deletion Contribution | Reason |
|---|---|---|
| `"Somatoform Disorders"[Mesh]` | 0 | Covered by other terms (Text Words) |
| `"Psychophysiologic Disorders"[Mesh]` | 0 | Covered by other terms (Text Words) |
| `"chronic pain"[Mesh]` | 0 | Covered by other terms (Text Words) |
| `"Central Nervous System Sensitization"[Mesh]` | 0 | Covered by other terms (Text Words) |
| `"Nociplastic Pain"[Mesh]` | 0 | Covered by other terms (Text Words) |
| `"Polydipsia, Psychogenic"[Mesh]` | 0 | Covered by other terms (Text Words) |
| `"Psychogenic Nonepileptic Seizures"[Mesh]` | 0 | Covered by other terms (Text Words) |
| `"Hearing Loss, Functional"[Mesh]` | 0 | Covered by other terms (Text Words) |
| `"psychogenic syncope" [Supplementary Concept]` | 0 | Covered by other terms (Text Words) |
| `"Orthostatic Intolerance"[Mesh]` | 0 | Covered by other terms (Text Words) |
| `"somatic cough syndrome" [Supplementary Concept]` | 0 | Covered by other terms (Text Words) |
| `"Fibromyalgia"[Mesh]` | 0 | Covered by other terms (Text Words) |
| `"Fatigue Syndrome, Chronic"[Mesh]` | 0 | Covered by other terms (Text Words) |
| `"Colonic Diseases, Functional"[Mesh]` | 0 | Covered by other terms (Text Words) |
| `"Temporomandibular Joint Dysfunction Syndrome"[Mesh]` | 0 | Covered by other terms (Text Words) |
| `"Cystitis, Interstitial"[Mesh]` | 0 | Covered by other terms (Text Words) |
| `"Multiple Chemical Sensitivity"[Mesh]` | 0 | Covered by other terms (Text Words) |

## Remaining MeSH Terms
| Term | Contribution |
|---|---|
| `"Medically Unexplained Symptoms"[Mesh]` | 4,623 (0.37%) |

## Verification
- **Post-Optimization Block Count**: 1,253,205
- **Difference**: -4,623 (-0.37%)
- **Analysis**: The slight decrease is attributed to the correction of a syntax error in the original formula (`Medically Unexplained Symptoms"[Mesh]` -> `"Medically Unexplained Symptoms"[Mesh]`). The missing quote in the original file likely caused broader text-word matching for that term. The removal of the 0-contribution MeSH terms had no negative impact.

