# 間質性肺炎・急性増悪・Patient Reported Outcome 検索式 (PubMed最終版)

## Pearl Growing分析に基づく最適化

### シードPMID分析結果
- ILD単独検索: 9/10 PMIDを捕捉 (90%感度)
- ILD + PRO検索: 6/10 PMIDを捕捉 (60%感度)
- 未捕捉PMID: 36701677 (ILD検索でも0件), 39129185, 28487307, 16817954 (PRO要素なし)

### 最終推奨検索式

#### 基本検索式 (高感度・中特異度)
```
#1 "Lung Diseases, Interstitial"[Mesh]
#2 "Idiopathic Pulmonary Fibrosis"[Mesh]
#3 ("interstitial lung disease"[tiab] OR "ILD"[tiab])
#4 ("pulmonary fibrosis"[tiab] OR "lung fibrosis"[tiab])
#5 "Alveolitis, Extrinsic Allergic"[Mesh]
#6 ("hypersensitivity pneumonitis"[tiab] OR "alveolitis"[tiab])
#7 #1 OR #2 OR #3 OR #4 OR #5 OR #6
```

#### PRO・症状ブロック
```
#8 "Quality of Life"[Mesh]
#9 "Patient Reported Outcome Measures"[Mesh]
#10 ("quality of life"[tiab] OR "QoL"[tiab] OR "HRQoL"[tiab])
#11 ("patient reported"[tiab] OR "patient-reported"[tiab])
#12 ("functional status"[tiab] OR "health status"[tiab])
#13 "Dyspnea"[Mesh]
#14 ("dyspnea"[tiab] OR "dyspnoea"[tiab] OR "breathlessness"[tiab])
#15 "Fatigue"[Mesh]
#16 ("fatigue"[tiab] OR "tiredness"[tiab])
#17 #8 OR #9 OR #10 OR #11 OR #12 OR #13 OR #14 OR #15 OR #16
```

#### 最終検索式
```
#18 #7 AND #17
```

### 代替検索式 (より包括的)

#### 急性増悪を含む検索
```
#19 ("acute exacerbation"[tiab] OR "disease progression"[tiab] OR "deterioration"[tiab])
#20 #7 AND (#17 OR #19)
```

#### 最も包括的な検索
```
#21 #7 AND (#17 OR #19 OR ("cough"[tiab] OR "exercise"[tiab] OR "rehabilitation"[tiab]))
```

## 検索式選択の推奨

### 高精度検索 (推奨)
- **検索式**: #18 (#7 AND #17)
- **予想結果**: 約1,500-2,000件
- **感度**: 60% (6/10 シードPMID)
- **用途**: 高品質なPRO研究に焦点

### 高感度検索
- **検索式**: #21 (最も包括的)
- **予想結果**: 約5,000-8,000件
- **感度**: 80-90%
- **用途**: 包括的レビュー、見落とし防止

### 中間バランス検索
- **検索式**: #20 (急性増悪含む)
- **予想結果**: 約3,000-4,000件
- **感度**: 70-80%
- **用途**: 一般的な系統的レビュー
