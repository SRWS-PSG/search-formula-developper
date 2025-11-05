# Search Block Overlap Analysis

Analysis Date: 2025-11-05 14:19:13

Input File: temp_block_2a.txt

## #2A MeSH (with 10y + Animal filters) - Hit Count Analysis

| Line | Term | Individual Count | Cumulative (OR) | Added | % of Total |
|------|------|------------------|-----------------|-------|------------|
| 1 | `("Physicians"[Mesh] OR physician*[tiab] OR doctor*[tiab] OR "general practitione...` | 549,664 | 549,664 | **+549,664** | 60.6% |
| 2 | `"Personal Satisfaction"[Mesh]` | 28,347 | 576,734 | **+27,070** | 3.0% |
| 3 | `"Job Satisfaction"[Mesh]` | 31,323 | 604,449 | **+27,715** | 3.1% |
| 4 | `"Motivation"[Mesh]` | 208,497 | 802,072 | **+197,623** | 21.8% |
| 5 | `"Professional Role"[Mesh]` | 91,929 | 882,806 | **+80,734** | 8.9% |
| 6 | `"Professional Autonomy"[Mesh]` | 9,849 | 888,244 | **+5,438** | 0.6% |
| 7 | `"Career Choice"[Mesh]` | 27,060 | 907,013 | **+18,769** | 2.1% |
| 8 | `)` | 0 | 907,013 | **+0** | 0.0% |

### Summary

- **Total unique papers**: 907,013
- **Most effective term**: Line 1 (+549,664 papers, 60.6% of total)
- **Low-value terms** (Added < 1% of total): Lines 6, 8

### Final Combined Query

```
(("Physicians"[Mesh] OR physician*[tiab] OR doctor*[tiab] OR "general practitioner*"[tiab] OR clinician*[tiab]) AND ("2015/01/01"[PDAT] : "3000"[PDAT]) NOT (animals[Mesh] NOT humans[Mesh]) AND () OR ("Personal Satisfaction"[Mesh]) OR ("Job Satisfaction"[Mesh]) OR ("Motivation"[Mesh]) OR ("Professional Role"[Mesh]) OR ("Professional Autonomy"[Mesh]) OR ("Career Choice"[Mesh]) OR ())
```
