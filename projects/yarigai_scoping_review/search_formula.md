# 日本の医師における「やりがい」スコーピングレビュー検索式

## PubMed/MEDLINE

### 検索式構造

#### #1 Population (医師)
```
"Physicians"[Mesh] OR
physician*[tiab] OR
doctor*[tiab] OR
"general practitioner*"[tiab] OR
clinician*[tiab] 

```

#### #2A MeSH用語（やりがい関連・主要テーマ）
```
"Personal Satisfaction"[Majr] OR
"Job Satisfaction"[Majr] OR
"Motivation"[Majr:noexp] OR
"Work Engagement"[Mesh] OR
"Professional Autonomy"[Majr]
```

#### #2B Meaningful Work関連
```
"meaningful work"[tiab] OR
"work meaningfulness"[tiab] OR
"meaningfulness of work"[tiab] OR
"meaning in work"[tiab] OR
"work meaning"[tiab] OR
"sense of meaning"[tiab]
```

#### #2C Work Engagement関連
```
"work engagement"[tiab] OR
vigor[tiab] OR
dedication[tiab] OR
absorption[tiab] OR
"engaged at work"[tiab]
```

#### #2D Calling/Vocation関連
```
calling[tiab] OR
"career calling"[tiab] OR
"vocational calling"[tiab] OR
vocation*[tiab] OR
"calling orientation"[tiab]
```

#### #2E Motivation関連
```
"prosocial motivation"[tiab] OR
"intrinsic motivation"[tiab] OR
"work motivation"[tiab] OR
(
  motivat*[tiab] AND
  (work*[tiab] OR job*[tiab] OR career*[tiab] OR professional*[tiab] OR workplace[tiab])
)
```

#### #2F Satisfaction関連
```
"job satisfaction"[tiab] OR
"work satisfaction"[tiab] OR
"career satisfaction"[tiab] OR
"professional satisfaction"[tiab] OR
"compassion satisfaction"[tiab]
```

#### #2G Professional Fulfillment/Quality of Life
```
"professional fulfillment"[tiab] OR
"professional quality of life"[tiab] OR
"quality of professional life"[tiab] OR
fulfillment[tiab] OR
fulfilment[tiab]
```

#### #2H 日本語概念（ローマ字表記）
```
yarigai[tiab] OR
ikigai[tiab]
```

#### #2I 心理的ニーズ/Thriving
```
"psychological need*"[tiab] OR
(
  (autonomy[tiab] OR competence[tiab] OR relatedness[tiab]) AND
  (work*[tiab] OR job*[tiab] OR professional*[tiab] OR workplace[tiab])
) OR
"thriving at work"[tiab] OR
"workplace thriving"[tiab]
```

#### #2J Task Significance
```
"task significance"[tiab] OR
"meaningful task*"[tiab] OR
"work significance"[tiab]
```

#### #2 統合 - 全てのConcept要素
```
#2A OR #2B OR #2C OR #2D OR #2E OR #2F OR #2G OR #2H OR #2I OR #2J
```

#### #3 測定尺度（オプション - より特異的な検索用）
```
"Work and Meaning Inventory"[tiab] OR
WAMI[tiab] OR
"Calling and Vocation Questionnaire"[tiab] OR
CVQ[tiab] OR
"Professional Fulfillment Index"[tiab] OR
PFI[tiab] OR
"Utrecht Work Engagement Scale"[tiab] OR
UWES[tiab] OR
"Basic Psychological Need Satisfaction at Work Scale"[tiab] OR
BPNSWS[tiab] OR
"Thriving at Work Scale"[tiab] OR
"Job Diagnostic Survey"[tiab] OR
JDS[tiab] OR
ProQOL[tiab] OR
"Professional Quality of Life"[tiab]
```

#### #4 日本関連（RQ1用 - 日本の医師）
```
Japan[Mesh:noexp] OR
Japan[tiab] OR
Japanese[tiab] OR
Nippon[tiab] OR
Nihon[tiab]
```

### 最終検索式

#### 検索式A: 日本の医師におけるやりがい（RQ1）
```
#1 AND #2 AND #4
```

#### 検索式B: 世界の医師におけるやりがい（RQ2）
```
#1 AND #2
NOT (animals[mh] NOT humans[mh])
```

#### 検索式C: 測定尺度を使用した研究（より特異的）
```
#1 AND (#2 OR #3)
```

### フィルター（必要に応じて適用）
```
Humans[Mesh]
English[lang] OR Japanese[lang]
```

### 除外基準
```
NOT (
  "Medical Students"[Mesh] OR
  "Students, Medical"[Mesh] OR
  "medical student*"[tiab] OR
  "Burnout, Professional"[Mesh:noexp] OR
  (burnout[tiab] NOT (recovery[tiab] OR resilience[tiab] OR "positive"[tiab]))
)
```

## 検索戦略の注意点

### 感度と特異度のバランス
- この検索式は高感度（high sensitivity）を重視し、関連する可能性のある研究を広く捕捉する設計
- #2のConcept部分は意図的に広範囲をカバー（meaningful work, engagement, calling, satisfaction等）
- スクリーニング段階で詳細な適格基準を適用して絞り込む

### やりがいの概念について
- "やりがい"は英語に直訳困難な日本語概念
- プロトコルの参考文献（Nishigori et al. 2024）では、meaningful work, intrinsic motivation, achievement, satisfactionを包含する概念として定義
- 検索式では関連する複数の英語概念（meaningful work, work engagement, calling, job satisfaction等）を組み合わせて捕捉

### Incentivesの除外
- プロトコルの指示に従い、外発的動機付け（incentives）に関する研究は概念として除外
- ただし、"motivation"は内発的動機も含むため組み入れ、スクリーニングで判断

### 医学生の扱い
- 除外基準に医学生を含めているが、必要に応じて調整可能
- プロトコルでは「臨床医」を対象としているため除外

### Burnoutとの関係
- Burnoutのみに焦点を当てた研究は除外
- ただし、burnoutからの回復や、burnoutとやりがいの関係を論じた研究は含める可能性があるため、完全除外ではなく注意深く除外

## 推定検索件数

初回検索実行前の推定：
- #1 (医師): 約1,500,000件
- #2 (やりがい関連概念): 約800,000件
- #4 (日本): 約500,000件
- RQ1 (#1 AND #2 AND #4): 推定2,000-5,000件
- RQ2 (#1 AND #2): 推定15,000-30,000件

## 次のステップ

1. `check_search_lines.py`で各検索行のヒット件数を確認
2. シード論文のPMIDリストを作成（`seed_pmids.txt`）
3. `extract_mesh.py`でシード論文のMeSH用語を分析
4. 必要に応じて検索式を調整
5. `check_final_query.py`で最終検索を実行し、シード論文の包含を確認
6. 他データベース（Embase, CINAHL, PsycInfo, ERIC, ICHUSHI）への変換

## 参考文献

Nishigori H, Shimazono Y, Busari J, Dornan T. Exploring yarigai: The meaning of working as a physician in teaching medical professionalism. Med Teach. 2024 Nov;46(11):1486–93.
