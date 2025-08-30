# rule
As an information specialist, you are tasked with translating search formulas from PubMed into dialog style. Here are the translation rules:

## Basic Conversion Rules
- Convert [Title/Abstract] to TI() and AB(). For example, transplant*[Title/Abstract] becomes TI(transplant*) OR AB(transplant*).
- Replace [MeSH Terms] with EMB.EXACT.EXPLODE(). For example, "Stem Cell Transplantation"[MeSH Terms] becomes EMB.EXACT.EXPLODE("allogeneic stem cell transplantation").
- Similarly, convert [tiab] to TI() and AB(). For example, transplant*[tiab] becomes TI(transplant*) OR AB(transplant*).
- Replace [mh] with EMB.EXACT.EXPLODE(). For example, "Stem Cell Transplantation"[mh] becomes EMB.EXACT.EXPLODE("allogeneic stem cell transplantation").

## PubMed Standard Format Support (NEW)
- `exp Term/` → `EMB.EXACT.EXPLODE("term")` (MeSH terms in standard format)
- `.tw.` → `(TI() OR AB())` (text words in title/abstract)
- `.ti,ab.` → `(TI() OR AB())` (title and abstract fields)
- `adj3` → `NEAR/3` (proximity operators)

## Input Format Support
- Standard PubMed format: `1. exp Term/` (automatically normalized)
- Internal format: `#1 exp Term/` (existing format)
- Line numbering: Replace numbered lines with S1, S2, etc.

## Other Rules
- For date limit, use the following format: 2018/12/1:2024/9/30[DP] should be translated as PD(20181201-20240930)
- Please show the translated search formula in the code block.

## Important Notes
⚠️ **Dialog format vs. Regular Embase format**
- **Dialog format**: Command-line style using `EMB.EXACT.EXPLODE("term")`
- **Regular Embase format**: Web interface style using `'term'/exp`

# translated search formula

## Example: Standard PubMed Format Conversion

### Input (PubMed Standard Format)
```
1. exp Lung Diseases, Interstitial/
2. (Interstitial adj3 (lung$ or pulmonary)).tw.
3. ILD.ti,ab.
4. 1 or 2 or 3
```

### Output (Dialog Format)
```
S1 EMB.EXACT.EXPLODE("lung diseases, interstitial")
S2 (TI(Interstitial NEAR/3 (lung$ or pulmonary)) OR AB(Interstitial NEAR/3 (lung$ or pulmonary)))
S3 (TI(ILD) OR AB(ILD))
S4 S1 OR S2 OR S3
```

# Breast Cancer
S1 EMB.EXACT.EXPLODE("breast cancer")
S2 EMB.EXACT.EXPLODE("breast carcinoma")
S3 EMB.EXACT.EXPLODE("breast tumor")
S4 (TI(breast NEAR/3 (cancer* OR tumo?r* OR neoplas* OR carcinom* OR adenocarcinom* OR malignan* OR metasta*)) OR AB(breast NEAR/3 (cancer* OR tumo?r* OR neoplas* OR carcinom* OR adenocarcinom* OR malignan* OR metasta*)))
S5 S1 OR S2 OR S3 OR S4

# Radiotherapy
S6 EMB.EXACT.EXPLODE("radiotherapy")
S7 EMB.EXACT.EXPLODE("radiation therapy")
S8 EMB.EXACT.EXPLODE("radiation dose")
S9 EMB.EXACT.EXPLODE("irradiation")
S10 (TI(radiotherap* OR radiat* OR irradiat*) OR AB(radiotherap* OR radiat* OR irradiat*))
S11 S6 OR S7 OR S8 OR S9 OR S10

# Combine Population and Intervention
S12 S5 AND S11

# Precise Filter for Economic Evaluation
S13 EMB.EXACT.EXPLODE("cost utility analysis")
S14 (TI(cost* AND ((qualit* NEAR/2 adjust* NEAR/2 life*) OR qaly*)) OR AB(cost* AND ((qualit* NEAR/2 adjust* NEAR/2 life*) OR qaly*)))
S15 (TI((incremental* NEAR/2 cost*) OR ICER) OR AB((incremental* NEAR/2 cost*) OR ICER))
S16 (TI(cost NEAR/2 utilit*) OR AB(cost NEAR/2 utilit*))
S17 (TI(cost* AND ((net NEAR/1 benefit*) OR (net NEAR/1 monetary NEAR/1 benefit*) OR (net NEAR/1 health NEAR/1 benefit*))) OR AB(cost* AND ((net NEAR/1 benefit*) OR (net NEAR/1 monetary NEAR/1 benefit*) OR (net NEAR/1 health NEAR/1 benefit*))))
S18 (TI((cost NEAR/2 effect*) AND (quality NEAR/1 of NEAR/1 life)) OR AB((cost NEAR/2 effect*) AND (quality NEAR/1 of NEAR/1 life)))
S19 TI(cost AND (effect* OR utilit*))
S20 S13 OR S14 OR S15 OR S16 OR S17 OR S18 OR S19

# Final Combined Search
S21 S12 AND S20

## copy and past for command line in Dialog
```
EMB.EXACT.EXPLODE("breast cancer")
EMB.EXACT.EXPLODE("breast carcinoma")
EMB.EXACT.EXPLODE("breast tumor")
(TI(breast NEAR/3 (cancer* OR tumo?r* OR neoplas* OR carcinom* OR adenocarcinom* OR malignan* OR metasta*)) OR AB(breast NEAR/3 (cancer* OR tumo?r* OR neoplas* OR carcinom* OR adenocarcinom* OR malignan* OR metasta*)))
S1 OR S2 OR S3 OR S4
EMB.EXACT.EXPLODE("radiotherapy")
EMB.EXACT.EXPLODE("radiation therapy")
EMB.EXACT.EXPLODE("radiation dose")
EMB.EXACT.EXPLODE("irradiation")
(TI(radiotherap* OR radiat* OR irradiat*) OR AB(radiotherap* OR radiat* OR irradiat*))
S6 OR S7 OR S8 OR S9 OR S10
EMB.EXACT.EXPLODE("cost utility analysis")
(TI(cost* AND ((qualit* NEAR/2 adjust* NEAR/2 life*) OR qaly*)) OR AB(cost* AND ((qualit* NEAR/2 adjust* NEAR/2 life*) OR qaly*)))
(TI((incremental* NEAR/2 cost*) OR ICER) OR AB((incremental* NEAR/2 cost*) OR ICER))
(TI(cost NEAR/2 utilit*) OR AB(cost NEAR/2 utilit*))
(TI(cost* AND ((net NEAR/1 benefit*) OR (net NEAR/1 monetary NEAR/1 benefit*) OR (net NEAR/1 health NEAR/1 benefit*))) OR AB(cost* AND ((net NEAR/1 benefit*) OR (net NEAR/1 monetary NEAR/1 benefit*) OR (net NEAR/1 health NEAR/1 benefit*))))
(TI((cost NEAR/2 effect*) AND (quality NEAR/1 of NEAR/1 life)) OR AB((cost NEAR/2 effect*) AND (quality NEAR/1 of NEAR/1 life)))
TI(cost AND (effect* OR utilit*))
S12 OR S13 OR S14 OR S15 OR S16 OR S17 OR S18
S5 AND S11 AND S19



```

# RCT filter for Embase (Dialog)
```
( EMB.EXACT.EXPLODE("randomized controlled trial") OR EMB.EXACT.EXPLODE("controlled clinical trial") OR TI(random*) OR AB(random*) OR EMB.EXACT.EXACT("randomization") OR EMB.EXACT.EXACT("intermethod comparison") OR TI(placebo) OR AB(placebo) OR TI(compare OR compared OR comparison) OR AB(compare OR compared OR comparison) OR ( AB(evaluated OR evaluate OR evaluating OR assessed OR assess) AND AB(compare OR compared OR comparing OR comparison) ) OR TI(open NEAR/1 label) OR AB(open NEAR/1 label) OR ( ( TI(double OR single OR doubly OR singly) NEAR/1 TI(blind OR blinded OR blindly) ) OR ( AB(double OR single OR doubly OR singly) NEAR/1 AB(blind OR blinded OR blindly) ) ) OR EMB.EXACT.EXACT("double blind procedure") OR TI(parallel NEAR/1 group*) OR AB(parallel NEAR/1 group*) OR TI(crossover OR "cross over") OR AB(crossover OR "cross over") OR ( ( TI(assign* OR match OR matched OR allocation) NEAR/6 TI(alternate OR group OR groups OR intervention OR interventions OR patient OR patients OR subject OR subjects OR participant OR participants) ) OR ( AB(assign* OR match OR matched OR allocation) NEAR/6 AB(alternate OR group OR groups OR intervention OR interventions OR patient OR patients OR subject OR subjects OR participant OR participants) ) ) OR TI(assigned OR allocated) OR AB(assigned OR allocated) OR ( ( TI(controlled) NEAR/8 TI(study OR design OR trial) ) OR ( AB(controlled) NEAR/8 AB(study OR design OR trial) ) ) OR TI(volunteer OR volunteers) OR AB(volunteer OR volunteers) OR EMB.EXACT.EXACT("human experiment") OR TI(trial) ) NOT ( ( ( TI(random* NEAR/1 sampl*) OR AB(random* NEAR/1 sampl*) ) AND ( TI("cross section*" OR questionnaire* OR survey OR surveys OR database OR databases) OR AB("cross section*" OR questionnaire* OR survey OR surveys OR database OR databases) ) ) OR ( EMB.EXACT.EXACT("cross-sectional study") AND NOT ( EMB.EXACT.EXPLODE("randomized controlled trial") OR EMB.EXACT.EXACT("controlled clinical study") OR EMB.EXACT.EXACT("controlled study") OR TI("randomised controlled") OR AB("randomised controlled") OR TI("randomized controlled") OR AB("randomized controlled") OR TI("control group") OR AB("control group") OR TI("control groups") OR AB("control groups") ) ) OR ( ( TI("case control*") OR AB("case control*") ) AND ( TI(random*) OR AB(random*) ) AND NOT ( TI("randomised controlled") OR AB("randomised controlled") OR TI("randomized controlled") OR AB("randomized controlled") ) ) OR ( ( TI(nonrandom*) OR AB(nonrandom*)) AND NOT ( TI(random*) OR AB(random*) ) ) OR TI("random field*") OR AB("random field*") OR TI("random cluster" NEAR/4 sampl*) OR AB("random cluster" NEAR/4 sampl*) OR ( AB(review) AND TI(review) AND NOT TI(trial) ) OR ( AB("we searched") AND ( TI(review) OR RTYPE(review) ) ) OR AB("update review") OR ( AB(databases NEAR/5 searched) ) OR ( TI("systematic review") NOT TI(trial OR study) ) OR ( ( ( TI(rat OR rats OR mouse OR mice OR swine OR porcine OR murine OR sheep OR lambs OR pigs OR piglets OR rabbit OR rabbits OR cat OR cats OR dog OR dogs OR cattle OR bovine OR monkey OR monkeys OR trout OR marmoset*) OR AB(rat OR rats OR mouse OR mice OR swine OR porcine OR murine OR sheep OR lambs OR pigs OR piglets OR rabbit OR rabbits OR cat OR cats OR dog OR dogs OR cattle OR bovine OR monkey OR monkeys OR trout OR marmoset*) ) AND EMB.EXACT.EXACT("animal experiment") ) OR ( EMB.EXACT.EXACT("animal experiment") NOT ( EMB.EXACT.EXACT("human experiment") OR EMB.EXACT.EXACT("human") ) ) ) )
```

ソース
https://training.cochrane.org/handbook/current/chapter-04#section-4-4-7

