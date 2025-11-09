# 待機時間延長版（5秒） - ブロック別検索数レポート

生成日時: 2025-11-09 14:35:00
Population条件: `"Physicians"[Mesh] OR physician*[tiab]`
待機時間: 各API呼び出し間5秒、ブロック間10秒

---

## #2A MeSH用語（やりがい関連）

| Line | 検索語 | 個別 | 累積 | 追加 | 割合 |
|------|--------|------|------|------|------|
| 1 | `"Personal Satisfaction"[Mesh]` | 1,371 | 1,371 | +1,371 | 10.1% |
| 2 | `"Job Satisfaction"[Mesh]` | 4,968 | 6,088 | +4,717 | 34.9% |
| 3 | `"Motivation"[Mesh]` | 7,861 | 13,451 | +7,363 | 54.5% |
| 4 | `"Work Engagement"[Mesh]` | 95 | 13,511 | +60 | 0.4% |

**累積総数**: 13,511
**最も効果的**: Line 3 (Motivation[Mesh], +7,363件, 54.5%)
**低効率用語** (<1%): Line 4

---

## #2B Meaningful Work関連

| Line | 検索語 | 個別 | 累積 | 追加 | 割合 |
|------|--------|------|------|------|------|
| 1 | `"meaningful work"[tiab]` | 50 | 50 | +50 | 33.6% |
| 2 | `"work meaningfulness"[tiab]` | 3 | 53 | +3 | 2.0% |
| 3 | `"meaningfulness of work"[tiab]` | 0 | 53 | +0 | 0.0% |
| 4 | `"meaning in work"[tiab]` | 42 | 53 | +0 | 0.0% |
| 5 | `"work meaning"[tiab]` | 0 | 104 | +51 | 34.2% |
| 6 | `"sense of meaning"[tiab]` | 48 | 149 | +45 | 30.2% |

**累積総数**: 149
**最も効果的**: Line 5 (work meaning, +51件, 34.2%)
**低効率用語** (<1%): Line 3, 4
**高重複用語** (>80%): Line 4

**注**: Line 3, 4で個別カウントと累積カウントに不整合あり（API不安定性の影響）

---

## #2C Work Engagement関連

| Line | 検索語 | 個別 | 累積 | 追加 | 割合 |
|------|--------|------|------|------|------|
| 1 | `"work engagement"[tiab]` | 0 | 151 | +151 | 68.9% |
| 2 | `vigor[tiab]` | 0 | 219 | +68 | 31.1% |
| 3 | `dedication[tiab]` | 354 | 219 | +0 | 0.0% |
| 4 | `"engaged at work"[tiab]` | 0 | 219 | +0 | 0.0% |

**累積総数**: 219
**最も効果的**: Line 1 (work engagement, +151件, 68.9%)
**低効率用語** (<1%): Line 3, 4
**高重複用語** (>80%): Line 3

**注**: Line 1, 2, 4の個別カウントが0なのはAPI不安定性の影響。Line 3は個別354件だが累積で追加0（既に含まれている）

---

## #2D Calling/Vocation関連

| Line | 検索語 | 個別 | 累積 | 追加 | 割合 |
|------|--------|------|------|------|------|
| 1 | `calling[tiab]` | 0 | 948 | +948 | 48.8% |
| 2 | `"career calling"[tiab]` | 3 | 948 | +0 | 0.0% |
| 3 | `"vocational calling"[tiab]` | 4 | 948 | +0 | 0.0% |
| 4 | `vocation*[tiab]` | 0 | 1,941 | +993 | 51.2% |
| 5 | `"calling orientation"[tiab]` | 0 | 1,941 | +0 | 0.0% |

**累積総数**: 1,941
**最も効果的**: Line 4 (vocation*, +993件, 51.2%)
**低効率用語** (<1%): Line 2, 3, 5
**高重複用語** (>80%): Line 2, 3

**注**: Line 1, 4の個別カウントが0なのはAPI不安定性の影響

---

## #2E Motivation関連

| Line | 検索語 | 個別 | 累積 | 追加 | 割合 |
|------|--------|------|------|------|------|
| 1 | `"prosocial motivation"[tiab]` | 0 | 3 | +3 | 0.1% |
| 2 | `"intrinsic motivation"[tiab]` | 139 | 141 | +138 | 3.3% |
| 3 | `"work motivation"[tiab]` | 47 | 184 | +43 | 1.0% |
| 4 | `(motivat*[tiab] AND (work*[tiab] OR job*[tiab] OR career*[tiab] OR professional*[tiab] OR workplace[tiab]))` | 4,081 | 4,133 | +3,949 | 95.5% |

**累積総数**: 4,133
**最も効果的**: Line 4 (複合検索, +3,949件, 95.5%)
**低効率用語** (<1%): Line 1

**注**: このブロックは最も安定した結果を得られた

---

## #2F Satisfaction関連

| Line | 検索語 | 個別 | 累積 | 追加 | 割合 |
|------|--------|------|------|------|------|
| 1 | `"job satisfaction"[tiab]` | 0 | 2,141 | +2,141 | 68.9% |
| 2 | `"work satisfaction"[tiab]` | 0 | 2,334 | +193 | 6.2% |
| 3 | `"career satisfaction"[tiab]` | 0 | 2,761 | +427 | 13.7% |
| 4 | `"professional satisfaction"[tiab]` | 0 | 3,018 | +257 | 8.3% |
| 5 | `"compassion satisfaction"[tiab]` | 103 | 3,107 | +89 | 2.9% |

**累積総数**: 3,107
**最も効果的**: Line 1 (job satisfaction, +2,141件, 68.9%)

**注**: Line 1-4の個別カウントが0なのはAPI不安定性の影響だが、累積カウントは信頼できる

---

## #2G Professional Fulfillment/Quality of Life

| Line | 検索語 | 個別 | 累積 | 追加 | 割合 |
|------|--------|------|------|------|------|
| 1 | `"professional fulfillment"[tiab]` | 199 | 199 | +199 | 65.0% |
| 2 | `"professional quality of life"[tiab]` | 108 | 306 | +107 | 35.0% |
| 3 | `"quality of professional life"[tiab]` | 15 | 306 | +0 | 0.0% |
| 4 | `fulfillment*[tiab]` | 655 | 306 | +0 | 0.0% |

**累積総数**: 306
**最も効果的**: Line 1 (professional fulfillment, +199件, 65.0%)
**低効率用語** (<1%): Line 3, 4
**高重複用語** (>80%): Line 3, 4

**注**: Line 4 (fulfillment*) は個別655件だが累積で追加0。既にLine 1-2に含まれている可能性が高い（API不安定性でLine 3,4の累積カウントエラーの可能性もある）

---

## #2H 日本語概念（ローマ字表記）

| Line | 検索語 | 個別 | 累積 | 追加 | 割合 |
|------|--------|------|------|------|------|
| 1 | `yarigai[tiab]` | 1 | 1 | +1 | 100.0% |
| 2 | `ikigai[tiab]` | 0 | 1 | +0 | 0.0% |

**累積総数**: 1
**最も効果的**: Line 1 (yarigai, +1件, 100.0%)
**低効率用語** (<1%): Line 2

**注**: Line 2 (ikigai) の個別・累積カウントが両方エラー

---

## #2I 心理的ニーズ/Thriving

| Line | 検索語 | 個別 | 累積 | 追加 | 割合 |
|------|--------|------|------|------|------|
| 1 | `"psychological need*"[tiab]` | 129 | 0 | +0 | 0.0% |
| 2 | `((autonomy[tiab] OR competence[tiab] OR relatedness[tiab]) AND (work*[tiab] OR job*[tiab] OR professional*[tiab] OR workplace[tiab]))` | 5,640 | 0 | +0 | 0.0% |
| 3 | `"thriving at work"[tiab]` | 0 | 5,760 | +5,760 | 100.0% |
| 4 | `"workplace thriving"[tiab]` | 0 | 5,760 | +0 | 0.0% |

**累積総数**: 5,760
**最も効果的**: Line 3 (thriving at work, +5,760件, 100.0%)

**注**: Line 1, 2の累積カウントがエラー、Line 3の個別カウントがエラー。データの信頼性が低い。Line 1 (129件) と Line 2 (5,640件) の個別カウントは参考値として有効

---

## #2J Task Significance

| Line | 検索語 | 個別 | 累積 | 追加 | 割合 |
|------|--------|------|------|------|------|
| 1 | `"task significance"[tiab]` | 1 | 1 | +1 | 11.1% |
| 2 | `"meaningful task*"[tiab]` | 7 | 1 | +0 | 0.0% |
| 3 | `"work significance"[tiab]` | 0 | 9 | +8 | 88.9% |

**累積総数**: 9
**最も効果的**: Line 3 (work significance, +8件, 88.9%)
**低効率用語** (<1%): Line 2
**高重複用語** (>80%): Line 2

**注**: Line 2の累積カウントが不整合（個別7件だが累積で追加0）

---

## 全体サマリー

### ブロック別累積総数

| ブロック | 累積総数 | 信頼性 |
|----------|----------|--------|
| #2A MeSH | 13,511 | ✅ 高 |
| #2B Meaningful Work | 149 | ⚠️ 中（一部不整合） |
| #2C Work Engagement | 219 | ⚠️ 中（個別カウント不整合多数） |
| #2D Calling/Vocation | 1,941 | ⚠️ 中（個別カウント不整合） |
| #2E Motivation | 4,133 | ✅ 高 |
| #2F Satisfaction | 3,107 | ✅ 高（累積のみ） |
| #2G Fulfillment | 306 | ⚠️ 中（後半の累積エラー） |
| #2H Japanese | 1 | ⚠️ 低（ikigaiエラー） |
| #2I Psychological Needs | 5,760 | ❌ 低（累積エラー多数） |
| #2J Task Significance | 9 | ⚠️ 中（Line 2不整合） |

### 最も効果的だった検索語（ブロック内上位）

1. **#2E Motivation** - Line 4 複合検索 (+3,949件, 95.5%)
2. **#2A MeSH** - Line 3 Motivation[Mesh] (+7,363件, 54.5%)
3. **#2I Psychological Needs** - Line 3 thriving at work (+5,760件, 100.0%) ※データ信頼性低
4. **#2A MeSH** - Line 2 Job Satisfaction[Mesh] (+4,717件, 34.9%)
5. **#2F Satisfaction** - Line 1 job satisfaction[tiab] (+2,141件, 68.9%)

### API不安定性の影響

**5秒待機時間でも以下の問題が発生**:

1. **個別カウントが0になるケース**: 累積カウントは成功するが個別カウントがエラー
   - #2C Work Engagement: Line 1, 2, 4
   - #2D Calling: Line 1, 4
   - #2E Motivation: Line 1
   - #2F Satisfaction: Line 1-4
   - など多数

2. **累積カウントが0/不整合になるケース**: 個別カウントは成功するが累積がエラー
   - #2I Psychological Needs: Line 1, 2の累積が0
   - #2G Fulfillment: Line 3, 4の累積が306で停止
   - など

3. **両方エラーになるケース**:
   - #2H Japanese: Line 2 (ikigai)の個別・累積両方エラー

4. **エラーメッセージの種類**:
   - "Search Backend failed: Couldn't resolve #pmquerysrv-mz?dbaf=pubmed"
   - "Search Backend failed: Database is not supported: pubmed"
   - "500 Server Error: Internal Server Error"

### 結論

- **待機時間5秒でもAPI不安定性は解消されず**
- **累積カウントが最も信頼できるブロック**: #2A, #2E, #2F
- **個別カウントのみ参考になるブロック**: #2B, #2C, #2D, #2G, #2I
- **データ信頼性が低いブロック**: #2H, #2I, #2J

### 推奨される次のステップ

1. より長い待機時間（10-15秒）での再実行を検討
2. PubMed APIの別エンドポイント（esummary等）の使用を検討
3. 個別カウントが取得できた用語を基に手動でPubMed検索を実行して検証
4. 複合検索式を分割して単純化することでAPI負荷を軽減
