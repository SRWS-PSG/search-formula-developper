## PubMed/MEDLINE (line-by-line)

#1 ICU/critical care
    "Intensive Care Units"[Mesh] OR
    "Critical Care"[Mesh] OR
    "Critical Illness"[Mesh] OR
    "Emergency Medical Services"[Mesh] OR
    "Anesthesia"[Mesh] OR
    "Operating Rooms"[Mesh] OR
    icu[tiab] OR
    "intensive care"[tiab] OR
    "critical care"[tiab] OR
    perioperative[tiab]

#2 Environmental/quality terms
    "Carbon Footprint"[Mesh] OR
    "Medical Waste"[Mesh] OR
    "Quality Improvement"[Mesh] OR
    "Medical Audit"[Mesh] OR
    "Recycling"[Mesh] OR
    "climate change"[tiab] OR
    "carbon footprint"[tiab] OR
    "planetary health"[tiab] OR
    "green ICU"[tiab] OR
    "quality improvement"[tiab] OR
    audit[tiab] OR
    "life cycle assessment"[tiab] OR
    planet[tiab] OR
    "environmental impact"[tiab] OR
    "waste reduction"[tiab] OR
    "medical waste"[tiab] OR
    (green[tiab] AND (ICU[tiab] OR team[tiab])) OR
    (waste[tiab] AND (reduction[tiab] OR audit[tiab])) OR
    (carbon[tiab] AND footprint[tiab])

#3 Drug/procedure + planet/audit/reduction
    (paracetamol[tiab] OR "beta-lactam"[tiab] OR phlebotomy[tiab]) AND
    (planet[tiab] OR audit[tiab] OR reduction[tiab])

#4 Journal + planet/footprint/green
    ("intensive care medicine"[Journal] OR "critical care"[Journal]) AND
    (planet[tiab] OR footprint[tiab] OR green[tiab])

#5 Final
    #1 AND (#2 OR #3 OR #4)

## Embase (Dialog)

```
EMB.EXACT.EXPLODE("intensive care unit")
EMB.EXACT.EXPLODE("intensive care")
EMB.EXACT.EXPLODE("critical illness")
EMB.EXACT.EXPLODE("emergency health service")
EMB.EXACT.EXPLODE("anesthesia")
EMB.EXACT.EXPLODE("operating room")
(TI("icu") OR AB("icu"))
(TI("intensive care") OR AB("intensive care"))
(TI("critical care") OR AB("critical care"))
(TI("perioperative") OR AB("perioperative"))
S1 OR S2 OR S3 OR S4 OR S5 OR S6 OR S7 OR S8 OR S9 OR S10

EMB.EXACT.EXPLODE("carbon footprint")
EMB.EXACT.EXPLODE("hospital waste")
EMB.EXACT.EXPLODE("total quality management")
EMB.EXACT.EXPLODE("clinical audit")
EMB.EXACT.EXPLODE("recycling")
EMB.EXACT.EXPLODE("planetary health")
(TI("climate change") OR AB("climate change"))
(TI("carbon footprint") OR AB("carbon footprint"))
(TI("planetary health") OR AB("planetary health"))
(TI("green ICU") OR AB("green ICU"))
(TI("quality improvement") OR AB("quality improvement"))
(TI("audit") OR AB("audit"))
(TI("life cycle assessment") OR AB("life cycle assessment"))
(TI("planet") OR AB("planet"))
(TI("environmental impact") OR AB("environmental impact"))
(TI("waste reduction") OR AB("waste reduction"))
(TI("medical waste") OR AB("medical waste"))
(TI("green") OR AB("green")) AND ((TI("ICU") OR AB("ICU")) OR (TI("team") OR AB("team")))
(TI("waste") OR AB("waste")) AND ((TI("reduction") OR AB("reduction")) OR (TI("audit") OR AB("audit")))
(TI("carbon") OR AB("carbon")) AND (TI("footprint") OR AB("footprint"))
S12 OR S13 OR S14 OR S15 OR S16 OR S17 OR S18 OR S19 OR S20 OR S21 OR S22 OR S23 OR S24 OR S25 OR S26 OR S27 OR S28 OR S29 OR S30 OR S31

(TI("paracetamol") OR AB("paracetamol"))
(TI("beta-lactam") OR AB("beta-lactam"))
(TI("phlebotomy") OR AB("phlebotomy"))
S33 OR S34 OR S35
(TI("planet") OR AB("planet"))
(TI("audit") OR AB("audit"))
(TI("reduction") OR AB("reduction"))
S37 OR S38 OR S39
S36 AND S40

(JN("intensive care medicine") OR JN("critical care"))
(TI("planet") OR AB("planet"))
(TI("footprint") OR AB("footprint"))
(TI("green") OR AB("green"))
S43 OR S44 OR S45
S42 AND S46

S32 OR S41 OR S47
S11 AND S48
```
