import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import os

def convert_md_to_pdf(md_file_path, pdf_file_path):
    """
    MarkdownファイルをPDFに変換する
    
    Args:
        md_file_path: 入力Markdownファイルのパス
        pdf_file_path: 出力PDFファイルのパス
    """
    
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    html_content = markdown.markdown(
        md_content, 
        extensions=['tables', 'codehilite', 'fenced_code']
    )
    
    css_style = """
    @page {
        size: A4;
        margin: 2cm;
    }
    
    body {
        font-family: "DejaVu Sans", "Noto Sans CJK JP", "Hiragino Sans", "Yu Gothic", sans-serif;
        font-size: 10pt;
        line-height: 1.4;
        color: #333;
    }
    
    h1 {
        color: #2c3e50;
        font-size: 18pt;
        margin-bottom: 20px;
        border-bottom: 2px solid #3498db;
        padding-bottom: 10px;
    }
    
    h2 {
        color: #34495e;
        font-size: 14pt;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    
    h3 {
        color: #7f8c8d;
        font-size: 12pt;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
        font-size: 8pt;
    }
    
    th, td {
        border: 1px solid #bdc3c7;
        padding: 6px 8px;
        text-align: left;
        vertical-align: top;
        word-wrap: break-word;
    }
    
    th {
        background-color: #ecf0f1;
        font-weight: bold;
        color: #2c3e50;
    }
    
    tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    
    code {
        background-color: #f1f2f6;
        padding: 2px 4px;
        border-radius: 3px;
        font-family: "Courier New", monospace;
        font-size: 8pt;
        word-break: break-all;
    }
    
    pre {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        overflow-x: auto;
        font-size: 8pt;
    }
    
    .number {
        text-align: right;
        font-weight: bold;
        color: #e74c3c;
    }
    
    strong {
        color: #c0392b;
        font-weight: bold;
    }
    """
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>検索式分析結果</title>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    font_config = FontConfiguration()
    
    HTML(string=html_template).write_pdf(
        pdf_file_path,
        stylesheets=[CSS(string=css_style)],
        font_config=font_config
    )
    
    print(f"PDFファイルが正常に作成されました: {pdf_file_path}")

if __name__ == "__main__":
    input_md = "search_formula/social_isolation_tech/search_lines_results.md"
    output_pdf = "search_formula/social_isolation_tech/search_lines_results.pdf"
    
    if not os.path.exists(input_md):
        print(f"エラー: 入力ファイルが見つかりません: {input_md}")
        exit(1)
    
    output_dir = os.path.dirname(output_pdf)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        convert_md_to_pdf(input_md, output_pdf)
        print("変換が完了しました。")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        exit(1)
