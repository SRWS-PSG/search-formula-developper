# Test Report for Fixed check_block_overlap.py

## Test Date

2026-03-01T10:08:03.393934

## Test Results

✗ **Some tests failed**

## Analysis Report

## Test Block - Hit Count Analysis

| Line | Term | Individual Count | Cumulative (OR) | Added | % of Total |
|------|------|------------------|-----------------|-------|------------|
| 1 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "meaningful work"[tiab])` | 50 | 50 | **+50** | 4.1% |
| 2 | `(("Physicians"[Mesh] OR physician*[tiab]) AND "work engagement"[tiab])` | 155 | 204 | **+154** | 12.5% |
| 3 | `(("Physicians"[Mesh] OR physician*[tiab]) AND vigor[tiab])` | 79 | 272 | **+68** | 5.5% |
| 4 | `(("Physicians"[Mesh] OR physician*[tiab]) AND calling[tiab])` | 959 | 1,228 | **+956** | 77.9% |

### Summary

- **Total unique papers**: 1,228
- **Most effective term**: Line 4 (+956 papers, 77.9% of total)

### Final Combined Query

```
((("Physicians"[Mesh] OR physician*[tiab]) AND "meaningful work"[tiab])) OR ((("Physicians"[Mesh] OR physician*[tiab]) AND "work engagement"[tiab])) OR ((("Physicians"[Mesh] OR physician*[tiab]) AND vigor[tiab])) OR ((("Physicians"[Mesh] OR physician*[tiab]) AND calling[tiab]))
```
