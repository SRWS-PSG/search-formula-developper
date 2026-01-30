# PubMed Search Formula for nitta_depression

## 検索式

### Block 1: Cancer Terms
```
(neoplasms[MeSH] OR neoplasm*[tiab] OR cancer*[tiab] OR carcinoma*[tiab] OR tumour*[tiab] OR tumor*[tiab] OR adenocarcinoma*[tiab] OR leukemi*[tiab] OR leukaemi*[tiab] OR lymphoma*[tiab] OR myeloma*[tiab] OR sarcoma*[tiab] OR melanoma*[tiab] OR glioma*[tiab] OR malignan*[tiab] OR oncolog*[tiab] OR metastati*[tiab] OR metastas*[tiab])
```

### Block 2: Japanese Database Terms
```
((NDB[tiab] OR "National Database"[tiab]) OR (JMDC[tiab] OR "Japan Medical Data Center"[tiab]) OR DeSC[tiab] OR ("DPC"[tiab] OR "Diagnosis Procedure Combination database"[tiab]) OR (NCD[tiab] OR "National Clinical Database"[tiab]) OR ("MID-NET"[tiab] OR "Medical Information Database Network"[tiab]) OR (NCDA[tiab] OR "National Hospital Organization Clinical Data Archives"[tiab]) OR JAMDAS[tiab] OR (FHRD[tiab] OR "Flatiron"[tiab]) OR ("LIFE Study"[tiab] OR "longevity improvement and fair evidence study"[tiab]) OR REZULT[tiab] OR IQVIA[tiab] OR (NHWS[tiab] OR "National Health and Wellness Survey"[tiab]) OR (KDB[tiab] OR Kokuho[tiab]) OR (MDV[tiab] OR "Medical data Vision"[tiab]) OR ((RWD[tiab] OR "real-world data"[tiab]) OR administrative data*[tiab] OR claims data*[tiab] OR insurance data*[tiab] OR payer data*[tiab] OR ("record linkage"[tiab] OR "data linkage"[tiab] OR linked data*[tiab]) OR registry[tiab] OR "cancer registry"[tiab]))
```

### Block 3: Japan Filter
```
(Japan[Mesh] OR Japan*[tiab] OR Japanese[tiab])
```

### Block 4: Depression Terms
```
(depression[MeSH] OR "depressive disorder"[MeSH] OR depress*[tiab])
```

### Block 5: Combined Search (Cancer AND Database AND Japan AND Depression)
```
((neoplasms[MeSH] OR neoplasm*[tiab] OR cancer*[tiab] OR carcinoma*[tiab] OR tumour*[tiab] OR tumor*[tiab] OR adenocarcinoma*[tiab] OR leukemi*[tiab] OR leukaemi*[tiab] OR lymphoma*[tiab] OR myeloma*[tiab] OR sarcoma*[tiab] OR melanoma*[tiab] OR glioma*[tiab] OR malignan*[tiab] OR oncolog*[tiab] OR metastati*[tiab] OR metastas*[tiab])) AND (((NDB[tiab] OR "National Database"[tiab]) OR (JMDC[tiab] OR "Japan Medical Data Center"[tiab]) OR DeSC[tiab] OR ("DPC"[tiab] OR "Diagnosis Procedure Combination database"[tiab]) OR (NCD[tiab] OR "National Clinical Database"[tiab]) OR ("MID-NET"[tiab] OR "Medical Information Database Network"[tiab]) OR (NCDA[tiab] OR "National Hospital Organization Clinical Data Archives"[tiab]) OR JAMDAS[tiab] OR (FHRD[tiab] OR "Flatiron"[tiab]) OR ("LIFE Study"[tiab] OR "longevity improvement and fair evidence study"[tiab]) OR REZULT[tiab] OR IQVIA[tiab] OR (NHWS[tiab] OR "National Health and Wellness Survey"[tiab]) OR (KDB[tiab] OR Kokuho[tiab]) OR (MDV[tiab] OR "Medical data Vision"[tiab]) OR ((RWD[tiab] OR "real-world data"[tiab]) OR administrative data*[tiab] OR claims data*[tiab] OR insurance data*[tiab] OR payer data*[tiab] OR ("record linkage"[tiab] OR "data linkage"[tiab] OR linked data*[tiab]) OR registry[tiab] OR "cancer registry"[tiab]))) AND ((Japan[Mesh] OR Japan*[tiab] OR Japanese[tiab])) AND ((depression[MeSH] OR "depressive disorder"[MeSH] OR depress*[tiab]))
```

### Block 6-9: Animal Exclusion Filter
```
NOT (animals[mh] NOT humans[mh])
```

### Final Query (#9)
```
(((neoplasms[MeSH] OR neoplasm*[tiab] OR cancer*[tiab] OR carcinoma*[tiab] OR tumour*[tiab] OR tumor*[tiab] OR adenocarcinoma*[tiab] OR leukemi*[tiab] OR leukaemi*[tiab] OR lymphoma*[tiab] OR myeloma*[tiab] OR sarcoma*[tiab] OR melanoma*[tiab] OR glioma*[tiab] OR malignan*[tiab] OR oncolog*[tiab] OR metastati*[tiab] OR metastas*[tiab])) AND (((NDB[tiab] OR "National Database"[tiab]) OR (JMDC[tiab] OR "Japan Medical Data Center"[tiab]) OR DeSC[tiab] OR ("DPC"[tiab] OR "Diagnosis Procedure Combination database"[tiab]) OR (NCD[tiab] OR "National Clinical Database"[tiab]) OR ("MID-NET"[tiab] OR "Medical Information Database Network"[tiab]) OR (NCDA[tiab] OR "National Hospital Organization Clinical Data Archives"[tiab]) OR JAMDAS[tiab] OR (FHRD[tiab] OR "Flatiron"[tiab]) OR ("LIFE Study"[tiab] OR "longevity improvement and fair evidence study"[tiab]) OR REZULT[tiab] OR IQVIA[tiab] OR (NHWS[tiab] OR "National Health and Wellness Survey"[tiab]) OR (KDB[tiab] OR Kokuho[tiab]) OR (MDV[tiab] OR "Medical data Vision"[tiab]) OR ((RWD[tiab] OR "real-world data"[tiab]) OR administrative data*[tiab] OR claims data*[tiab] OR insurance data*[tiab] OR payer data*[tiab] OR ("record linkage"[tiab] OR "data linkage"[tiab] OR linked data*[tiab]) OR registry[tiab] OR "cancer registry"[tiab]))) AND ((Japan[Mesh] OR Japan*[tiab] OR Japanese[tiab])) AND ((depression[MeSH] OR "depressive disorder"[MeSH] OR depress*[tiab]))) NOT (animals[mh] NOT humans[mh])
```

## Seed Papers
- PMID: 32779276
- PMID: 33070280
- PMID: 35001472
- PMID: 40879352
- PMID: 35109805
