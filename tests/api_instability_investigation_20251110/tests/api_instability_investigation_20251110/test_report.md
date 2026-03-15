# Test Report for Fixed check_block_overlap.py

## Test Date

2025-11-10T14:24:15.670711

## Test Results

✓ **All tests passed**

## Analysis Report

## Test Block - Hit Count Analysis

| Line | Term | Individual Count | Cumulative (OR) | Added | % of Total |
|------|------|------------------|-----------------|-------|------------|
| 1 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "meaningful work"[tiab])` | 50 | 50 | **+50** | 4.1% |
| 2 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "work engagement"[tiab])` | 151 | 200 | **+150** | 12.4% |
| 3 | `(("Physicians"[Mesh] OR physician*[tiab]) AND vigor[tiab])` | 78 | 268 | **+68** | 5.6% |
| 4 | `(("Physicians"[Mesh] OR physician*[tiab]) AND calling[tiab])` | 948 | 1,213 | **+945** | 77.9% |

### Summary

- **Total unique papers**: 1,213
- **Most effective term**: Line 4 (+945 papers, 77.9% of total)

### Final Combined Query

```
((("Physicians"[Mesh] OR physician*[tiab]) AND "meaningful work"[tiab])) OR ((("Physicians"[Mesh] OR physician*[tiab]) AND "work engagement"[tiab])) OR ((("Physicians"[Mesh] OR physician*[tiab]) AND vigor[tiab])) OR ((("Physicians"[Mesh] OR physician*[tiab]) AND calling[tiab]))
```
