## PubMed/MEDLINE (line-by-line)

#1 ICU/critical care
    "Intensive Care Units"[Mesh] OR
    "Critical Care"[Mesh] OR
    "Critical Illness"[Mesh] OR
    icu[tiab] OR
    "intensive care"[tiab] OR
    "critical care"[tiab] OR
    perioperative[tiab] OR
    "Lancet Respiratory Medicine"[Journal] OR
    "Intensive Care Medicine"[Journal] OR
    "American Journal of Respiratory and Critical Care Medicine"[Journal] OR
    "Critical Care"[Journal] OR
    "Chest"[Journal] OR
    "Critical Care Medicine"[Journal] OR
    "Annals of Intensive Care"[Journal] OR
    "Intensive and Critical Care Nursing"[Journal] OR
    "Anaesthesia Critical Care & Pain Medicine"[Journal] OR
    "Journal of Intensive Care"[Journal]

#2 Environmental/quality terms
    "Carbon Footprint"[Mesh] OR
    "Medical Waste"[Mesh] OR
    "Recycling"[Mesh] OR "Climate Change"[MeSH] OR
    "climate change"[tiab] OR
    "carbon footprint"[tiab] OR
    "planetary health"[tiab] OR
    "green ICU"[tiab] OR
    "green team"[tiab] OR
    "sustainability team"[tiab] OR
    "life cycle assessment"[tiab] OR
    "material flow"[tiab] OR
    planet[tiab] OR
    "environmental impact"[tiab] OR
    "waste reduction"[tiab] OR
    "medical waste"[tiab] OR
    (green[tiab] AND (ICU[tiab] OR "intensive care"[tiab])) OR
    (waste[tiab] AND (reduction[tiab] OR audit[tiab])) OR
    (carbon[tiab] AND footprint[tiab]) OR
    (("Quality Improvement"[Mesh] OR "Medical Audit"[Mesh] OR "quality improvement"[tiab] OR audit[tiab]) AND
     (carbon[tiab] OR footprint[tiab] OR waste[tiab] OR environmental[tiab] OR climate[tiab] OR sustainability[tiab]))

#3 Drug/procedure + planet/audit/reduction
    (("Acetaminophen"[Mesh] OR paracetamol[tiab] OR acetaminophen[tiab]) OR
     ("beta-Lactams"[Mesh] OR "beta-lactam"[tiab]) OR
     ("Phlebotomy"[Mesh] OR phlebotomy[tiab])) AND
    (planet[tiab] OR "Quality Improvement"[Mesh] OR "Medical Audit"[Mesh] OR "quality improvement"[tiab] OR audit[tiab] OR reduction[tiab])

#4 #1 AND (#2 OR #3)

## Seed論文の確認メモ

### Seed論文リスト（18件）

25192883, 19775048, 38296752, 38866584, 40113716, 36480046, 30482138, 39998996,
39058393, 39665859, 36657786, 38755050, 39466377, 39887498, 26017132, 28948594,
36439332, 40394680

### 組み入れにならなかったものの理由

- 19775048: 麻酔/手術室中心の監査でICUスコープ外寄り。Pブロックから `Anesthesia`/`Operating Rooms`を外しているため捕捉されない。
- 39998996: ICUスコープ外（手術室の麻酔薬のカーボンフットプリント）。

## Embase (Dialog)

```
EMB.EXACT.EXPLODE("intensive care unit")
EMB.EXACT.EXPLODE("intensive care")
EMB.EXACT.EXPLODE("critical illness")
(TI("icu") OR AB("icu"))
(TI("intensive care") OR AB("intensive care"))
(TI("critical care") OR AB("critical care"))
(TI("perioperative") OR AB("perioperative"))
(JN("lancet respiratory medicine") OR JN("intensive care medicine") OR JN("american journal of respiratory and critical care medicine") OR JN("critical care") OR JN("chest") OR JN("critical care medicine") OR JN("annals of intensive care") OR JN("intensive and critical care nursing") OR JN("anaesthesia critical care & pain medicine") OR JN("journal of intensive care"))
S1 OR S2 OR S3 OR S4 OR S5 OR S6 OR S7 OR S8
EMB.EXACT.EXPLODE("carbon footprint")
EMB.EXACT.EXPLODE("hospital waste")
EMB.EXACT.EXPLODE("recycling")
EMB.EXACT.EXPLODE("planetary health")
(TI("climate change") OR AB("climate change"))
(TI("carbon footprint") OR AB("carbon footprint"))
(TI("planetary health") OR AB("planetary health"))
(TI("green ICU") OR AB("green ICU"))
(TI("green team") OR AB("green team"))
(TI("sustainability team") OR AB("sustainability team"))
(TI("life cycle assessment") OR AB("life cycle assessment"))
(TI("material flow") OR AB("material flow"))
(TI("planet") OR AB("planet"))
(TI("environmental impact") OR AB("environmental impact"))
(TI("waste reduction") OR AB("waste reduction"))
(TI("medical waste") OR AB("medical waste"))
(TI("green") OR AB("green")) AND ((TI("ICU") OR AB("ICU")) OR (TI("intensive care") OR AB("intensive care")))
(TI("waste") OR AB("waste")) AND ((TI("reduction") OR AB("reduction")) OR (TI("audit") OR AB("audit")))
(TI("carbon") OR AB("carbon")) AND (TI("footprint") OR AB("footprint"))
(TI("quality improvement") OR AB("quality improvement") OR TI("audit") OR AB("audit") OR EMB.EXACT.EXPLODE("total quality management") OR EMB.EXACT.EXPLODE("clinical audit")) AND (TI("carbon") OR AB("carbon") OR TI("footprint") OR AB("footprint") OR TI("waste") OR AB("waste") OR TI("environmental") OR AB("environmental") OR TI("climate") OR AB("climate") OR TI("sustainability") OR AB("sustainability"))
S10 OR S11 OR S12 OR S13 OR S14 OR S15 OR S16 OR S17 OR S18 OR S19 OR S20 OR S21 OR S22 OR S23 OR S24 OR S25 OR S26 OR S27 OR S28 OR S29
(EMB.EXACT.EXPLODE("paracetamol") OR TI("paracetamol") OR AB("paracetamol"))
(EMB.EXACT.EXPLODE("beta-lactam") OR TI("beta-lactam") OR AB("beta-lactam"))
(EMB.EXACT.EXPLODE("phlebotomy") OR TI("phlebotomy") OR AB("phlebotomy"))
S31 OR S32 OR S33
(EMB.EXACT.EXPLODE("planetary health") OR TI("planet") OR AB("planet"))
(EMB.EXACT.EXPLODE("total quality management") OR TI("quality improvement") OR AB("quality improvement"))
(EMB.EXACT.EXPLODE("clinical audit") OR TI("audit") OR AB("audit"))
(TI("reduction") OR AB("reduction"))
S35 OR S36 OR S37 OR S38
S34 AND S39
S30 OR S40
S9 AND S41
```
