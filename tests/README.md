# Tests Directory

This directory contains test files and analysis results for the search formula development system.

## Directory Structure

### Test Files
- `test_ovid_to_pubmed.py` - Unit tests for Ovid to PubMed conversion
- `conftest.py` - Pytest configuration

### Analysis Results (Current)
- `yarigai_comprehensive_line_counts_20251110.md` - Comprehensive analysis of all search blocks with detailed hit counts
- `final_concept_block_count_20251110.md` - Summary of final concept block counts
- `three_year_counts_2023plus.md` - Three-year period analysis (2023+)

### Analysis Subdirectories
- `block_overlap_20251105/` - Block overlap analysis results (identifying redundant search terms)
- `yarigai_line_counts/` - Initial line count analysis
- `yarigai_line_counts_refined_20251109/` - Refined line count analysis with automated scripts
- `api_instability_investigation_20251110/` - Investigation of PubMed API instability issues

### Archive
- `analysis_archive_20251110/` - Archive of analysis scripts and intermediate data files
  - Contains ad-hoc scripts used for data collection and processing
  - Includes intermediate JSON and markdown files
  - Preserved for reproducibility but not actively used

## File Naming Conventions

- Analysis reports: `*_YYYYMMDD.md` (dated markdown reports)
- Analysis scripts (archived): `get_*.py`, `add_*.py`, `update_*.py`
- Test files: `test_*.py`

## Usage

Run all tests:
```bash
pytest -q
```

Run specific test file:
```bash
pytest tests/test_ovid_to_pubmed.py -q
```

## Notes

- Analysis scripts in `analysis_archive_20251110/` are preserved for reproducibility but have been archived
- Final analysis reports remain in the main tests directory for easy access
- Subdirectories contain specialized analysis results organized by date and topic
