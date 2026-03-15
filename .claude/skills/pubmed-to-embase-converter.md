# PubMed to Embase (Dialog) Converter

Convert PubMed search formulas to Embase (Dialog) syntax format.

## Trigger Keywords

- "PubMed式をEmbaseに変換"
- "DialogのEmbase検索式に変換"
- "convert to Embase Dialog"
- "Embase変換"
- "Dialogコピペ用"
- "Dialog一括コピペ"

## Task Description

You are a specialized converter for transforming PubMed/MEDLINE search formulas into Embase (Dialog platform) syntax. Follow the conversion rules strictly to ensure valid Dialog queries.

## Output Formats

### Standard Format (for documentation)
Numbered lines (S1, S2, etc.) with block structure, suitable for inclusion in protocol appendices.

### Copy-Paste Format (for execution)
**When user requests "コピペ用" or "一括コピペ"**, output search terms line-by-line WITHOUT line numbers, followed by OR/AND combination lines. This format allows:
- Pasting all lines at once into Dialog command line
- Dialog automatically assigns line numbers (S1, S2, etc.)
- Easy identification of invalid terms (Dialog shows errors immediately)
- Verification that each term exists in Emtree

**Copy-Paste Format Structure:**
```
[Term 1 without line number]
[Term 2 without line number]
[Term 3 without line number]
...
S1 OR S2 OR S3 OR ... (combine first block)
[Next block terms...]
S27 OR S28 OR ... (combine second block)
[Next block terms...]
S32 OR S33 OR ... (combine third block)
S26 AND S31 AND S36 (final query)
```

## Conversion Rules Reference

### 0. Prerequisites

- Target: Searching **Embase (Emtree)** on the **Dialog platform**
- Convert PubMed field tags `[ ]` and MeSH syntax to Dialog field codes + modifiers (EXACT/EXPLODE)

### 1. Free Text (Title/Abstract) Conversion

#### 1.1 Field Tags

| PubMed | Dialog |
|--------|--------|
| `term[tiab]` | `TI,AB(term)` |
| `term[ti]` | `TI(term)` |
| `term[ab]` | `AB(term)` |

**Note**: Dialog uses field code `( )` format. Use comma-separated field codes for multiple fields.

#### 1.2 Phrases

- PubMed: `"functional disorder"`
- Dialog: `"functional disorder"`

**Warning**: In Dialog, `" "` quotes disable automatic word variation expansion. Use quotes + truncation as needed.

#### 1.3 Truncation/Wildcards

| Type | Syntax | Example |
|------|--------|---------|
| Prefix (forward) | `TOXIC*` | Matches TOXIC, TOXICITY, etc. |
| Internal wildcard | `TOX*C` | Matches TOXIC, TOXICODENDRON |
| Partial match | `*TOXIC*` | Matches DETOXIC, TOXICITY |
| Suffix (backward) | `*OXIDE` | Matches DIOXIDE, OXIDE |
| Fixed character count | `TOXIC???` | Exactly 3 chars after TOXIC |
| Max chars after root | `TOXIC[*3]` | Up to 3 chars after TOXIC |

#### 1.4 Proximity Operators (for PubMed ADJ / proximity needs)

| Type | Dialog Syntax | Short Form | Example |
|------|---------------|------------|---------|
| Unordered proximity | `NEAR/n` | `n/n` | `functional NEAR/2 symptom*` |
| Ordered proximity | `PRE/n` | `p/n` | `functional PRE/2 gut` |
| Adjacent (0 words) | `NEAR/0` | `n/0` | `narrative NEAR/0 medicine` |

### 2. Thesaurus Conversion: MeSH → Emtree (Dialog)

#### 2.1 Standard Forms (OFFICIAL SYNTAX)

**Emtree with EXPLODE (includes subheadings):**
```
EMB.EXACT.EXPLODE("narrative medicine")
```

**Emtree without EXPLODE:**
```
EMB.EXACT("narrative medicine")
```

- `EMB` = Emtree thesaurus
- `EXACT` = Exact match (preferred term)
- `EXPLODE` = Include narrower terms

#### 2.2 Major Topic (equivalent to PubMed `[Majr]`)

**Major Emtree with EXPLODE:**
```
MJEMB.EXACT.EXPLODE("term")
```

**Major Emtree without EXPLODE:**
```
MJEMB.EXACT("term")
```

- `MJEMB` = Major topic in Emtree

#### 2.3 Multi-file Search (MeSH + Emtree)

**Search both MeSH and Emtree:**
```
MESH,EMB(eye)
```

**Note**: Comma-separated field codes = OR logic

#### 2.4 EXPLODE Shorthand with `#` (requires dot)

**Valid shorthand:**
```
EMB.#(term)
MJEMB.#(term)
```

**Invalid (will error):**
```
EMB#(term)  ❌ Missing dot
```

### 3. Qualifiers/Subheadings with LNK (Link)

#### 3.1 Rules

- Use `LNK` to link qualifiers to thesaurus terms
- Qualifiers are database-specific (don't mix MEDLINE and Embase qualifiers)

#### 3.2 Typical Form (use Embase qualifier codes)

```
EMB.EXACT("term" LNK (XX OR YY OR "long qualifier name"))
```

**Example:**
```
EMB.EXACT("diabetes mellitus" LNK (TH OR PC))
```
- `TH` = Therapy
- `PC` = Prevention

### 4. Date/Language/Abstract Filters (PubMed filters equivalent)

#### 4.1 Publication Date/Year

| PubMed | Dialog |
|--------|--------|
| Date range | `PD(20190517)` / `PD(201905)` / `PD(2019)` |
| Date comparison | `PD(>20190601)` |
| Year | `YR(2019)` / `YR(2018-2021)` |

#### 4.2 Language

| PubMed | Dialog |
|--------|--------|
| `english[la]` | `LA(english)` |

#### 4.3 Abstract Present

**Add to query:**
```
... AND ABANY(YES)
```

### 5. PubMed → Dialog Syntax Conversion Cheat Sheet

| PubMed Syntax | Dialog Syntax | Notes |
|---------------|---------------|-------|
| `AND` / `OR` / `NOT` | Same | Parentheses preserved |
| `[tiab]` | `TI,AB(...)` | Title OR Abstract |
| `[ti]` | `TI(...)` | Title only |
| `[ab]` | `AB(...)` | Abstract only |
| `"phrase"` | `"phrase"` | Quotes disable variation |
| `*` | `*` | Plus `*TOXIC*`, `TOXIC[*3]` |
| Ovid `ADJ2` (unordered) | `NEAR/2` or `n/2` | Proximity operator |
| Ovid `ADJ2` (ordered) | `PRE/2` or `p/2` | Ordered proximity |
| `[Mesh]` | `EMB.EXACT.EXPLODE("term")` | With EXPLODE |
| `[mesh:noexp]` | `EMB.EXACT("term")` | No EXPLODE |
| `[Majr]` | `MJEMB.EXACT.EXPLODE("term")` | Major topic |
| MeSH qualifier | `LNK (qualifier codes)` | DB-specific codes |
| `[dp]` date range | `PD(YYYY-YYYY)` or `YR(YYYY-YYYY)` | Date/Year |
| `[la]` | `LA(language)` | Language |

### 6. Common Errors ("We can't interpret your search")

**Avoid these when converting:**

1. ❌ Leaving Ovid/PubMed trailing notation (`.ti,ab.` or trailing periods)
2. ❌ Leaving `ADJ2` unconverted (use `NEAR/2` or `PRE/2`)
3. ❌ Smart quotes `" "` mixed in (use standard `" "`)
4. ❌ Unmatched parentheses or missing field code parentheses
5. ❌ EXPLODE shorthand without dot (`field#` → should be `field.#(...)`)

### 7. Recommended Conversion Template

**Structure:**

```
(
  TI,AB(synonym1 OR synonym2 OR synonym3) OR
  TI,AB(phrase1 NEAR/2 phrase2)
)
OR
(
  EMB.EXACT.EXPLODE("preferred term 1") OR
  EMB.EXACT.EXPLODE("preferred term 2") OR
  EMB.EXACT("exact term without children")
)
```

**Always:**
- Separate free text (TI,AB) and controlled vocabulary (EMB/MJEMB) sections
- Explicitly use `EXACT` / `EXACT.EXPLODE` for Emtree terms
- Combine sections with `AND` / `OR` as needed

## Task Workflow

When user provides a PubMed search formula to convert:

### Step 1: Read Input Formula

```bash
Read the PubMed search formula from the specified file or user input
```

### Step 2: Parse and Identify Components

Identify and categorize:
- Free text terms with field tags `[tiab]`, `[ti]`, `[ab]`
- MeSH terms `[Mesh]`, `[mesh:noexp]`, `[Majr]`
- Filters `[la]`, `[dp]`, etc.
- Boolean operators and parentheses structure

### Step 3: Apply Conversion Rules

For each component:

1. **Free text conversion:**
   - `[tiab]` → `TI,AB(...)`
   - `[ti]` → `TI(...)`
   - `[ab]` → `AB(...)`
   - Preserve phrases in `" "`
   - Keep truncation `*` as-is

2. **MeSH → Emtree conversion:**
   - Map MeSH terms to Emtree equivalents (note: may require manual verification)
   - `[Mesh]` → `EMB.EXACT.EXPLODE("term")`
   - `[mesh:noexp]` → `EMB.EXACT("term")`
   - `[Majr]` → `MJEMB.EXACT.EXPLODE("term")`

3. **Proximity operators:**
   - If Ovid `ADJ` present, convert to `NEAR/n` or `PRE/n`
   - PubMed proximity (if any) → `NEAR/n` or `PRE/n`

4. **Filters:**
   - `[la]` → `LA(...)`
   - `[dp]` → `PD(...)` or `YR(...)`
   - Add `ABANY(YES)` if abstract filter needed

5. **Preserve structure:**
   - Keep `AND`, `OR`, `NOT` as-is
   - Maintain parentheses grouping

### Step 4: Generate Output

#### Standard Format (for documentation)

Create converted Embase (Dialog) search formula in markdown format:

```markdown
# [Project Name] - Embase (Dialog) Search Formula

## Conversion Notes
- Converted from: [source PubMed formula file]
- Conversion date: [YYYY-MM-DD]
- **IMPORTANT**: MeSH to Emtree term mapping may require manual verification in Emtree browser

## Embase (Dialog) Search Strategy

### Block 1: [Block Name]
```
S1: [Converted Dialog syntax]
S2: [Converted Dialog syntax]
...
SN: S1 OR S2 OR ...
```

### Block 2: [Block Name]
```
[Converted Dialog syntax]
```

### Final Query
```
[Combined query with AND/OR logic]
```

## Warnings and Manual Review Required

[List any terms that need manual verification, ambiguous conversions, or potential issues]
```

#### Copy-Paste Format (when user requests "コピペ用" or "一括コピペ")

**IMPORTANT**: When user explicitly requests copy-paste format, output search terms WITHOUT line numbers (S1, S2, etc.), allowing Dialog to auto-assign them:

```
EMB.EXACT.EXPLODE("term1")
EMB.EXACT.EXPLODE("term2")
TI,AB(freetext terms...)
TI,AB(more terms...)
S1 OR S2 OR S3 OR S4
EMB.EXACT.EXPLODE("next block term1")
TI,AB(next block terms...)
S6 OR S7 OR S8
EMB.EXACT.EXPLODE("final block term1")
TI,AB(final block terms...)
S10 OR S11 OR S12
S5 AND S9 AND S13
```

**Benefits of copy-paste format:**
- User can paste entire block into Dialog at once
- Dialog shows errors for invalid Emtree terms immediately
- Easy to identify which specific terms need correction
- No need to manually type line numbers

### Step 5: Generate Warnings

Highlight issues that require manual review:
- MeSH terms that may have different Emtree equivalents
- Complex proximity operators
- Field tags not directly convertible
- Smart quotes or syntax that might cause errors

## Example Conversion

### Input (PubMed):

```markdown
#1 Population
"Physicians"[Mesh] OR
physician*[tiab] OR
"general practitioner"[tiab]

#2 Intervention
"Burnout, Professional"[Mesh] OR
burnout[tiab] OR
"emotional exhaustion"[tiab]

#3 Final
#1 AND #2
Filters: 2020-2025[dp], english[la]
```

### Output (Standard Format):

```markdown
#1 Population
S1: EMB.EXACT.EXPLODE("physician")
S2: TI,AB(physician*)
S3: TI,AB("general practitioner")
S4: S1 OR S2 OR S3

#2 Intervention
S5: EMB.EXACT.EXPLODE("burnout")
S6: TI,AB(burnout)
S7: TI,AB("emotional exhaustion")
S8: S5 OR S6 OR S7

#3 Final
S9: S4 AND S8 AND YR(2020-2025) AND LA(english)
```

### Output (Copy-Paste Format when requested):

```
EMB.EXACT.EXPLODE("physician")
TI,AB(physician*)
TI,AB("general practitioner")
S1 OR S2 OR S3
EMB.EXACT.EXPLODE("burnout")
TI,AB(burnout)
TI,AB("emotional exhaustion")
S5 OR S6 OR S7
S4 AND S8 AND YR(2020-2025) AND LA(english)
```

## Important Reminders

1. **MeSH ≠ Emtree**: MeSH and Emtree are different thesauri. Always verify term mappings in the Emtree browser.

2. **EXACT.EXPLODE is mandatory syntax**: Don't omit `EXACT` or `EXPLODE` - Dialog requires explicit modifiers.

3. **Test queries**: Always test converted queries in Dialog to catch syntax errors.

4. **Field codes need parentheses**: `TI,AB(term)` not `TI,AB term`

5. **Smart quotes break queries**: Use straight quotes `" "` only.

6. **Proximity syntax matters**: `NEAR/2` (unordered) vs `PRE/2` (ordered) - choose appropriately.

7. **Don't mix database qualifiers**: Use Embase qualifier codes with EMB, not MEDLINE codes.

8. **Copy-paste format advantage**: Outputting terms without line numbers allows Dialog to validate each term immediately upon pasting.

## Files to Read/Write

- **Input**: `projects/[PROJECT_NAME]/search_formula.md` (PubMed format)
- **Output Standard**: `projects/[PROJECT_NAME]/embase_dialog_search_formula.md`
- **Output Copy-Paste**: Display in chat when user requests "コピペ用"

## Validation Checklist

After conversion, verify:

- [ ] All field tags converted (no remaining `[tiab]`, `[Mesh]`, etc.)
- [ ] All EMB/MJEMB terms use `.EXACT` or `.EXACT.EXPLODE`
- [ ] Parentheses balanced for field codes `TI,AB(...)`
- [ ] No smart quotes `" "` (use `" "`)
- [ ] No Ovid `ADJ` operators (converted to `NEAR/PRE`)
- [ ] Date filters use `YR()` or `PD()`
- [ ] Language filters use `LA()`
- [ ] MeSH→Emtree mapping noted for manual review
- [ ] If copy-paste format: No line numbers before search terms (only in OR/AND lines)

## Success Criteria

The conversion is successful when:
1. All PubMed syntax is converted to valid Dialog syntax
2. Boolean logic and parentheses structure is preserved
3. Warnings generated for terms needing manual verification
4. Output query is syntactically valid for Dialog platform
5. Conversion notes document all changes and assumptions
6. If copy-paste format requested: Terms output without line numbers for easy validation

## References

- Dialog Operator Guide: https://dialog.g-search.jp/download/guide/dialog_operator.pdf
- Dialog Pharma Literature Guide: https://dialog.g-search.jp/download/guide/dialog_guide_pharma.pdf