# サンプル検索式

## PubMed/MEDLINE

### 基本構造
```
#1 Population（対象集団）
    "Disease"[Mesh] OR
    disease[tiab] OR
    condition[tiab]

#2 Intervention（介入）
    "Therapy"[Mesh] OR
    treatment[tiab] OR
    therapy[tiab]

#3 最終検索式
    #1 AND #2
    Filters: Language
```

## 検索実行結果
（2025年5月14日現在）

### 各検索ブロックの件数
- #1 Population: 約35,000件
- #2 Intervention: 約68,000件

### 最終検索式の結果
- #1 AND #2: 約3,200件
- フィルター適用後: 約2,800件

## 確定論文のMeSH
- Disease Category
  - Disease Subcategory
    - Specific Disease
- Therapeutics
  - Specific Therapy
