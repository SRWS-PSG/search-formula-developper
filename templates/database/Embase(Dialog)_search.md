# rule
As an information specialist, you are tasked with translating search formulas from PubMed into dialog style. Here are the translation rules:
Convert [Title/Abstract] to TI() and AB(). For example, transplant*[Title/Abstract] becomes TI(transplant*) OR AB(transplant*).
Replace [MeSH Terms] with EMB.EXACT.EXPLODE(). For example, "Stem Cell Transplantation"[MeSH Terms] becomes EMB.EXACT.EXPLODE("allogeneic stem cell transplantation").
Similarly, convert [tiab] to TI() and AB(). For example, transplant*[tiab] becomes TI(transplant*) OR AB(transplant*).
Replace [mh] with EMB.EXACT.EXPLODE(). 
For example, "Stem Cell Transplantation"[mh] becomes EMB.EXACT.EXPLODE("allogeneic stem cell transplantation").
Replace the numbered lines with the logical designation number. For example, replace #1 with S1.
Please show the translated search formula in the code block.
For date limit, use the followin format: 2018/12/1:2024/9/30[DP] should be translated as PD(20181201-20240930)

# translated search formula

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
