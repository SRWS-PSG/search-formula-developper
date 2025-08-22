# 最適化拡張検索式: 認知症・高齢者・悲嘆（MeSH分析基盤改善版）

## 検索戦略

MeSH用語分析に基づいて、不足していた5件のPMIDを捕捉するために検索ブロックを最適化しました。

## 拡張検索ブロック

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

### 高齢者ブロック（変更なし）
#10 "Aged"[Mesh]
#11 "Aged, 80 and over"[Mesh]
#12 "Frail Elderly"[Mesh]
#13 aged[tiab]
#14 elderly[tiab]
#15 older[tiab]
#16 #10 OR #11 OR #12 OR #13 OR #14 OR #15

### 悲嘆・喪失ブロック（最適化拡張版）
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
#37 "Social Identification"[Mesh]
#38 "social identity"[tiab]
#39 "autoethnography"[tiab]
#40 "qualitative research"[tiab]
#41 #17 OR #18 OR #19 OR #20 OR #21 OR #22 OR #23 OR #24 OR #25 OR #26 OR #27 OR #28 OR #29 OR #30 OR #31 OR #32 OR #33 OR #34 OR #35 OR #36 OR #37 OR #38 OR #39 OR #40

### 最終検索式
#42 #9 AND #16 AND #41

## 追加された用語の根拠

### 認知症ブロックへの追加
- **"Aphasia, Primary Progressive"[Mesh]**: PMID 36054090で主要トピック
- **"primary progressive aphasia"[tiab]**: 対応するテキスト語

### 悲嘆・喪失ブロックへの追加
- **"Bereavement"[Mesh]**: PMID 30249213で使用、死別悲嘆の重要概念
- **"Self Concept"[Mesh]**: PMID 24776791で主要トピック、自己概念の喪失
- **"Ego"[Mesh]**: PMID 24776791で主要トピック、自我・アイデンティティ
- **"Social Identification"[Mesh]**: PMID 33839469で使用、社会的アイデンティティ
- **"autoethnography"[tiab]**: PMID 33839469のタイトルから、質的研究手法
- **"qualitative research"[tiab]**: PMID 33839469, 36054090で使用

## 不足PMIDの分析結果

| PMID | タイトル | 主要な不足概念 | 対応する追加用語 |
|------|----------|---------------|------------------|
| 24776791 | Expressed Sense of Self by People With Alzheimer's Disease | Self Concept, Ego | "Self Concept"[Mesh], "Ego"[Mesh] |
| 36054090 | The affective, behavioural, and cognitive reactions to a diagnosis of Primary Progressive Aphasia | Primary Progressive Aphasia | "Aphasia, Primary Progressive"[Mesh] |
| 30249213 | Meaningful connections in dementia end of life care | Bereavement, End-of-life care | "Bereavement"[Mesh] |
| 33839469 | Analytic autoethnography of familial and institutional social identity construction | Social Identification, Autoethnography | "Social Identification"[Mesh], "autoethnography"[tiab] |
| 1468208 | Characterization of metalloproteinases | Metalloproteinases (生化学研究) | 研究目的外のため除外 |

## 改善戦略の特徴

1. **精密な用語選択**: 過度に広範囲にならないよう、最も関連性の高い用語のみを追加
2. **MeSH階層の活用**: MeSH用語とその対応するテキスト語を組み合わせ
3. **研究目的との整合性**: 認知症当事者の悲嘆体験に焦点を維持
4. **質的研究の包含**: autoethnography、qualitative researchなどの研究手法を追加

## 期待される効果

- **包括性向上**: 悲嘆概念の多面的な捉え方を実現
- **精度維持**: 関連性の高い論文の捕捉
- **論理的一貫性**: 元の検索戦略の論理構造を維持
- **効率性**: 適度な結果数の増加

## PubMed検索式（コピー&ペースト用）

```
(("Dementia"[Mesh]) OR (dementia[tiab]) OR (alzheimer*[tiab]) OR ("lewy body"[tiab]) OR ("frontotemporal dementia"[tiab]) OR ("cognitive impairment"[tiab]) OR ("Aphasia, Primary Progressive"[Mesh]) OR ("primary progressive aphasia"[tiab])) AND (("Aged"[Mesh]) OR ("Aged, 80 and over"[Mesh]) OR ("Frail Elderly"[Mesh]) OR (aged[tiab]) OR (elderly[tiab]) OR (older[tiab])) AND (("Grief"[Mesh]) OR (grief[tiab]) OR (grieving[tiab]) OR (mourning[tiab]) OR (sorrow[tiab]) OR (lament*[tiab]) OR ("ambiguous loss"[tiab]) OR ("feeling of loss"[tiab]) OR ("experience of loss"[tiab]) OR ("loss of self"[tiab]) OR ("loss of identity"[tiab]) OR ("loss of function"[tiab]) OR ("loss of independence"[tiab]) OR ("loss of autonomy"[tiab]) OR ("Bereavement"[Mesh]) OR (bereavement[tiab]) OR ("Self Concept"[Mesh]) OR ("self concept"[tiab]) OR ("sense of self"[tiab]) OR ("Ego"[Mesh]) OR ("Social Identification"[Mesh]) OR ("social identity"[tiab]) OR ("autoethnography"[tiab]) OR ("qualitative research"[tiab]))
```

## 注意事項

PMID 1468208（メタロプロテアーゼ研究）は生化学的研究であり、認知症当事者の悲嘆体験という研究目的から外れるため、この検索式では意図的に除外しています。研究の焦点と論理的一貫性を維持するための判断です。
