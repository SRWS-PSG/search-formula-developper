# 検索戦略の詳細説明

## 概要

このドキュメントでは、「日本の医師における『やりがい』スコーピングレビュー」のための検索戦略について詳細に説明します。

## 検索戦略の設計原則

### 1. 高感度（High Sensitivity）アプローチ
- スコーピングレビューの目的に沿い、関連する可能性のある文献を広く捕捉
- 偽陽性（無関係な文献）を多く含むことを許容し、スクリーニングで絞り込む
- 偽陰性（見落とし）を最小化することを優先

### 2. 概念の包括性
- 「やりがい」という日本語概念は英語に直訳困難
- 複数の関連概念（meaningful work, work engagement, calling, job satisfaction等）を組み合わせて捕捉
- Nishigori et al. (2024)の定義を参考に、内在的動機、達成感、満足感を含む広範な概念として捉える

### 3. PCCフレームワークの適用
- **P**opulation: 医師（広義：physician, doctor, clinician等）
- **C**oncept: やりがい関連概念（10のサブカテゴリー）
- **C**ontext: 臨床現場（日本/世界）

## 検索ブロックの構造

### #1 Population（医師）

#### MeSH用語
- `"Physicians"[Mesh]`: 医師全般を指すMeSH用語（自動展開により下位概念も含む）
- `"General Practitioners"[Mesh]`: 一般診療医・家庭医を含む

#### フリーテキスト
- `physician*`, `doctor*`: 基本的な職種名（ワイルドカードで複数形等も捕捉）
- `"general practitioner*"`: フレーズ検索で一般診療医を捕捉
- `clinician*`: 臨床医全般を指す広義の用語
- `"medical professional*"`, `"health care professional*"`, `"healthcare professional*"`: より広い範囲の医療専門職（主に医師を指す文脈で使用されることを想定）
- `"medical staff"`, `"hospital staff"`: 病院職員（医師を含む集団）

**設計意図**:
- 医師を指す様々な表現を捕捉
- 専門医、一般医、研修医等を広く含む
- 医学生は除外基準で別途除外

### #2 Concept（やりがい関連概念）

やりがいの概念を10のサブカテゴリーに分類し、それぞれ独立した検索ブロックとして構築。

#### #2A: MeSH用語
**含まれる用語**:
- `"Personal Satisfaction"[Mesh]`: 個人的満足
- `"Job Satisfaction"[Mesh]`: 仕事の満足度
- `"Motivation"[Mesh]`: 動機付け
- `"Work Engagement"[Mesh]`: ワークエンゲージメント（MeSHに存在する場合）
- `"Professional Role"[Mesh]`: 専門職としての役割
- `"Professional Autonomy"[Mesh]`: 専門職の自律性
- `"Career Choice"[Mesh]`: キャリア選択
- `"Vocation"[Mesh]`: 天職・職業的召命

**設計意図**:
- 統制語彙（MeSH）を活用し、インデクシングされた文献を効率的に捕捉
- MeSHツリーの自動展開により、下位概念も含む

#### #2B: Meaningful Work（有意義な仕事）
**含まれる用語**:
- `"meaningful work"`: 最も直接的な表現
- `"work meaningfulness"`: 仕事の有意義性
- `"meaningfulness of work"`: 仕事の意味深さ
- `"meaning in work"`: 仕事における意味
- `"work meaning"`: 仕事の意味
- `"sense of meaning"`: 意味の感覚

**設計意図**:
- Work and Meaning Inventory (WAMI)で測定される概念
- Steger et al. (2012)の定義に基づく
- 「やりがい」の中核的要素の一つ

#### #2C: Work Engagement（ワークエンゲージメント）
**含まれる用語**:
- `"work engagement"`: ワークエンゲージメント全般
- `vigor`: 活力（UWESの第1因子）
- `dedication`: 献身（UWES の第2因子）
- `absorption`: 没頭（UWESの第3因子）
- `"engaged at work"`: 仕事への没入状態

**設計意図**:
- Utrecht Work Engagement Scale (UWES)で測定される概念
- Schaufeliの定義に基づく3つの下位概念を含む
- ポジティブな仕事への心理状態を捕捉

**注意点**:
- `vigor`, `dedication`, `absorption`は単独では多義的な語（例：vigorは活力だけでなく力強さ等）
- しかし、医師とやりがいの文脈ではwork engagementを指すことが多いため採用
- 検証段階でノイズが多い場合は、フレーズ検索に限定することを検討

#### #2D: Calling/Vocation（天職・召命）
**含まれる用語**:
- `calling`: 天職、召命
- `"career calling"`: キャリアとしての天職
- `"vocational calling"`: 職業的召命
- `vocation*`: 職業、天職（ワイルドカードで派生語を含む）
- `"calling orientation"`: 天職志向

**設計意図**:
- Calling and Vocation Questionnaire (CVQ)で測定される概念
- Dik & Duffy (2009)の定義：超越的な召命、意味/目的の表現、向社会的志向
- 医師が職業を「天職」として捉える側面を捕捉

#### #2E: Motivation（動機付け）
**含まれる用語**:
- `"prosocial motivation"`: 向社会的動機
- `"intrinsic motivation"`: 内発的動機
- `"work motivation"`: 仕事の動機付け
- `motivat*`: 動機付け全般（ワイルドカード）

**設計意図**:
- 自己決定理論（SDT）における内発的動機を中心に捕捉
- `motivat*`は広義だが、やりがいの重要な要素
- 外発的動機（incentives, rewards）は除外基準で別途扱う

**注意点**:
- `motivat*`は非常に広範囲をカバーし、外発的動機も含む可能性
- スクリーニング段階で、内発的動機に焦点を当てた研究を選別

#### #2F: Satisfaction（満足感）
**含まれる用語**:
- `"job satisfaction"`: 仕事の満足度（最も一般的）
- `"work satisfaction"`: 仕事満足
- `"career satisfaction"`: キャリア満足
- `"professional satisfaction"`: 専門職としての満足
- `"compassion satisfaction"`: 共感満足（ProQOLの下位尺度）

**設計意図**:
- Job satisfactionは「やりがい」と密接に関連する概念
- ProQOL (Professional Quality of Life)のポジティブ側面を捕捉
- 医師の仕事に対する肯定的感情を広く含む

#### #2G: Professional Fulfillment（専門職としての充足感）
**含まれる用語**:
- `"professional fulfillment"`: 専門職としての充足
- `"professional quality of life"`: 専門職のQOL
- `"quality of professional life"`: 専門職生活の質
- `fulfillment`, `fulfilment`: 充足感（米英スペリング両方）

**設計意図**:
- Professional Fulfillment Index (PFI)で測定される概念
- Trockel et al. (2017)により開発
- Burnoutの対極にある肯定的状態を捕捉

#### #2H: 日本語概念（ローマ字表記）
**含まれる用語**:
- `yarigai`: やりがい（ローマ字表記）
- `ikigai`: 生きがい（関連概念）

**設計意図**:
- 日本文化特有の概念が英語論文で言及される場合を捕捉
- Nishigori et al. (2024)のような、日本語概念を扱った論文を確実に拾う
- 国際誌でもローマ字表記で使用されることがある

#### #2I: 心理的ニーズ/Thriving（心理的ニーズと繁栄）
**含まれる用語**:
- `"psychological need*"`: 心理的ニーズ
- `autonomy`: 自律性（SDTの基本的心理欲求）
- `competence`: 有能感（SDTの基本的心理欲求）
- `relatedness`: 関係性（SDTの基本的心理欲求）
- `"thriving at work"`: 職場での繁栄
- `thriving`: 繁栄、成長

**設計意図**:
- 自己決定理論（SDT）の基本的心理欲求を捕捉
- Basic Psychological Need Satisfaction at Work Scale (BPNSWS)に対応
- Thriving at Work Scale（Spreitzer et al. 2005）の概念を含む
- やりがいを支える根本的な心理的要因を捕捉

**注意点**:
- `autonomy`, `competence`, `relatedness`は多義的（医学用語としても使用）
- `#1 AND #2`の組み合わせにより、医師のやりがい文脈に限定
- ノイズが多い場合は、より特異的なフレーズに限定することを検討

#### #2J: Task Significance（仕事の重要性）
**含まれる用語**:
- `"task significance"`: タスクの重要性
- `"meaningful task*"`: 有意義なタスク
- `"work significance"`: 仕事の重要性

**設計意図**:
- Job Diagnostic Survey (JDS)の5つのコア職務特性の一つ
- Hackman & Oldham (1976)のJob Characteristics Model
- 「自分の仕事が他者に影響を与えている」という認識を捕捉

### #3: 測定尺度（オプション）

**含まれる尺度**:
- Work and Meaning Inventory (WAMI)
- Calling and Vocation Questionnaire (CVQ)
- Professional Fulfillment Index (PFI)
- Utrecht Work Engagement Scale (UWES)
- Basic Psychological Need Satisfaction at Work Scale (BPNSWS)
- Thriving at Work Scale
- Job Diagnostic Survey (JDS)
- Professional Quality of Life (ProQOL)

**設計意図**:
- 尺度名で検索することで、やりがいを測定した量的研究を効率的に捕捉
- 略語も含めることで、Methods sectionでの言及を拾う
- より特異的な検索が必要な場合に使用

### #4: 日本関連（RQ1専用）

**含まれる用語**:
- `Japan[Mesh:noexp]`: 日本（MeSH、展開なし）
- `Japan[tiab]`: 日本（タイトル・抄録）
- `Japanese[tiab]`: 日本の、日本人
- `Nippon[tiab]`: 日本（別表記）
- `Nihon[tiab]`: 日本（別表記）

**設計意図**:
- RQ1（日本の医師）に特化した検索
- MeSH地理タグと自由テキストの組み合わせで高い捕捉率を実現
- `[Mesh:noexp]`で地理的範囲を日本に限定（下位地域への展開を防ぐ）

## 最終検索式の構成

### RQ1: 日本の医師におけるやりがい
```
#1 AND #2 AND #4
```

**想定される結果**:
- 日本で実施された研究
- 日本人医師を対象とした研究
- 日本の医療システム文脈での研究

**推定ヒット数**: 2,000-5,000件

### RQ2: 世界の医師におけるやりがい
```
#1 AND #2
NOT (animals[mh] NOT humans[mh])
```

**想定される結果**:
- 世界中の医師を対象とした研究（日本含む）
- より広範な国際比較の基盤

**動物実験の除外**:
- `animals[mh] NOT humans[mh]`: 動物のみの研究を除外
- 人間を対象とした研究は保持

**推定ヒット数**: 15,000-30,000件

## 除外戦略

### 医学生の除外
```
NOT (
  "Medical Students"[Mesh] OR
  "Students, Medical"[Mesh] OR
  "medical student*"[tiab]
)
```

**理由**:
- プロトコルでは「臨床医」を対象
- 医学生は医師ではないため除外
- ただし、研修医は医師免許保有者として含む

### Burnoutの扱い
```
NOT (
  "Burnout, Professional"[Mesh:noexp] OR
  (burnout[tiab] NOT (recovery[tiab] OR resilience[tiab] OR "positive"[tiab]))
)
```

**理由**:
- Burnoutのみに焦点を当てた研究は「やりがい」の対極であり除外
- ただし、burnoutとやりがいの関係、burnoutからの回復を論じた研究は含める
- `recovery`, `resilience`, `positive`と共起する場合は保持

**注意**:
- この除外基準は慎重に適用すべき
- 初回検索では除外せず、スクリーニング段階で判断することも検討

## 検索戦略の妥当性検証

### シード論文による検証
1. Nishigori et al. (2024): Exploring yarigai - 主要シード論文
2. その他のシード論文（5-10本）を特定
3. 検索式で全てのシード論文が捕捉されることを確認

### 検証手順
1. `check_search_lines.py`で各検索ブロックのヒット数を確認
2. `extract_mesh.py`でシード論文のMeSH用語を分析
3. 検索式に不足しているMeSH用語やキーワードを特定
4. `check_final_query.py`で最終検索を実行し、シード論文の包含を確認
5. 必要に応じて検索式を調整

## 他データベースへの適応

### 予定データベース
1. **Embase**: 欧州中心、薬学文献が豊富
2. **APA PsycInfo**: 心理学文献、尺度開発研究が多い
3. **ERIC**: 教育文献、医学教育関連
4. **CINAHL**: 看護・医療専門職文献
5. **医中誌（ICHUSHI）**: 日本語医学文献

### 適応のポイント
- **Embase**: Emtree用語への変換（Dialog形式）
- **PsycInfo**: PsycINFO Thesaurusへの変換
- **ERIC**: ERIC Descriptorsへの変換
- **CINAHL**: CINAHL Headingsへの変換
- **医中誌**: 日本語キーワード（シソーラス）への変換

## 想定される課題と対応

### 課題1: ヒット数が多すぎる
**対応策**:
- 測定尺度（#3）を追加して特異度を上げる
- より特異的なフレーズ検索に限定
- 出版年制限を追加（例：過去20年）
- 研究デザインで絞り込み（質的研究、横断研究等）

### 課題2: シード論文が捕捉されない
**対応策**:
- 該当論文のMeSH用語とキーワードを分析
- 不足している用語を検索式に追加
- 同義語を追加
- フィールドタグを調整（[tiab]から[tw]へ等）

### 課題3: ノイズが多い（無関係な文献が多い）
**対応策**:
- スクリーニング段階で対応（スコーピングレビューでは想定内）
- より特異的な用語の組み合わせを検討
- 除外基準を強化

### 課題4: 言語の壁
**対応策**:
- 英語・日本語以外の重要文献は、必要に応じて翻訳を検討
- 多言語対応データベース（Embase, PsycInfo）を活用

## まとめ

この検索戦略は：
- PCCフレームワークに基づく体系的構造
- 高感度アプローチで広範囲をカバー
- 複数の関連概念を組み合わせて「やりがい」を捕捉
- 妥当性検証とフィードバックループを含む
- 他データベースへの適応可能性を考慮

検索式の実行と検証を経て、必要に応じて調整を行います。
