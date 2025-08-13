# シードスタディのMeSH用語分析
生成日時: 2025-08-13 22:10:29

## 分析サマリー

- 分析論文数: 10件
- 抽出されたユニークMeSH用語数: 59個

## 主要なMeSH用語（出現頻度順 - 上位20件）

| MeSH UI | MeSH 用語 | 出現数 | 主要トピック論文数 |
|---------|----------|-------|------------------|
| D006801 | Humans | 10 | 0 |
| D004417 | Dyspnea | 7 | 2 |
| D017563 | Lung Diseases, Interstitial | 6 | 4 |
| D000368 | Aged | 5 | 0 |
| D008875 | Middle Aged | 5 | 0 |
| D054990 | Idiopathic Pulmonary Fibrosis | 4 | 2 |
| D011788 | Quality of Life | 4 | 1 |
| D000328 | Adult | 4 | 0 |
| D005260 | Female | 4 | 0 |
| D017079 | Exercise Tolerance | 3 | 1 |
| D003937 | Diagnosis, Differential | 3 | 0 |
| D008297 | Male | 3 | 0 |
| D029424 | Pulmonary Disease, Chronic Obstructive | 2 | 2 |
| D003371 | Cough | 2 | 1 |
| D012720 | Severity of Illness Index | 2 | 1 |
| D011379 | Prognosis | 2 | 0 |
| D015444 | Exercise | 2 | 0 |
| D015995 | Prevalence | 2 | 0 |
| D000369 | Aged, 80 and over | 2 | 0 |
| D000070857 | Walk Test | 2 | 0 |

## MeSH用語の階層構造 (上位用語ベース)

以下のMermaid図は、論文から抽出された主要なMeSH用語とその階層構造をカテゴリ別に示しています。
未知の親階層の用語名も可能な限り補完しています。

## カテゴリ B: 生物 (Organisms)
```mermaid
flowchart TD
    node_B01["Eukaryota [B01]"]
    node_B01_050["Animals [050]"]
    node_B01_050_150["Chordata [150]"]
    node_B01_050_150_900["Vertebrates [900]"]
    node_B01_050_150_900_649["Mammals [649]"]
    node_B01_050_150_900_649_313["Eutheria [313]"]
    node_B01_050_150_900_649_313_988["Primates [988]"]
    node_B01_050_150_900_649_313_988_400["Haplorhini [400]"]
    node_B01_050_150_900_649_313_988_400_112["Catarrhini [112]"]
    node_B01_050_150_900_649_313_988_400_112_400["Hominidae [400]"]
    node_B01_050_150_900_649_313_988_400_112_400_400["Humans [400]"]
    node_B01 --> node_B01_050
    node_B01_050 --> node_B01_050_150
    node_B01_050_150 --> node_B01_050_150_900
    node_B01_050_150_900 --> node_B01_050_150_900_649
    node_B01_050_150_900_649 --> node_B01_050_150_900_649_313
    node_B01_050_150_900_649_313 --> node_B01_050_150_900_649_313_988
    node_B01_050_150_900_649_313_988 --> node_B01_050_150_900_649_313_988_400
    node_B01_050_150_900_649_313_988_400 --> node_B01_050_150_900_649_313_988_400_112
    node_B01_050_150_900_649_313_988_400_112 --> node_B01_050_150_900_649_313_988_400_112_400
    node_B01_050_150_900_649_313_988_400_112_400 --> node_B01_050_150_900_649_313_988_400_112_400_400
    style node_B01_050_150_900_649_313_988_400_112_400_400 fill:#ff8c00,stroke:#333,stroke-width:2px
```

| MeSH UI | MeSH 用語 | 出現数 | ツリー番号 (カテゴリ内) |
|---------|----------|-------|-----------------------|
| D006801 | Humans | 10 | B01.050.150.900.649.313.988.400.112.400.400 |
| D056890 | Eukaryota | 0 | B01 |
| D000818 | Animals | 0 | B01.050 |
| D043344 | Chordata | 0 | B01.050.150 |
| D014714 | Vertebrates | 0 | B01.050.150.900 |
| D008322 | Mammals | 0 | B01.050.150.900.649 |
| D000073566 | Eutheria | 0 | B01.050.150.900.649.313 |
| D011323 | Primates | 0 | B01.050.150.900.649.313.988 |
| D000882 | Haplorhini | 0 | B01.050.150.900.649.313.988.400 |
| D051079 | Catarrhini | 0 | B01.050.150.900.649.313.988.400.112 |
| D015186 | Hominidae | 0 | B01.050.150.900.649.313.988.400.112.400 |

## カテゴリ C: 疾患 (Diseases)
```mermaid
flowchart TD
    node_C08["Respiratory Tract Diseases [C08]"]
    node_C08_381["Lung Diseases [381]"]
    node_C08_381_483["Lung Diseases, Interstitial [483]"]
    node_C08_381_483_652["Pulmonary Fibrosis [652]"]
    node_C08_381_483_652_500["Idiopathic Pulmonary Fibrosis [500]"]
    node_C08_381_495["Lung Diseases, Obstructive [495]"]
    node_C08_381_495_389["Pulmonary Disease, Chronic Obstructive [389]"]
    node_C08_618["Respiration Disorders [618]"]
    node_C08_618_248["Cough [248]"]
    node_C08_618_326["Dyspnea [326]"]
    node_C23["Pathological Conditions, Signs and Symptoms [C23]"]
    node_C23_550["Pathologic Processes [550]"]
    node_C23_550_291["Disease Attributes [291]"]
    node_C23_550_291_500["Chronic Disease [500]"]
    node_C23_550_291_500_875["Pulmonary Disease, Chronic Obstructive [875]"]
    node_C23_888["Signs and Symptoms [888]"]
    node_C23_888_852["Signs and Symptoms, Respiratory [852]"]
    node_C23_888_852_293["Cough [293]"]
    node_C23_888_852_371["Dyspnea [371]"]
    node_C08 --> node_C08_381
    node_C08_381 --> node_C08_381_483
    node_C08_381_483 --> node_C08_381_483_652
    node_C08_381_483_652 --> node_C08_381_483_652_500
    node_C08_381 --> node_C08_381_495
    node_C08_381_495 --> node_C08_381_495_389
    node_C08 --> node_C08_618
    node_C08_618 --> node_C08_618_248
    node_C08_618 --> node_C08_618_326
    node_C23 --> node_C23_550
    node_C23_550 --> node_C23_550_291
    node_C23_550_291 --> node_C23_550_291_500
    node_C23_550_291_500 --> node_C23_550_291_500_875
    node_C23 --> node_C23_888
    node_C23_888 --> node_C23_888_852
    node_C23_888_852 --> node_C23_888_852_293
    node_C23_888_852 --> node_C23_888_852_371
    style node_C08_618_326 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_C23_888_852_371 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_C08_381_483 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_C08_381_483_652_500 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_C08_381_495_389 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_C23_550_291_500_875 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_C08_618_248 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_C23_888_852_293 fill:#ff8c00,stroke:#333,stroke-width:2px
```

| MeSH UI | MeSH 用語 | 出現数 | ツリー番号 (カテゴリ内) |
|---------|----------|-------|-----------------------|
| D004417 | Dyspnea | 7 | C08.618.326, C23.888.852.371 |
| D017563 | Lung Diseases, Interstitial | 6 | C08.381.483 |
| D054990 | Idiopathic Pulmonary Fibrosis | 4 | C08.381.483.652.500 |
| D029424 | Pulmonary Disease, Chronic Obstructive | 2 | C08.381.495.389, C23.550.291.500.875 |
| D003371 | Cough | 2 | C08.618.248, C23.888.852.293 |
| D012140 | Respiratory Tract Diseases | 0 | C08 |
| D008171 | Lung Diseases | 0 | C08.381 |
| D011658 | Pulmonary Fibrosis | 0 | C08.381.483.652 |
| D008173 | Lung Diseases, Obstructive | 0 | C08.381.495 |
| D012120 | Respiration Disorders | 0 | C08.618 |
| D013568 | Pathological Conditions, Signs and Symptoms | 0 | C23 |
| D010335 | Pathologic Processes | 0 | C23.550 |
| D020969 | Disease Attributes | 0 | C23.550.291 |
| D002908 | Chronic Disease | 0 | C23.550.291.500 |
| D012816 | Signs and Symptoms | 0 | C23.888 |
| D012818 | Signs and Symptoms, Respiratory | 0 | C23.888.852 |

## カテゴリ E: 分析・診断・治療技術と装置 (Techniques and Equipment)
```mermaid
flowchart TD
    node_E01["Diagnosis [E01]"]
    node_E01_171["Diagnosis, Differential [171]"]
    node_E01_370["Diagnostic Techniques and Procedures [370]"]
    node_E01_370_370["Diagnostic Techniques, Cardiovascular [370]"]
    node_E01_370_370_380["Heart Function Tests [380]"]
    node_E01_370_370_380_250["Exercise Test [250]"]
    node_E01_370_370_380_250_500["Walk Test [500]"]
    node_E01_789["Prognosis [789]"]
    node_E05["Investigative Techniques [E05]"]
    node_E05_318["Epidemiologic Methods [318]"]
    node_E05_318_308["Data Collection [308]"]
    node_E05_318_308_980["Surveys and Questionnaires [980]"]
    node_E05_318_308_980_438["Health Surveys [438]"]
    node_E05_318_308_980_438_475["Health Status Indicators [475]"]
    node_E05_318_308_980_438_475_456["Patient Acuity [456]"]
    node_E05_318_308_980_438_475_456_500["Severity of Illness Index [500]"]
    node_E05_318_308_985["Vital Statistics [985]"]
    node_E05_318_308_985_525["Morbidity [525]"]
    node_E05_318_308_985_525_750["Prevalence [750]"]
    node_E01 --> node_E01_171
    node_E01 --> node_E01_370
    node_E01_370 --> node_E01_370_370
    node_E01_370_370 --> node_E01_370_370_380
    node_E01_370_370_380 --> node_E01_370_370_380_250
    node_E01_370_370_380_250 --> node_E01_370_370_380_250_500
    node_E01 --> node_E01_789
    node_E05 --> node_E05_318
    node_E05_318 --> node_E05_318_308
    node_E05_318_308 --> node_E05_318_308_980
    node_E05_318_308_980 --> node_E05_318_308_980_438
    node_E05_318_308_980_438 --> node_E05_318_308_980_438_475
    node_E05_318_308_980_438_475 --> node_E05_318_308_980_438_475_456
    node_E05_318_308_980_438_475_456 --> node_E05_318_308_980_438_475_456_500
    node_E05_318_308 --> node_E05_318_308_985
    node_E05_318_308_985 --> node_E05_318_308_985_525
    node_E05_318_308_985_525 --> node_E05_318_308_985_525_750
    style node_E01_171 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_E05_318_308_980_438_475_456_500 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_E01_789 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_E05_318_308_985_525_750 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_E01_370_370_380_250_500 fill:#ff8c00,stroke:#333,stroke-width:2px
```

| MeSH UI | MeSH 用語 | 出現数 | ツリー番号 (カテゴリ内) |
|---------|----------|-------|-----------------------|
| D003937 | Diagnosis, Differential | 3 | E01.171 |
| D012720 | Severity of Illness Index | 2 | E05.318.308.980.438.475.456.500 |
| D011379 | Prognosis | 2 | E01.789 |
| D015995 | Prevalence | 2 | E05.318.308.985.525.750 |
| D000070857 | Walk Test | 2 | E01.370.370.380.250.500 |
| D003933 | Diagnosis | 0 | E01 |
| D019937 | Diagnostic Techniques and Procedures | 0 | E01.370 |
| D003935 | Diagnostic Techniques, Cardiovascular | 0 | E01.370.370 |
| D006334 | Heart Function Tests | 0 | E01.370.370.380 |
| D005080 | Exercise Test | 0 | E01.370.370.380.250 |
| D008919 | Investigative Techniques | 0 | E05 |
| D004812 | Epidemiologic Methods | 0 | E05.318 |
| D003625 | Data Collection | 0 | E05.318.308 |
| D011795 | Surveys and Questionnaires | 0 | E05.318.308.980 |
| D006306 | Health Surveys | 0 | E05.318.308.980.438 |
| D006305 | Health Status Indicators | 0 | E05.318.308.980.438.475 |
| D062072 | Patient Acuity | 0 | E05.318.308.980.438.475.456 |
| D014798 | Vital Statistics | 0 | E05.318.308.985 |
| D009017 | Morbidity | 0 | E05.318.308.985.525 |

## カテゴリ G: 生物学・物理学 (Biological Sciences)
```mermaid
flowchart TD
    node_G11["Musculoskeletal and Neural Physiological Phenomena [G11]"]
    node_G11_427["Musculoskeletal Physiological Phenomena [427]"]
    node_G11_427_410["Movement [410]"]
    node_G11_427_410_698["Motor Activity [698]"]
    node_G11_427_410_698_277["Exercise [277]"]
    node_G11_427_680["Physical Endurance [680]"]
    node_G11_427_680_270["Exercise Tolerance [270]"]
    node_G11 --> node_G11_427
    node_G11_427 --> node_G11_427_410
    node_G11_427_410 --> node_G11_427_410_698
    node_G11_427_410_698 --> node_G11_427_410_698_277
    node_G11_427 --> node_G11_427_680
    node_G11_427_680 --> node_G11_427_680_270
    style node_G11_427_680_270 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_G11_427_410_698_277 fill:#ff8c00,stroke:#333,stroke-width:2px
```

| MeSH UI | MeSH 用語 | 出現数 | ツリー番号 (カテゴリ内) |
|---------|----------|-------|-----------------------|
| D017079 | Exercise Tolerance | 3 | G11.427.680.270 |
| D015444 | Exercise | 2 | G11.427.410.698.277 |
| D055687 | Musculoskeletal and Neural Physiological Phenomena | 0 | G11 |
| D009142 | Musculoskeletal Physiological Phenomena | 0 | G11.427 |
| D009068 | Movement | 0 | G11.427.410 |
| D009043 | Motor Activity | 0 | G11.427.410.698 |
| D010807 | Physical Endurance | 0 | G11.427.680 |

## カテゴリ I: 人類学・教育・社会・社会現象 (Social Phenomena)
```mermaid
flowchart TD
    node_I01["Social Sciences [I01]"]
    node_I01_800["Quality of Life [800]"]
    node_I03["Human Activities [I03]"]
    node_I03_350["Exercise [350]"]
    node_I01 --> node_I01_800
    node_I03 --> node_I03_350
    style node_I01_800 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_I03_350 fill:#ff8c00,stroke:#333,stroke-width:2px
```

| MeSH UI | MeSH 用語 | 出現数 | ツリー番号 (カテゴリ内) |
|---------|----------|-------|-----------------------|
| D011788 | Quality of Life | 4 | I01.800 |
| D015444 | Exercise | 2 | I03.350 |
| D012942 | Social Sciences | 0 | I01 |
| D006802 | Human Activities | 0 | I03 |

## カテゴリ K: 人文科学 (Humanities)
```mermaid
flowchart TD
    node_K01["Humanities [K01]"]
    node_K01_752["Philosophy [752]"]
    node_K01_752_400["Life [400]"]
    node_K01_752_400_750["Quality of Life [750]"]
    node_K01 --> node_K01_752
    node_K01_752 --> node_K01_752_400
    node_K01_752_400 --> node_K01_752_400_750
    style node_K01_752_400_750 fill:#ff8c00,stroke:#333,stroke-width:2px
```

| MeSH UI | MeSH 用語 | 出現数 | ツリー番号 (カテゴリ内) |
|---------|----------|-------|-----------------------|
| D011788 | Quality of Life | 4 | K01.752.400.750 |
| D006809 | Humanities | 0 | K01 |
| D010684 | Philosophy | 0 | K01.752 |
| D019369 | Life | 0 | K01.752.400 |

## カテゴリ M: 人物 (Named Groups)
```mermaid
flowchart TD
    node_M01["Persons [M01]"]
    node_M01_060["Age Groups [060]"]
    node_M01_060_116["Adult [116]"]
    node_M01_060_116_100["Aged [100]"]
    node_M01_060_116_100_080["Aged, 80 and over [080]"]
    node_M01_060_116_630["Middle Aged [630]"]
    node_M01 --> node_M01_060
    node_M01_060 --> node_M01_060_116
    node_M01_060_116 --> node_M01_060_116_100
    node_M01_060_116_100 --> node_M01_060_116_100_080
    node_M01_060_116 --> node_M01_060_116_630
    style node_M01_060_116_100 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_M01_060_116_630 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_M01_060_116 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_M01_060_116_100_080 fill:#ff8c00,stroke:#333,stroke-width:2px
```

| MeSH UI | MeSH 用語 | 出現数 | ツリー番号 (カテゴリ内) |
|---------|----------|-------|-----------------------|
| D000368 | Aged | 5 | M01.060.116.100 |
| D008875 | Middle Aged | 5 | M01.060.116.630 |
| D000328 | Adult | 4 | M01.060.116 |
| D000369 | Aged, 80 and over | 2 | M01.060.116.100.080 |
| D009272 | Persons | 0 | M01 |
| D009273 | Age Groups | 0 | M01.060 |

## カテゴリ N: 健康管理 (Health Care)
```mermaid
flowchart TD
    node_N01["Population Characteristics [N01]"]
    node_N01_224["Demography [224]"]
    node_N01_224_935["Vital Statistics [935]"]
    node_N01_224_935_597["Morbidity [597]"]
    node_N01_224_935_597_750["Prevalence [750]"]
    node_N05["Health Care Quality, Access, and Evaluation [N05]"]
    node_N05_715["Quality of Health Care [715]"]
    node_N05_715_360["Health Care Evaluation Mechanisms [360]"]
    node_N05_715_360_300["Data Collection [300]"]
    node_N05_715_360_300_800["Surveys and Questionnaires [800]"]
    node_N05_715_360_300_800_438["Health Surveys [438]"]
    node_N05_715_360_300_800_438_375["Health Status Indicators [375]"]
    node_N05_715_360_300_800_438_375_364["Patient Acuity [364]"]
    node_N05_715_360_300_800_438_375_364_500["Severity of Illness Index [500]"]
    node_N06["Environment and Public Health [N06]"]
    node_N06_850["Public Health [850]"]
    node_N06_850_505["Epidemiologic Measurements [505]"]
    node_N06_850_505_400["Demography [400]"]
    node_N06_850_505_400_425["Health Status [425]"]
    node_N06_850_505_400_425_837["Quality of Life [837]"]
    node_N06_850_505_400_975["Vital Statistics [975]"]
    node_N06_850_505_400_975_525["Morbidity [525]"]
    node_N06_850_505_400_975_525_750["Prevalence [750]"]
    node_N06_850_520["Epidemiologic Methods [520]"]
    node_N06_850_520_308["Data Collection [308]"]
    node_N06_850_520_308_980["Surveys and Questionnaires [980]"]
    node_N06_850_520_308_980_438["Health Surveys [438]"]
    node_N06_850_520_308_980_438_475["Health Status Indicators [475]"]
    node_N06_850_520_308_980_438_475_364["Patient Acuity [364]"]
    node_N06_850_520_308_980_438_475_364_500["Severity of Illness Index [500]"]
    node_N06_850_520_308_985["Vital Statistics [985]"]
    node_N06_850_520_308_985_525["Morbidity [525]"]
    node_N06_850_520_308_985_525_750["Prevalence [750]"]
    node_N01 --> node_N01_224
    node_N01_224 --> node_N01_224_935
    node_N01_224_935 --> node_N01_224_935_597
    node_N01_224_935_597 --> node_N01_224_935_597_750
    node_N05 --> node_N05_715
    node_N05_715 --> node_N05_715_360
    node_N05_715_360 --> node_N05_715_360_300
    node_N05_715_360_300 --> node_N05_715_360_300_800
    node_N05_715_360_300_800 --> node_N05_715_360_300_800_438
    node_N05_715_360_300_800_438 --> node_N05_715_360_300_800_438_375
    node_N05_715_360_300_800_438_375 --> node_N05_715_360_300_800_438_375_364
    node_N05_715_360_300_800_438_375_364 --> node_N05_715_360_300_800_438_375_364_500
    node_N06 --> node_N06_850
    node_N06_850 --> node_N06_850_505
    node_N06_850_505 --> node_N06_850_505_400
    node_N06_850_505_400 --> node_N06_850_505_400_425
    node_N06_850_505_400_425 --> node_N06_850_505_400_425_837
    node_N06_850_505_400 --> node_N06_850_505_400_975
    node_N06_850_505_400_975 --> node_N06_850_505_400_975_525
    node_N06_850_505_400_975_525 --> node_N06_850_505_400_975_525_750
    node_N06_850 --> node_N06_850_520
    node_N06_850_520 --> node_N06_850_520_308
    node_N06_850_520_308 --> node_N06_850_520_308_980
    node_N06_850_520_308_980 --> node_N06_850_520_308_980_438
    node_N06_850_520_308_980_438 --> node_N06_850_520_308_980_438_475
    node_N06_850_520_308_980_438_475 --> node_N06_850_520_308_980_438_475_364
    node_N06_850_520_308_980_438_475_364 --> node_N06_850_520_308_980_438_475_364_500
    node_N06_850_520_308 --> node_N06_850_520_308_985
    node_N06_850_520_308_985 --> node_N06_850_520_308_985_525
    node_N06_850_520_308_985_525 --> node_N06_850_520_308_985_525_750
    style node_N06_850_505_400_425_837 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_N05_715_360_300_800_438_375_364_500 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_N06_850_520_308_980_438_475_364_500 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_N01_224_935_597_750 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_N06_850_505_400_975_525_750 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_N06_850_520_308_985_525_750 fill:#ff8c00,stroke:#333,stroke-width:2px
```

| MeSH UI | MeSH 用語 | 出現数 | ツリー番号 (カテゴリ内) |
|---------|----------|-------|-----------------------|
| D011788 | Quality of Life | 4 | N06.850.505.400.425.837 |
| D012720 | Severity of Illness Index | 2 | N05.715.360.300.800.438.375.364.500, N06.850.520.308.980.438.475.364.500 |
| D015995 | Prevalence | 2 | N01.224.935.597.750, N06.850.505.400.975.525.750, N06.850.520.308.985.525.750 |
| D011154 | Population Characteristics | 0 | N01 |
| D003710 | Demography | 0 | N01.224 |
| D017530 | Health Care Quality, Access, and Evaluation | 0 | N05 |
| D011787 | Quality of Health Care | 0 | N05.715 |
| D017531 | Health Care Evaluation Mechanisms | 0 | N05.715.360 |
| D004778 | Environment and Public Health | 0 | N06 |
| D011634 | Public Health | 0 | N06.850 |
| D015991 | Epidemiologic Measurements | 0 | N06.850.505 |
| D006304 | Health Status | 0 | N06.850.505.400.425 |

## カテゴリ X: カテゴリ X
```mermaid
flowchart TD
    node_X999998["Male [X999998]"]
    node_X999999["Female [X999999]"]
    style node_X999999 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_X999998 fill:#ff8c00,stroke:#333,stroke-width:2px
```

| MeSH UI | MeSH 用語 | 出現数 | ツリー番号 (カテゴリ内) |
|---------|----------|-------|-----------------------|
| D005260 | Female | 4 | X999999 |
| D008297 | Male | 3 | X999998 |

### 凡例

- オレンジ色のノード: Seed論文に実際に付与されていたMeSH用語 (上位20件に含まれるもの)
- 通常のノード: 上記MeSH用語の階層を構成する親ノード (可能な場合、用語名を補完)

## 論文別MeSH用語

### PMID: 38648021

- タイトル: Interstitial Lung Disease: A Review.
- ジャーナル: JAMA (2024)
- 著者: Maher Toby M
- MeSH用語数: 13

| MeSH UI | MeSH 用語 | 主要トピック | 修飾語 |
|---------|----------|------------|-------|
| D006801 | Humans | No |  |
| D000088962 | Antifibrotic Agents | No | therapeutic use |
| D003240 | Connective Tissue Diseases | No | complications, diagnosis, therapy |
| D004417 | Dyspnea | No | etiology |
| D054990 | Idiopathic Pulmonary Fibrosis | No | complications, diagnosis, therapy |
| D007211 | Indoles | No | therapeutic use |
| D017563 | Lung Diseases, Interstitial | Yes | diagnosis, etiology, therapy |
| D016040 | Lung Transplantation | No |  |
| D011379 | Prognosis | No |  |
| D011728 | Pyridones | No | therapeutic use |
| D019141 | Respiratory System Agents | No | therapeutic use |
| D014481 | United States | No |  |
| D014797 | Vital Capacity | No |  |

---

### PMID: 35964592

- タイトル: Interstitial lung diseases.
- ジャーナル: Lancet (London, England) (2022)
- 著者: Wijsenbeek Marlies, Suzuki Atsushi, Maher Toby M
- MeSH用語数: 7

| MeSH UI | MeSH 用語 | 主要トピック | 修飾語 |
|---------|----------|------------|-------|
| D004417 | Dyspnea | No | etiology |
| D017079 | Exercise Tolerance | No |  |
| D006801 | Humans | No |  |
| D008168 | Lung | No |  |
| D017563 | Lung Diseases, Interstitial | Yes | diagnosis, epidemiology, etiology |
| D011658 | Pulmonary Fibrosis | Yes | complications, etiology |
| D011788 | Quality of Life | No |  |

---

### PMID: 34559419

- タイトル: Pulmonary rehabilitation for interstitial lung disease.
- ジャーナル: The Cochrane database of systematic reviews (2021)
- 著者: Dowman Leona, Hill Catherine J, May Anthony, Holland Anne E
- MeSH用語数: 9

| MeSH UI | MeSH 用語 | 主要トピック | 修飾語 |
|---------|----------|------------|-------|
| D000328 | Adult | No |  |
| D000368 | Aged | No |  |
| D004417 | Dyspnea | No | etiology, rehabilitation |
| D015444 | Exercise | No |  |
| D017079 | Exercise Tolerance | No |  |
| D006801 | Humans | No |  |
| D017563 | Lung Diseases, Interstitial | Yes |  |
| D008875 | Middle Aged | No |  |
| D011788 | Quality of Life | Yes |  |

---

### PMID: 36701677

- タイトル: Differential Diagnosis of Suspected Chronic Obstructive Pulmonary Disease Exacerbations in the Acute Care Setting: Best Practice.
- ジャーナル: American journal of respiratory and critical care medicine (2023)
- 著者: Celli Bartolome R, Fabbri Leonardo M, Aaron Shawn D, Agusti Alvar, Brook Robert D, Criner Gerard J, Franssen Frits M E, Humbert Marc, Hurst John R, Montes de Oca Maria, Pantoni Leonardo, Papi Alberto, Rodriguez-Roisin Roberto, Sethi Sanjay, Stolz Daiana, Torres Antoni, Vogelmeier Claus F, Wedzicha Jadwiga A
- MeSH用語数: 5

| MeSH UI | MeSH 用語 | 主要トピック | 修飾語 |
|---------|----------|------------|-------|
| D029424 | Pulmonary Disease, Chronic Obstructive | Yes | diagnosis |
| D006801 | Humans | No |  |
| D003937 | Diagnosis, Differential | No |  |
| D004417 | Dyspnea | Yes | etiology |
| D003371 | Cough | No |  |

---

### PMID: 38536110

- タイトル: Epidemiology and Prognostic Significance of Cough in Fibrotic Interstitial Lung Disease.
- ジャーナル: American journal of respiratory and critical care medicine (2024)
- 著者: Khor Yet H, Johannson Kerri A, Marcoux Veronica, Fisher Jolene H, Assayag Deborah, Manganas Helene, Khalil Nasreen, Kolb Martin, Ryerson Christopher J
- MeSH用語数: 16

| MeSH UI | MeSH 用語 | 主要トピック | 修飾語 |
|---------|----------|------------|-------|
| D006801 | Humans | No |  |
| D003371 | Cough | Yes | etiology, physiopathology, epidemiology |
| D008297 | Male | No |  |
| D005260 | Female | No |  |
| D000368 | Aged | No |  |
| D008875 | Middle Aged | No |  |
| D011379 | Prognosis | No |  |
| D017563 | Lung Diseases, Interstitial | Yes | physiopathology, epidemiology, mortality |
| D012720 | Severity of Illness Index | Yes |  |
| D002170 | Canada | No | epidemiology |
| D054990 | Idiopathic Pulmonary Fibrosis | Yes | epidemiology, physiopathology, complications, mortality |
| D011446 | Prospective Studies | No |  |
| D011788 | Quality of Life | No |  |
| D018450 | Disease Progression | No |  |
| D012042 | Registries | No |  |
| D015995 | Prevalence | No |  |

---

### PMID: 28213592

- タイトル: The evidence of benefits of exercise training in interstitial lung disease: a randomised controlled trial.
- ジャーナル: Thorax (2017)
- 著者: Dowman Leona M, McDonald Christine F, Hill Catherine J, Lee Annemarie L, Barker Kathryn, Boote Claire, Glaspole Ian, Goh Nicole S L, Southcott Anne M, Burge Angela T, Gillies Rebecca, Martin Alicia, Holland Anne E
- MeSH用語数: 18

| MeSH UI | MeSH 用語 | 主要トピック | 修飾語 |
|---------|----------|------------|-------|
| D000368 | Aged | No |  |
| D000369 | Aged, 80 and over | No |  |
| D001195 | Asbestosis | No | physiopathology, rehabilitation |
| D004417 | Dyspnea | No | etiology |
| D015444 | Exercise | No | physiology* |
| D005081 | Exercise Therapy | Yes |  |
| D005260 | Female | No |  |
| D006801 | Humans | No |  |
| D054990 | Idiopathic Pulmonary Fibrosis | No | physiopathology, rehabilitation |
| D017563 | Lung Diseases, Interstitial | No | etiology, physiopathology*, rehabilitation* |
| D008297 | Male | No |  |
| D008875 | Middle Aged | No |  |
| D064797 | Physical Conditioning, Human | No | physiology* |
| D011788 | Quality of Life | No |  |
| D016037 | Single-Blind Method | No |  |
| D011795 | Surveys and Questionnaires | No |  |
| D013997 | Time Factors | No |  |
| D000070857 | Walk Test | No |  |

---

### PMID: 36179385

- タイトル: Qualitative validation of the modified Medical Research Council (mMRC) dyspnoea scale as a patient-reported measure of breathlessness severity.
- ジャーナル: Respiratory medicine (2022)
- 著者: Sunjaya Anthony, Poulos Leanne, Reddel Helen, Jenkins Christine
- MeSH用語数: 11

| MeSH UI | MeSH 用語 | 主要トピック | 修飾語 |
|---------|----------|------------|-------|
| D006801 | Humans | No |  |
| D055815 | Young Adult | No |  |
| D000328 | Adult | No |  |
| D008875 | Middle Aged | No |  |
| D000368 | Aged | No |  |
| D000369 | Aged, 80 and over | No |  |
| D029424 | Pulmonary Disease, Chronic Obstructive | Yes | drug therapy |
| D012720 | Severity of Illness Index | No |  |
| D004417 | Dyspnea | No | diagnosis, psychology |
| D035843 | Biomedical Research | Yes |  |
| D000071066 | Patient Reported Outcome Measures | No |  |

---

### PMID: 39129185

- タイトル: Effects of home-based telerehabilitation-assisted inspiratory muscle training in patients with idiopathic pulmonary fibrosis: A randomized controlled trial.
- ジャーナル: Respirology (Carlton, Vic.) (2024)
- 著者: Aktan Rıdvan, Tertemiz Kemal Can, Yiğit Salih, Özalevli Sevgi, Ozgen Alpaydin Aylin, Uçan Eyüp Sabri
- MeSH用語数: 16

| MeSH UI | MeSH 用語 | 主要トピック | 修飾語 |
|---------|----------|------------|-------|
| D006801 | Humans | No |  |
| D008297 | Male | No |  |
| D005260 | Female | No |  |
| D054990 | Idiopathic Pulmonary Fibrosis | Yes | rehabilitation, physiopathology |
| D000368 | Aged | No |  |
| D001945 | Breathing Exercises | Yes | methods |
| D000069350 | Telerehabilitation | Yes |  |
| D012132 | Respiratory Muscles | Yes | physiopathology |
| D004417 | Dyspnea | Yes | rehabilitation, etiology, physiopathology |
| D017079 | Exercise Tolerance | Yes | physiology |
| D008875 | Middle Aged | No |  |
| D053580 | Muscle Strength | No | physiology |
| D016896 | Treatment Outcome | No |  |
| D012129 | Respiratory Function Tests | No |  |
| D006699 | Home Care Services | No |  |
| D000070857 | Walk Test | No |  |

---

### PMID: 28487307

- タイトル: Aripiprazole-induced hypersensitivity pneumonitis.
- ジャーナル: BMJ case reports (2017)
- 著者: Gunasekaran Kulothungan, Murthi Swetha, Jennings Jeffrey, Lone Nazir
- MeSH用語数: 10

| MeSH UI | MeSH 用語 | 主要トピック | 修飾語 |
|---------|----------|------------|-------|
| D000328 | Adult | No |  |
| D000542 | Alveolitis, Extrinsic Allergic | No | chemically induced, diagnosis*, diagnostic imaging |
| D014150 | Antipsychotic Agents | No | adverse effects* |
| D000068180 | Aripiprazole | No | adverse effects* |
| D003937 | Diagnosis, Differential | No |  |
| D005260 | Female | No |  |
| D006801 | Humans | No |  |
| D017563 | Lung Diseases, Interstitial | No | chemically induced, diagnosis*, diagnostic imaging |
| D012559 | Schizophrenia | No | drug therapy |
| D014057 | Tomography, X-Ray Computed | No |  |

---

### PMID: 16817954

- タイトル: Hypersensitivity pneumonitis.
- ジャーナル: Orphanet journal of rare diseases (2006)
- 著者: Lacasse Yves, Cormier Yvon
- MeSH用語数: 9

| MeSH UI | MeSH 用語 | 主要トピック | 修飾語 |
|---------|----------|------------|-------|
| D000328 | Adult | No |  |
| D000542 | Alveolitis, Extrinsic Allergic | No | classification, diagnosis*, epidemiology, therapy* |
| D003937 | Diagnosis, Differential | No |  |
| D005203 | Farmer's Lung | No | epidemiology |
| D014943 | Global Health | No |  |
| D006801 | Humans | No |  |
| D015994 | Incidence | No |  |
| D008171 | Lung Diseases | No | diagnosis |
| D015995 | Prevalence | No |  |

---

