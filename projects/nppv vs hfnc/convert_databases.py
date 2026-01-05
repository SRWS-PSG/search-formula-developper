#!/usr/bin/env python3
"""PubMed検索式を他のデータベース形式に変換してsearch_formula.mdに追記"""

import re

# PubMedの各ブロック
hfnc_block = '''("high flow nasal cannula"[tiab] OR "high flow oxygen therapy"[tiab] OR "nasal high flow therapy"[tiab] OR "nasal high flow"[tiab] OR hfnc[tiab] OR hfno[tiab] OR "heated humidified high flow"[tiab] OR "Precision Flow"[tiab] OR "HVT"[tiab] OR ProSoft[tiab] OR Optiflow[tiab] OR AIRVO[tiab])'''

respiratory_block = '''("Respiratory Insufficiency"[Mesh] OR "Respiratory Failure"[tiab] OR "Acute respiratory failure"[tiab] OR hypercapnia[Mesh] OR hypercapnia[tiab] OR hypercapnic[tiab])'''

rct_filter = '''((randomized controlled trial[pt] OR controlled clinical trial[pt] OR randomized[tiab] OR placebo[tiab] OR drug therapy[sh] OR randomly[tiab] OR trial[tiab] OR groups[tiab]) NOT (animals[mh] NOT humans[mh]))'''


def convert_to_central(pubmed_block: str) -> str:
    """PubMed形式をCENTRAL形式に変換"""
    result = pubmed_block
    # [tiab] -> :ti,ab,kw
    result = re.sub(r'\[tiab\]', ':ti,ab,kw', result)
    # [Mesh] -> MeSH descriptor
    result = re.sub(r'"([^"]+)"\[Mesh\]', r'[mh "\1"]', result)
    # [pt] -> :pt
    result = re.sub(r'\[pt\]', ':pt', result)
    # [sh] -> :kw (subheading to keyword)
    result = re.sub(r'\[sh\]', ':kw', result)
    # [mh] -> MeSH
    result = re.sub(r'(\w+)\[mh\]', r'[mh \1]', result)
    return result


def convert_to_dialog(pubmed_block: str) -> str:
    """PubMed形式をDialog/Embase形式に変換"""
    result = pubmed_block
    # [tiab] -> NEAR/(title,abstract)
    result = re.sub(r'"([^"]+)"\[tiab\]', r'TI("\1") OR AB("\1")', result)
    result = re.sub(r'(\w+)\[tiab\]', r'TI(\1) OR AB(\1)', result)
    # [Mesh] -> EMB.EXACT.EXPLODE
    result = re.sub(r'"([^"]+)"\[Mesh\]', r'EMB.EXACT.EXPLODE("\1")', result)
    # [pt] -> PT
    result = re.sub(r'(\w+\s*\w*)\[pt\]', r'PT(\1)', result)
    # [sh] -> subheading
    result = re.sub(r'(\w+)\[sh\]', r'SH(\1)', result)
    # [mh] -> EMB.EXACT
    result = re.sub(r'(\w+)\[mh\]', r'EMB.EXACT(\1)', result)
    return result


def convert_to_clinicaltrials(pubmed_block: str) -> str:
    """PubMed形式をClinicalTrials.gov形式に変換（簡易版）"""
    result = pubmed_block
    # 引用符とフィールドタグを削除
    result = re.sub(r'\[tiab\]', '', result)
    result = re.sub(r'\[Mesh\]', '', result)
    result = re.sub(r'\[pt\]', '', result)
    result = re.sub(r'\[sh\]', '', result)
    result = re.sub(r'\[mh\]', '', result)
    # 内側の引用符を保持
    return result


def convert_to_ictrp(pubmed_block: str) -> str:
    """PubMed形式をICTRP形式に変換（簡易版）"""
    result = pubmed_block
    # フィールドタグを削除してシンプルに
    result = re.sub(r'\[tiab\]', '', result)
    result = re.sub(r'\[Mesh\]', '', result)
    result = re.sub(r'\[pt\]', '', result)
    result = re.sub(r'\[sh\]', '', result)
    result = re.sub(r'\[mh\]', '', result)
    return result


# 変換実行
output = """

---

## Cochrane CENTRAL

### #1 HFNC
```
("high flow nasal cannula":ti,ab,kw OR "high flow oxygen therapy":ti,ab,kw OR "nasal high flow therapy":ti,ab,kw OR "nasal high flow":ti,ab,kw OR hfnc:ti,ab,kw OR hfno:ti,ab,kw OR "heated humidified high flow":ti,ab,kw OR "Precision Flow":ti,ab,kw OR "HVT":ti,ab,kw OR ProSoft:ti,ab,kw OR Optiflow:ti,ab,kw OR AIRVO:ti,ab,kw)
```

### #2 呼吸不全/2型呼吸不全
```
([mh "Respiratory Insufficiency"] OR "Respiratory Failure":ti,ab,kw OR "Acute respiratory failure":ti,ab,kw OR [mh hypercapnia] OR hypercapnia:ti,ab,kw OR hypercapnic:ti,ab,kw)
```

### #3 最終検索式
```
#1 AND #2
```

> **Note**: CENTRALはRCTのみを収録しているため、RCTフィルターは不要です。

---

## Embase (Dialog)

### S1 HFNC
```
(TI("high flow nasal cannula") OR AB("high flow nasal cannula") OR TI("high flow oxygen therapy") OR AB("high flow oxygen therapy") OR TI("nasal high flow therapy") OR AB("nasal high flow therapy") OR TI("nasal high flow") OR AB("nasal high flow") OR TI(hfnc) OR AB(hfnc) OR TI(hfno) OR AB(hfno) OR TI("heated humidified high flow") OR AB("heated humidified high flow") OR TI("Precision Flow") OR AB("Precision Flow") OR TI("HVT") OR AB("HVT") OR TI(ProSoft) OR AB(ProSoft) OR TI(Optiflow) OR AB(Optiflow) OR TI(AIRVO) OR AB(AIRVO))
```

### S2 呼吸不全/2型呼吸不全  
```
(EMB.EXACT.EXPLODE("respiratory failure") OR TI("Respiratory Failure") OR AB("Respiratory Failure") OR TI("Acute respiratory failure") OR AB("Acute respiratory failure") OR EMB.EXACT.EXPLODE("hypercapnia") OR TI(hypercapnia) OR AB(hypercapnia) OR TI(hypercapnic) OR AB(hypercapnic))
```

### S3 RCT Filter
```
(EMB.EXACT.EXPLODE("randomized controlled trial") OR EMB.EXACT.EXPLODE("controlled clinical trial") OR TI(randomized) OR AB(randomized) OR TI(placebo) OR AB(placebo) OR TI(randomly) OR AB(randomly) OR TI(trial) OR AB(trial) OR TI(groups) OR AB(groups)) NOT (EMB.EXACT(animal) NOT EMB.EXACT(human))
```

### S4 最終検索式
```
S1 AND S2 AND S3
```

---

## ClinicalTrials.gov

### Condition or disease
```
Respiratory Failure OR Respiratory Insufficiency OR hypercapnia OR hypercapnic
```

### Intervention/treatment
```
high flow nasal cannula OR high flow oxygen therapy OR nasal high flow OR HFNC OR HFNO OR Optiflow OR AIRVO
```

### Study type
- Interventional Studies (Clinical Trials)

---

## ICTRP (WHO International Clinical Trials Registry Platform)

### Title
```
high flow nasal cannula OR high flow oxygen OR nasal high flow OR HFNC OR HFNO
```

### Condition
```
respiratory failure OR hypercapnia OR hypercapnic respiratory failure
```

### Intervention
```
high flow nasal cannula OR high flow oxygen therapy OR HFNC
```

---
"""

# search_formula.mdに追記
with open("projects/nppv vs hfnc/search_formula.md", "a", encoding="utf-8") as f:
    f.write(output)

print("✅ 他のデータベース検索式を追記しました:")
print("  - Cochrane CENTRAL")
print("  - Embase (Dialog)")
print("  - ClinicalTrials.gov")
print("  - ICTRP")
