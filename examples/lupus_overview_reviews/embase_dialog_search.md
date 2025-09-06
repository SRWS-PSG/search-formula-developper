# Embase Dialog Search Formula: Systemic Lupus Erythematosus and Lupus Nephritis Prognosis - Overview of Reviews

## Search Strategy for Embase Dialog Interface

### Block S1: Population (Systemic Lupus Erythematosus and Lupus Nephritis)
```
S1 EMB.EXACT.EXPLODE("Lupus Erythematosus, Systemic") OR
   EMB.EXACT.EXPLODE("Lupus Nephritis") OR
   TI("systemic lupus erythematosus") OR AB("systemic lupus erythematosus") OR
   TI("lupus erythematosus, systemic") OR AB("lupus erythematosus, systemic") OR
   TI("lupus nephritis") OR AB("lupus nephritis") OR
   TI("SLE") OR AB("SLE") OR
   (TI(lupus) OR AB(lupus)) AND (TI(systemic) OR AB(systemic) OR TI(nephritis) OR AB(nephritis) OR TI(renal) OR AB(renal) OR TI(kidney) OR AB(kidney)) OR
   TI("lupus glomerulonephritis") OR AB("lupus glomerulonephritis") OR
   TI("lupus kidney disease") OR AB("lupus kidney disease")
```

### Block S2: Prognosis and Outcomes (Enhanced)
```
S2 EMB.EXACT.EXPLODE("Prognosis") OR
   EMB.EXACT.EXPLODE("Disease Progression") OR
   EMB.EXACT.EXPLODE("Treatment Outcome") OR
   EMB.EXACT.EXPLODE("Mortality") OR
   EMB.EXACT.EXPLODE("Renal Insufficiency, Chronic") OR
   EMB.EXACT.EXPLODE("Kidney Failure, Chronic") OR
   TI(prognosis) OR AB(prognosis) OR
   TI("prognostic factors") OR AB("prognostic factors") OR
   TI("prognostic factor") OR AB("prognostic factor") OR
   TI("renal outcome") OR AB("renal outcome") OR
   TI("renal outcomes") OR AB("renal outcomes") OR
   TI("kidney outcome") OR AB("kidney outcome") OR
   TI("kidney outcomes") OR AB("kidney outcomes") OR
   TI("end-stage renal disease") OR AB("end-stage renal disease") OR
   TI("ESRD") OR AB("ESRD") OR
   TI("chronic kidney disease") OR AB("chronic kidney disease") OR
   TI("CKD") OR AB("CKD") OR
   TI("renal function") OR AB("renal function") OR
   TI("kidney function") OR AB("kidney function") OR
   TI("glomerular filtration rate") OR AB("glomerular filtration rate") OR
   TI("GFR") OR AB("GFR") OR
   TI("renal survival") OR AB("renal survival") OR
   TI("kidney survival") OR AB("kidney survival") OR
   TI(mortality) OR AB(mortality) OR
   TI(survival) OR AB(survival) OR
   TI("disease progression") OR AB("disease progression") OR
   TI("treatment response") OR AB("treatment response") OR
   TI("treatment outcome") OR AB("treatment outcome") OR
   TI("clinical outcome") OR AB("clinical outcome") OR
   TI("long-term outcome") OR AB("long-term outcome") OR
   TI("predictive factor") OR AB("predictive factor") OR
   TI("risk factor") OR AB("risk factor")
```

### Block S3: Overview of Reviews and Systematic Reviews (Enhanced)
```
S3 PT("Review") OR
   PT("Systematic Review") OR
   PT("Meta-Analysis") OR
   TI("systematic review") OR AB("systematic review") OR
   TI("systematic reviews") OR AB("systematic reviews") OR
   TI("meta-analysis") OR AB("meta-analysis") OR
   TI("meta-analyses") OR AB("meta-analyses") OR
   TI("overview of reviews") OR AB("overview of reviews") OR
   TI("umbrella review") OR AB("umbrella review") OR
   TI("umbrella reviews") OR AB("umbrella reviews") OR
   TI("review of reviews") OR AB("review of reviews") OR
   TI("overview of systematic reviews") OR AB("overview of systematic reviews") OR
   TI("meta-review") OR AB("meta-review") OR
   TI("meta-reviews") OR AB("meta-reviews") OR
   TI("Cochrane review") OR AB("Cochrane review") OR
   TI("Cochrane reviews") OR AB("Cochrane reviews") OR
   TI("pooled analysis") OR AB("pooled analysis") OR
   TI("pooled analyses") OR AB("pooled analyses") OR
   (TI(review) OR AB(review)) AND (TI(systematic) OR AB(systematic) OR TI(comprehensive) OR AB(comprehensive) OR TI(literature) OR AB(literature)) OR
   TI("evidence synthesis") OR AB("evidence synthesis") OR
   TI("research synthesis") OR AB("research synthesis")
```

### Final Search Formula
```
S4 S1 AND S2 AND S3
```

### Filters (Apply after S4)
```
AND LA(English) AND HUMAN
```

## Command Line Format for Copy-Paste

### Step 1: Population Block
```
EMB.EXACT.EXPLODE("Lupus Erythematosus, Systemic") OR EMB.EXACT.EXPLODE("Lupus Nephritis") OR TI("systemic lupus erythematosus") OR AB("systemic lupus erythematosus") OR TI("lupus erythematosus, systemic") OR AB("lupus erythematosus, systemic") OR TI("lupus nephritis") OR AB("lupus nephritis") OR TI("SLE") OR AB("SLE") OR (TI(lupus) OR AB(lupus)) AND (TI(systemic) OR AB(systemic) OR TI(nephritis) OR AB(nephritis) OR TI(renal) OR AB(renal) OR TI(kidney) OR AB(kidney)) OR TI("lupus glomerulonephritis") OR AB("lupus glomerulonephritis") OR TI("lupus kidney disease") OR AB("lupus kidney disease")
```

### Step 2: Prognosis Block
```
EMB.EXACT.EXPLODE("Prognosis") OR EMB.EXACT.EXPLODE("Disease Progression") OR EMB.EXACT.EXPLODE("Treatment Outcome") OR EMB.EXACT.EXPLODE("Mortality") OR EMB.EXACT.EXPLODE("Renal Insufficiency, Chronic") OR EMB.EXACT.EXPLODE("Kidney Failure, Chronic") OR TI(prognosis) OR AB(prognosis) OR TI("prognostic factors") OR AB("prognostic factors") OR TI("prognostic factor") OR AB("prognostic factor") OR TI("renal outcome") OR AB("renal outcome") OR TI("renal outcomes") OR AB("renal outcomes") OR TI("kidney outcome") OR AB("kidney outcome") OR TI("kidney outcomes") OR AB("kidney outcomes") OR TI("end-stage renal disease") OR AB("end-stage renal disease") OR TI("ESRD") OR AB("ESRD") OR TI("chronic kidney disease") OR AB("chronic kidney disease") OR TI("CKD") OR AB("CKD") OR TI("renal function") OR AB("renal function") OR TI("kidney function") OR AB("kidney function") OR TI("glomerular filtration rate") OR AB("glomerular filtration rate") OR TI("GFR") OR AB("GFR") OR TI("renal survival") OR AB("renal survival") OR TI("kidney survival") OR AB("kidney survival") OR TI(mortality) OR AB(mortality) OR TI(survival) OR AB(survival) OR TI("disease progression") OR AB("disease progression") OR TI("treatment response") OR AB("treatment response") OR TI("treatment outcome") OR AB("treatment outcome") OR TI("clinical outcome") OR AB("clinical outcome") OR TI("long-term outcome") OR AB("long-term outcome") OR TI("predictive factor") OR AB("predictive factor") OR TI("risk factor") OR AB("risk factor")
```

### Step 3: Review Literature Block
```
PT("Review") OR PT("Systematic Review") OR PT("Meta-Analysis") OR TI("systematic review") OR AB("systematic review") OR TI("systematic reviews") OR AB("systematic reviews") OR TI("meta-analysis") OR AB("meta-analysis") OR TI("meta-analyses") OR AB("meta-analyses") OR TI("overview of reviews") OR AB("overview of reviews") OR TI("umbrella review") OR AB("umbrella review") OR TI("umbrella reviews") OR AB("umbrella reviews") OR TI("review of reviews") OR AB("review of reviews") OR TI("overview of systematic reviews") OR AB("overview of systematic reviews") OR TI("meta-review") OR AB("meta-review") OR TI("meta-reviews") OR AB("meta-reviews") OR TI("Cochrane review") OR AB("Cochrane review") OR TI("Cochrane reviews") OR AB("Cochrane reviews") OR TI("pooled analysis") OR AB("pooled analysis") OR TI("pooled analyses") OR AB("pooled analyses") OR (TI(review) OR AB(review)) AND (TI(systematic) OR AB(systematic) OR TI(comprehensive) OR AB(comprehensive) OR TI(literature) OR AB(literature)) OR TI("evidence synthesis") OR AB("evidence synthesis") OR TI("research synthesis") OR AB("research synthesis")
```

### Step 4: Combine All Blocks
```
S1 AND S2 AND S3 AND LA(English) AND HUMAN
```

## Key Features of this Dialog Search

### Embase-Specific Syntax
- **EMB.EXACT.EXPLODE()**: Searches Emtree terms with automatic hierarchy expansion
- **TI()**: Title field search
- **AB()**: Abstract field search  
- **PT()**: Publication Type field
- **LA()**: Language filter
- **HUMAN**: Species filter

### Enhanced Coverage
- **MeSH/Emtree Terms**: Comprehensive controlled vocabulary coverage
- **Text Words**: Extensive free-text terminology including abbreviations
- **Review Types**: Specific terminology for overview of reviews methodology
- **Outcome Terms**: Comprehensive prognosis and renal outcome terminology

### Search Strategy Notes
1. Execute each block (S1, S2, S3) separately in Dialog interface
2. Combine using final formula: S1 AND S2 AND S3
3. Apply language and species filters
4. Expected results: Comprehensive coverage for overview of reviews on SLE/LN prognosis

---
*Generated: September 6, 2025*  
*Database: Embase Dialog Interface*  
*Methodology: Overview of Reviews*
