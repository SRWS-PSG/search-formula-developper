# データベース別検索式

変換日時: 2025-09-06 06:38:19

## PubMed

```
# Improved Search Formula for Overview of Reviews: Systemic Lupus Erythematosus and Lupus Nephritis Prognosis

## Original Search Formula (User Provided)
```
(("systemic lupus erythematosus"[MeSH Terms] OR "lupus erythematosus, systemic"[Title/Abstract] OR "lupus nephritis"[MeSH Terms] OR "lupus nephritis"[Title/Abstract]))
AND (("prognosis"[MeSH Terms] OR "prognosis"[Title/Abstract] OR "prognostic factors"[Title/Abstract] OR "renal outcome"[Title/Abstract] OR "kidney failure, chronic"[MeSH Terms] OR "end-stage renal disease"[Title/Abstract]))
AND (("systematic review"[Publication Type] OR "meta-analysis"[Publication Type] OR "systematic review"[Title/Abstract] OR "meta-analysis"[Title/Abstract]))
```

## Improved Search Formula for MEDLINE (PubMed)

### Block 1: Population (Systemic Lupus Erythematosus and Lupus Nephritis)
```
#1 "Lupus Erythematosus, Systemic"[Mesh] OR
    "Lupus Nephritis"[Mesh] OR
    "systemic lupus erythematosus"[tiab] OR
    "lupus erythematosus, systemic"[tiab] OR
    "lupus nephritis"[tiab] OR
    "SLE"[tiab] OR
    (lupus[tiab] AND (systemic[tiab] OR nephritis[tiab] OR renal[tiab] OR kidney[tiab])) OR
    "lupus glomerulonephritis"[tiab] OR
    "lupus kidney disease"[tiab]
```

### Block 2: Prognosis and Outcomes (Enhanced)
```
#2 "Prognosis"[Mesh] OR
    "Disease Progression"[Mesh] OR
    "Treatment Outcome"[Mesh] OR
    "Mortality"[Mesh] OR
    "Renal Insufficiency, Chronic"[Mesh] OR
    "Kidney Failure, Chronic"[Mesh] OR
    prognosis[tiab] OR
    "prognostic factors"[tiab] OR
    "prognostic factor"[tiab] OR
    "renal outcome"[tiab] OR
    "renal outcomes"[tiab] OR
    "kidney outcome"[tiab] OR
    "kidney outcomes"[tiab] OR
    "end-stage renal disease"[tiab] OR
    "ESRD"[tiab] OR
    "chronic kidney disease"[tiab] OR
    "CKD"[tiab] OR
    "renal function"[tiab] OR
    "kidney function"[tiab] OR
    "glomerular filtration rate"[tiab] OR
    "GFR"[tiab] OR
    "renal survival"[tiab] OR
    "kidney survival"[tiab] OR
    mortality[tiab] OR
    survival[tiab] OR
    "disease progression"[tiab] OR
    "treatment response"[tiab] OR
    "treatment outcome"[tiab] OR
    "clinical outcome"[tiab] OR
    "long-term outcome"[tiab] OR
    "predictive factor"[tiab] OR
    "risk factor"[tiab]
```

### Block 3: Overview of Reviews and Systematic Reviews (Enhanced)
```
#3 "Review"[Publication Type] OR
    "Systematic Review"[Publication Type] OR
    "Meta-Analysis"[Publication Type] OR
    "systematic review"[tiab] OR
    "systematic reviews"[tiab] OR
    "meta-analysis"[tiab] OR
    "meta-analyses"[tiab] OR
    "overview of reviews"[tiab] OR
    "umbrella review"[tiab] OR
    "umbrella reviews"[tiab] OR
    "review of reviews"[tiab] OR
    "overview of systematic reviews"[tiab] OR
    "meta-review"[tiab] OR
    "meta-reviews"[tiab] OR
    "Cochrane review"[tiab] OR
    "Cochrane reviews"[tiab] OR
    "pooled analysis"[tiab] OR
    "pooled analyses"[tiab] OR
    (review[tiab] AND (systematic[tiab] OR comprehensive[tiab] OR literature[tiab])) OR
    "evidence synthesis"[tiab] OR
    "research synthesis"[tiab]
```

### Final Search Formula
```
#4 #1 AND #2 AND #3
Filters: English, Humans
```

## Key Improvements Made

### 1. Enhanced MeSH Terms
- Added "Lupus Erythematosus, Systemic"[Mesh] (proper MeSH format)
- Added "Disease Progression"[Mesh], "Treatment Outcome"[Mesh], "Mortality"[Mesh]
- Added "Renal Insufficiency, Chronic"[Mesh] for better renal outcome coverage

### 2. Expanded Text Word Coverage
- Added common abbreviations: SLE, ESRD, CKD, GFR
- Added synonymous terms: lupus glomerulonephritis, lupus kidney disease
- Enhanced prognosis terms: survival, mortality, disease progression, treatment response
- Added renal function terminology: glomerular filtration rate, renal survival

### 3. Comprehensive Review Literature Identification
- Added "overview of reviews" and "umbrella review" terms specifically
- Added "Review"[Publication Type] for broader coverage
- Added Cochrane-specific terms
- Added evidence synthesis terminology

### 4. Improved Search Logic
- Used proper field tags [tiab] instead of [Title/Abstract]
- Structured in clear conceptual blocks
- Added proximity considerations with AND logic within concepts

### 5. Quality Filters
- Added language filter (English)
- Added species filter (Humans)

## Estimated Search Performance
- **Sensitivity**: High - comprehensive coverage of SLE/LN terminology and outcomes
- **Specificity**: Improved - focused on review literature with specific outcome measures
- **Precision**: Enhanced - structured Boolean logic reduces irrelevant results

## Alternative Versions

### High Sensitivity Version (for comprehensive screening)
Use all terms as above

### High Precision Version (for focused results)
```
("Lupus Erythematosus, Systemic"[Mesh] OR "Lupus Nephritis"[Mesh])
AND ("Prognosis"[Mesh] OR "Treatment Outcome"[Mesh] OR prognosis[tiab] OR "prognostic factors"[tiab])
AND ("overview of reviews"[tiab] OR "umbrella review"[tiab] OR ("systematic review"[tiab] AND review[tiab]))
```

## Notes for Database Conversion
- This search can be converted to CENTRAL, Embase Dialog, and other databases using the conversion tools in this repository
- MeSH terms will need mapping to Emtree terms for Embase
- Proximity operators may need adjustment for different database syntaxes

```

## Cochrane CENTRAL

```
# Improved Search Formula for Overview of Reviews: Systemic Lupus Erythematosus and Lupus Nephritis Prognosis

## Original Search Formula (User Provided)
```
(("systemic lupus erythematosus"[MeSH Terms] OR "lupus erythematosus, systemic"[Title/Abstract] OR "lupus nephritis"[MeSH Terms] OR "lupus nephritis"[Title/Abstract]))
AND (("prognosis"[MeSH Terms] OR "prognosis"[Title/Abstract] OR "prognostic factors"[Title/Abstract] OR "renal outcome"[Title/Abstract] OR "kidney failure, chronic"[MeSH Terms] OR "end-stage renal disease"[Title/Abstract]))
AND (("systematic review"[Publication Type] OR "meta-analysis"[Publication Type] OR "systematic review"[Title/Abstract] OR "meta-analysis"[Title/Abstract]))
```

## Improved Search Formula for MEDLINE (PubMed)

### Block 1: Population (Systemic Lupus Erythematosus and Lupus Nephritis)
```
#1 [mh "Lupus Erythematosus, Systemic"] OR
"Lupus Nephritis"[Mesh] OR
"systemic lupus erythematosus"[tiab] OR
"lupus erythematosus, systemic"[tiab] OR
"lupus nephritis"[tiab] OR
"SLE"[tiab] OR
(lupus[tiab] AND (systemic[tiab] OR nephritis[tiab] OR renal[tiab] OR kidney[tiab])) OR
"lupus glomerulonephritis"[tiab] OR
"lupus kidney disease"[tiab]
```

### Block 2: Prognosis and Outcomes (Enhanced)
```
#2 [mh "Prognosis"] OR
"Disease Progression"[Mesh] OR
"Treatment Outcome"[Mesh] OR
"Mortality"[Mesh] OR
"Renal Insufficiency, Chronic"[Mesh] OR
"Kidney Failure, Chronic"[Mesh] OR
prognosis[tiab] OR
"prognostic factors"[tiab] OR
"prognostic factor"[tiab] OR
"renal outcome"[tiab] OR
"renal outcomes"[tiab] OR
"kidney outcome"[tiab] OR
"kidney outcomes"[tiab] OR
"end-stage renal disease"[tiab] OR
"ESRD"[tiab] OR
"chronic kidney disease"[tiab] OR
"CKD"[tiab] OR
"renal function"[tiab] OR
"kidney function"[tiab] OR
"glomerular filtration rate"[tiab] OR
"GFR"[tiab] OR
"renal survival"[tiab] OR
"kidney survival"[tiab] OR
mortality[tiab] OR
survival[tiab] OR
"disease progression"[tiab] OR
"treatment response"[tiab] OR
"treatment outcome"[tiab] OR
"clinical outcome"[tiab] OR
"long-term outcome"[tiab] OR
"predictive factor"[tiab] OR
"risk factor"[tiab]
```

### Block 3: Overview of Reviews and Systematic Reviews (Enhanced)
```
#3 "Review"[Publication Type] OR
"Systematic Review"[Publication Type] OR
"Meta-Analysis"[Publication Type] OR
"systematic review"[tiab] OR
"systematic reviews"[tiab] OR
"meta-analysis"[tiab] OR
"meta-analyses"[tiab] OR
"overview of reviews"[tiab] OR
"umbrella review"[tiab] OR
"umbrella reviews"[tiab] OR
"review of reviews"[tiab] OR
"overview of systematic reviews"[tiab] OR
"meta-review"[tiab] OR
"meta-reviews"[tiab] OR
"Cochrane review"[tiab] OR
"Cochrane reviews"[tiab] OR
"pooled analysis"[tiab] OR
"pooled analyses"[tiab] OR
(review[tiab] AND (systematic[tiab] OR comprehensive[tiab] OR literature[tiab])) OR
"evidence synthesis"[tiab] OR
"research synthesis"[tiab]
```

### Final Search Formula
```
#4 #1 AND #2 AND #3
Filters: English, Humans
```

## Key Improvements Made

### 1. Enhanced MeSH Terms
- Added "Lupus Erythematosus, Systemic"[Mesh] (proper MeSH format)
- Added "Disease Progression"[Mesh], "Treatment Outcome"[Mesh], "Mortality"[Mesh]
- Added "Renal Insufficiency, Chronic"[Mesh] for better renal outcome coverage

### 2. Expanded Text Word Coverage
- Added common abbreviations: SLE, ESRD, CKD, GFR
- Added synonymous terms: lupus glomerulonephritis, lupus kidney disease
- Enhanced prognosis terms: survival, mortality, disease progression, treatment response
- Added renal function terminology: glomerular filtration rate, renal survival

### 3. Comprehensive Review Literature Identification
- Added "overview of reviews" and "umbrella review" terms specifically
- Added "Review"[Publication Type] for broader coverage
- Added Cochrane-specific terms
- Added evidence synthesis terminology

### 4. Improved Search Logic
- Used proper field tags [tiab] instead of [Title/Abstract]
- Structured in clear conceptual blocks
- Added proximity considerations with AND logic within concepts

### 5. Quality Filters
- Added language filter (English)
- Added species filter (Humans)

## Estimated Search Performance
- **Sensitivity**: High - comprehensive coverage of SLE/LN terminology and outcomes
- **Specificity**: Improved - focused on review literature with specific outcome measures
- **Precision**: Enhanced - structured Boolean logic reduces irrelevant results

## Alternative Versions

### High Sensitivity Version (for comprehensive screening)
Use all terms as above

### High Precision Version (for focused results)
```
("Lupus Erythematosus, Systemic"[Mesh] OR "Lupus Nephritis"[Mesh])
AND ("Prognosis"[Mesh] OR "Treatment Outcome"[Mesh] OR prognosis[tiab] OR "prognostic factors"[tiab])
AND ("overview of reviews"[tiab] OR "umbrella review"[tiab] OR ("systematic review"[tiab] AND review[tiab]))
```

## Notes for Database Conversion
- This search can be converted to CENTRAL, Embase Dialog, and other databases using the conversion tools in this repository
- MeSH terms will need mapping to Emtree terms for Embase
- Proximity operators may need adjustment for different database syntaxes
```

## Dialog (Embase)

```
# Improved Search Formula for Overview of Reviews: Systemic Lupus Erythematosus and Lupus Nephritis Prognosis

## Original Search Formula (User Provided)
```
(("systemic lupus erythematosus"[MeSH Terms] OR "lupus erythematosus, systemic"[Title/Abstract] OR "lupus nephritis"[MeSH Terms] OR "lupus nephritis"[Title/Abstract]))
AND (("prognosis"[MeSH Terms] OR "prognosis"[Title/Abstract] OR "prognostic factors"[Title/Abstract] OR "renal outcome"[Title/Abstract] OR "kidney failure, chronic"[MeSH Terms] OR "end-stage renal disease"[Title/Abstract]))
AND (("systematic review"[Publication Type] OR "meta-analysis"[Publication Type] OR "systematic review"[Title/Abstract] OR "meta-analysis"[Title/Abstract]))
```

## Improved Search Formula for MEDLINE (PubMed)

### Block 1: Population (Systemic Lupus Erythematosus and Lupus Nephritis)
```
S1 EMB.EXACT.EXPLODE("Lupus Erythematosus, Systemic") OR
"Lupus Nephritis"[Mesh] OR
"systemic lupus erythematosus"[tiab] OR
"lupus erythematosus, systemic"[tiab] OR
"lupus nephritis"[tiab] OR
"SLE"[tiab] OR
(lupus[tiab] AND (systemic[tiab] OR nephritis[tiab] OR renal[tiab] OR kidney[tiab])) OR
"lupus glomerulonephritis"[tiab] OR
"lupus kidney disease"[tiab]
```

### Block 2: Prognosis and Outcomes (Enhanced)
```
S2 EMB.EXACT.EXPLODE("Prognosis") OR
"Disease Progression"[Mesh] OR
"Treatment Outcome"[Mesh] OR
"Mortality"[Mesh] OR
"Renal Insufficiency, Chronic"[Mesh] OR
"Kidney Failure, Chronic"[Mesh] OR
prognosis[tiab] OR
"prognostic factors"[tiab] OR
"prognostic factor"[tiab] OR
"renal outcome"[tiab] OR
"renal outcomes"[tiab] OR
"kidney outcome"[tiab] OR
"kidney outcomes"[tiab] OR
"end-stage renal disease"[tiab] OR
"ESRD"[tiab] OR
"chronic kidney disease"[tiab] OR
"CKD"[tiab] OR
"renal function"[tiab] OR
"kidney function"[tiab] OR
"glomerular filtration rate"[tiab] OR
"GFR"[tiab] OR
"renal survival"[tiab] OR
"kidney survival"[tiab] OR
mortality[tiab] OR
survival[tiab] OR
"disease progression"[tiab] OR
"treatment response"[tiab] OR
"treatment outcome"[tiab] OR
"clinical outcome"[tiab] OR
"long-term outcome"[tiab] OR
"predictive factor"[tiab] OR
"risk factor"[tiab]
```

### Block 3: Overview of Reviews and Systematic Reviews (Enhanced)
```
S3 "Review"[Publication Type] OR
"Systematic Review"[Publication Type] OR
"Meta-Analysis"[Publication Type] OR
"systematic review"[tiab] OR
"systematic reviews"[tiab] OR
"meta-analysis"[tiab] OR
"meta-analyses"[tiab] OR
"overview of reviews"[tiab] OR
"umbrella review"[tiab] OR
"umbrella reviews"[tiab] OR
"review of reviews"[tiab] OR
"overview of systematic reviews"[tiab] OR
"meta-review"[tiab] OR
"meta-reviews"[tiab] OR
"Cochrane review"[tiab] OR
"Cochrane reviews"[tiab] OR
"pooled analysis"[tiab] OR
"pooled analyses"[tiab] OR
(review[tiab] AND (systematic[tiab] OR comprehensive[tiab] OR literature[tiab])) OR
"evidence synthesis"[tiab] OR
"research synthesis"[tiab]
```

### Final Search Formula
```
S4 S1 AND S2 AND S3
Filters: English, Humans
```

## Key Improvements Made

### 1. Enhanced MeSH Terms
- Added "Lupus Erythematosus, Systemic"[Mesh] (proper MeSH format)
- Added "Disease Progression"[Mesh], "Treatment Outcome"[Mesh], "Mortality"[Mesh]
- Added "Renal Insufficiency, Chronic"[Mesh] for better renal outcome coverage

### 2. Expanded Text Word Coverage
- Added common abbreviations: SLE, ESRD, CKD, GFR
- Added synonymous terms: lupus glomerulonephritis, lupus kidney disease
- Enhanced prognosis terms: survival, mortality, disease progression, treatment response
- Added renal function terminology: glomerular filtration rate, renal survival

### 3. Comprehensive Review Literature Identification
- Added "overview of reviews" and "umbrella review" terms specifically
- Added "Review"[Publication Type] for broader coverage
- Added Cochrane-specific terms
- Added evidence synthesis terminology

### 4. Improved Search Logic
- Used proper field tags [tiab] instead of [Title/Abstract]
- Structured in clear conceptual blocks
- Added proximity considerations with AND logic within concepts

### 5. Quality Filters
- Added language filter (English)
- Added species filter (Humans)

## Estimated Search Performance
- **Sensitivity**: High - comprehensive coverage of SLE/LN terminology and outcomes
- **Specificity**: Improved - focused on review literature with specific outcome measures
- **Precision**: Enhanced - structured Boolean logic reduces irrelevant results

## Alternative Versions

### High Sensitivity Version (for comprehensive screening)
Use all terms as above

### High Precision Version (for focused results)
```
("Lupus Erythematosus, Systemic"[Mesh] OR "Lupus Nephritis"[Mesh])
AND ("Prognosis"[Mesh] OR "Treatment Outcome"[Mesh] OR prognosis[tiab] OR "prognostic factors"[tiab])
AND ("overview of reviews"[tiab] OR "umbrella review"[tiab] OR ("systematic review"[tiab] AND review[tiab]))
```

## Notes for Database Conversion
- This search can be converted to CENTRAL, Embase Dialog, and other databases using the conversion tools in this repository
- MeSH terms will need mapping to Emtree terms for Embase
- Proximity operators may need adjustment for different database syntaxes
```

## Command Line for Dialog

Dialog検索画面でコピー&ペーストして使用するコマンドライン形式：

```
```
(("systemic lupus erythematosus"[MeSH Terms] OR "lupus erythematosus, systemic"[Title/Abstract] OR "lupus nephritis"[MeSH Terms] OR "lupus nephritis"[Title/Abstract]))
AND (("prognosis"[MeSH Terms] OR "prognosis"[Title/Abstract] OR "prognostic factors"[Title/Abstract] OR "renal outcome"[Title/Abstract] OR "kidney failure, chronic"[MeSH Terms] OR "end-stage renal disease"[Title/Abstract]))
AND (("systematic review"[Publication Type] OR "meta-analysis"[Publication Type] OR "systematic review"[Title/Abstract] OR "meta-analysis"[Title/Abstract]))
```
```
EMB.EXACT.EXPLODE("Lupus Erythematosus, Systemic") OR
"Lupus Nephritis"[Mesh] OR
"systemic lupus erythematosus"[tiab] OR
"lupus erythematosus, systemic"[tiab] OR
"lupus nephritis"[tiab] OR
"SLE"[tiab] OR
(lupus[tiab] AND (systemic[tiab] OR nephritis[tiab] OR renal[tiab] OR kidney[tiab])) OR
"lupus glomerulonephritis"[tiab] OR
"lupus kidney disease"[tiab]
```
```
EMB.EXACT.EXPLODE("Prognosis") OR
"Disease Progression"[Mesh] OR
"Treatment Outcome"[Mesh] OR
"Mortality"[Mesh] OR
"Renal Insufficiency, Chronic"[Mesh] OR
"Kidney Failure, Chronic"[Mesh] OR
prognosis[tiab] OR
"prognostic factors"[tiab] OR
"prognostic factor"[tiab] OR
"renal outcome"[tiab] OR
"renal outcomes"[tiab] OR
"kidney outcome"[tiab] OR
"kidney outcomes"[tiab] OR
"end-stage renal disease"[tiab] OR
"ESRD"[tiab] OR
"chronic kidney disease"[tiab] OR
"CKD"[tiab] OR
"renal function"[tiab] OR
"kidney function"[tiab] OR
"glomerular filtration rate"[tiab] OR
"GFR"[tiab] OR
"renal survival"[tiab] OR
"kidney survival"[tiab] OR
mortality[tiab] OR
survival[tiab] OR
"disease progression"[tiab] OR
"treatment response"[tiab] OR
"treatment outcome"[tiab] OR
"clinical outcome"[tiab] OR
"long-term outcome"[tiab] OR
"predictive factor"[tiab] OR
"risk factor"[tiab]
```
```
"Review"[Publication Type] OR
"Systematic Review"[Publication Type] OR
"Meta-Analysis"[Publication Type] OR
"systematic review"[tiab] OR
"systematic reviews"[tiab] OR
"meta-analysis"[tiab] OR
"meta-analyses"[tiab] OR
"overview of reviews"[tiab] OR
"umbrella review"[tiab] OR
"umbrella reviews"[tiab] OR
"review of reviews"[tiab] OR
"overview of systematic reviews"[tiab] OR
"meta-review"[tiab] OR
"meta-reviews"[tiab] OR
"Cochrane review"[tiab] OR
"Cochrane reviews"[tiab] OR
"pooled analysis"[tiab] OR
"pooled analyses"[tiab] OR
(review[tiab] AND (systematic[tiab] OR comprehensive[tiab] OR literature[tiab])) OR
"evidence synthesis"[tiab] OR
"research synthesis"[tiab]
```
```
S1 AND S2 AND S3
Filters: English, Humans
```
- Added "Lupus Erythematosus, Systemic"[Mesh] (proper MeSH format)
- Added "Disease Progression"[Mesh], "Treatment Outcome"[Mesh], "Mortality"[Mesh]
- Added "Renal Insufficiency, Chronic"[Mesh] for better renal outcome coverage
- Added common abbreviations: SLE, ESRD, CKD, GFR
- Added synonymous terms: lupus glomerulonephritis, lupus kidney disease
- Enhanced prognosis terms: survival, mortality, disease progression, treatment response
- Added renal function terminology: glomerular filtration rate, renal survival
- Added "overview of reviews" and "umbrella review" terms specifically
- Added "Review"[Publication Type] for broader coverage
- Added Cochrane-specific terms
- Added evidence synthesis terminology
- Used proper field tags [tiab] instead of [Title/Abstract]
- Structured in clear conceptual blocks
- Added proximity considerations with AND logic within concepts
- Added language filter (English)
- Added species filter (Humans)
- **Sensitivity**: High - comprehensive coverage of SLE/LN terminology and outcomes
- **Specificity**: Improved - focused on review literature with specific outcome measures
- **Precision**: Enhanced - structured Boolean logic reduces irrelevant results
Use all terms as above
```
("Lupus Erythematosus, Systemic"[Mesh] OR "Lupus Nephritis"[Mesh])
AND ("Prognosis"[Mesh] OR "Treatment Outcome"[Mesh] OR prognosis[tiab] OR "prognostic factors"[tiab])
AND ("overview of reviews"[tiab] OR "umbrella review"[tiab] OR ("systematic review"[tiab] AND review[tiab]))
```
- This search can be converted to CENTRAL, Embase Dialog, and other databases using the conversion tools in this repository
- MeSH terms will need mapping to Emtree terms for Embase
- Proximity operators may need adjustment for different database syntaxes
```
