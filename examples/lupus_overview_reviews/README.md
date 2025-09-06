# Improved Search Formula for Overview of Reviews: Systemic Lupus Erythematosus and Lupus Nephritis Prognosis

## Project Overview

This project contains an improved search formula for conducting an overview of reviews (umbrella review) on the prognosis of systemic lupus erythematosus (SLE) and lupus nephritis. The search strategy has been significantly enhanced from the original user-provided formula to improve both sensitivity and specificity.

## Files in this Directory

- `lupus_overview_reviews_improved.md` - The main improved search formula with detailed explanations
- `lupus_overview_reviews_validation_results.md` - Validation results showing hit counts for search terms
- `all_database_search.md` - Multi-database converted versions (PubMed, CENTRAL, Embase Dialog)
- `README.md` - This documentation file

## Key Improvements Made

### 1. Enhanced MeSH Terms
- Added proper MeSH format: "Lupus Erythematosus, Systemic"[Mesh], "Lupus Nephritis"[Mesh]
- Added outcome-related MeSH: "Disease Progression"[Mesh], "Treatment Outcome"[Mesh], "Mortality"[Mesh]
- Added renal-specific MeSH: "Renal Insufficiency, Chronic"[Mesh], "Kidney Failure, Chronic"[Mesh]

### 2. Expanded Text Word Coverage
- Added common abbreviations: SLE, ESRD, CKD, GFR
- Added synonymous terms: lupus glomerulonephritis, lupus kidney disease
- Enhanced prognosis terminology: survival, mortality, disease progression, treatment response
- Added renal function terms: glomerular filtration rate, renal survival

### 3. Comprehensive Review Literature Identification
- Added specific "overview of reviews" and "umbrella review" terminology
- Added "Review"[Publication Type] for broader coverage
- Added Cochrane-specific terms and evidence synthesis terminology
- Enhanced systematic review identification

### 4. Improved Search Structure
- Used proper field tags [tiab] instead of [Title/Abstract]
- Structured in clear conceptual blocks (Population, Outcomes, Study Design)
- Added quality filters (English, Humans)

## Search Performance

**Validation Results:**
- Final combined search: **1,281 results**
- Individual block validation completed successfully
- Appropriate balance between sensitivity and specificity for overview of reviews

**Original vs. Improved:**
- Original: Basic MeSH + Title/Abstract approach
- Improved: Comprehensive multi-faceted approach with enhanced terminology

## Database Formats Available

1. **PubMed/MEDLINE** - Primary format with full MeSH and text word coverage
2. **Cochrane CENTRAL** - Converted with proper [mh] syntax and field tags
3. **Embase Dialog** - Command-line format with EMB.EXACT.EXPLODE() syntax

## Usage Instructions

### For PubMed:
Copy the search blocks from `lupus_overview_reviews_improved.md` and execute sequentially, then combine with #1 AND #2 AND #3.

### For Other Databases:
Use the converted formats in `all_database_search.md` - each database section contains ready-to-use search syntax.

### Alternative Versions:
- **High Sensitivity**: Use the full improved formula (recommended for comprehensive screening)
- **High Precision**: Use the simplified version provided for focused results

## Quality Assurance

- Search syntax validated using repository validation tools
- Hit counts verified for all major search components
- Multi-database conversion tested and formatted
- Follows best practices for systematic review search methodology

## Contact

This search formula was developed using the SRWS-PSG search-formula-developper toolkit. For questions about the methodology or further refinements, refer to the repository documentation.

---
*Generated: September 6, 2025*
*Validation: 1,281 results in PubMed*
*Status: Ready for use*
