# PubMed検索式: HFNC vs NPPV for Type 2 Respiratory Failure

## 検索式構造

```
#1 AND #2 AND #3
```

---

## #1 HFNC (High Flow Nasal Cannula)

```
("high flow nasal cannula"[tiab] OR "high flow oxygen therapy"[tiab] OR "nasal high flow therapy"[tiab] OR "nasal high flow"[tiab] OR hfnc[tiab] OR hfno[tiab] OR "heated humidified high flow"[tiab] OR "Precision Flow"[tiab] OR "HVT"[tiab] OR ProSoft[tiab] OR Optiflow[tiab] OR AIRVO[tiab])
```

---

## #2 呼吸不全/2型呼吸不全

```
("Respiratory Insufficiency"[Mesh] OR "Respiratory Failure"[tiab] OR "Acute respiratory failure"[tiab] OR hypercapnia[Mesh] OR hypercapnia[tiab] OR hypercapnic[tiab])
```

---

## #3 Cochrane RCT Filter (Sensitivity-maximizing version, 2008 revision)

```
(randomized controlled trial[pt] OR controlled clinical trial[pt] OR randomized[tiab] OR placebo[tiab] OR drug therapy[sh] OR randomly[tiab] OR trial[tiab] OR groups[tiab]) NOT (animals[mh] NOT humans[mh])
```

---

## 最終検索式

```
(("high flow nasal cannula"[tiab] OR "high flow oxygen therapy"[tiab] OR "nasal high flow therapy"[tiab] OR "nasal high flow"[tiab] OR hfnc[tiab] OR hfno[tiab] OR "heated humidified high flow"[tiab] OR "Precision Flow"[tiab] OR "HVT"[tiab] OR ProSoft[tiab] OR Optiflow[tiab] OR AIRVO[tiab]) AND ("Respiratory Insufficiency"[Mesh] OR "Respiratory Failure"[tiab] OR "Acute respiratory failure"[tiab] OR hypercapnia[Mesh] OR hypercapnia[tiab] OR hypercapnic[tiab])) AND ((randomized controlled trial[pt] OR controlled clinical trial[pt] OR randomized[tiab] OR placebo[tiab] OR drug therapy[sh] OR randomly[tiab] OR trial[tiab] OR groups[tiab]) NOT (animals[mh] NOT humans[mh]))
```

---

## 検索実行情報

- 検索日: 2026-01-05
- データベース: PubMed
- 件数: 681

---

## Seed Trials

- PMID 39657981: JAMA 2025 - BRIC-NET (Francio F et al.)
- PMID 39111544: Respir Med 2024 - Pantazopoulos et al.


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
