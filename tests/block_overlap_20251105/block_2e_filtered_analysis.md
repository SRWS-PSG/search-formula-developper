# Search Block Overlap Analysis

Analysis Date: 2025-11-05 14:20:18

Input File: temp_block_2e.txt

## #2E Motivation (with 10y + Animal filters) - Hit Count Analysis

| Line | Term | Individual Count | Cumulative (OR) | Added | % of Total |
|------|------|------------------|-----------------|-------|------------|
| 1 | `("Physicians"[Mesh] OR physician*[tiab] OR doctor*[tiab] OR "general practitione...` | 549,664 | 549,664 | **+549,664** | 73.2% |
| 2 | `"intrinsic motivation"[tiab]` | 3,163 | 552,632 | **+2,968** | 0.4% |
| 3 | `motivat*[tiab]` | 211,169 | 750,990 | **+198,358** | 26.4% |
| 4 | `)` | 0 | 750,990 | **+0** | 0.0% |

### Summary

- **Total unique papers**: 750,990
- **Most effective term**: Line 1 (+549,664 papers, 73.2% of total)
- **Low-value terms** (Added < 1% of total): Lines 2, 4

### Final Combined Query

```
(("Physicians"[Mesh] OR physician*[tiab] OR doctor*[tiab] OR "general practitioner*"[tiab] OR clinician*[tiab]) AND ("2015/01/01"[PDAT] : "3000"[PDAT]) NOT (animals[Mesh] NOT humans[Mesh]) AND () OR ("intrinsic motivation"[tiab]) OR (motivat*[tiab]) OR ())
```
