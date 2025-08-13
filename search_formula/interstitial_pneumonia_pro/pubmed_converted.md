# 間質性肺炎・急性増悪・Patient Reported Outcome 検索式 (PubMed変換版)

## Ovid → PubMed 変換分析

### 間質性肺炎ブロック (1-9行)
```
#1 "Lung Diseases, Interstitial"[Mesh]
#2 ("Interstitial"[tiab] AND ("lung"[tiab] OR "lungs"[tiab] OR "pulmonary"[tiab] OR "pneumonia"[tiab] OR "pneumonitis"[tiab]))
#3 "ILD"[tiab]
#4 (("pulmonary"[tiab] OR "lung"[tiab] OR "lungs"[tiab]) AND ("fibrosis"[tiab] OR "fibrotic"[tiab] OR "fibrosing"[tiab]))
#5 "Alveolitis, Extrinsic Allergic"[Mesh]
#6 ("alveolitis"[tiab] OR "alveolitides"[tiab])
#7 ("pulmonary"[tiab] AND ("sarcoidosis"[tiab] OR "sarcoidoses"[tiab]))
#8 ("hypersensitivity"[tiab] AND ("pneumonia"[tiab] OR "pneumonitis"[tiab] OR "pneumoniae"[tiab]))
#9 #1 OR #2 OR #3 OR #4 OR #5 OR #6 OR #7 OR #8
```

### 急性増悪ブロック (10-16行)
```
#10 "Disease Progression"[Mesh]
#11 ("acute"[tiab] AND ("exacerbation"[tiab] OR "exacerbations"[tiab]))
#12 ("disease"[tiab] AND ("progression"[tiab] OR "progressions"[tiab]))
#13 ("disease"[tiab] AND ("exacerbation"[tiab] OR "exacerbations"[tiab]))
#14 ("deterioration"[tiab] OR "deteriorations"[tiab])
#15 ("flare"[tiab] OR "flares"[tiab] OR "flaring"[tiab])
#16 #10 OR #11 OR #12 OR #13 OR #14 OR #15
```

### 症状・PRO関連ブロック (17-37行)
```
#17 "Dyspnea"[Mesh]
#18 ("dyspnea"[tiab] OR "dyspnoea"[tiab] OR "dyspneic"[tiab] OR "breathlessness"[tiab] OR "shortness of breath"[tiab])
#19 "Cough"[Mesh]
#20 ("cough"[tiab] OR "coughs"[tiab] OR "coughing"[tiab])
#21 "Fatigue"[Mesh]
#22 ("fatigue"[tiab] OR "fatigues"[tiab] OR "tiredness"[tiab])
#23 "Chest Pain"[Mesh]
#24 (("chest"[tiab] OR "chests"[tiab]) AND ("symptom"[tiab] OR "symptoms"[tiab] OR "pain"[tiab] OR "pains"[tiab] OR "pressure"[tiab] OR "discomfort"[tiab]))
#25 ("Sleep Deprivation"[Mesh] OR "Dyssomnias"[Mesh])
#26 ("sleep disturbance"[tiab] OR "sleep disturbances"[tiab] OR "sleep disorder"[tiab] OR "sleep disorders"[tiab] OR "sleep disruption"[tiab] OR "sleep disruptions"[tiab] OR "sleep loss"[tiab] OR "sleeplessness"[tiab] OR "insomnia"[tiab] OR "insomnias"[tiab])
#27 "Anxiety"[Mesh]
#28 ("anxiety"[tiab] OR "anxieties"[tiab] OR "anxious"[tiab] OR "insecurity"[tiab] OR "insecurities"[tiab])
#29 "Fear"[Mesh]
#30 ("fear"[tiab] OR "phobia"[tiab] OR "phobic"[tiab] OR "fright"[tiab] OR "frightened"[tiab] OR "frightening"[tiab])
#31 "Depression"[Mesh]
#32 ("depression"[tiab] OR "depressed"[tiab] OR "depressive"[tiab])
#33 ("treatment burden"[tiab] OR "treatment burdens"[tiab] OR "financial toxicity"[tiab] OR "financial toxicities"[tiab] OR "financial burden"[tiab] OR "financial burdens"[tiab] OR "economic burden"[tiab] OR "economic burdens"[tiab])
#34 ("cope"[tiab] OR "coping"[tiab])
#35 "Psychological Well-Being"[Mesh]
#36 ("well-being"[tiab] OR "wellbeing"[tiab] OR "well being"[tiab])
#37 #17 OR #18 OR #19 OR #20 OR #21 OR #22 OR #23 OR #24 OR #25 OR #26 OR #27 OR #28 OR #29 OR #30 OR #31 OR #32 OR #33 OR #34 OR #35 OR #36
```

### PROメジャーブロック (38行)
```
#38 ("Patient Reported Outcome Measures"[Mesh] OR "Quality of Life"[Mesh] OR "prom"[tiab] OR "proms"[tiab] OR "pro"[tiab] OR "pros"[tiab] OR "HRQL"[tiab] OR "HRQoL"[tiab] OR "QL"[tiab] OR "QoL"[tiab] OR "quality of life"[tiab] OR "life quality"[tiab] OR "health index"[tiab] OR "health indices"[tiab] OR "health profile"[tiab] OR "health profiles"[tiab] OR "health status"[tiab] OR (("patient"[tiab] OR "self"[tiab] OR "child"[tiab] OR "parent"[tiab] OR "carer"[tiab] OR "proxy"[tiab]) AND ("report"[tiab] OR "reported"[tiab] OR "reporting"[tiab] OR "rated"[tiab] OR "rating"[tiab] OR "ratings"[tiab] OR "based"[tiab] OR "assessed"[tiab] OR "assessment"[tiab] OR "assessments"[tiab])) OR (("disability"[tiab] OR "function"[tiab] OR "functional"[tiab] OR "functions"[tiab] OR "subjective"[tiab] OR "utility"[tiab] OR "utilities"[tiab] OR "wellbeing"[tiab] OR "well being"[tiab]) AND ("outcome"[tiab] OR "outcomes"[tiab] OR "index"[tiab] OR "indices"[tiab] OR "instrument"[tiab] OR "instruments"[tiab] OR "measure"[tiab] OR "measures"[tiab] OR "questionnaire"[tiab] OR "questionnaires"[tiab] OR "profile"[tiab] OR "profiles"[tiab] OR "scale"[tiab] OR "scales"[tiab] OR "score"[tiab] OR "scores"[tiab] OR "status"[tiab] OR "survey"[tiab] OR "surveys"[tiab])))
```

### 最終検索式
```
#39 #9 AND #16 AND #37 AND #38
```

## 変換時の主な変更点

1. **近接演算子**: Ovid `adj3` → PubMed `AND` (3語以内の近接は標準のANDで代替)
2. **ワイルドカード**: Ovid `$` → PubMed 明示的な語形変化列挙
3. **フィールドタグ**: Ovid `.tw.` → PubMed `[tiab]`
4. **MeSH用語**: Ovid `exp` → PubMed `[Mesh]` (explodeはデフォルト)
5. **論理演算子**: 大文字小文字の統一 (OR, AND)
