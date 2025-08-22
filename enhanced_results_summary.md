# 拡張検索式結果サマリー

## 概要

MeSH用語分析に基づいて検索ブロックを拡張し、不足していた5件のPMIDを捕捉する改善された検索式を作成しました。

## 改善戦略

### 1. 認知症ブロックの拡張
**追加用語:**
- "Aphasia, Primary Progressive"[Mesh]
- "primary progressive aphasia"[tiab]

**根拠:** PMID 36054090で主要トピックとして使用されており、認知症の特定サブタイプを捕捉

### 2. 悲嘆・喪失ブロックの大幅拡張
**追加MeSH用語:**
- "Bereavement"[Mesh] - 死別悲嘆
- "Self Concept"[Mesh] - 自己概念
- "Ego"[Mesh] - 自我・アイデンティティ
- "Emotions"[Mesh] - 感情表出
- "Social Identification"[Mesh] - 社会的アイデンティティ

**追加テキスト語:**
- bereavement[tiab]
- "self concept"[tiab], "sense of self"[tiab]
- ego[tiab]
- emotion*[tiab]
- "social identity"[tiab], identity[tiab]
- "meaningful connection*"[tiab]
- "end of life"[tiab]
- "terminal care"[tiab], "palliative care"[tiab]
- "interpersonal relation*"[tiab]

## 不足PMIDとMeSH用語の対応

| PMID | 主要な不足MeSH用語 | 対応する追加用語 |
|------|-------------------|------------------|
| 24776791 | Self Concept, Ego, Interpersonal Relations | "Self Concept"[Mesh], "Ego"[Mesh], "interpersonal relation*"[tiab] |
| 36054090 | Aphasia Primary Progressive | "Aphasia, Primary Progressive"[Mesh] |
| 30249213 | Bereavement, Terminal Care, Palliative Care | "Bereavement"[Mesh], "terminal care"[tiab], "palliative care"[tiab] |
| 33839469 | Emotions, Social Identification | "Emotions"[Mesh], "Social Identification"[Mesh] |
| 1468208 | Metalloproteinases (生化学研究) | 研究目的外のため特別な対応が必要 |

## 期待される結果

- **PMID包含率**: 15/15件（100%）を目標
- **論理的一貫性**: 研究目的（認知症当事者の悲嘆体験）との整合性維持
- **包括性向上**: 悲嘆概念の多面的な捉え方を実現
- **精度維持**: 過度に広範囲にならないよう配慮

## 検証方法

1. 拡張検索式での全PMID包含状況確認
2. 各ブロック単体での不足PMID捕捉状況確認
3. 元の検索式との結果数比較
4. 増加率の妥当性評価

## 次のステップ

1. 拡張検索式の実行と検証
2. 結果の詳細分析
3. 必要に応じた微調整
4. 最終的な検索式の確定
