# Ovid MEDLINE to PubMed Conversion

## Overview

This tool converts Ovid MEDLINE search formulas to PubMed format and verifies the converted search against a list of target PMIDs using the PubMed API.

## Conversion Rules

### MeSH Terms
- **Ovid**: `exp Term/`
- **PubMed**: `"Term"[MeSH Terms]`

### Field Tags
- **Ovid**: `.tw,kw.` (text words and keywords)
- **PubMed**: `[tiab]` (title and abstract)

### Proximity Operators
- **Ovid**: `adjN` (adjacent within N words)
- **PubMed**: `AND` (approximation, as PubMed lacks exact proximity operators)

### Boolean Operators
- Converted to uppercase: `and` → `AND`, `or` → `OR`

### Special Cases
- Malformed URLs in Ovid formulas are automatically corrected
- Complex nested boolean logic is preserved
- Wildcards (`*`) are maintained where possible

## Usage

### Basic Usage
```bash
cd /home/ubuntu/repos/search-formula-developper/scripts/conversion
python ovid_to_pubmed_converter.py
```

### Command Line Options
```bash
python ovid_to_pubmed_converter.py \
  --ovid-formula "your ovid formula here" \
  --pmids "pmid1,pmid2,pmid3" \
  --output results.json
```

## Output

The tool generates:
1. **Converted PubMed formula**: Direct conversion from Ovid syntax
2. **Simplified PubMed query**: Optimized version focusing on core concepts
3. **Verification results**: JSON file with coverage statistics and found/missing PMIDs

## Limitations

1. **Proximity Operators**: PubMed doesn't have exact equivalents to Ovid's `adjN` operators. The tool uses `AND` as an approximation.

2. **Field Mapping**: Some Ovid field tags don't have perfect PubMed equivalents. The tool uses the closest available mapping.

3. **Complex Syntax**: Very complex nested boolean logic may require manual review after conversion.

## API Requirements

- **PubMed E-utilities**: No API key required for basic usage (3 requests/second)
- **Optional**: Set `NCBI_API_KEY` environment variable for higher rate limits (10 requests/second)

## Example

### Input (Ovid MEDLINE)
```
(exp Helicobacter/ or exp Helicobacter Infections/ or (helicobacter or campylobacter).tw,kw. or (pylori or pyloridis or HP).tw,kw.) and (exp Anti-Inflammatory Agents, Non-Steroidal/ or nsaid*.tw,kw.)
```

### Output (PubMed)
```
("Helicobacter"[MeSH Terms] OR "Helicobacter Infections"[MeSH Terms] OR (helicobacter OR campylobacter)[tiab] OR (pylori OR pyloridis OR HP)[tiab]) AND ("Anti-Inflammatory Agents, Non-Steroidal"[MeSH Terms] OR nsaid*[tiab])
```

## Integration

This tool complements the existing PubMed → CENTRAL and PubMed → Dialog converters in the SRWS system, providing reverse conversion capability for Ovid MEDLINE formulas.
