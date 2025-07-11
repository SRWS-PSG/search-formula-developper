import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import os
import re

def convert_md_to_pdf(md_file_path, pdf_file_path):
    """
    MarkdownファイルをPDFに変換する（テーブル表示改善版）
    
    Args:
        md_file_path: 入力Markdownファイルのパス
        pdf_file_path: 出力PDFファイルのパス
    """
    
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    html_content = markdown.markdown(
        md_content, 
        extensions=['tables', 'codehilite', 'fenced_code', 'attr_list']
    )
    
    html_content = re.sub(r'<td>\s*</td>', r'<td class="empty-cell">-</td>', html_content)
    
    html_content = re.sub(r'<td>(\d{1,3}(?:,\d{3})*)</td>', r'<td class="number-cell">\1</td>', html_content)
    
    html_content = re.sub(r'<code>([^<]{50,})</code>', r'<code class="long-code">\1</code>', html_content)
    
    css_style = """
    @page {
        size: A4 landscape;
        margin: 1.2cm;
    }
    
    body {
        font-family: "DejaVu Sans", "Noto Sans CJK JP", "Hiragino Sans", "Yu Gothic", sans-serif;
        font-size: 9pt;
        line-height: 1.3;
        color: #333;
    }
    
    h1 {
        color: #2c3e50;
        font-size: 16pt;
        margin-bottom: 15px;
        border-bottom: 2px solid #3498db;
        padding-bottom: 8px;
        page-break-after: avoid;
    }
    
    h2 {
        color: #34495e;
        font-size: 13pt;
        margin-top: 20px;
        margin-bottom: 10px;
        page-break-after: avoid;
    }
    
    h3 {
        color: #7f8c8d;
        font-size: 11pt;
        margin-top: 15px;
        margin-bottom: 8px;
        page-break-after: avoid;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0 20px 0;
        font-size: 8pt;
        table-layout: fixed;
        page-break-inside: auto;
    }
    
    thead {
        display: table-header-group;
    }
    
    th {
        background-color: #34495e;
        color: white;
        font-weight: bold;
        padding: 10px 6px;
        border: 1px solid #2c3e50;
        text-align: center;
        vertical-align: middle;
        word-wrap: break-word;
        hyphens: auto;
        font-size: 9pt;
    }
    
    td {
        border: 1px solid #bdc3c7;
        padding: 8px 6px;
        vertical-align: top;
        word-wrap: break-word;
        hyphens: auto;
        overflow-wrap: break-word;
        line-height: 1.2;
    }
    
    /* 列幅の調整 */
    th:nth-child(1), td:nth-child(1) {
        width: 10%;
        text-align: center;
        font-weight: bold;
        background-color: #ecf0f1;
    }
    
    th:nth-child(2), td:nth-child(2) {
        width: 25%;
        font-size: 7pt;
    }
    
    th:nth-child(3), td:nth-child(3) {
        width: 50%;
        font-size: 7pt;
    }
    
    th:nth-child(4), td:nth-child(4) {
        width: 15%;
        text-align: right;
        font-weight: bold;
        color: #e74c3c;
        font-size: 8pt;
    }
    
    tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    
    /* 数値セルのスタイル */
    .number-cell {
        text-align: right;
        font-weight: bold;
        color: #e74c3c;
        font-family: "Courier New", monospace;
    }
    
    /* 空セルのスタイル */
    .empty-cell {
        color: #999;
        text-align: center;
        font-style: italic;
    }
    
    code {
        background-color: #f1f2f6;
        padding: 2px 4px;
        border-radius: 2px;
        font-family: "Courier New", "Monaco", monospace;
        font-size: 7pt;
        word-break: break-all;
        display: inline-block;
        max-width: 100%;
        line-height: 1.1;
    }
    
    .long-code {
        font-size: 6pt;
        padding: 1px 2px;
        line-height: 1.0;
    }
    
    pre {
        background-color: #f8f9fa;
        padding: 8px;
        border-radius: 4px;
        overflow-x: auto;
        font-size: 7pt;
        white-space: pre-wrap;
        word-wrap: break-word;
        line-height: 1.2;
    }
    
    strong {
        color: #c0392b;
        font-weight: bold;
    }
    
    /* ページ区切りの制御 */
    .page-break {
        page-break-before: always;
    }
    
    /* 行の高さ調整 */
    tr {
        page-break-inside: avoid;
    }
    
    /* テーブルヘッダーの繰り返し */
    @media print {
        thead {
            display: table-header-group;
        }
    }
    """
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>検索式分析結果</title>
        <style>
            .table-container {{
                overflow-x: auto;
                margin: 10px 0;
            }}
        </style>
    </head>
    <body>
        <div class="table-container">
            {html_content}
        </div>
    </body>
    </html>
    """
    
    font_config = FontConfiguration()
    
    HTML(string=html_template).write_pdf(
        pdf_file_path,
        stylesheets=[CSS(string=css_style)],
        font_config=font_config
    )
    
    print(f"改善されたPDFファイルが正常に作成されました: {pdf_file_path}")

if __name__ == "__main__":
    input_md = "search_formula/social_isolation_tech/search_lines_results.md"
    output_pdf = "search_formula/social_isolation_tech/search_lines_results_improved.pdf"
    
    if not os.path.exists(input_md):
        print(f"エラー: 入力ファイルが見つかりません: {input_md}")
        exit(1)
    
    output_dir = os.path.dirname(output_pdf)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        convert_md_to_pdf(input_md, output_pdf)
        print("テーブル表示改善版の変換が完了しました。")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        exit(1)
