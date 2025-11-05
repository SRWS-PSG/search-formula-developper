# Search Block Overlap Analysis

Analysis Date: 2025-11-05 14:19:59

Input File: temp_block_2i.txt

## #2I Psych Needs (with 10y + Animal filters) - Hit Count Analysis

| Line | Term | Individual Count | Cumulative (OR) | Added | % of Total |
|------|------|------------------|-----------------|-------|------------|
| 1 | `("Physicians"[Mesh] OR physician*[tiab] OR doctor*[tiab] OR "general practitione...` | 549,664 | 549,664 | **+549,664** | 78.9% |
| 2 | `"psychological need*"[tiab]` | 3,841 | 553,315 | **+3,651** | 0.5% |
| 3 | `autonomy[tiab]` | 48,114 | 595,524 | **+42,209** | 6.1% |
| 4 | `competence[tiab]` | 80,174 | 667,923 | **+72,399** | 10.4% |
| 5 | `relatedness[tiab]` | 26,624 | 692,792 | **+24,869** | 3.6% |
| 6 | `"thriving at work"[tiab]` | 98 | 692,882 | **+90** | 0.0% |
| 7 | `thriving[tiab]` | 4,581 | 697,100 | **+4,218** | 0.6% |
| 8 | `)` | 0 | 697,100 | **+0** | 0.0% |

### Summary

- **Total unique papers**: 697,100
- **Most effective term**: Line 1 (+549,664 papers, 78.9% of total)
- **Low-value terms** (Added < 1% of total): Lines 2, 6, 7, 8

### Final Combined Query

```
(("Physicians"[Mesh] OR physician*[tiab] OR doctor*[tiab] OR "general practitioner*"[tiab] OR clinician*[tiab]) AND ("2015/01/01"[PDAT] : "3000"[PDAT]) NOT (animals[Mesh] NOT humans[Mesh]) AND () OR ("psychological need*"[tiab]) OR (autonomy[tiab]) OR (competence[tiab]) OR (relatedness[tiab]) OR ("thriving at work"[tiab]) OR (thriving[tiab]) OR ())
```
