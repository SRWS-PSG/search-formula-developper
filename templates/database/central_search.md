# CENTRAL Search Formula

## Search History Format

```
#1 [mh "Leukemia, Myeloid, Acute"] OR [mh "Myelodysplastic Syndromes"] OR (acute NEXT myeloid NEXT leukemia):ti,ab OR AML:ti,ab OR (high-risk NEXT myelodysplastic NEXT syndrome):ti,ab OR (high NEXT risk NEXT MDS):ti,ab OR [mh "Remission Induction"] OR (induction NEXT therapy):ti,ab OR (intensive NEXT chemotherapy):ti,ab OR (remission NEXT induction):ti,ab OR [mh "Immunocompromised Host"] OR [mh "Agranulocytosis"] OR neutropeni*:ti,ab OR immunocompromised:ti,ab OR immunocompromized:ti,ab OR leukopeni*:ti,ab OR leucopeni*:ti,ab OR granulocytopeni*:ti,ab

#2 (neutropenic NEXT diet):ti,ab OR ((sterile:ti,ab OR clean:ti,ab OR (low NEXT bacteria*):ti,ab OR (low NEXT microb*):ti,ab OR (minimal NEXT bacteria*):ti,ab OR (minimal NEXT microb*):ti,ab OR (germ NEXT poor):ti,ab OR cooked:ti,ab OR (reduced NEXT bacteria*):ti,ab) AND ([mh diet] OR diet:ti,ab OR feeding:ti,ab OR dietar*:ti,ab OR food*:ti,ab OR nutrition:ti,ab)) OR (dietary NEXT restriction*):ti,ab

#3 #1 AND #2
```

## 主な変換ポイント

1. MeSH用語の表記変更
   - PubMed: [Mesh] → CENTRAL: [mh]
   例：`"Leukemia, Myeloid, Acute"[Mesh]` → `[mh "Leukemia, Myeloid, Acute"]`

2. タイトル/アブストラクト検索の表記変更
   - PubMed: [tiab] → CENTRAL: :ti,ab
   例：`AML[tiab]` → `AML:ti,ab`

3. 複数単語の結合
   - PubMed: スペース区切り → CENTRAL: NEXT演算子
   例：`acute myeloid leukemia` → `(acute NEXT myeloid NEXT leukemia)`

4. RCTフィルター
   - CENTRALは臨床試験のデータベースのため、RCTフィルターは不要

5. ワイルドカード（*）の使用
   - 両データベースで同様に使用可能
   例：`neutropeni*:ti,ab`

## 検索式の構造

1. ブロック1：疾患（AML/MDS）、治療（化学療法）、および免疫不全関連用語
2. ブロック2：食事療法関連用語
3. 最終検索：ブロック1 AND ブロック2
