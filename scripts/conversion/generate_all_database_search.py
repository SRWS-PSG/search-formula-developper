import argparse
import os
import sys
import json
import re
import datetime
from pathlib import Path

# 親ディレクトリをパスに追加してインポートを可能にする
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# 各データベースのコンバーターをインポート
from search_converter import convert_to_central, convert_to_dialog
from clinicaltrials.converter import convert_to_clinicaltrials, format_ct_output
from ictrp.converter import convert_to_ictrp

def load_mesh_synonyms(mesh_map_file):
    """MeSH用語の同義語マップを読み込む（任意）"""
    if mesh_map_file and os.path.exists(mesh_map_file):
        try:
            with open(mesh_map_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"MeSH同義語マップの読み込みエラー: {e}")
    return {}

def read_input_file(input_file):
    """入力ファイルを読み込む"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"入力ファイルの読み込みエラー: {e}")
        sys.exit(1)

def extract_search_lines(markdown_text):
    """search_formula.mdからPubMed検索行のみを抽出する。

    markdownファイルのコードブロック(```)内にある #N で始まる検索行を抽出し、
    タイトルやセクションヘッダー等のゴミを除外する。

    Returns:
        str: 検索行のみを改行区切りで結合した文字列
    """
    lines = markdown_text.split('\n')
    in_code_block = False
    search_lines = []
    line_num_pattern = re.compile(r'^#\d+\s+')

    for line in lines:
        stripped = line.strip()
        # コードブロックの開始/終了をトグル
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue
        # コードブロック内の #N で始まる行のみ抽出
        if in_code_block and line_num_pattern.match(stripped):
            search_lines.append(stripped)

    if search_lines:
        return '\n'.join(search_lines)

    # コードブロック内に検索行が見つからない場合、
    # ファイル全体から #N パターンの行を直接探す（フォールバック）
    for line in lines:
        stripped = line.strip()
        if line_num_pattern.match(stripped):
            search_lines.append(stripped)

    if search_lines:
        return '\n'.join(search_lines)

    # それでも見つからない場合は元テキストをそのまま返す
    print("警告: 検索行（#N 形式）が見つかりませんでした。入力テキストをそのまま使用します。")
    return markdown_text

def save_to_file(output_file, content):
    """出力ファイルを保存する"""
    try:
        # ディレクトリが存在しない場合は作成
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"出力ファイルを保存しました: {output_file}")
    except Exception as e:
        print(f"出力ファイルの保存エラー: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='PubMed検索式を複数データベース形式に変換するツール')
    parser.add_argument('--input', required=True, help='入力PubMed検索式ファイル')
    parser.add_argument('--output', required=True, help='出力ファイル（全データベース検索式）')
    parser.add_argument('--mesh-map', help='MeSH同義語マッピングのJSONファイル（任意）')
    args = parser.parse_args()
    
    # 入力ファイルを読み込み
    raw_text = read_input_file(args.input)

    # markdownから検索行のみを抽出
    pubmed_query = extract_search_lines(raw_text)
    print(f"抽出された検索行:\n{pubmed_query}\n")

    # MeSH同義語マップを読み込み（任意）
    mesh_map = load_mesh_synonyms(args.mesh_map)

    # 各データベース形式に変換
    print("Cochrane CENTRAL形式に変換中...")
    central_query = convert_to_central(pubmed_query)
    
    print("Dialog (Embase)形式に変換中...")
    dialog_query = convert_to_dialog(pubmed_query)
    
    print("ClinicalTrials.gov形式に変換中...")
    ct_query = convert_to_clinicaltrials(pubmed_query)
    ct_formatted = format_ct_output(ct_query)
    
    print("ICTRP形式に変換中...")
    ictrp_query = convert_to_ictrp(pubmed_query)
    
    # Dialog用のコマンドライン形式を生成
    cmdline_lines = []
    for line_content in dialog_query.split('\n'):
        stripped_line = line_content.strip()
        if stripped_line:
            match_s_num_content = re.match(r'^S\d+\s+(.*)$', stripped_line)
            if match_s_num_content:
                cmdline_lines.append(match_s_num_content.group(1).strip())
            elif not stripped_line.startswith('#') and not re.match(r'^S\d+\s*$', stripped_line):
                cmdline_lines.append(stripped_line)
    
    dialog_cmdline = '\n'.join(cmdline_lines)
    
    # 結果をMarkdownファイルに出力
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    md_content = f"# データベース別検索式\n\n"
    md_content += f"変換日時: {now}\n\n"
    
    # PubMed
    md_content += "## PubMed\n\n```\n"
    md_content += pubmed_query
    md_content += "\n```\n\n"
    
    # Cochrane CENTRAL
    md_content += "## Cochrane CENTRAL\n\n```\n"
    md_content += central_query
    md_content += "\n```\n\n"
    
    # Dialog (Embase)
    md_content += "## Dialog (Embase)\n\n```\n"
    md_content += dialog_query
    md_content += "\n```\n\n"
    
    # Dialog Command Line
    md_content += "## Command Line for Dialog\n\n"
    md_content += "Dialog検索画面でコピー&ペーストして使用するコマンドライン形式：\n\n```\n"
    md_content += dialog_cmdline
    md_content += "\n```\n\n"
    
    def clean_for_registry(query: str) -> str:
        """ClinicalTrials.gov/ICTRP向けにタグ・ワイルドカードを除去"""
        q = query
        # 近接演算子タグ [tiab:~2] 等を削除
        q = re.sub(r'\[[a-zA-Z/]+:~\d+\]', '', q)
        # フィールドタグ [tiab], [MeSH], [MeSH Terms], [ti], [ab], [tw] 等を削除
        q = re.sub(r'\[(Mesh|MeSH|MeSH Terms|mh|tiab|ti|ab|tw|Title/Abstract|Title|Affiliation|ad)\]', '', q)
        # ワイルドカード(*) を削除
        q = re.sub(r'\*', '', q)
        # 連続スペースを整理
        q = re.sub(r'  +', ' ', q)
        return q.strip()

    # ClinicalTrials.gov
    md_content += "## ClinicalTrials.gov\n\n```\n"
    for field, query in ct_query.items():
        clean_query = clean_for_registry(query)
        md_content += f"{field}: {clean_query}\n"
    md_content += "```\n\n"

    # Advanced Search UI表示形式
    md_content += "Advanced Search UI表示形式：\n```\n"
    ui_parts = []
    for field, query in ct_query.items():
        clean_query = clean_for_registry(query)
        ui_parts.append(f"( {field}: {clean_query} )")
    md_content += " AND\n".join(ui_parts)
    md_content += "\n```\n\n"

    md_content += "注意: ClinicalTrials.govではワイルドカード(*)は使用できません。MeSHタグも不要です。\n\n"

    # ICTRP
    md_content += "## ICTRP\n\n```\n"
    clean_ictrp_query = clean_for_registry(ictrp_query)
    md_content += clean_ictrp_query
    md_content += "\n```\n\n"
    md_content += "注意：ICTRPではMeSHタグ、ワイルドカード、近接演算子は使用できません。検索画面UIから日付制限を設定してください。\n"
    
    # 結果をファイルに保存
    save_to_file(args.output, md_content)
    
    print("すべてのデータベース向け検索式の変換が完了しました。")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n処理が中断されました。")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
