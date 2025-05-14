import re
import os
import sys
import argparse
from datetime import datetime

def convert_line_to_central(line_content: str) -> str:
    """PubMed形式の行内容をCochrane CENTRAL形式に変換する"""
    processed_content = line_content
    
    # 1. 近接検索変換 (finditerで全てのマッチを取得し、末尾から置換)
    proximity_pattern = re.compile(r'("[^"]+")\[(ti|tiab|ad|Title|Title/Abstract|Affiliation):~(\d+)\]')
    proximity_matches = list(proximity_pattern.finditer(processed_content))
    for match in reversed(proximity_matches):
        terms = match.group(1).strip('"').split()  # "term1 term2" → [term1, term2]
        field = match.group(2)                      # ti, tiab, ad など
        proximity = int(match.group(3))             # 近接値N
        
        # フィールドマッピング
        if field in ['ti', 'Title']:
            central_field = ':ti'
        elif field in ['tiab', 'Title/Abstract']:
            central_field = ':ti,ab,kw'
        elif field in ['ad', 'Affiliation']:
            central_field = ''  # CENTRALには対応するフィールドがない
        else:
            central_field = ':ti,ab,kw'  # デフォルト
        
        # 近接演算子変換
        if proximity == 0:
            # 隣接（間に単語なし）
            quoted_terms = [f'"{term}"' for term in terms]
            central_proximity = ' NEXT '
            transformed_prox = f'({central_proximity.join(quoted_terms)}){central_field}'
        else:
            # N語以内の近接
            if len(terms) == 2:  # 現在のPubMedでは2単語のみサポート
                transformed_prox = f'("{terms[0]}" NEAR/{proximity} "{terms[1]}"){central_field}'
            else:
                # 複数語の場合は、CENTRAL形式で適切に変換
                quoted_terms = [f'"{term}"' for term in terms]
                transformed_prox = f'({" AND ".join(quoted_terms)}){central_field}'
        
        start, end = match.span()
        processed_content = processed_content[:start] + transformed_prox + processed_content[end:]
    
    print(f"After Proximity (CENTRAL): {processed_content}")
    
    # 2. MeSH変換 (finditerで全てのマッチを取得し、末尾から置換)
    mesh_pattern = re.compile(r'("([^"]+)")\[(Mesh|mh)\]')
    mesh_matches = list(mesh_pattern.finditer(processed_content))
    for match in reversed(mesh_matches):
        term_only = match.group(2)      # Term
        transformed_term = f'[mh "{term_only}"]'
        start, end = match.span()
        processed_content = processed_content[:start] + transformed_term + processed_content[end:]
    print(f"After MeSH (CENTRAL): {processed_content}")

    # 3. tiab変換 (finditerで全てのマッチを取得し、末尾から置換)
    tiab_pattern = re.compile(r'((?:"[^"]+"|\S+?))\s*\[tiab\]') # 修正後のパターン
    tiab_matches = list(tiab_pattern.finditer(processed_content))
    for match in reversed(tiab_matches):
        term = match.group(1) # 検索語部分
        # CENTRAL形式では、検索語にそのまま :ti,ab,kw を付与
        transformed_tiab = f'{term}:ti,ab,kw'
        
        start, end = match.span() # マッチ全体の範囲（例: "term[tiab]"）
        processed_content = processed_content[:start] + transformed_tiab + processed_content[end:]
    
    print(f"CENTRAL conversion result for '{line_content}': {processed_content}")
    return processed_content

def convert_to_central(pubmed_query: str) -> str:
    lines = pubmed_query.strip().split('\n')
    central_lines = []
    line_num_pattern = re.compile(r'^#(\d+)\s+(.*)$')
    for original_line in lines:
        line = original_line.strip()
        if not line:
            central_lines.append('')
            continue
        print(f"Processing CENTRAL line (raw): {line}")
        match_line_num = line_num_pattern.match(line)
        if match_line_num:
            num, content = match_line_num.groups()
            print(f"Found CENTRAL line number: #{num}, content: {content}")
            processed_content = convert_line_to_central(content)
            central_lines.append(f"#{num} {processed_content}")
        else:
            print(f"CENTRAL line without number (assuming combination): {line}")
            central_lines.append(line) 
    return '\n'.join(central_lines)

def convert_line_to_dialog(line_content: str) -> str:
    """PubMed形式の行内容をDialog (Embase)形式に変換する"""
    processed_content = line_content
    
    # 1. 近接検索変換
    proximity_pattern = re.compile(r'("[^"]+")\[(ti|tiab|ad|Title|Title/Abstract|Affiliation):~(\d+)\]')
    proximity_matches = list(proximity_pattern.finditer(processed_content))
    for match in reversed(proximity_matches):
        terms = match.group(1).strip('"').split()  # "term1 term2" → [term1, term2]
        field = match.group(2)                      # ti, tiab, ad など
        proximity = int(match.group(3))             # 近接値N
        
        # フィールドマッピング
        if field in ['ti', 'Title']:
            dialog_field = 'TI'
        elif field in ['tiab', 'Title/Abstract']:
            dialog_field = 'TI,AB'
        elif field in ['ad', 'Affiliation']:
            dialog_field = 'CS'  # 所属機関フィールド
        else:
            dialog_field = 'TI,AB'  # デフォルト
        
        # 近接演算子変換
        if len(terms) == 2:  # 現在のPubMedでは2単語のみサポート
            if proximity == 0:
                # 隣接（間に単語なし）- W/1（順序固定で1単語以内）
                transformed_prox = f'{dialog_field}({terms[0]} W/1 {terms[1]})'
            else:
                # N語以内の近接 - N/n（順序不同でn単語以内）
                transformed_prox = f'{dialog_field}({terms[0]} N/{proximity} {terms[1]})'
        else:
            # 複数語の場合は、Dialog形式で適切に変換（ANDで結合）
            transformed_prox = f'{dialog_field}({" AND ".join(terms)})'
        
        start, end = match.span()
        processed_content = processed_content[:start] + transformed_prox + processed_content[end:]
    
    print(f"After Proximity (Dialog): {processed_content}")
    
    # 2. MeSH変換
    mesh_pattern = re.compile(r'("([^"]+)")\[(Mesh|mh)\]')
    mesh_matches = list(mesh_pattern.finditer(processed_content))
    for match in reversed(mesh_matches):
        term_only = match.group(2)
        transformed_term = f'EMB.EXACT.EXPLODE("{term_only}")'
        start, end = match.span()
        processed_content = processed_content[:start] + transformed_term + processed_content[end:]
    print(f"After MeSH (Dialog): {processed_content}")

    # 2. tiab変換
    tiab_pattern = re.compile(r'((?:"[^"]+"|\S+?))\s*\[tiab\]') # 修正後のパターン
    tiab_matches = list(tiab_pattern.finditer(processed_content))
    for match in reversed(tiab_matches):
        term = match.group(1) # 検索語部分
        # Dialog形式では、TI(検索語) OR AB(検索語)
        # 検索語がダブルクォートで囲まれていない場合、DialogのTI/AB内ではダブルクォートで囲むのが一般的
        if term.startswith('"') and term.endswith('"'):
            transformed_tiab = f'(TI({term}) OR AB({term}))'
        else:
            transformed_tiab = f'(TI("{term}") OR AB("{term}"))'
        
        start, end = match.span() # マッチ全体の範囲（例: "term[tiab]"）
        processed_content = processed_content[:start] + transformed_tiab + processed_content[end:]
    print(f"After tiab (Dialog): {processed_content}")

    # 3. 日付範囲の変換
    date_pattern = re.compile(r'(\d{4})/(\d{1,2})/(\d{1,2}):(\d{4})/(\d{1,2})/(\d{1,2})\[DP\]')
    processed_content = date_pattern.sub(lambda m: f"PD({m.group(1)}{m.group(2).zfill(2)}{m.group(3).zfill(2)}-{m.group(4)}{m.group(5).zfill(2)}{m.group(6).zfill(2)})", processed_content)
    
    print(f"Dialog line conversion result for '{line_content}': {processed_content}")
    return processed_content

def convert_to_dialog(pubmed_query: str) -> str:
    lines = pubmed_query.strip().split('\n')
    dialog_lines = []
    line_counter = 1
    line_mapping = {} 
    line_num_pattern = re.compile(r'^#(\d+)\s+(.*)$')

    temp_converted_lines = []
    for original_line in lines:
        line = original_line.strip()
        if not line:
            temp_converted_lines.append("")
            continue
        print(f"Dialog processing line (raw): {line}")
        match_line_num = line_num_pattern.match(line)
        if match_line_num:
            pubmed_num, content = match_line_num.groups()
            dialog_s_num = f"S{line_counter}"
            line_mapping[f"#{pubmed_num}"] = dialog_s_num
            print(f"Found Dialog line number: #{pubmed_num} -> {dialog_s_num}, content: {content}")
            converted_content = convert_line_to_dialog(content)
            temp_converted_lines.append(f"{dialog_s_num} {converted_content}")
            line_counter += 1
        else:
            print(f"Dialog line without number (assuming combination): {line}")
            temp_converted_lines.append(line)

    final_dialog_lines = []
    for line_to_process_refs in temp_converted_lines:
        final_line = line_to_process_refs
        sorted_refs = sorted(line_mapping.items(), key=lambda item: len(item[0]), reverse=True)
        for pubmed_ref, dialog_ref in sorted_refs:
            # #記号で始まり、数字が続くパターンを正確にマッチさせる
            pattern = r'(?<![a-zA-Z0-9_#])' + re.escape(pubmed_ref) + r'(?![a-zA-Z0-9_])'
            final_line = re.sub(pattern, dialog_ref, final_line)
        final_dialog_lines.append(final_line)
        
    return '\n'.join(final_dialog_lines)

def save_to_file(project_dir, content, filename):
    """ファイルを指定したディレクトリに保存する。パスの正規化とデバッグ出力を追加"""
    # パスの正規化（Windowsでのパス区切り文字の問題対応）
    project_dir = os.path.normpath(project_dir)
    os.makedirs(project_dir, exist_ok=True)
    
    # ファイルパスの構築と正規化
    filepath = os.path.normpath(os.path.join(project_dir, filename))
    print(f"保存先ファイルパス: {filepath}")
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"ファイル保存成功: {filepath}")
        # 保存したファイルが存在するか確認
        if os.path.exists(filepath):
            print(f"ファイル確認: {filepath} が正常に作成されました")
        else:
            print(f"警告: ファイル {filepath} が見つかりません")
    except Exception as e:
        print(f"ファイル保存エラー: {str(e)}")
        raise
    
    return filepath

def main():
    parser = argparse.ArgumentParser(description='PubMed検索式をCENTRALとDialog形式に変換するツール')
    parser.add_argument('input', nargs='?', help='PubMed検索式のテキストファイル（指定がなければ標準入力から読み込み）')
    parser.add_argument('--project', '-p', default=None, help='プロジェクト名（search_formula/配下のディレクトリ名）')
    args = parser.parse_args()
    text = ""
    if args.input:
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"ファイルの読み込みに失敗しました: {str(e)}")
            return
    else:
        print("PubMed検索式を入力してください（終了するには Ctrl+D または Ctrl+Z を押してください）:")
        text = sys.stdin.read()
    
    project_name = args.project if args.project else f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    project_dir = os.path.join("search_formula", project_name)
    os.makedirs(project_dir, exist_ok=True)
    print(f"プロジェクトディレクトリ: {project_dir}")
    
    print("\nCENTRAL形式に変換中...")
    central_query = convert_to_central(text)
    
    print("\nDialog(Embase)形式に変換中...")
    dialog_query = convert_to_dialog(text)
    
    md_content = f"# データベース別検索式\n\n変換日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    md_content += f"## PubMed\n\n```\n{text}\n```\n\n"
    md_content += f"## Cochrane CENTRAL\n\n```\n{central_query}\n```\n\n"
    md_content += f"## Dialog (Embase)\n\n```\n{dialog_query}\n```\n\n"
    
    cmdline_lines = []
    for line_content in dialog_query.split('\n'):
        stripped_line = line_content.strip()
        if stripped_line:
            match_s_num_content = re.match(r'^S\d+\s+(.*)$', stripped_line)
            if match_s_num_content:
                cmdline_lines.append(match_s_num_content.group(1).strip())
            elif not stripped_line.startswith('#') and not re.match(r'^S\d+\s*$', stripped_line):
                 cmdline_lines.append(stripped_line)

    md_content += "## Command Line for Dialog\n\nDialog検索画面でコピー&ペーストして使用するコマンドライン形式：\n\n```\n"
    md_content += '\n'.join(cmdline_lines)
    md_content += "\n```\n"
    
    all_search_file = save_to_file(project_dir, md_content, "all_database_search.md")
    print(f"データベース用検索式をまとめて保存しました: {all_search_file}")
    
    print("\n処理が完了しました。")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n処理が中断されました。")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
