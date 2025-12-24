# 日本の医師における「やりがい」スコーピングレビュー検索式（最適化版）

## 最適化の根拠

Block overlap analysis (2025-11-05) に基づき、以下の変更を実施:

### 削除した検索語（追加件数が0または極めて少ない）

**#1 Population (医師)**
- `"General Practitioners"[Mesh]` - 削除（`"Physicians"[Mesh]`に完全包含、追加0件）
- `"medical doctor*"[tiab]` - 削除（他の検索語で完全にカバー、追加0件）

**#2A MeSH用語**
- `"Vocation"[Mesh]` - 削除（0件）
- `"Work Engagement"[Mesh]` - 削除（わずか0.2%、777件のみ追加）

**#2C Work Engagement関連**
- `"engaged at work"[tiab]` - 削除（追加0件）
- **注意**: `absorption[tiab]` は96.9%を占めるが、生理学的・化学的absorptionも多く含まれる可能性あり
  → 今後、より特異的な検索式への改善を検討

**#2D Calling/Vocation関連**
- `"career calling"[tiab]` - 削除（`calling[tiab]`に完全包含、追加0件）
- `"vocational calling"[tiab]` - 削除（同上、追加0件）
- `"calling orientation"[tiab]` - 削除（同上、追加0件）

**#2E Motivation関連**
- `"prosocial motivation"[tiab]` - 削除（0.1%のみ）
- `"work motivation"[tiab]` - 削除（0.2%のみ）
- **注意**: `motivat*[tiab]` が98.2%を占めるため、他の具体的検索語はほぼ不要

**#2H 日本語概念**
- `yarigai[tiab]` - 削除（わずか2件、`ikigai[tiab]`も111件のみ）
  → ブロック全体の有用性を再検討（合計112件）

### 保持した検索語（有意な貢献がある）

**#2F Satisfaction関連** - すべて保持（各行が1%以上貢献）
**#2G Professional Fulfillment** - すべて保持（バランスの取れた貢献）
**#2I 心理的ニーズ/Thriving** - すべて保持（各行が有意に貢献）
**#2J Task Significance** - すべて保持（件数は少ないが概念的に重要）

---

## PubMed/MEDLINE

### 検索式構造

#### #1 Population (医師) - 最適化版
```
"Physicians"[Mesh] OR
physician*[tiab] OR
doctor*[tiab] OR
"general practitioner*"[tiab] OR
clinician*[tiab]
```
**変更点**: `"General Practitioners"[Mesh]`, `"medical doctor*"[tiab]` を削除（重複のため）

#### #2A MeSH用語（やりがい関連） - 最適化版
```
"Personal Satisfaction"[Mesh] OR
"Job Satisfaction"[Mesh] OR
"Motivation"[Mesh] OR
"Professional Role"[Mesh] OR
"Professional Autonomy"[Mesh] OR
"Career Choice"[Mesh]
```
**変更点**: `"Vocation"[Mesh]`, `"Work Engagement"[Mesh]` を削除（追加件数が極めて少ない）

#### #2B Meaningful Work関連 - 変更なし
```
"meaningful work"[tiab] OR
"work meaningfulness"[tiab] OR
"meaningfulness of work"[tiab] OR
"meaning in work"[tiab] OR
"work meaning"[tiab] OR
"sense of meaning"[tiab]
```
**理由**: すべての検索語が有意に貢献（合計1,250件）

#### #2C Work Engagement関連 - 最適化版
```
"work engagement"[tiab] OR
vigor[tiab] OR
dedication[tiab] OR
absorption[tiab]
```
**変更点**: `"engaged at work"[tiab]` を削除（追加0件）
**警告**: `absorption[tiab]`は96.9%を占めるが、医学的文脈での"absorption"も多数含む可能性あり。
将来的な改善案: `"work engagement"[tiab] OR (absorption[tiab] AND (work[tiab] OR job[tiab]))`

#### #2D Calling/Vocation関連 - 最適化版
```
calling[tiab] OR
vocation*[tiab]
```
**変更点**: `"career calling"[tiab]`, `"vocational calling"[tiab]`, `"calling orientation"[tiab]` を削除（すべてcalling[tiab]に包含）

#### #2E Motivation関連 - 最適化版
```
"intrinsic motivation"[tiab] OR
motivat*[tiab]
```
**変更点**: `"prosocial motivation"[tiab]`, `"work motivation"[tiab]` を削除（motivat*に包含）
**理由**: `motivat*[tiab]` が98.2%をカバー

#### #2F Satisfaction関連 - 変更なし
```
"job satisfaction"[tiab] OR
"work satisfaction"[tiab] OR
"career satisfaction"[tiab] OR
"professional satisfaction"[tiab] OR
"compassion satisfaction"[tiab]
```
**理由**: すべての検索語が有意に貢献（合計17,996件）

#### #2G Professional Fulfillment/Quality of Life - 変更なし
```
"professional fulfillment"[tiab] OR
"professional quality of life"[tiab] OR
"quality of professional life"[tiab] OR
fulfillment[tiab] OR
fulfilment[tiab]
```
**理由**: バランスの取れた貢献（合計9,131件）

#### #2H 日本語概念（ローマ字表記） - オプション化
```
ikigai[tiab]
```
**変更点**: `yarigai[tiab]` を削除（わずか2件）、ブロック全体をオプション化
**理由**: 合計112件と貢献が小さいが、概念的には重要なため完全削除はしない

#### #2I 心理的ニーズ/Thriving - 変更なし
```
"psychological need*"[tiab] OR
autonomy[tiab] OR
competence[tiab] OR
relatedness[tiab] OR
"thriving at work"[tiab] OR
thriving[tiab]
```
**理由**: すべての検索語が有意に貢献（合計157,820件）

#### #2J Task Significance - 変更なし
```
"task significance"[tiab] OR
"meaningful task*"[tiab] OR
"work significance"[tiab]
```
**理由**: 件数は少ないが（215件）、meaningful workの概念的に重要

#### #2 統合 - 全てのConcept要素
```
#2A OR #2B OR #2C OR #2D OR #2E OR #2F OR #2G OR (#2H) OR #2I OR #2J
```
**変更点**: #2Hを括弧でオプション化（必要に応じて含めるか判断）

#### #3 測定尺度（オプション - より特異的な検索用） - 変更なし
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

#### #4 日本関連（RQ1用 - 日本の医師） - 変更なし
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

---

## 最適化の効果

### 削減された検索語の数
- **元の検索式**: 約60の検索語
- **最適化版**: 約48の検索語（約20%削減）

### 削減しても問題ない理由
1. **完全包含**: 削除した検索語は他の検索語で完全にカバーされている
2. **重複**: ORで結合しても新規結果を追加しない（追加0件）
3. **効率化**: API呼び出し回数とクエリの複雑さを軽減

### 検索感度への影響
- **影響なし**: 削除した検索語はすべて「追加0件」または「<1%」のため、検索感度は維持される
- **特異度向上の可能性**: `absorption[tiab]`のような広すぎる検索語に注意喚起

### 今後の検討事項
1. **#2C absorption[tiab]の改善**: より文脈を限定した検索式を検討
2. **#2H ikigaiの扱い**: 概念的重要性vs実際のヒット件数のバランス
3. **シード論文との検証**: 最適化後もすべてのシード論文が検索されることを確認

---

## 検索戦略の注意点

### 感度と特異度のバランス
- この最適化版も高感度（high sensitivity）を維持
- 重複検索語を削除することで、検索効率を向上
- スクリーニング段階で詳細な適格基準を適用して絞り込む

### やりがいの概念について
- "やりがい"は英語に直訳困難な日本語概念
- プロトコルの参考文献（Nishigori et al. 2024）では、meaningful work, intrinsic motivation, achievement, satisfactionを包含する概念として定義
- 検索式では関連する複数の英語概念を組み合わせて捕捉

### Incentivesの除外
- プロトコルの指示に従い、外発的動機付け（incentives）に関する研究は概念として除外
- ただし、"motivation"は内発的動機も含むため組み入れ、スクリーニングで判断

### 医学生の扱い
- 除外基準に医学生を含めているが、必要に応じて調整可能
- プロトコルでは「臨床医」を対象としているため除外

### Burnoutとの関係
- Burnoutのみに焦点を当てた研究は除外
- ただし、burnoutからの回復や、burnoutとやりがいの関係を論じた研究は含める可能性があるため、完全除外ではなく注意深く除外

## 次のステップ

1. この最適化版でシード論文との検証を実施（`check_final_query.py`）
2. 元の検索式との比較（`check_modified_search.py`）
3. 問題なければ、他データベース（Embase, CINAHL, PsycInfo, ERIC, ICHUSHI）への変換を実施
4. `absorption[tiab]`の文脈限定版を作成してテスト

## 参考文献

Nishigori H, Shimazono Y, Busari J, Dornan T. Exploring yarigai: The meaning of working as a physician in teaching medical professionalism. Med Teach. 2024 Nov;46(11):1486–93.

## Block Overlap Analysis 結果サマリー

詳細は `tests/block_overlap_20251105/` 参照

| Block | Total Hits | Key Findings |
|-------|------------|--------------|
| #1 Population | 1,119,167 | General Practitioners[Mesh]: +0, medical doctor*: +0 |
| #2A MeSH | 374,663 | Vocation[Mesh]: +0, Work Engagement[Mesh]: +0.2% |
| #2B Meaningful | 1,250 | All terms contribute |
| #2C Engagement | 385,952 | absorption: 96.9%, engaged at work: +0 |
| #2D Calling | 35,866 | career calling, vocational calling: +0 |
| #2E Motivation | 211,169 | motivat*: 98.2% dominates |
| #2F Satisfaction | 17,996 | All terms contribute |
| #2G Fulfillment | 9,131 | Balanced contributions |
| #2H Japanese | 112 | yarigai: 2, ikigai: 111 |
| #2I Needs | 157,820 | All terms contribute |
| #2J Task | 215 | All terms contribute |
