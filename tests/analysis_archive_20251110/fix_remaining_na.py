#!/usr/bin/env python3
"""
残りのN/Aを正しい値で置き換え
"""

import re

def fix_remaining_na(input_file, output_file):
    """残りのN/Aを修正"""

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    replacements = [
        # (pattern, replacement, description)
        (
            r'(\|\s*2\s*\|\s*`physician\*\[tiab\]`\s*\|\s*[\d,]+\s*\|\s*)N/?A(\s*\|)',
            r'\1-\2',
        ),
        (
            r'(\|\s*5\s*\|\s*`#1 AND "engaged at work"\[tiab\]`\s*\|\s*[\d,]+\s*\|\s*)N/?A(\s*\|)',
            r'\g<1>0\2',
        ),
        (
            r'(\|\s*5\s*\|\s*`#1 AND "calling orientation"\[tiab\]`\s*\|\s*[\d,]+\s*\|\s*)N/?A(\s*\|)',
            r'\g<1>0\2',
        ),
        (
            r'(\|\s*2\s*\|\s*`#1 AND "iki-gai"\[tiab\]`\s*\|\s*[\d,]+\s*\|\s*)N/?A(\s*\|)',
            r'\g<1>0\2',
        ),
        (
            r'(\|\s*4\s*\|\s*`#1 AND "yari-gai"\[tiab\]`\s*\|\s*[\d,]+\s*\|\s*)N/?A(\s*\|)',
            r'\g<1>0\2',
        ),
        (
            r'(\|\s*3\s*\|\s*`#1 AND "job significance"\[tiab\]`\s*\|\s*[\d,]+\s*\|\s*)N/?A(\s*\|)',
            r'\1-\2',
        ),
    ]

    for pattern, replacement in replacements:
        content, count = re.subn(pattern, replacement, content)
        if count == 0:
            print(f"  ⚠️ 置換に失敗: {pattern}")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    print("=" * 80)
    print("残りのN/Aを修正")
    print("=" * 80)
    print()

    input_file = "tests/yarigai_comprehensive_line_counts_20251110.md"
    output_file = "tests/yarigai_comprehensive_line_counts_20251110.md"

    fix_remaining_na(input_file, output_file)

    print("✓ 完了")
    print()
    print("修正内容:")
    print("  1. physician*[tiab]: N/A → '-' (個別データなし)")
    print("  2. 'engaged at work'[tiab]: N/A → 0 (全期間で0件)")
    print("  3. 'calling orientation'[tiab]: N/A → 0 (全期間で0件)")
    print("  4. 'iki-gai'[tiab]: N/A → 0 (全期間で0件)")
    print("  5. 'yari-gai'[tiab]: N/A → 0 (全期間で0件)")
    print("  6. 'job significance'[tiab]: N/A → '-' (データなし)")
    print()
    print("注記:")
    print("  '-' = 元データに該当する検索語がない（個別に分解されていない）")
    print("  '0' = 全期間で0件のため、5年限定も0件")
    print("=" * 80)

if __name__ == "__main__":
    main()
