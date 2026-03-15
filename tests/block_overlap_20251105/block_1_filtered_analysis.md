# Search Block Overlap Analysis

Analysis Date: 2025-11-05 14:26:01

Input File: temp_block_1.txt

## #1 Population (with 10y + Animal filters) - Hit Count Analysis

| Line | Term | Individual Count | Cumulative (OR) | Added | % of Total |
|------|------|------------------|-----------------|-------|------------|
| 1 | `("2015/01/01"[PDAT] : "3000"[PDAT]) NOT (animals[Mesh] NOT humans[Mesh]) AND (` | 13,653,979 | 13,653,979 | **+13,653,979** | 96.0% |
| 2 | `"Physicians"[Mesh]` | 194,555 | 13,757,231 | **+103,252** | 0.7% |
| 3 | `physician*[tiab]` | 510,049 | 14,006,248 | **+249,017** | 1.8% |
| 4 | `doctor*[tiab]` | 171,596 | 14,075,803 | **+69,555** | 0.5% |
| 5 | `"general practitioner*"[tiab]` | 63,212 | 14,099,429 | **+23,626** | 0.2% |
| 6 | `clinician*[tiab]` | 366,281 | 14,223,482 | **+124,053** | 0.9% |
| 7 | `)` | 0 | 14,223,482 | **+0** | 0.0% |

### Summary

- **Total unique papers**: 14,223,482
- **Most effective term**: Line 1 (+13,653,979 papers, 96.0% of total)
- **Low-value terms** (Added < 1% of total): Lines 2, 4, 5, 6, 7

### Final Combined Query

```
(("2015/01/01"[PDAT] : "3000"[PDAT]) NOT (animals[Mesh] NOT humans[Mesh]) AND () OR ("Physicians"[Mesh]) OR (physician*[tiab]) OR (doctor*[tiab]) OR ("general practitioner*"[tiab]) OR (clinician*[tiab]) OR ())
```
