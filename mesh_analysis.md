# シードスタディのMeSH用語分析
生成日時: 2025-08-22 03:29:31

## 分析サマリー

- 分析論文数: 5件
- 抽出されたユニークMeSH用語数: 40個

## 主要なMeSH用語（出現頻度順 - 上位20件）

| MeSH UI | MeSH 用語 | 出現数 | 主要トピック論文数 |
|---------|----------|-------|------------------|
| D006801 | Humans | 5 | 0 |
| D008297 | Male | 3 | 0 |
| D007398 | Interpersonal Relations | 2 | 2 |
| D000544 | Alzheimer Disease | 2 | 1 |
| D003704 | Dementia | 2 | 1 |
| D000368 | Aged | 2 | 0 |
| D005260 | Female | 2 | 0 |
| D008875 | Middle Aged | 2 | 0 |
| D036301 | Qualitative Research | 2 | 0 |
| D004532 | Ego | 1 | 1 |
| D012649 | Self Concept | 1 | 1 |
| D018888 | Aphasia, Primary Progressive | 1 | 1 |
| D009735 | Nursing Homes | 1 | 1 |
| D007407 | Interviews as Topic | 1 | 0 |
| D012657 | Self-Help Groups | 1 | 0 |
| D000595 | Amino Acid Sequence | 1 | 0 |
| D004789 | Enzyme Activation | 1 | 0 |
| D006023 | Glycoproteins | 1 | 0 |
| D008666 | Metalloendopeptidases | 1 | 0 |
| D008969 | Molecular Sequence Data | 1 | 0 |

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
| D006801 | Humans | 5 | B01.050.150.900.649.313.988.400.112.400.400 |
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
    node_C10["Nervous System Diseases [C10]"]
    node_C10_228["Central Nervous System Diseases [228]"]
    node_C10_228_140["Brain Diseases [140]"]
    node_C10_228_140_380["Dementia [380]"]
    node_C10_228_140_380_100["Alzheimer Disease [100]"]
    node_C10_228_140_380_132["Aphasia, Primary Progressive [132]"]
    node_C10_574["Neurodegenerative Diseases [574]"]
    node_C10_574_945["Tauopathies [945]"]
    node_C10_574_945_249["Alzheimer Disease [249]"]
    node_C10_597["Neurologic Manifestations [597]"]
    node_C10_597_606["Neurobehavioral Manifestations [606]"]
    node_C10_597_606_150["Communication Disorders [150]"]
    node_C10_597_606_150_500["Language Disorders [500]"]
    node_C10_597_606_150_500_800["Speech Disorders [800]"]
    node_C10_597_606_150_500_800_100["Aphasia [100]"]
    node_C10_597_606_150_500_800_100_155["Aphasia, Primary Progressive [155]"]
    node_C23["Pathological Conditions, Signs and Symptoms [C23]"]
    node_C23_888["Signs and Symptoms [888]"]
    node_C23_888_592["Neurologic Manifestations [592]"]
    node_C23_888_592_604["Neurobehavioral Manifestations [604]"]
    node_C23_888_592_604_150["Communication Disorders [150]"]
    node_C23_888_592_604_150_500["Language Disorders [500]"]
    node_C23_888_592_604_150_500_800["Speech Disorders [800]"]
    node_C23_888_592_604_150_500_800_100["Aphasia [100]"]
    node_C23_888_592_604_150_500_800_100_155["Aphasia, Primary Progressive [155]"]
    node_C10 --> node_C10_228
    node_C10_228 --> node_C10_228_140
    node_C10_228_140 --> node_C10_228_140_380
    node_C10_228_140_380 --> node_C10_228_140_380_100
    node_C10_228_140_380 --> node_C10_228_140_380_132
    node_C10 --> node_C10_574
    node_C10_574 --> node_C10_574_945
    node_C10_574_945 --> node_C10_574_945_249
    node_C10 --> node_C10_597
    node_C10_597 --> node_C10_597_606
    node_C10_597_606 --> node_C10_597_606_150
    node_C10_597_606_150 --> node_C10_597_606_150_500
    node_C10_597_606_150_500 --> node_C10_597_606_150_500_800
    node_C10_597_606_150_500_800 --> node_C10_597_606_150_500_800_100
    node_C10_597_606_150_500_800_100 --> node_C10_597_606_150_500_800_100_155
    node_C23 --> node_C23_888
    node_C23_888 --> node_C23_888_592
    node_C23_888_592 --> node_C23_888_592_604
    node_C23_888_592_604 --> node_C23_888_592_604_150
    node_C23_888_592_604_150 --> node_C23_888_592_604_150_500
    node_C23_888_592_604_150_500 --> node_C23_888_592_604_150_500_800
    node_C23_888_592_604_150_500_800 --> node_C23_888_592_604_150_500_800_100
    node_C23_888_592_604_150_500_800_100 --> node_C23_888_592_604_150_500_800_100_155
    style node_C10_228_140_380_100 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_C10_574_945_249 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_C10_228_140_380 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_C10_228_140_380_132 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_C10_597_606_150_500_800_100_155 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_C23_888_592_604_150_500_800_100_155 fill:#ff8c00,stroke:#333,stroke-width:2px
```

| MeSH UI | MeSH 用語 | 出現数 | ツリー番号 (カテゴリ内) |
|---------|----------|-------|-----------------------|
| D000544 | Alzheimer Disease | 2 | C10.228.140.380.100, C10.574.945.249 |
| D003704 | Dementia | 2 | C10.228.140.380 |
| D018888 | Aphasia, Primary Progressive | 1 | C10.228.140.380.132, C10.597.606.150.500.800.100.155, C23.888.592.604.150.500.800.100.155 |
| D009422 | Nervous System Diseases | 0 | C10 |
| D002493 | Central Nervous System Diseases | 0 | C10.228 |
| D001927 | Brain Diseases | 0 | C10.228.140 |
| D019636 | Neurodegenerative Diseases | 0 | C10.574 |
| D024801 | Tauopathies | 0 | C10.574.945 |
| D009461 | Neurologic Manifestations | 0 | C10.597 |
| D019954 | Neurobehavioral Manifestations | 0 | C10.597.606 |
| D003147 | Communication Disorders | 0 | C10.597.606.150 |
| D007806 | Language Disorders | 0 | C10.597.606.150.500 |
| D013064 | Speech Disorders | 0 | C10.597.606.150.500.800 |
| D001037 | Aphasia | 0 | C10.597.606.150.500.800.100 |
| D013568 | Pathological Conditions, Signs and Symptoms | 0 | C23 |
| D012816 | Signs and Symptoms | 0 | C23.888 |

## カテゴリ D: 化学物質と医薬品 (Chemicals and Drugs)
```mermaid
flowchart TD
    node_D08["Enzymes and Coenzymes [D08]"]
    node_D08_811["Enzymes [811]"]
    node_D08_811_277["Hydrolases [277]"]
    node_D08_811_277_656["Peptide Hydrolases [656]"]
    node_D08_811_277_656_300["Endopeptidases [300]"]
    node_D08_811_277_656_300_480["Metalloendopeptidases [480]"]
    node_D08_811_277_656_675["Metalloproteases [675]"]
    node_D08_811_277_656_675_374["Metalloendopeptidases [374]"]
    node_D09["Carbohydrates [D09]"]
    node_D09_400["Glycoconjugates [400]"]
    node_D09_400_430["Glycoproteins [430]"]
    node_D12["Amino Acids, Peptides, and Proteins [D12]"]
    node_D12_776["Proteins [776]"]
    node_D12_776_395["Glycoproteins [395]"]
    node_D08 --> node_D08_811
    node_D08_811 --> node_D08_811_277
    node_D08_811_277 --> node_D08_811_277_656
    node_D08_811_277_656 --> node_D08_811_277_656_300
    node_D08_811_277_656_300 --> node_D08_811_277_656_300_480
    node_D08_811_277_656 --> node_D08_811_277_656_675
    node_D08_811_277_656_675 --> node_D08_811_277_656_675_374
    node_D09 --> node_D09_400
    node_D09_400 --> node_D09_400_430
    node_D12 --> node_D12_776
    node_D12_776 --> node_D12_776_395
    style node_D09_400_430 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_D12_776_395 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_D08_811_277_656_300_480 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_D08_811_277_656_675_374 fill:#ff8c00,stroke:#333,stroke-width:2px
```

| MeSH UI | MeSH 用語 | 出現数 | ツリー番号 (カテゴリ内) |
|---------|----------|-------|-----------------------|
| D006023 | Glycoproteins | 1 | D09.400.430, D12.776.395 |
| D008666 | Metalloendopeptidases | 1 | D08.811.277.656.300.480, D08.811.277.656.675.374 |
| D045762 | Enzymes and Coenzymes | 0 | D08 |
| D004798 | Enzymes | 0 | D08.811 |
| D006867 | Hydrolases | 0 | D08.811.277 |
| D010447 | Peptide Hydrolases | 0 | D08.811.277.656 |
| D010450 | Endopeptidases | 0 | D08.811.277.656.300 |
| D045726 | Metalloproteases | 0 | D08.811.277.656.675 |
| D002241 | Carbohydrates | 0 | D09 |
| D006001 | Glycoconjugates | 0 | D09.400 |
| D000602 | Amino Acids, Peptides, and Proteins | 0 | D12 |
| D011506 | Proteins | 0 | D12.776 |

## カテゴリ E: 分析・診断・治療技術と装置 (Techniques and Equipment)
```mermaid
flowchart TD
    node_E05["Investigative Techniques [E05]"]
    node_E05_318["Epidemiologic Methods [318]"]
    node_E05_318_308["Data Collection [308]"]
    node_E05_318_308_420["Interviews as Topic [420]"]
    node_E05 --> node_E05_318
    node_E05_318 --> node_E05_318_308
    node_E05_318_308 --> node_E05_318_308_420
    style node_E05_318_308_420 fill:#ff8c00,stroke:#333,stroke-width:2px
```

| MeSH UI | MeSH 用語 | 出現数 | ツリー番号 (カテゴリ内) |
|---------|----------|-------|-----------------------|
| D007407 | Interviews as Topic | 1 | E05.318.308.420 |
| D008919 | Investigative Techniques | 0 | E05 |
| D004812 | Epidemiologic Methods | 0 | E05.318 |
| D003625 | Data Collection | 0 | E05.318.308 |

## カテゴリ F: 精神医学と心理学 (Psychiatry and Psychology)
```mermaid
flowchart TD
    node_F01["Behavior and Behavior Mechanisms [F01]"]
    node_F01_752["Personality [752]"]
    node_F01_752_747["Personality Development [747]"]
    node_F01_752_747_189["Ego [189]"]
    node_F01_752_747_792["Self Concept [792]"]
    node_F01_829["Psychology, Social [829]"]
    node_F01_829_401["Interpersonal Relations [401]"]
    node_F02["Psychological Phenomena [F02]"]
    node_F02_739["Psychological Theory [739]"]
    node_F02_739_794["Psychoanalytic Theory [794]"]
    node_F02_739_794_206["Ego [206]"]
    node_F03["Mental Disorders [F03]"]
    node_F03_615["Neurocognitive Disorders [615]"]
    node_F03_615_400["Dementia [400]"]
    node_F03_615_400_100["Alzheimer Disease [100]"]
    node_F03_615_400_125["Aphasia, Primary Progressive [125]"]
    node_F01 --> node_F01_752
    node_F01_752 --> node_F01_752_747
    node_F01_752_747 --> node_F01_752_747_189
    node_F01_752_747 --> node_F01_752_747_792
    node_F01 --> node_F01_829
    node_F01_829 --> node_F01_829_401
    node_F02 --> node_F02_739
    node_F02_739 --> node_F02_739_794
    node_F02_739_794 --> node_F02_739_794_206
    node_F03 --> node_F03_615
    node_F03_615 --> node_F03_615_400
    node_F03_615_400 --> node_F03_615_400_100
    node_F03_615_400 --> node_F03_615_400_125
    style node_F01_829_401 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_F03_615_400_100 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_F03_615_400 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_F01_752_747_189 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_F02_739_794_206 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_F01_752_747_792 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_F03_615_400_125 fill:#ff8c00,stroke:#333,stroke-width:2px
```

| MeSH UI | MeSH 用語 | 出現数 | ツリー番号 (カテゴリ内) |
|---------|----------|-------|-----------------------|
| D007398 | Interpersonal Relations | 2 | F01.829.401 |
| D000544 | Alzheimer Disease | 2 | F03.615.400.100 |
| D003704 | Dementia | 2 | F03.615.400 |
| D004532 | Ego | 1 | F01.752.747.189, F02.739.794.206 |
| D012649 | Self Concept | 1 | F01.752.747.792 |
| D018888 | Aphasia, Primary Progressive | 1 | F03.615.400.125 |
| D001520 | Behavior and Behavior Mechanisms | 0 | F01 |
| D010551 | Personality | 0 | F01.752 |
| D010553 | Personality Development | 0 | F01.752.747 |
| D011593 | Psychology, Social | 0 | F01.829 |
| D011579 | Psychological Phenomena | 0 | F02 |
| D011582 | Psychological Theory | 0 | F02.739 |
| D011574 | Psychoanalytic Theory | 0 | F02.739.794 |
| D001523 | Mental Disorders | 0 | F03 |
| D019965 | Neurocognitive Disorders | 0 | F03.615 |

## カテゴリ G: 生物学・物理学 (Biological Sciences)
```mermaid
flowchart TD
    node_G02["Chemical Phenomena [G02]"]
    node_G02_111["Biochemical Phenomena [111]"]
    node_G02_111_263["Enzyme Activation [263]"]
    node_G02_111_570["Molecular Structure [570]"]
    node_G02_111_570_060["Amino Acid Sequence [060]"]
    node_G03["Metabolic Phenomena [G03]"]
    node_G03_328["Enzyme Activation [328]"]
    node_G02 --> node_G02_111
    node_G02_111 --> node_G02_111_263
    node_G02_111 --> node_G02_111_570
    node_G02_111_570 --> node_G02_111_570_060
    node_G03 --> node_G03_328
    style node_G02_111_570_060 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_G02_111_263 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_G03_328 fill:#ff8c00,stroke:#333,stroke-width:2px
```

| MeSH UI | MeSH 用語 | 出現数 | ツリー番号 (カテゴリ内) |
|---------|----------|-------|-----------------------|
| D000595 | Amino Acid Sequence | 1 | G02.111.570.060 |
| D004789 | Enzyme Activation | 1 | G02.111.263, G03.328 |
| D055598 | Chemical Phenomena | 0 | G02 |
| D001669 | Biochemical Phenomena | 0 | G02.111 |
| D015394 | Molecular Structure | 0 | G02.111.570 |
| D055754 | Metabolic Phenomena | 0 | G03 |

## カテゴリ H: 自然科学 (Physical Sciences)
```mermaid
flowchart TD
    node_H01["Natural Science Disciplines [H01]"]
    node_H01_770["Science [770]"]
    node_H01_770_644["Research [644]"]
    node_H01_770_644_241["Empirical Research [241]"]
    node_H01_770_644_241_850["Qualitative Research [850]"]
    node_H01 --> node_H01_770
    node_H01_770 --> node_H01_770_644
    node_H01_770_644 --> node_H01_770_644_241
    node_H01_770_644_241 --> node_H01_770_644_241_850
    style node_H01_770_644_241_850 fill:#ff8c00,stroke:#333,stroke-width:2px
```

| MeSH UI | MeSH 用語 | 出現数 | ツリー番号 (カテゴリ内) |
|---------|----------|-------|-----------------------|
| D036301 | Qualitative Research | 2 | H01.770.644.241.850 |
| D010811 | Natural Science Disciplines | 0 | H01 |
| D012586 | Science | 0 | H01.770 |
| D012106 | Research | 0 | H01.770.644 |
| D036262 | Empirical Research | 0 | H01.770.644.241 |

## カテゴリ L: 情報科学 (Information Science)
```mermaid
flowchart TD
    node_L01["Information Science [L01]"]
    node_L01_399["Information Management [399]"]
    node_L01_399_250["Data Collection [250]"]
    node_L01_399_250_520["Interviews as Topic [520]"]
    node_L01_462["Information Sources [462]"]
    node_L01_462_750["Information Services [750]"]
    node_L01_462_750_245["Documentation [245]"]
    node_L01_462_750_245_667["Molecular Sequence Data [667]"]
    node_L01_462_750_245_667_060["Amino Acid Sequence [060]"]
    node_L01 --> node_L01_399
    node_L01_399 --> node_L01_399_250
    node_L01_399_250 --> node_L01_399_250_520
    node_L01 --> node_L01_462
    node_L01_462 --> node_L01_462_750
    node_L01_462_750 --> node_L01_462_750_245
    node_L01_462_750_245 --> node_L01_462_750_245_667
    node_L01_462_750_245_667 --> node_L01_462_750_245_667_060
    style node_L01_399_250_520 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_L01_462_750_245_667_060 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_L01_462_750_245_667 fill:#ff8c00,stroke:#333,stroke-width:2px
```

| MeSH UI | MeSH 用語 | 出現数 | ツリー番号 (カテゴリ内) |
|---------|----------|-------|-----------------------|
| D007407 | Interviews as Topic | 1 | L01.399.250.520 |
| D000595 | Amino Acid Sequence | 1 | L01.462.750.245.667.060 |
| D008969 | Molecular Sequence Data | 1 | L01.462.750.245.667 |
| D007254 | Information Science | 0 | L01 |
| D019451 | Information Management | 0 | L01.399 |
| D000093983 | Information Sources | 0 | L01.462 |
| D007255 | Information Services | 0 | L01.462.750 |
| D004282 | Documentation | 0 | L01.462.750.245 |

## カテゴリ M: 人物 (Named Groups)
```mermaid
flowchart TD
    node_M01["Persons [M01]"]
    node_M01_060["Age Groups [060]"]
    node_M01_060_116["Adult [116]"]
    node_M01_060_116_100["Aged [100]"]
    node_M01_060_116_630["Middle Aged [630]"]
    node_M01 --> node_M01_060
    node_M01_060 --> node_M01_060_116
    node_M01_060_116 --> node_M01_060_116_100
    node_M01_060_116 --> node_M01_060_116_630
    style node_M01_060_116_100 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_M01_060_116_630 fill:#ff8c00,stroke:#333,stroke-width:2px
```

| MeSH UI | MeSH 用語 | 出現数 | ツリー番号 (カテゴリ内) |
|---------|----------|-------|-----------------------|
| D000368 | Aged | 2 | M01.060.116.100 |
| D008875 | Middle Aged | 2 | M01.060.116.630 |
| D009272 | Persons | 0 | M01 |
| D009273 | Age Groups | 0 | M01.060 |
| D000328 | Adult | 0 | M01.060.116 |

## カテゴリ N: 健康管理 (Health Care)
```mermaid
flowchart TD
    node_N02["Health Care Facilities, Manpower, and Services [N02]"]
    node_N02_278["Health Facilities [278]"]
    node_N02_278_825["Residential Facilities [825]"]
    node_N02_278_825_610["Nursing Homes [610]"]
    node_N03["Health Care Economics and Organizations [N03]"]
    node_N03_540["Organizations [540]"]
    node_N03_540_782["Self-Help Groups [782]"]
    node_N05["Health Care Quality, Access, and Evaluation [N05]"]
    node_N05_715["Quality of Health Care [715]"]
    node_N05_715_360["Health Care Evaluation Mechanisms [360]"]
    node_N05_715_360_300["Data Collection [300]"]
    node_N05_715_360_300_400["Interviews as Topic [400]"]
    node_N06["Environment and Public Health [N06]"]
    node_N06_850["Public Health [850]"]
    node_N06_850_520["Epidemiologic Methods [520]"]
    node_N06_850_520_308["Data Collection [308]"]
    node_N06_850_520_308_420["Interviews as Topic [420]"]
    node_N02 --> node_N02_278
    node_N02_278 --> node_N02_278_825
    node_N02_278_825 --> node_N02_278_825_610
    node_N03 --> node_N03_540
    node_N03_540 --> node_N03_540_782
    node_N05 --> node_N05_715
    node_N05_715 --> node_N05_715_360
    node_N05_715_360 --> node_N05_715_360_300
    node_N05_715_360_300 --> node_N05_715_360_300_400
    node_N06 --> node_N06_850
    node_N06_850 --> node_N06_850_520
    node_N06_850_520 --> node_N06_850_520_308
    node_N06_850_520_308 --> node_N06_850_520_308_420
    style node_N02_278_825_610 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_N05_715_360_300_400 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_N06_850_520_308_420 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_N03_540_782 fill:#ff8c00,stroke:#333,stroke-width:2px
```

| MeSH UI | MeSH 用語 | 出現数 | ツリー番号 (カテゴリ内) |
|---------|----------|-------|-----------------------|
| D009735 | Nursing Homes | 1 | N02.278.825.610 |
| D007407 | Interviews as Topic | 1 | N05.715.360.300.400, N06.850.520.308.420 |
| D012657 | Self-Help Groups | 1 | N03.540.782 |
| D005159 | Health Care Facilities, Manpower, and Services | 0 | N02 |
| D006268 | Health Facilities | 0 | N02.278 |
| D012112 | Residential Facilities | 0 | N02.278.825 |
| D004472 | Health Care Economics and Organizations | 0 | N03 |
| D009938 | Organizations | 0 | N03.540 |
| D017530 | Health Care Quality, Access, and Evaluation | 0 | N05 |
| D011787 | Quality of Health Care | 0 | N05.715 |
| D017531 | Health Care Evaluation Mechanisms | 0 | N05.715.360 |
| D004778 | Environment and Public Health | 0 | N06 |
| D011634 | Public Health | 0 | N06.850 |

## カテゴリ X: カテゴリ X
```mermaid
flowchart TD
    node_X999998["Male [X999998]"]
    node_X999999["Female [X999999]"]
    style node_X999998 fill:#ff8c00,stroke:#333,stroke-width:2px
    style node_X999999 fill:#ff8c00,stroke:#333,stroke-width:2px
```

| MeSH UI | MeSH 用語 | 出現数 | ツリー番号 (カテゴリ内) |
|---------|----------|-------|-----------------------|
| D008297 | Male | 3 | X999998 |
| D005260 | Female | 2 | X999999 |

### 凡例

- オレンジ色のノード: Seed論文に実際に付与されていたMeSH用語 (上位20件に含まれるもの)
- 通常のノード: 上記MeSH用語の階層を構成する親ノード (可能な場合、用語名を補完)

## 論文別MeSH用語

### PMID: 24776791

- タイトル: Expressed Sense of Self by People With Alzheimer's Disease in a Support Group Interpreted in Terms of Agency and Communion.
- ジャーナル: Journal of applied gerontology : the official journal of the Southern Gerontological Society (2016)
- 著者: Hedman Ragnhild, Hansebo Görel, Ternestedt Britt-Marie, Hellström Ingrid, Norberg Astrid
- MeSH用語数: 11

| MeSH UI | MeSH 用語 | 主要トピック | 修飾語 |
|---------|----------|------------|-------|
| D000368 | Aged | No |  |
| D000544 | Alzheimer Disease | No | psychology* |
| D004532 | Ego | Yes |  |
| D005260 | Female | No |  |
| D006801 | Humans | No |  |
| D007398 | Interpersonal Relations | Yes |  |
| D007407 | Interviews as Topic | No |  |
| D008297 | Male | No |  |
| D008875 | Middle Aged | No |  |
| D012649 | Self Concept | Yes |  |
| D012657 | Self-Help Groups | No |  |

---

### PMID: 1468208

- タイトル: Characterization of metalloproteinases and tissue inhibitors of metalloproteinases in human plasma.
- ジャーナル: Connective tissue research (1992)
- 著者: Moutsiakis D, Mancuso P, Krutzsch H, Stetler-Stevenson W, Zucker S
- MeSH用語数: 9

| MeSH UI | MeSH 用語 | 主要トピック | 修飾語 |
|---------|----------|------------|-------|
| D000595 | Amino Acid Sequence | No |  |
| D004789 | Enzyme Activation | No |  |
| D006023 | Glycoproteins | No | blood* |
| D006801 | Humans | No |  |
| D008666 | Metalloendopeptidases | No | antagonists & inhibitors*, blood*, isolation & purification |
| D008969 | Molecular Sequence Data | No |  |
| D009363 | Neoplasm Proteins | No | blood* |
| D019716 | Tissue Inhibitor of Metalloproteinase-2 | No |  |
| D019714 | Tissue Inhibitor of Metalloproteinases | No |  |

---

### PMID: 36054090

- タイトル: The affective, behavioural, and cognitive reactions to a diagnosis of Primary Progressive Aphasia: A qualitative descriptive study.
- ジャーナル: Dementia (London, England) (2022)
- 著者: Lo Kang-Chi, Bricker-Katz Geraldine, Ballard Kirrie, Piguet Olivier
- MeSH用語数: 6

| MeSH UI | MeSH 用語 | 主要トピック | 修飾語 |
|---------|----------|------------|-------|
| D006801 | Humans | No |  |
| D003704 | Dementia | Yes |  |
| D036301 | Qualitative Research | No |  |
| D005190 | Family | No | psychology |
| D003071 | Cognition | No |  |
| D018888 | Aphasia, Primary Progressive | Yes | diagnosis, psychology |

---

### PMID: 30249213

- タイトル: Meaningful connections in dementia end of life care in long term care homes.
- ジャーナル: BMC psychiatry (2018)
- 著者: McCleary Lynn, Thompson Genevieve N, Venturato Lorraine, Wickson-Griffiths Abigail, Hunter Paulette, Sussman Tamara, Kaasalainen Sharon
- MeSH用語数: 19

| MeSH UI | MeSH 用語 | 主要トピック | 修飾語 |
|---------|----------|------------|-------|
| D000368 | Aged | No |  |
| D000369 | Aged, 80 and over | No |  |
| D001601 | Bereavement | No |  |
| D002170 | Canada | No |  |
| D017028 | Caregivers | No | psychology |
| D003704 | Dementia | No | psychology, therapy* |
| D005195 | Family Relations | No |  |
| D005260 | Female | No |  |
| D017144 | Focus Groups | No |  |
| D006801 | Humans | No |  |
| D007398 | Interpersonal Relations | Yes |  |
| D008134 | Long-Term Care | No | psychology |
| D008297 | Male | No |  |
| D008875 | Middle Aged | No |  |
| D009735 | Nursing Homes | Yes |  |
| D010166 | Palliative Care | No | psychology* |
| D011369 | Professional-Patient Relations | No |  |
| D036301 | Qualitative Research | No |  |
| D013727 | Terminal Care | No | methods, psychology* |

---

### PMID: 33839469

- タイトル: Analytic autoethnography of familial and institutional social identity construction of My Dad with Alzheimer's: In the emergency room with Erving Goffman and Oliver Sacks.
- ジャーナル: Social science & medicine (1982) (2021)
- 著者: Smith Robert Courtney
- MeSH用語数: 8

| MeSH UI | MeSH 用語 | 主要トピック | 修飾語 |
|---------|----------|------------|-------|
| D000328 | Adult | No |  |
| D000544 | Alzheimer Disease | Yes |  |
| D003617 | Dangerous Behavior | No |  |
| D004636 | Emergency Service, Hospital | No |  |
| D004644 | Emotions | No |  |
| D006801 | Humans | No |  |
| D008297 | Male | No |  |
| D012933 | Social Identification | No |  |

---

