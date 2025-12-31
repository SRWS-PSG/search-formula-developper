# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a systematic review search strategy development support system (SRWS). The system helps researchers develop, validate, and convert search formulas for systematic reviews and scoping reviews across multiple medical databases.

## Skills Integration

このリポジトリには、Claude Codeの自然言語対話で発動するSkillsが実装されています。Skillsを使用することで、systematic reviewプロジェクトの主要なタスクを効率的に実行できます。

### Available Skills

| Skill名 | 発動キーワード例 | 主な機能 |
|---------|-----------------|---------|
| **search-validator** | "検索式を検証して" | 検索式検証、seed paper捕捉確認 |
| **mesh-analyzer** | "MeSHを抽出して" | MeSH抽出・階層分析・重複チェック |
| **database-converter** | "全データベース形式に変換" | PubMed → CENTRAL/Embase/ClinicalTrials/ICTRP変換 |
| **term-counter** | "各キーワードの件数を調べて" | 検索語件数確認・ブロック重複分析 |
| **project-initializer** | "新しいプロジェクトを作成" | プロジェクト構造初期化 |
| **eric-searcher** | "ERICで検索" | ERIC検索・シソーラス確認 |

詳細は [.claude/skills/README.md](.claude/skills/README.md) を参照してください。

### Typical Workflow with Skills

```
1. project-initializer → プロジェクト作成
2. (手動) protocol.md編集、seed PMIDs登録
3. mesh-analyzer → MeSH抽出
4. (外部AI) 検索式作成
5. search-validator → 検索式検証
6. term-counter → 検索語最適化
7. database-converter → 他DB形式変換
8. eric-searcher → ERIC検索 (教育研究の場合)
```

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
│   ├── eric/           # ERIC database integration
│   │   ├── eric_api.py         # ERIC API client
│   │   ├── search_eric.py      # ERIC search CLI
│   │   ├── eric_thesaurus.py   # Thesaurus scraper
│   │   └── check_eric_thesaurus.py  # Thesaurus CLI
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

projects/               # Project workspace (one directory per research project)
├── PROJECT_NAME/
│   ├── protocol.md     # Research protocol with PICO/RQ definition
│   ├── seed_papers/    # Key papers bibliography (RIS, NBIB, or text)
│   ├── seed_pmids.txt  # PMIDs extracted from seed papers
│   ├── search_formula.md  # Main search formula
│   ├── mesh_analysis.md   # MeSH extraction results (optional)
│   └── log/            # Validation and search results
templates/              # Templates for PICO, RQ, and database searches
```

## Project Setup Workflow

### Standard Project Structure

Each systematic review project should follow this structure in `projects/PROJECT_NAME/`:

1. **protocol.md** - Research protocol defining:
   - Research question (RQ)
   - PICO framework (Population, Intervention, Comparison, Outcome)
   - Inclusion/exclusion criteria
   - Study design requirements

2. **seed_papers/** (optional) - Bibliography files of key papers:
   - RIS format (`.ris`)
   - NBIB format (`.nbib`)
   - Plain text with DOIs/PMIDs
   - RTF or Word documents with references

3. **seed_pmids.txt** - Extracted PMIDs (one per line):
   ```
   12345678
   23456789
   # Comments allowed with #
   34567890
   ```

4. **search_formula.md** - Main search formula developed iteratively

5. **log/** (auto-created) - Validation results and search outputs

### Starting a New Project

**Step 1: Create project folder**
```bash
mkdir -p projects/PROJECT_NAME/seed_papers
```

**Step 2: Create protocol from template**
```bash
cp templates/rq_template.md projects/PROJECT_NAME/protocol.md
# Edit protocol.md to define RQ and PICO
```

**Step 3: Prepare seed papers**
- Place key papers bibliography in `seed_papers/`
- Extract PMIDs to `seed_pmids.txt` (manual or scripted)

**Step 4: Interactive search formula development**
- Use external AI assistant (VS Code Copilot, ChatGPT, etc.) to:
  - Analyze protocol and seed papers
  - Suggest initial search terms based on PICO
  - Iteratively refine search formula
- Save results to `projects/PROJECT_NAME/search_formula.md`

**Step 5: Validate with automated tools**
```bash
# Validate seed paper capture
python scripts/search/query_executor/check_final_query.py \
  --formula-file projects/PROJECT_NAME/search_formula.md \
  --pmid-file projects/PROJECT_NAME/seed_pmids.txt \
  --output-dir projects/PROJECT_NAME/

# Extract MeSH terms from seeds
python scripts/search/extract_mesh.py \
  --pmid-file projects/PROJECT_NAME/seed_pmids.txt \
  --output-dir projects/PROJECT_NAME/
```

### AI-Assisted Development (External to Repository)

This repository provides **validation and conversion tools** only. The actual search formula development is expected to be done interactively with AI assistants **outside this repository**:

- **VS Code Copilot Chat** - Context-aware suggestions within IDE
- **ChatGPT / Claude** - Iterative dialogue for search strategy
- **GitHub Copilot** - Inline term suggestions

**Recommended workflow**:
1. Share `protocol.md` and seed paper bibliography with AI assistant
2. Iteratively develop search formula through dialogue
3. Paste resulting formula into `projects/PROJECT_NAME/search_formula.md`
4. Validate with repository scripts
5. Refine based on validation results → return to step 2

**Benefits of this approach**:
- Leverage AI's medical knowledge and synonym generation
- Maintain human oversight for clinical relevance
- Use repository tools for objective validation
- Keep iterative dialogue history outside version control

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
python scripts/search/term_validator/check_search_lines.py --input-formula projects/PROJECT_NAME/search_formula.md --output projects/PROJECT_NAME/log/search_lines_results.md
```

Execute final query with seed paper validation:
```bash
python scripts/search/query_executor/check_final_query.py --formula-file projects/PROJECT_NAME/search_formula.md --pmid-file projects/PROJECT_NAME/seed_pmids.txt --output-dir projects/PROJECT_NAME/
```

**Important**: This script validates seed papers efficiently by checking each PMID individually (`query AND pmid[PMID]`) rather than retrieving all search results. This ensures accurate validation even for large result sets (>10,000 hits), as older papers may not appear in the first batch of results returned by PubMed API.

**Output includes**:
- Total search result count
- Individual seed paper capture status (✅ captured / ❌ missed)
- Overall capture rate (e.g., 5/5 = 100%)

**Note**: RIS file export is skipped for performance. To export results, use PubMed Web UI or modify the script to include `export_to_ris()` with full result retrieval.

### MeSH Analysis

Extract and analyze MeSH terms from seed papers:
```bash
python scripts/search/extract_mesh.py --pmid-file projects/PROJECT_NAME/seed_pmids.txt --output-dir projects/PROJECT_NAME/
```

Check specific MeSH terms:
```bash
python scripts/search/mesh_analyzer/check_mesh.py --terms "Term1,Term2,Term3"
```

Analyze MeSH overlap between terms:
```bash
python scripts/search/mesh_analyzer/check_mesh_overlap.py --terms "Term1,Term2,Term3"
```

### ERIC Search (Education Database)

Search ERIC database for education research:
```bash
# Basic search
python scripts/search/eric/search_eric.py -q "medical education" -r 20

# Thesaurus (descriptor) + free word search
python scripts/search/eric/search_eric.py -q "subject:\"Medical School Faculty\" AND burnout"

# Peer-reviewed only (using --peer-reviewed flag)
python scripts/search/eric/search_eric.py -q "faculty development" --peer-reviewed --count-only

# Year range filter (2020 onwards)
python scripts/search/eric/search_eric.py -q "faculty development" --year-min 2020 --count-only

# Full filter combination
python scripts/search/eric/search_eric.py -q "medical education" --peer-reviewed --year-min 2020 --year-max 2025 --count-only

# IES Funded research only
python scripts/search/eric/search_eric.py -q "reading" --ies-funded --count-only

# WWC (What Works Clearinghouse) reviewed only
python scripts/search/eric/search_eric.py -q "reading" --wwc-reviewed y --count-only

# Export to RIS
python scripts/search/eric/search_eric.py -q "medical education" -o results.ris
```

**CLI Filter Options:**
| Option | Description |
|--------|-------------|
| `--peer-reviewed` | Peer-reviewed articles only |
| `--year-min YYYY` | Minimum publication year |
| `--year-max YYYY` | Maximum publication year |
| `--fulltext` | Full text available only |
| `--ies-funded` | IES funded research only |
| `--wwc-reviewed [y/r/n]` | WWC reviewed (y=Meets Standards, r=With Reservations, n=Does Not Meet) |

**Programmatic Query Building with ERICQueryBuilder:**
```python
from scripts.search.eric.eric_api import ERICQueryBuilder, search_eric

builder = ERICQueryBuilder()
query = (builder
    .add_term("faculty development", field="title")
    .add_descriptor("Medical School Faculty")
    .peer_reviewed_only()
    .set_date_range(min_year=2020)
    .build())

result = search_eric(query, rows=10)
print(f"Total: {result.total_count}")
```

**Available QueryBuilder methods:**
- `.add_term(term, field=None, required=False, excluded=False)` - Add search term
- `.add_descriptor(descriptor, exact=False)` - Add thesaurus term
- `.add_or_group(terms, field=None)` - Add OR-grouped terms
- `.set_date_range(min_year=None, max_year=None)` - Set year range
- `.peer_reviewed_only()` - Filter peer-reviewed
- `.fulltext_only()` - Filter full text available
- `.ies_funded_only()` - Filter IES funded
- `.wwc_reviewed(level)` - Filter WWC reviewed (y/r/n)
- `.build()` - Generate query string
- `.reset()` - Reset builder

**Convenience search functions:**
```python
from scripts.search.eric.eric_api import (
    search_eric_peer_reviewed,
    search_eric_with_date_range,
    search_eric_fulltext,
    search_eric_ies_funded,
    search_eric_wwc_reviewed,
)

# Peer-reviewed only
result = search_eric_peer_reviewed("faculty development", rows=10)

# With date range
result = search_eric_with_date_range("medical education", min_year=2020, max_year=2025)

# IES funded
result = search_eric_ies_funded("reading", rows=10)
```

Lookup ERIC Thesaurus terms:
```bash
# Get term info (category, related terms)
python scripts/search/eric/check_eric_thesaurus.py -t "Medical School Faculty"

# Generate search query with related terms
python scripts/search/eric/check_eric_thesaurus.py -t "Faculty Development" --build-query

# Check if term exists
python scripts/search/eric/check_eric_thesaurus.py -t "Some Term" --check-only
```

### Database Conversion

Convert PubMed formula to all supported database formats:
```bash
python scripts/conversion/generate_all_database_search.py --input projects/PROJECT_NAME/search_formula.md --output-dir projects/PROJECT_NAME/
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
python scripts/search_results_to_review/search_results_processor.py --input-dir projects/PROJECT_NAME/ --output-dir projects/PROJECT_NAME/processed/
```

### Validation and Analysis

Analyze which search components match specific papers:
```bash
python scripts/validation/seed_analyzer/check_specific_papers.py --formula-file projects/PROJECT_NAME/search_formula.md --pmid-file projects/PROJECT_NAME/seed_pmids.txt
```

Compare original vs modified search formulas:
```bash
python scripts/validation/result_validator/check_modified_search.py --original original.md --modified modified.md --pmids seed_pmids.txt
```

### Block Overlap Analysis

Analyze overlap and effectiveness of search terms within a single block (e.g., checking if OR-connected terms actually add new results):

```bash
# From a text file containing the search block
python scripts/search/term_validator/check_block_overlap.py \
  -i block_input.txt \
  -o tests/block_overlap_YYYYMMDD/block_analysis.md \
  --block-name "Block Description"

# From standard input (paste block and press Ctrl+Z on Windows / Ctrl+D on Unix)
python scripts/search/term_validator/check_block_overlap.py \
  -o tests/block_overlap_YYYYMMDD/block_analysis.md \
  --block-name "Block Description"
```

**Input format** (text file or stdin):
```
#### #2A Block Name
```
"Term1"[Mesh] OR
"Term2"[Mesh] OR
term3[tiab] OR
term4[tiab]
```
```

**Output**: Markdown report showing:
- Individual hit count for each term
- Cumulative hit count as terms are OR-ed together
- Number of papers added by each term
- Percentage contribution to total
- Identification of low-value terms (< 1% contribution)
- Identification of high-overlap terms (> 80% already covered)

**Organization**:
- Results should be saved in dated folders: `tests/block_overlap_YYYYMMDD/`
- Input `.txt` files are gitignored (pattern: `tests/block_overlap_*/*.txt`)
- Output `.md` reports are tracked in git

**Use cases**:
- Identify redundant search terms that don't add new results
- Optimize search strategies by removing low-value terms
- Validate that each term in an OR chain contributes meaningfully
- Detect overly broad terms that dominate results (e.g., `absorption[tiab]` capturing 96.9% of results)

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

### Proximity Operator

PubMed supports proximity searching to find terms within a specified number of words of each other:

**Syntax:**
```
"search terms"[field:~N]
```

**Parameters:**
- `search terms` = Two or more words enclosed in double quotes
- `field` = The search field tag (typically `[Title]` or `[Title/Abstract]`)
- `N` = The maximum number of words that may appear between your search terms

**Examples:**
```
"hip pain"[Title/Abstract:~2]
```
Finds citations where "hip" and "pain" appear with no more than 2 words between them in the Title/Abstract field.

```
"faculty development"[tiab:~3]
```
Finds citations where "faculty" and "development" appear within 3 words of each other in Title/Abstract.

**Common use cases:**
- Capturing phrase variations: `"professional development"[tiab:~2]` captures "professional development", "professional faculty development", etc.
- Flexible term matching: `"program evaluation"[tiab:~3]` captures "program evaluation", "program design and evaluation", etc.

**Important notes:**
- Proximity operators work only with `[Title]`, `[Title/Abstract]`, `[Abstract]`, and `[Text Word]` fields
- They do NOT work with `[Mesh]` terms
- The order of terms matters in some cases
- Maximum useful proximity distance is typically 5-10 words

### File Naming

- Project directories: `projects/project_name/`
- Research protocol: `protocol.md`
- Seed papers folder: `seed_papers/` (RIS, NBIB, RTF, etc.)
- Seed PMIDs: `seed_pmids.txt` (one PMID per line, `#` for comments)
- Search formula: `search_formula.md`
- MeSH analysis output: `mesh_analysis.md`, `mesh_analysis_results.json`
- Search results: `log/search_results_YYYYMMDD_HHMMSS.ris`
- Validation reports: `log/validation_YYYYMMDD_HHMMSS.md`
- Block overlap session logs use `block_overlap_*_YYYYMMDD.md` and stay untracked via `.gitignore`; keep narrative reports like `physician_concept_optimized.md` committed.

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

### Report File Documentation Standards

**IMPORTANT**: All analysis reports (`.md` files) generated by scripts MUST include metadata comments for reproducibility and traceability.

**Required metadata at the top of each report**:
```markdown
<!--
Generated by: scripts/path/to/script.py
Command: python scripts/path/to/script.py --arg1 value1 --arg2 value2
Input data: path/to/input/data.txt (or description of data source)
Output directory: path/to/output/
Generated on: YYYY-MM-DD HH:MM:SS
-->
```

**Example**:
```markdown
<!--
Generated by: scripts/search/term_validator/check_block_overlap.py
Command: python scripts/search/term_validator/check_block_overlap.py -i temp_block_2a.txt -o tests/block_overlap_20251105/block_2a_filtered_analysis.md --block-name "#2A MeSH (with 10y + Animal filters)"
Input data: temp_block_2a.txt (MeSH terms block with physician AND filters)
Output directory: tests/block_overlap_20251105/
Generated on: 2025-11-05 14:19:13
-->

# Search Block Overlap Analysis
...
```

**Rationale**:
- Enables quick understanding of how a report was generated without searching through code
- Facilitates reproduction of analysis
- Documents data provenance for systematic review methodology
- Helps collaborators understand analysis workflow

**When creating new scripts that generate reports**:
1. Add a metadata comment block at the beginning of the output file
2. Include the script path, command used, input files, and timestamp
3. For validation reports (e.g., seed paper validation), also include:
   - Query used
   - Filter criteria
   - Validation criteria (e.g., "100% seed paper capture required")

## Project-Specific Context

This repository is designed for medical/health sciences researchers conducting systematic reviews and meta-analyses. The typical user:
- Has a research question with PICO elements documented in `protocol.md`
- Has identified 5-10 "seed papers" (key papers that should be captured)
- **Uses external AI assistants (ChatGPT, Claude, Copilot) for interactive search formula development**
- Uses this repository's scripts for **validation and conversion** only
- Needs to search multiple databases (PubMed, CENTRAL, Embase, trial registries)
- Must document the search strategy for publication/peer review
- Requires reproducible, validated search formulas

### Repository Role

This system is **NOT** an end-to-end AI search assistant. Instead, it provides:
- ✅ Validation tools (seed paper capture, MeSH checking)
- ✅ Database format converters (PubMed ↔ CENTRAL ↔ Embase, etc.)
- ✅ Analysis utilities (term overlap, block optimization)
- ❌ NOT: Interactive search formula generation (use external AI)
- ❌ NOT: PICO extraction from protocol text (use external AI)

When developing features, prioritize:
1. **Tool reliability** - Scripts should be deterministic and testable
2. **Interoperability** - Easy input/output with external AI tools
3. Search sensitivity (capturing all relevant papers) over specificity
4. Clear documentation of conversion rules and limitations
5. Validation against seed papers
6. PRISMA-compliant reporting
