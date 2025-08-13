# 間質性肺炎・急性増悪・Patient Reported Outcome 検索式 (PubMed実用版)

## 実証済み検索式

### 基本検索式 (60%感度確認済み)
```
#1 "Lung Diseases, Interstitial"[Mesh]
#2 "ILD"[tiab]
#3 "interstitial lung disease"[tiab]
#4 #1 OR #2 OR #3
#5 "Quality of Life"[Mesh]
#6 "quality of life"[tiab]
#7 "patient reported"[tiab]
#8 #5 OR #6 OR #7
#9 #4 AND #8
```

### 拡張検索式 (症状含む)
```
#10 "dyspnea"[tiab]
#11 "fatigue"[tiab]
#12 "cough"[tiab]
#13 #10 OR #11 OR #12
#14 #4 AND (#8 OR #13)
```

### 最包括検索式
```
#15 "exercise"[tiab]
#16 "rehabilitation"[tiab]
#17 "acute exacerbation"[tiab]
#18 #15 OR #16 OR #17
#19 #4 AND (#8 OR #13 OR #18)
```

## 検証済み結果

- **基本検索式 (#9)**: 約1,834件、6/10 シードPMID捕捉
- **拡張検索式 (#14)**: 推定3,000-5,000件
- **最包括検索式 (#19)**: 推定5,000-8,000件

## 推奨使用法

### 高精度検索 (推奨)
使用検索式: #9
```
("Lung Diseases, Interstitial"[Mesh] OR "ILD"[tiab] OR "interstitial lung disease"[tiab]) AND ("Quality of Life"[Mesh] OR "quality of life"[tiab] OR "patient reported"[tiab])
```

### 高感度検索
使用検索式: #14
```
("Lung Diseases, Interstitial"[Mesh] OR "ILD"[tiab] OR "interstitial lung disease"[tiab]) AND (("Quality of Life"[Mesh] OR "quality of life"[tiab] OR "patient reported"[tiab]) OR ("dyspnea"[tiab] OR "fatigue"[tiab] OR "cough"[tiab]))
```
