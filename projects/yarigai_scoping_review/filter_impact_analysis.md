# フィルター効果分析レポート

生成日時: 2025-11-05 14:11:27

## 分析目的

検索結果を2桁絞り込むために、各種フィルターの効果を段階的に測定。

## フィルター適用順序

1. **Base**: フィルターなし (#1 AND #2X)
2. **+10 years**: 過去10年フィルター追加
3. **+Animal**: 動物除外フィルター追加
4. **Both**: 10年 + 動物除外
5. **+Humans**: Humans[Mesh]追加
6. **+Language**: English OR Japanese追加
7. **+PubType**: Editorial/Letter/Comment除外

---

## サマリーテーブル

| Block | Base | +10y | +Animal | Both | +Humans | +Lang | +PubType | Total Reduction |
|-------|------|------|---------|------|---------|-------|----------|-----------------|
| #2A MeSH | 47,968 | 16,576 | 47,956 | 16,569 | 16,328 | 15,500 | 14,532 | -33,436 (69.7%) |
| #2B Meaningful Work | 205 | 172 | 205 | 172 | 138 | 138 | 136 | -69 (33.7%) |
| #2C Work Engagement | 2,816 | 1,429 | 2,759 | 1,410 | 989 | 942 | 926 | -1,890 (67.1%) |
| #2D Calling | 3,374 | 1,558 | 3,370 | 1,554 | 1,252 | 1,167 | 1,142 | -2,232 (66.2%) |
| #2E Motivation | 16,572 | 9,857 | 16,553 | 9,843 | 7,456 | 7,065 | 7,016 | -9,556 (57.7%) |
| #2F Satisfaction | 3,985 | 2,456 | 3,984 | 0 | 1,962 | 1,876 | 1,841 | -2,144 (53.8%) |
| #2G Fulfillment | 1,318 | 884 | 1,316 | 884 | 683 | 649 | 631 | -687 (52.1%) |
| #2H Japanese | 3 | 3 | 3 | 3 | 3 | 3 | 2 | -1 (33.3%) |
| #2I Psych Needs | 18,590 | 10,389 | 18,583 | 10,384 | 8,111 | 7,620 | 7,484 | -11,106 (59.7%) |
| #2J Task Significance | 14 | 10 | 14 | 10 | 9 | 9 | 9 | -5 (35.7%) |
| **TOTAL** | **94,845** | - | - | - | - | - | **33,719** | **-61,126 (64.4%)** |

---

## 各ブロック詳細

### #2A MeSH

**検索式:**
```
"Personal Satisfaction"[Mesh] OR "Job Satisfaction"[Mesh] OR "Motivation"[Mesh] OR "Professional Role"[Mesh] OR "Professional Autonomy"[Mesh] OR "Career Choice"[Mesh]
```

| Filter Stage | Hit Count | Reduction from Previous | Reduction from Base |
|--------------|-----------|-------------------------|---------------------|
| Base | 47,968 | - | - |
| +10 years | 16,576 | -31,392 (65.4%) | -31,392 (65.4%) |
| +Animal | 47,956 | --31,380 (-189.3%) | -12 (0.0%) |
| Both (10y+Animal) | 16,569 | -31,387 (65.4%) | -31,399 (65.5%) |
| +Humans | 16,328 | -241 (1.5%) | -31,640 (66.0%) |
| +Language | 15,500 | -828 (5.1%) | -32,468 (67.7%) |
| +PubType | 14,532 | -968 (6.2%) | -33,436 (69.7%) |

### #2B Meaningful Work

**検索式:**
```
"meaningful work"[tiab] OR "work meaningfulness"[tiab] OR "meaningfulness of work"[tiab] OR "meaning in work"[tiab] OR "work meaning"[tiab] OR "sense of meaning"[tiab]
```

| Filter Stage | Hit Count | Reduction from Previous | Reduction from Base |
|--------------|-----------|-------------------------|---------------------|
| Base | 205 | - | - |
| +10 years | 172 | -33 (16.1%) | -33 (16.1%) |
| +Animal | 205 | --33 (-19.2%) | -0 (0.0%) |
| Both (10y+Animal) | 172 | -33 (16.1%) | -33 (16.1%) |
| +Humans | 138 | -34 (19.8%) | -67 (32.7%) |
| +Language | 138 | -0 (0.0%) | -67 (32.7%) |
| +PubType | 136 | -2 (1.4%) | -69 (33.7%) |

### #2C Work Engagement

**検索式:**
```
"work engagement"[tiab] OR vigor[tiab] OR dedication[tiab] OR absorption[tiab]
```

| Filter Stage | Hit Count | Reduction from Previous | Reduction from Base |
|--------------|-----------|-------------------------|---------------------|
| Base | 2,816 | - | - |
| +10 years | 1,429 | -1,387 (49.3%) | -1,387 (49.3%) |
| +Animal | 2,759 | --1,330 (-93.1%) | -57 (2.0%) |
| Both (10y+Animal) | 1,410 | -1,349 (48.9%) | -1,406 (49.9%) |
| +Humans | 989 | -421 (29.9%) | -1,827 (64.9%) |
| +Language | 942 | -47 (4.8%) | -1,874 (66.5%) |
| +PubType | 926 | -16 (1.7%) | -1,890 (67.1%) |

### #2D Calling

**検索式:**
```
calling[tiab] OR vocation*[tiab]
```

| Filter Stage | Hit Count | Reduction from Previous | Reduction from Base |
|--------------|-----------|-------------------------|---------------------|
| Base | 3,374 | - | - |
| +10 years | 1,558 | -1,816 (53.8%) | -1,816 (53.8%) |
| +Animal | 3,370 | --1,812 (-116.3%) | -4 (0.1%) |
| Both (10y+Animal) | 1,554 | -1,816 (53.9%) | -1,820 (53.9%) |
| +Humans | 1,252 | -302 (19.4%) | -2,122 (62.9%) |
| +Language | 1,167 | -85 (6.8%) | -2,207 (65.4%) |
| +PubType | 1,142 | -25 (2.1%) | -2,232 (66.2%) |

### #2E Motivation

**検索式:**
```
"intrinsic motivation"[tiab] OR motivat*[tiab]
```

| Filter Stage | Hit Count | Reduction from Previous | Reduction from Base |
|--------------|-----------|-------------------------|---------------------|
| Base | 16,572 | - | - |
| +10 years | 9,857 | -6,715 (40.5%) | -6,715 (40.5%) |
| +Animal | 16,553 | --6,696 (-67.9%) | -19 (0.1%) |
| Both (10y+Animal) | 9,843 | -6,710 (40.5%) | -6,729 (40.6%) |
| +Humans | 7,456 | -2,387 (24.3%) | -9,116 (55.0%) |
| +Language | 7,065 | -391 (5.2%) | -9,507 (57.4%) |
| +PubType | 7,016 | -49 (0.7%) | -9,556 (57.7%) |

### #2F Satisfaction

**検索式:**
```
"job satisfaction"[tiab] OR "work satisfaction"[tiab] OR "career satisfaction"[tiab] OR "professional satisfaction"[tiab] OR "compassion satisfaction"[tiab]
```

| Filter Stage | Hit Count | Reduction from Previous | Reduction from Base |
|--------------|-----------|-------------------------|---------------------|
| Base | 3,985 | - | - |
| +10 years | 2,456 | -1,529 (38.4%) | -1,529 (38.4%) |
| +Animal | 3,984 | --1,528 (-62.2%) | -1 (0.0%) |
| Both (10y+Animal) | 0 | -3,984 (100.0%) | -3,985 (100.0%) |
| +Humans | 1,962 | --1,962 (0.0%) | -2,023 (50.8%) |
| +Language | 1,876 | -86 (4.4%) | -2,109 (52.9%) |
| +PubType | 1,841 | -35 (1.9%) | -2,144 (53.8%) |

### #2G Fulfillment

**検索式:**
```
"professional fulfillment"[tiab] OR "professional quality of life"[tiab] OR "quality of professional life"[tiab] OR fulfillment[tiab] OR fulfilment[tiab]
```

| Filter Stage | Hit Count | Reduction from Previous | Reduction from Base |
|--------------|-----------|-------------------------|---------------------|
| Base | 1,318 | - | - |
| +10 years | 884 | -434 (32.9%) | -434 (32.9%) |
| +Animal | 1,316 | --432 (-48.9%) | -2 (0.2%) |
| Both (10y+Animal) | 884 | -432 (32.8%) | -434 (32.9%) |
| +Humans | 683 | -201 (22.7%) | -635 (48.2%) |
| +Language | 649 | -34 (5.0%) | -669 (50.8%) |
| +PubType | 631 | -18 (2.8%) | -687 (52.1%) |

### #2H Japanese

**検索式:**
```
ikigai[tiab]
```

| Filter Stage | Hit Count | Reduction from Previous | Reduction from Base |
|--------------|-----------|-------------------------|---------------------|
| Base | 3 | - | - |
| +10 years | 3 | -0 (0.0%) | -0 (0.0%) |
| +Animal | 3 | -0 (0.0%) | -0 (0.0%) |
| Both (10y+Animal) | 3 | -0 (0.0%) | -0 (0.0%) |
| +Humans | 3 | -0 (0.0%) | -0 (0.0%) |
| +Language | 3 | -0 (0.0%) | -0 (0.0%) |
| +PubType | 2 | -1 (33.3%) | -1 (33.3%) |

### #2I Psych Needs

**検索式:**
```
"psychological need*"[tiab] OR autonomy[tiab] OR competence[tiab] OR relatedness[tiab] OR "thriving at work"[tiab] OR thriving[tiab]
```

| Filter Stage | Hit Count | Reduction from Previous | Reduction from Base |
|--------------|-----------|-------------------------|---------------------|
| Base | 18,590 | - | - |
| +10 years | 10,389 | -8,201 (44.1%) | -8,201 (44.1%) |
| +Animal | 18,583 | --8,194 (-78.9%) | -7 (0.0%) |
| Both (10y+Animal) | 10,384 | -8,199 (44.1%) | -8,206 (44.1%) |
| +Humans | 8,111 | -2,273 (21.9%) | -10,479 (56.4%) |
| +Language | 7,620 | -491 (6.1%) | -10,970 (59.0%) |
| +PubType | 7,484 | -136 (1.8%) | -11,106 (59.7%) |

### #2J Task Significance

**検索式:**
```
"task significance"[tiab] OR "meaningful task*"[tiab] OR "work significance"[tiab]
```

| Filter Stage | Hit Count | Reduction from Previous | Reduction from Base |
|--------------|-----------|-------------------------|---------------------|
| Base | 14 | - | - |
| +10 years | 10 | -4 (28.6%) | -4 (28.6%) |
| +Animal | 14 | --4 (-40.0%) | -0 (0.0%) |
| Both (10y+Animal) | 10 | -4 (28.6%) | -4 (28.6%) |
| +Humans | 9 | -1 (10.0%) | -5 (35.7%) |
| +Language | 9 | -0 (0.0%) | -5 (35.7%) |
| +PubType | 9 | -0 (0.0%) | -5 (35.7%) |

---

## 結論と推奨事項

### 最も効果的なフィルター

各フィルターの平均削減率（全ブロック平均）:

| Filter | Avg Reduction % | Comment |
|--------|-----------------|---------|
| 10 years | 36.9% | |
| Humans | 14.9% | |
| PubType | 5.2% | |
| Language | 3.7% | |
| Animal exclusion | 0.2% | |

### 推奨フィルター組み合わせ

- **Conservative (保守的)**: 10年 + 動物除外 → 約X%削減
- **Moderate (中程度)**: 上記 + Humans + Language → 約Y%削減
- **Aggressive (積極的)**: 上記 + PubType除外 → 約Z%削減
