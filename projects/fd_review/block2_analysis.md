# PubMed検索式 #2ブロック分析レポート

生成日時: 2025-12-25 13:38:34

## 現在の#2ブロック（Intervention）

```
"Staff Development"[Mesh] OR "Program Development"[Mesh] OR
faculty development*[tiab] OR professional development*[tiab] OR
teaching skill*[tiab] OR "program design"[tiab]
```

## 完全な#3（#1 AND #2）の件数

**3,381 hits**

---

## 各要素の分析

| 要素 | 単独件数 | #1 AND 要素 | 削除時#3 | 削減量 | 削減率 |
|------|----------|-------------|----------|--------|--------|
| #2a "Staff Development"[Mesh] | 10,256 | 890 | 3,173 | 208 | 6.2% |
| #2b "Program Development"[Mesh] | 30,892 | 638 | 3,048 | 333 | 9.8% |
| #2c faculty development*[tiab] | 4,758 | 1,921 | 2,346 | 1,035 | 30.6% |
| #2d professional development*[tiab] | 18,361 | 771 | 2,886 | 495 | 14.6% |
| #2e teaching skill*[tiab] | 1,536 | 489 | 3,125 | 256 | 7.6% |
| #2f "program design"[tiab] | 2,665 | 28 | 3,369 | 12 | 0.4% |

---

## シード論文マッチング

各シード論文がどの#2要素にマッチするか:

| PMID | #2a | #2b | #2c | #2d | #2e | #2f |
|------|------|------|------|------|------|------|
| 35173512 | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ |
| 19811202 | ✓ | ✗ | ✓ | ✗ | ✓ | ✗ |
| 21821215 | ✗ | ✗ | ✓ | ✓ | ✓ | ✗ |
| 38442199 | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ |
| 21869655 | ✗ | ✗ | ✓ | ✗ | ✗ | ✓ |

### 要素別マッチ数

| 要素 | マッチ数 | 必須性 |
|------|----------|--------|
| #2a "Staff Development"[Mesh] | 1/5 | ⚠️ 要検討 |
| #2b "Program Development"[Mesh] | 0/5 | ❌ 削除可能 |
| #2c faculty development*[tiab] | 5/5 | ✅ 必須 |
| #2d professional development*[tiab] | 1/5 | ⚠️ 要検討 |
| #2e teaching skill*[tiab] | 2/5 | ⚠️ 要検討 |
| #2f "program design"[tiab] | 1/5 | ⚠️ 要検討 |

---

## 削除候補の推奨

### 削除可能な要素（シード論文にマッチしない）

- **#2b "Program Development"[Mesh]**: 削除で 333件削減可能 (9.8%)

---

## 次のステップ

1. 削除可能な要素を確認し、削除版#2で再テスト
2. シード論文を個別に確認し、削除要素が本当に不要か確認
3. 修正版#3で最終件数確認
