# Faculty Development for Physicians - MEDLINE Search Formula

## 研究目的

医師向けFaculty Development（FD）プログラムの目標、内容、提供方法、評価方法が、診療科間でどのように異なるかを明らかにする（スコーピングレビュー）

## PCC要素（スコーピングレビュー）

### Population（対象集団）

- 臨床教育に従事する医師（医学生、研修医、専攻医への教育を行う医師）
- 大学病院、一般病院、外来診療所等の臨床現場で教育活動を行う医師

### Concept（概念）

- Faculty Developmentプログラム
- 以下の少なくとも1つを記述している研究：
  - プログラムの目標
  - 内容（教育手法、評価方法、カリキュラム設計等）
  - 提供方法（ワークショップ、セミナー、縦断的プログラム、メンターシップ等）
  - 評価アプローチ



### Context（文脈）

- すべての診療科
- 臨床教育の場（病院、外来、シミュレーションラボ等）
- 卒前・卒後医学教育

## PubMed/MEDLINE

### 検索式構造（最適化版 v2 - 2025-12-25）

```
#1 "Faculty, Medical"[Majr] OR medical faculty[tiab] OR clinical educator*[tiab] OR clinician educator*[tiab] OR medical educator*[tiab] OR clinical teacher*[tiab] OR clinical teaching[tiab]

#2 "Staff Development"[Mesh] OR "Program Development"[Mesh] OR faculty development*[tiab] OR professional development*[tiab] OR teaching skill*[tiab] OR "program design"[tiab]

#3 #1 AND #2
```

### 最適化履歴

| バージョン | 変更内容 | #3件数 | シード捕捉 |
|------------|----------|--------|-----------|
| v1 (original) | - | ~3,381 | 5/5 |
| **v2 (current)** | `[Mesh]` → `[Majr]` 変更 | **2,832** | **5/5 ✓** |

> **注**: `[Majr]`（Major Topic）は「Faculty, Medical」が論文の主題の場合のみマッチ。副次的にタグ付けされた論文を除外し、精度を向上。

### 診療科ブロック（参考・オプション）

> **注意**: 下記の診療科ブロックを追加すると、シード論文の一部（35173512, 38442199）が捕捉できなくなります。これらの論文は「Faculty, Medical」MeSHを持つが診療科MeSHを持たないFD総論的論文のため。診療科による分析が必要な場合は、検索後のサブグループ分析で使用してください。

```
(optional) Physicians[mh] OR "Internal Medicine/education"[MAJR] OR internist*[tiab] OR "internal medicine"[tiab] OR physician*[tiab] OR Pediatricians[mh] OR "Pediatrics/education"[MAJR] OR pediatric*[tiab] OR paediatric*[tiab] OR Dermatologists[mh] OR "Dermatology/education"[MAJR] OR dermatolog*[tiab] OR Psychiatrists[mh] OR "Psychiatry/education"[MAJR] OR psychiat*[tiab] OR Surgeons[mh] OR "General Surgery/education"[MAJR] OR surgeon*[tiab] OR "Orthopedic Surgeons"[mh] OR "Orthopedics/education"[MAJR] OR Orthopedic*[tiab] OR Gynecologists[mh] OR Obstetricians[mh] OR "Obstetrics/education"[MAJR] OR "Gynecology/education"[MAJR] OR gynecolog*[tiab] OR obstetrician*[tiab] OR Ophthalmologists[mh] OR "Ophthalmology/education"[MAJR] OR ophthalmolog*[tiab] OR Otolaryngologists[mh] OR "Otolaryngology/education"[MAJR] OR otolaryngolog*[tiab] OR Urologists[mh] OR "Urology/education"[MAJR] OR urolog*[tiab] OR Neurosurgeons[mh] OR "Neurosurgery/education"[MAJR] OR neurosurgeon*[tiab] OR Radiologists[mh] OR "Radiology/education"[MAJR] OR radiolog*[tiab] OR Anesthesiologists[mh] OR "Anesthesiology/education"[MAJR] OR anesthesiolog*[tiab] OR anaesthesiolog*[tiab] OR anesthetist*[tiab] OR Pathologists[mh] OR "Pathology/education"[MAJR] OR patholog*[tiab] OR "Clinical Laboratory Techniques/education"[MAJR] OR "clinical laboratory*"[tiab] OR "medical technolog*"[tiab] OR "laboratory medicine"[tiab] OR "Emergency Medicine/education"[MAJR] OR "emergency physician*"[tiab] OR "emergency medicine"[tiab] OR "ER doctor*"[tiab] OR "Surgery, Plastic/education"[MAJR] OR "plastic surgeon*"[tiab] OR "reconstructive surgeon*"[tiab] OR "cosmetic surgeon*"[tiab] OR Physiatrists[mh] OR "Physical and Rehabilitation Medicine/education"[MAJR] OR physiatrist*[tiab] OR "rehabilitation physician*"[tiab] OR "General Practitioners"[mh] OR "Family Practice/education"[MAJR] OR "Primary Health Care/education"[MAJR] OR "general practitioner*"[tiab] OR "family physician*"[tiab] OR "primary care physician*"[tiab]
```

## シード論文（必須捕捉対象）

以下の5件のPMIDはすべて検索式で捕捉される必要がある：

1. PMID: 35173512 - Nair et al. 2022 (FDプログラムの影響測定)
2. PMID: 19811202 - Johansson et al. 2009 (Stanford FDプログラムの汎用性)
3. PMID: 21821215 - Peyre et al. 2011 (外科医向けFDプログラム - 専門科特異的)
4. PMID: 38442199 - Mahan et al. 2024 (Clinician Educator Milestones)
5. PMID: 21869655 - Srinivasan et al. 2011 (Teaching as a Competency)

## 検索実行手順

1. 各ブロックの妥当性検証:

   ```bash
   python scripts/search/term_validator/check_search_lines.py --input-formula search_formula/fd_review/search_formula.md --output search_formula/fd_review/search_lines_results.md
   ```
2. シード論文からMeSH用語抽出:

   ```bash
   python scripts/search/extract_mesh.py --pmid-file search_formula/fd_review/seed_pmids.txt --output-dir search_formula/fd_review/
   ```
3. 最終クエリ実行とシード論文検証:

   ```bash
   python scripts/search/query_executor/check_final_query.py --formula-file search_formula/fd_review/search_formula.md --pmid-file search_formula/fd_review/seed_pmids.txt --output-dir search_formula/fd_review/
   ```

## 注記

- **言語制限なし**: 英語抄録があれば非英語論文も含める
- **年代制限なし**: すべての年代を対象
- **研究デザイン制限なし**: スコーピングレビューのため、すべての研究デザインを含む
- **高感度優先**: 網羅性を重視し、特異度は二次スクリーニングで調整
- **専門科用語**: 最初は含めず、必要に応じて後で追加検討

## 調整予定事項

- [ ] MeSH用語の階層確認と最適化
- [ ] テキストワードのバリエーション追加
- [ ] 各ブロックのヒット件数確認
- [ ] シード論文100%捕捉の確認
- [ ] 必要に応じてブロック構造の再編成
