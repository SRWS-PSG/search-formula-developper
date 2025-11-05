# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a systematic review search strategy development support system (SRWS). The system helps researchers develop, validate, and convert search formulas for systematic reviews and scoping reviews across multiple medical databases.

**Core Purpose**: Automate the systematic review search process by:
- Structuring search formulas in markdown format
- Validating search terms against PubMed/MEDLINE
- Analyzing MeSH terms from seed papers
- Converting search formulas between database formats (PubMed ↔ CENTRAL ↔ Embase/Dialog ↔ ClinicalTrials.gov ↔ ICTRP ↔ Ovid)
- Processing search results for screening tools like Rayyan

## Architecture

### Directory Structure
```
scripts/
├── search/              # Search formula validation and execution
│   ├── term_validator/  # Individual term and line validation
│   ├── mesh_analyzer/   # MeSH term analysis and hierarchy
│   ├── query_executor/  # Final query execution and RIS export
│   └── extract_mesh.py  # MeSH extraction from seed PMIDs
├── conversion/          # Database format converters
│   ├── ovid/           # Ovid → PubMed conversion
│   ├── clinicaltrials/ # ClinicalTrials.gov conversion
│   └── ictrp/          # ICTRP conversion
├── validation/         # Search formula validation tools
│   ├── seed_analyzer/  # Seed paper analysis
│   └── result_validator/ # Result validation
├── search_results_to_review/  # Post-search processing
└── utils/              # Analysis utilities

search_formula/         # Project workspace (one dir per research project)
templates/              # Templates for PICO, RQ, and database searches
```

### Key Workflows

1. **Search Formula Development**:
   - Define PICO framework → Structure search formula → Validate each line → Check MeSH terms → Execute final query → Export RIS

2. **MeSH Analysis**:
   - Provide seed PMIDs → Extract MeSH terms → Generate hierarchy diagrams → Select optimal terms → Integrate into search formula

3. **Database Conversion**:
   - PubMed formula → Parse and convert → Output format for target database

## Common Commands

### Search Formula Validation

Check individual search lines and terms:
```bash
python scripts/search/term_validator/check_search_lines.py --input-formula search_formula/PROJECT_NAME/search_formula.md --output search_formula/PROJECT_NAME/search_lines_results.md
```

Execute final query with seed paper validation:
```bash
python scripts/search/query_executor/check_final_query.py --formula-file search_formula/PROJECT_NAME/search_formula.md --pmid-file search_formula/PROJECT_NAME/seed_pmids.txt --output-dir search_formula/PROJECT_NAME/
```

### MeSH Analysis

Extract and analyze MeSH terms from seed papers:
```bash
python scripts/search/extract_mesh.py --pmid-file search_formula/PROJECT_NAME/seed_pmids.txt --output-dir search_formula/PROJECT_NAME/
```

Check specific MeSH terms:
```bash
python scripts/search/mesh_analyzer/check_mesh.py --terms "Term1,Term2,Term3"
```

Analyze MeSH overlap between terms:
```bash
python scripts/search/mesh_analyzer/check_mesh_overlap.py --terms "Term1,Term2,Term3"
```

### Database Conversion

Convert PubMed formula to all supported database formats:
```bash
python scripts/conversion/generate_all_database_search.py --input search_formula/PROJECT_NAME/search_formula.md --output-dir search_formula/PROJECT_NAME/
```

Convert individual format using search_converter.py:
```bash
python scripts/conversion/search_converter.py --input search_formula.md --output output.md --target-db [central|dialog|clinicaltrials|ictrp]
```

Convert Ovid to PubMed programmatically:
```python
from scripts.conversion.ovid.converter import convert_ovid_to_pubmed
pubmed_query, warnings = convert_ovid_to_pubmed(ovid_query)
```

### Search Results Processing

Process search results from multiple databases for Rayyan:
```bash
python scripts/search_results_to_review/search_results_processor.py --input-dir search_formula/PROJECT_NAME/ --output-dir search_formula/PROJECT_NAME/processed/
```

### Validation and Analysis

Analyze which search components match specific papers:
```bash
python scripts/validation/seed_analyzer/check_specific_papers.py --formula-file search_formula/PROJECT_NAME/search_formula.md --pmid-file search_formula/PROJECT_NAME/seed_pmids.txt
```

Compare original vs modified search formulas:
```bash
python scripts/validation/result_validator/check_modified_search.py --original original.md --modified modified.md --pmids seed_pmids.txt
```

### Testing

Run all tests:
```bash
pytest -q
```

Run specific test file:
```bash
pytest tests/test_ovid_to_pubmed.py -q
```

## Important Conventions

### Search Formula Format

Search formulas are written in markdown with specific structure:
```markdown
# Project Name

## PubMed/MEDLINE

### Block structure
#1 Population
    "Disease"[Mesh] OR
    disease[tiab] OR
    condition[tiab]

#2 Intervention
    "Therapy"[Mesh] OR
    treatment[tiab]

#3 Final Query
    #1 AND #2
    Filters: Humans, English
```

### Field Tags

PubMed field tags used throughout:
- `[Mesh]` or `[MeSH Terms]` - MeSH descriptor
- `[tiab]` - Title/Abstract
- `[ti]` - Title only
- `[ab]` - Abstract only
- `[tw]` - Text Word
- `[tiab:~N]` - Proximity operator (within N words)

### File Naming

- Project directories: `search_formula/project_name/`
- Search formula: `search_formula.md`
- Seed PMIDs: `seed_pmids.txt` (one PMID per line, `#` for comments)
- MeSH analysis output: `mesh_analysis.md`, `mesh_analysis_results.json`
- Search results: `log/search_results_YYYYMMDD_HHMMSS.ris`

### PICO Framework

Projects should define PICO elements:
- **P**opulation - Target patient group or population
- **I**ntervention - Treatment, exposure, or diagnostic test
- **C**omparison - Comparator or control (if applicable)
- **O**utcome - Outcomes or endpoints of interest

Use `templates/rq_template.md` as starting point for new research questions.

## Key Technical Details

### API Usage

- All scripts use NCBI E-utilities API for PubMed queries
- API rate limit: 3 requests/second (without API key), 10 requests/second (with API key)
- Scripts include `time.sleep()` to respect rate limits
- Set `NCBI_API_KEY` environment variable if you have an API key

### MeSH Hierarchy

The MeSH extraction system:
1. Fetches paper details via PubMed API
2. Extracts MeSH descriptors and qualifiers
3. Retrieves tree numbers from NCBI MeSH browser
4. Queries RDF endpoint for hierarchy information
5. Generates Mermaid diagrams showing hierarchical structure
6. Highlights terms appearing in seed papers

### Database Conversion Logic

Each database has specific syntax requirements:
- **CENTRAL**: Uses `MeSH descriptor: [Term] explode all trees` and `:ti,ab,kw` fields
- **Dialog/Embase**: Uses `EMB.EXACT.EXPLODE()` and `S1`, `S2` line references
- **ClinicalTrials.gov**: Expands MeSH to synonyms, separates into Condition/Intervention/Other
- **ICTRP**: Simple format with shallow nesting, MeSH expanded to synonyms
- **Ovid→PubMed**: Converts `exp`, `adj` operators, field tags, and handles wildcards

### RIS File Processing

The search results processor:
- Auto-detects file formats (RIS, NBIB, XML)
- Deduplicates based on DOI and title similarity
- Outputs Rayyan-compatible CSV files
- Generates PRISMA flow statistics
- Splits large result sets (500 records per file)

## Development Notes

- Python 3.7+ required
- PEP 8 coding style
- Type hints encouraged for new code
- Scripts should handle API errors gracefully with retries
- All new database converters should include comprehensive unit tests
- When modifying conversion logic, update both the converter and tests

## Project-Specific Context

This repository is designed for medical/health sciences researchers conducting systematic reviews and meta-analyses. The typical user:
- Has a research question with PICO elements
- Has identified 5-10 "seed papers" that should be captured by the search
- Needs to search multiple databases (PubMed, CENTRAL, Embase, trial registries)
- Must document the search strategy for publication/peer review
- Requires reproducible, validated search formulas

When developing features, prioritize:
1. Search sensitivity (capturing all relevant papers) over specificity
2. Clear documentation of conversion rules and limitations
3. Validation against seed papers
4. PRISMA-compliant reporting
