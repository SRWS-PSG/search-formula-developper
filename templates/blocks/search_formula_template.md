# 乳がん放射線療法の検索式テンプレート

## PubMed/MEDLINE

### 基本構造
```
#1 Population（乳がん）
    "Breast Neoplasms"[Mesh] OR
    "Carcinoma, Ductal, Breast"[Mesh] OR
    breast cancer[tiab] OR
    breast carcinoma[tiab] OR
    breast adenocarcinoma[tiab] OR
    breast tumor[tiab] OR
    breast tumour[tiab] OR
    breast dcis[tiab] OR
    (breast[tiab] AND (ductal carcinoma[tiab] OR intraductal carcinoma[tiab] OR invasive[tiab] OR infiltrat*[tiab])) OR
    (ductal carcinoma[tiab] AND breast[tiab]) OR
    (intraductal carcinoma[tiab] AND breast[tiab]) OR
    (invasive ductal carcinoma[tiab] AND breast[tiab])

#2 Intervention（放射線療法）
    "Radiotherapy"[Mesh] OR
    "Brachytherapy"[Mesh] OR
    radiotherapy[tiab] OR
    radiation therapy[tiab] OR
    radiation[tiab] OR
    irradiation[tiab] OR
    brachytherapy[tiab]

#3 費用対効果分析フィルター (High Sensitive)
    "Cost-Benefit Analysis"[Mesh] OR
    "Quality-Adjusted Life Years"[Mesh] OR
    "Markov Chains"[Mesh] OR
    "Models, Economic"[Mesh] OR
    cost*[ti] OR
    (cost*[tiab] AND utilit*[tiab]) OR
    (cost*[tiab] AND (effective*[tiab] OR assess*[tiab] OR evaluat*[tiab] OR analys*[tiab] OR model*[tiab] OR benefit*[tiab] OR threshold*[tiab] OR quality[tiab] OR expens*[tiab] OR saving*[tiab] OR reduc*[tiab])) OR
    (economic*[tiab] AND (evaluat*[tiab] OR assess*[tiab] OR analys*[tiab] OR model*[tiab] OR outcome*[tiab] OR benefit*[tiab] OR threshold*[tiab] OR expens*[tiab] OR saving*[tiab] OR reduc*[tiab])) OR
    (qualit*[tiab] AND adjust*[tiab] AND life*[tiab]) OR
    QALY*[tiab] OR
    (incremental*[tiab] AND cost*[tiab]) OR
    ICER[tiab] OR
    utilities[tiab] OR
    markov*[tiab] OR
    (dollar*[tiab] OR USD[tiab] OR cents[tiab] OR pound[tiab] OR pounds[tiab] OR GBP[tiab] OR sterling*[tiab] OR pence[tiab] OR euro[tiab] OR euros[tiab] OR yen[tiab] OR JPY[tiab]) OR
    ((utility[tiab] OR effective*[tiab]) AND analys*[tiab]) OR
    (willing*[tiab] AND pay*[tiab]) OR
    (Eq. 5D*[tiab] OR EQ-5D*[tiab]) OR
    ((euroqol[tiab] OR euro-qol[tiab] OR euroquol[tiab] OR euro-quol[tiab] OR eurocol[tiab] OR euro-col[tiab]) AND ("5"[tiab] OR five[tiab])) OR
    (european*[tiab] AND quality[tiab] AND ("5"[tiab] OR five[tiab]))

#4 最終検索式
    #1 AND #2 AND #3
    Filters: English
```

## Cochrane Library (CENTRAL)

### 基本構造
```
#1 Population（乳がん）
    MeSH descriptor: [Breast Neoplasms] explode all trees OR
    MeSH descriptor: [Carcinoma, Ductal, Breast] explode all trees OR
    (breast NEXT (cancer OR carcinoma OR adenocarcinoma OR tumor OR tumour OR dcis)):ti,ab,kw OR
    ((breast) AND (ductal NEXT carcinoma OR intraductal NEXT carcinoma OR invasive OR infiltrat*)):ti,ab,kw OR
    ((ductal NEXT carcinoma OR intraductal NEXT carcinoma OR invasive NEXT ductal NEXT carcinoma) AND breast):ti,ab,kw

#2 Intervention（放射線療法）
    MeSH descriptor: [Radiotherapy] explode all trees OR
    MeSH descriptor: [Brachytherapy] explode all trees OR
    (radiotherapy OR (radiation NEXT therapy) OR radiation OR irradiation OR brachytherapy):ti,ab,kw

#3 費用対効果分析フィルター
    MeSH descriptor: [Cost-Benefit Analysis] explode all trees OR
    MeSH descriptor: [Quality-Adjusted Life Years] explode all trees OR
    MeSH descriptor: [Markov Chains] explode all trees OR
    MeSH descriptor: [Models, Economic] explode all trees OR
    cost*:ti OR
    (cost* AND utilit*):ti,ab OR
    (cost* AND (effective* OR assess* OR evaluat* OR analys* OR model* OR benefit* OR threshold* OR quality OR expens* OR saving* OR reduc*)):ti,ab OR
    (economic* AND (evaluat* OR assess* OR analys* OR model* OR outcome* OR benefit* OR threshold* OR expens* OR saving* OR reduc*)):ti,ab OR
    (qualit* AND adjust* AND life*):ti,ab OR
    QALY*:ti,ab OR
    (incremental* AND cost*):ti,ab OR
    ICER:ti,ab OR
    utilities:ti,ab OR
    markov*:ti,ab OR
    (dollar* OR USD OR cents OR pound OR pounds OR GBP OR sterling* OR pence OR euro OR euros OR yen OR JPY):ti,ab OR
    ((utility OR effective*) AND analys*):ti,ab OR
    (willing* AND pay*):ti,ab OR
    (Eq. 5D* OR EQ-5D*):ti,ab OR
    ((euroqol OR euro-qol OR euroquol OR euro-quol OR eurocol OR euro-col) AND ("5" OR five)):ti,ab OR
    (european* AND quality AND ("5" OR five)):ti,ab

#4 最終検索式
    #1 AND #2 AND #3
```

## 検索式構築の手順

1. 各要素の主要語の特定
   - Population: 乳がんの様々な表現形式を網羅
   - Intervention: 放射線療法に関する用語を包括的に収集
   - Study Design: 費用対効果分析に関する用語を包括的に収集

2. 同義語・類義語の収集
   - 乳がんの病理学的分類を考慮（浸潤性乳管癌、非浸潤性乳管癌等）
   - 放射線療法の様々な手法を包含（外部照射、小線源治療等）
   - 費用対効果分析の様々な手法を包含（費用効用分析、マルコフモデル等）

3. 構文の最適化
   - PubMed: [Mesh]と[tiab]の組み合わせ
   - CENTRAL: NEXT演算子を使用した正確な語句マッチング

4. 検索式のテスト
   - シードスタディの捕捉確認
   - PMID: 38065194
   - PMID: 35189767
   - PMID: 33558179

5. 検索式の最適化
   - ノイズとなる文献の分析
   - 必要に応じたフィルターの調整
   - 検索結果数の確認

6. 文書化
   - 検索式の変更履歴
   - 各データベースでの検索結果数
   - 重要論文の捕捉状況

## 注意事項

### PubMed検索時の留意点
- MeSH用語の展開（explode）を考慮
- フリーテキスト検索での語形変化への対応
- 費用対効果分析フィルターの感度と特異度のバランス

### CENTRAL検索時の留意点
- NEXT演算子の適切な使用
- MeSH用語の階層構造の活用
- フィールドタグ（ti,ab,kw）の使用

### 共通の注意点
- 定期的な検索結果の確認
- 新しい用語や概念の追加
- 検索精度の継続的な評価

## 検索式の評価基準

1. 感度（Sensitivity）
   - シードスタディの捕捉
   - 重要な文献の網羅性

2. 特異度（Specificity）
   - ノイズとなる文献の最小化
   - 関連性の高い文献の効率的な抽出

3. 精度（Precision）
   - 検索結果の適切な規模
   - 作業効率の確保

## 費用対効果分析フィルターのバリエーション

### PubMed/MEDLINE用

1. Sensitive Filter（高感度）
```
"Cost-Benefit Analysis"[Mesh] OR
"Quality-Adjusted Life Years"[Mesh] OR
"Markov Chains"[Mesh] OR
"Models, Economic"[Mesh] OR
cost*[ti] OR
(cost*[tiab] AND utilit*[tiab]) OR
(cost*[tiab] AND (effective*[tiab] OR assess*[tiab] OR evaluat*[tiab] OR analys*[tiab] OR model*[tiab] OR benefit*[tiab] OR threshold*[tiab] OR quality[tiab] OR expens*[tiab] OR saving*[tiab] OR reduc*[tiab])) OR
(economic*[tiab] AND (evaluat*[tiab] OR assess*[tiab] OR analys*[tiab] OR model*[tiab] OR outcome*[tiab] OR benefit*[tiab] OR threshold*[tiab] OR expens*[tiab] OR saving*[tiab] OR reduc*[tiab])) OR
(qualit*[tiab] AND adjust*[tiab] AND life*[tiab]) OR
QALY*[tiab] OR
(incremental*[tiab] AND cost*[tiab]) OR
ICER[tiab] OR
utilities[tiab] OR
markov*[tiab] OR
(dollar*[tiab] OR USD[tiab] OR cents[tiab] OR pound[tiab] OR pounds[tiab] OR GBP[tiab] OR sterling*[tiab] OR pence[tiab] OR euro[tiab] OR euros[tiab] OR yen[tiab] OR JPY[tiab]) OR
((utility[tiab] OR effective*[tiab]) AND analys*[tiab]) OR
(willing*[tiab] AND pay*[tiab]) OR
(Eq. 5D*[tiab] OR EQ-5D*[tiab]) OR
((euroqol[tiab] OR euro-qol[tiab] OR euroquol[tiab] OR euro-quol[tiab] OR eurocol[tiab] OR euro-col[tiab]) AND ("5"[tiab] OR five[tiab])) OR
(european*[tiab] AND quality[tiab] AND ("5"[tiab] OR five[tiab]))
```

2. Precise Filter（高精度）
```
"Cost-Benefit Analysis"[Mesh] OR
(cost* AND (qaly* OR (qualit* AND adjust* AND life*)))[tiab] OR
((incremental* AND cost*) OR ICER)[tiab] OR
(cost* AND utilit*)[tiab] OR
(cost* AND ((net AND benefit*) OR (net AND monetary AND benefit*) OR (net AND health AND benefit*)))[tiab] OR
((cost* AND effect*) AND (quality AND of AND life))[tiab] OR
(cost AND (effect* OR utilit*))[ti]
```

3. Free-Text only Filter（フリーテキストのみ）
```
(cost* AND (qaly* OR (qualit* AND adjust* AND life*)))[tiab] OR
((incremental* AND cost*) OR ICER)[tiab] OR
(cost* AND utilit*)[tiab] OR
(cost* AND ((net AND benefit*) OR (net AND monetary AND benefit*) OR (net AND health AND benefit*)))[tiab] OR
((cost* AND effect*) AND (quality AND of AND life))[tiab] OR
(cost AND (effect* OR utilit*))[ti]
```

## 更新履歴
- 初版作成: 2024-01-20
- 最終更新: 2024-01-20 RCTフィルターを費用対効果分析フィルターに変更
- 更新: 2024-01-21 費用対効果分析フィルターのバリエーション（Sensitive/Precise/Free-Text only）を追加
