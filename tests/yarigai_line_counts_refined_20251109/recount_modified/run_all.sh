#!/bin/bash
# 修正版検索式の各ブロック分析スクリプト

BASE_DIR="tests/yarigai_line_counts_refined_20251109/recount_modified"

echo "=========================================="
echo "修正版検索式ブロック分析開始"
echo "=========================================="

# 2A MeSH
echo ""
echo "[1/9] Analyzing #2A MeSH Terms (modified)..."
python3 scripts/search/term_validator/check_block_overlap.py \
  -i ${BASE_DIR}/block_2a_mesh.txt \
  -o ${BASE_DIR}/analysis_2a_mesh.md \
  --block-name "#2A MeSH Terms"
sleep 5

# 2B Meaningful Work
echo ""
echo "[2/9] Analyzing #2B Meaningful Work..."
python3 scripts/search/term_validator/check_block_overlap.py \
  -i ${BASE_DIR}/block_2b_meaningful.txt \
  -o ${BASE_DIR}/analysis_2b_meaningful.md \
  --block-name "#2B Meaningful Work"
sleep 5

# 2C Work Engagement
echo ""
echo "[3/9] Analyzing #2C Work Engagement..."
python3 scripts/search/term_validator/check_block_overlap.py \
  -i ${BASE_DIR}/block_2c_engagement.txt \
  -o ${BASE_DIR}/analysis_2c_engagement.md \
  --block-name "#2C Work Engagement"
sleep 5

# 2D Calling/Vocation
echo ""
echo "[4/9] Analyzing #2D Calling/Vocation..."
python3 scripts/search/term_validator/check_block_overlap.py \
  -i ${BASE_DIR}/block_2d_calling.txt \
  -o ${BASE_DIR}/analysis_2d_calling.md \
  --block-name "#2D Calling/Vocation"
sleep 5

# 2E Motivation
echo ""
echo "[5/9] Analyzing #2E Motivation..."
python3 scripts/search/term_validator/check_block_overlap.py \
  -i ${BASE_DIR}/block_2e_motivation.txt \
  -o ${BASE_DIR}/analysis_2e_motivation.md \
  --block-name "#2E Motivation"
sleep 5

# 2F Satisfaction
echo ""
echo "[6/9] Analyzing #2F Satisfaction..."
python3 scripts/search/term_validator/check_block_overlap.py \
  -i ${BASE_DIR}/block_2f_satisfaction.txt \
  -o ${BASE_DIR}/analysis_2f_satisfaction.md \
  --block-name "#2F Satisfaction"
sleep 5

# 2G Fulfillment
echo ""
echo "[7/9] Analyzing #2G Fulfillment..."
python3 scripts/search/term_validator/check_block_overlap.py \
  -i ${BASE_DIR}/block_2g_fulfillment.txt \
  -o ${BASE_DIR}/analysis_2g_fulfillment.md \
  --block-name "#2G Fulfillment"
sleep 5

# 2H Japanese
echo ""
echo "[8/9] Analyzing #2H Japanese Concepts..."
python3 scripts/search/term_validator/check_block_overlap.py \
  -i ${BASE_DIR}/block_2h_japanese.txt \
  -o ${BASE_DIR}/analysis_2h_japanese.md \
  --block-name "#2H Japanese Concepts"
sleep 5

# 2I Psychological Needs
echo ""
echo "[9/9] Analyzing #2I Psychological Needs..."
python3 scripts/search/term_validator/check_block_overlap.py \
  -i ${BASE_DIR}/block_2i_needs.txt \
  -o ${BASE_DIR}/analysis_2i_needs.md \
  --block-name "#2I Psychological Needs"
sleep 5

# 2J Task Significance
echo ""
echo "[10/9] Analyzing #2J Task Significance..."
python3 scripts/search/term_validator/check_block_overlap.py \
  -i ${BASE_DIR}/block_2j_task.txt \
  -o ${BASE_DIR}/analysis_2j_task.md \
  --block-name "#2J Task Significance"

echo ""
echo "=========================================="
echo "全ブロック分析完了"
echo "=========================================="
