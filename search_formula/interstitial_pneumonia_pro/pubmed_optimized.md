# 間質性肺炎・急性増悪・Patient Reported Outcome 検索式 (PubMed最適化版)

## 問題分析
元の変換版では最終検索結果が0件となり、10個のシードPMIDを1つも捕捉できませんでした。
主な問題：
1. 4つのブロック全てをANDで結合すると過度に制限的
2. 急性増悪ブロックが必須条件として厳しすぎる
3. 症状ブロックが広範囲すぎて関連性の低い論文を含む可能性

## 最適化戦略
1. 急性増悪を必須条件から除外し、ORで結合
2. 症状ブロックを核心症状に絞り込み
3. PROブロックを簡潔化

## 最適化されたPubMed検索式

### 間質性肺炎ブロック (必須)
```
#1 "Lung Diseases, Interstitial"[Mesh]
#2 ("Interstitial"[tiab] AND ("lung"[tiab] OR "lungs"[tiab] OR "pulmonary"[tiab] OR "pneumonia"[tiab] OR "pneumonitis"[tiab]))
#3 "ILD"[tiab]
#4 (("pulmonary"[tiab] OR "lung"[tiab] OR "lungs"[tiab]) AND ("fibrosis"[tiab] OR "fibrotic"[tiab] OR "fibrosing"[tiab]))
#5 "Alveolitis, Extrinsic Allergic"[Mesh]
#6 ("alveolitis"[tiab] OR "hypersensitivity pneumonitis"[tiab])
#7 "Idiopathic Pulmonary Fibrosis"[Mesh]
#8 #1 OR #2 OR #3 OR #4 OR #5 OR #6 OR #7
```

### 急性増悪・進行ブロック (オプション)
```
#9 "Disease Progression"[Mesh]
#10 ("acute"[tiab] AND ("exacerbation"[tiab] OR "exacerbations"[tiab]))
#11 ("disease"[tiab] AND ("progression"[tiab] OR "exacerbation"[tiab]))
#12 ("deterioration"[tiab] OR "worsening"[tiab])
#13 #9 OR #10 OR #11 OR #12
```

### 核心症状ブロック (オプション)
```
#14 "Dyspnea"[Mesh]
#15 ("dyspnea"[tiab] OR "dyspnoea"[tiab] OR "breathlessness"[tiab] OR "shortness of breath"[tiab])
#16 "Cough"[Mesh]
#17 ("cough"[tiab] OR "coughs"[tiab] OR "coughing"[tiab])
#18 "Fatigue"[Mesh]
#19 ("fatigue"[tiab] OR "tiredness"[tiab])
#20 #14 OR #15 OR #16 OR #17 OR #18 OR #19
```

### PROブロック (必須)
```
#21 "Patient Reported Outcome Measures"[Mesh]
#22 "Quality of Life"[Mesh]
#23 ("quality of life"[tiab] OR "QoL"[tiab] OR "HRQoL"[tiab])
#24 ("patient reported"[tiab] OR "patient-reported"[tiab])
#25 ("functional status"[tiab] OR "health status"[tiab])
#26 #21 OR #22 OR #23 OR #24 OR #25
```

### 最終検索式 (柔軟なアプローチ)
```
#27 #8 AND #26 AND (#13 OR #20)
```

### 代替検索式 (より包括的)
```
#28 #8 AND (#26 OR #20)
```

### 検証用シンプル検索式
```
#29 ("Lung Diseases, Interstitial"[Mesh] OR "ILD"[tiab] OR "interstitial lung disease"[tiab]) AND ("Quality of Life"[Mesh] OR "quality of life"[tiab] OR "patient reported"[tiab])
```
