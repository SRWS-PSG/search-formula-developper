# 拡張検索式: 認知症・高齢者・悲嘆（MeSH分析基盤改善版）

## 検索ブロック

### 認知症ブロック（拡張版）
#1 "Dementia"[Mesh]
#2 dementia[tiab]
#3 alzheimer*[tiab]
#4 "lewy body"[tiab]
#5 "frontotemporal dementia"[tiab]
#6 "cognitive impairment"[tiab]
#7 "Aphasia, Primary Progressive"[Mesh]
#8 "primary progressive aphasia"[tiab]
#9 #1 OR #2 OR #3 OR #4 OR #5 OR #6 OR #7 OR #8

### 高齢者ブロック
#10 "Aged"[Mesh]
#11 "Aged, 80 and over"[Mesh]
#12 "Frail Elderly"[Mesh]
#13 aged[tiab]
#14 elderly[tiab]
#15 older[tiab]
#16 #10 OR #11 OR #12 OR #13 OR #14 OR #15

### 悲嘆・喪失ブロック（大幅拡張版）
#17 "Grief"[Mesh]
#18 grief[tiab]
#19 grieving[tiab]
#20 mourning[tiab]
#21 sorrow[tiab]
#22 lament*[tiab]
#23 "ambiguous loss"[tiab]
#24 "feeling of loss"[tiab]
#25 "experience of loss"[tiab]
#26 "loss of self"[tiab]
#27 "loss of identity"[tiab]
#28 "loss of function"[tiab]
#29 "loss of independence"[tiab]
#30 "loss of autonomy"[tiab]
#31 "Bereavement"[Mesh]
#32 bereavement[tiab]
#33 "Self Concept"[Mesh]
#34 "self concept"[tiab]
#35 "sense of self"[tiab]
#36 "Ego"[Mesh]
#37 ego[tiab]
#38 "Emotions"[Mesh]
#39 emotion*[tiab]
#40 "Social Identification"[Mesh]
#41 "social identity"[tiab]
#42 identity[tiab]
#43 "meaningful connection*"[tiab]
#44 "end of life"[tiab]
#45 "terminal care"[tiab]
#46 "palliative care"[tiab]
#47 "interpersonal relation*"[tiab]
#48 #17 OR #18 OR #19 OR #20 OR #21 OR #22 OR #23 OR #24 OR #25 OR #26 OR #27 OR #28 OR #29 OR #30 OR #31 OR #32 OR #33 OR #34 OR #35 OR #36 OR #37 OR #38 OR #39 OR #40 OR #41 OR #42 OR #43 OR #44 OR #45 OR #46 OR #47

### 最終検索式
#49 #9 AND #16 AND #48

## 追加された用語の根拠

### 認知症ブロックへの追加
- **"Aphasia, Primary Progressive"[Mesh]**: PMID 36054090で主要トピックとして使用
- **"primary progressive aphasia"[tiab]**: 対応するテキスト語

### 悲嘆・喪失ブロックへの追加
- **"Bereavement"[Mesh]**: PMID 30249213で使用、死別悲嘆の重要概念
- **"Self Concept"[Mesh]**: PMID 24776791で主要トピック、自己概念の喪失
- **"Ego"[Mesh]**: PMID 24776791で主要トピック、自我・アイデンティティ
- **"Emotions"[Mesh]**: PMID 33839469で使用、感情表出
- **"Social Identification"[Mesh]**: PMID 33839469で使用、社会的アイデンティティ
- **"interpersonal relation*"[tiab]**: PMID 24776791, 30249213で主要トピック

### エンドオブライフケア関連用語
- **"meaningful connection*"[tiab]**: PMID 30249213のタイトルから
- **"end of life"[tiab]**: 終末期ケアの概念
- **"terminal care"[tiab]**: PMID 30249213で使用
- **"palliative care"[tiab]**: PMID 30249213で使用

## MeSH分析に基づく改善戦略

この拡張検索式は、5件の不足PMIDのMeSH用語分析に基づいて作成されました：

1. **PMID 24776791**: Self Concept, Ego, Interpersonal Relations
2. **PMID 1468208**: 生化学的研究（メタロプロテアーゼ）- 研究目的外のため除外
3. **PMID 36054090**: Aphasia Primary Progressive, Dementia
4. **PMID 30249213**: Bereavement, Terminal Care, Palliative Care
5. **PMID 33839469**: Emotions, Social Identification

## 期待される効果

- **包括性向上**: 悲嘆概念の多面的な捉え方
- **論理的一貫性**: 研究目的との整合性維持
- **精度向上**: 関連性の高い論文の捕捉
- **PMID包含率**: 15/15件（100%）を目標
