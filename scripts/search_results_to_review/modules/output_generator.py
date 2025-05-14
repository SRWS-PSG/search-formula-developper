import pandas as pd
import os
import math
import zipfile
from pathlib import Path
import datetime

def export_to_rayyan_csv(df, output_dir, test_size=50, split_size=500):
    """
    処理したデータをRayyan用CSVファイルとして出力する
    
    Parameters:
    ----------
    df : pandas.DataFrame
        出力するデータフレーム
    output_dir : str
        出力先ディレクトリのパス
    test_size : int, optional
        テストレビュー用に分割するレコード数（デフォルト：50）
    split_size : int, optional
        1ファイルあたりの最大レコード数（デフォルト：500）
        
    Returns:
    -------
    list
        作成されたCSVファイルのパスリスト
    """
    if df.empty:
        print("出力するデータがありません。")
        return []

    os.makedirs(output_dir, exist_ok=True)
    
    num_records = len(df)
    csv_files_created = []

    if num_records == 0:
        print("レコードが0件のため、CSVファイルは作成されませんでした。")
        return []

    # テストレビュー用ファイルの作成
    if num_records <= test_size:
        # データが少ない場合は全てテストレビュー用に
        test_review_df = df
        file_path = os.path.join(output_dir, "0_testreview.csv")
        test_review_df.to_csv(file_path, index=False, encoding='utf-8-sig')  # BOM付きUTF-8
        csv_files_created.append(file_path)
        print(f"  作成: {file_path} ({len(test_review_df)}件)")
    else:
        # テストレビュー用と残りに分割
        test_review_df = df.iloc[:test_size]
        file_path = os.path.join(output_dir, "0_testreview.csv")
        test_review_df.to_csv(file_path, index=False, encoding='utf-8-sig')
        csv_files_created.append(file_path)
        print(f"  作成: {file_path} ({len(test_review_df)}件)")

        # 残りのデータを指定サイズで分割
        remaining_df = df.iloc[test_size:]
        num_remaining = len(remaining_df)

        if num_remaining > 0:
            num_splits = math.ceil(num_remaining / split_size)
            for i in range(num_splits):
                start_index = i * split_size
                end_index = min((i + 1) * split_size, num_remaining)
                split_df = remaining_df.iloc[start_index:end_index]
                file_path = os.path.join(output_dir, f"{i+1}_search.csv")
                split_df.to_csv(file_path, index=False, encoding='utf-8-sig')
                csv_files_created.append(file_path)
                print(f"  作成: {file_path} ({len(split_df)}件)")
    
    # CSVファイルをZIP圧縮
    if csv_files_created:
        zip_path = os.path.join(output_dir, "rayyan_csv_files.zip")
        with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
            for f_path in csv_files_created:
                new_zip.write(f_path, arcname=os.path.basename(f_path))
        print(f"  圧縮ファイル作成: {zip_path}")
    
    return csv_files_created

def generate_summary_report(stats, output_dir):
    """
    統計情報のレポートを生成する
    
    Parameters:
    ----------
    stats : dict
        統計情報を含む辞書
    output_dir : str
        出力先ディレクトリのパス
        
    Returns:
    -------
    str
        生成されたレポートファイルのパス
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(output_dir, f"summary_report_{timestamp}.txt")
    
    # UTF-8 with BOMで書き込み
    with open(report_path, "w", encoding="utf-8-sig") as f:
        f.write("============================================\n")
        f.write("     システマティックレビュー検索結果処理レポート     \n")
        f.write("============================================\n")
        f.write(f"作成日時: {datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n\n")
        
        f.write("1. 各データソースの検索結果件数\n")
        f.write("--------------------------------------------\n")
        
        if stats.get("initial_counts"):
            # データベース別の件数
            for file_name, count in stats["initial_counts"].items():
                # ファイル名から拡張子を除去（データベース名として表示）
                db_name = Path(file_name).stem
                f.write(f"  {db_name}: {count}件\n")
        else:
            f.write("  データなし\n")
        
        f.write("\n2. 重複排除の結果\n")
        f.write("--------------------------------------------\n")
        f.write(f"  重複排除前の総レコード数: {stats.get('total_before_dedup', 0)}件\n")
        f.write(f"  削除された重複レコード数: {stats.get('deduplicated_count', 0)}件\n")
        f.write(f"  重複排除後の総レコード数: {stats.get('total_after_dedup', 0)}件\n")
        
        # 重複率の計算
        if stats.get('total_before_dedup', 0) > 0:
            duplication_rate = (stats.get('deduplicated_count', 0) / stats.get('total_before_dedup', 0)) * 100
            f.write(f"  重複率: {duplication_rate:.2f}%\n")
        
        f.write("\n3. PRISMAフローチャート用データ\n")
        f.write("--------------------------------------------\n")
        f.write("DATABASES:\n")
        
        if stats.get("initial_counts"):
            for file_name, count in stats["initial_counts"].items():
                # データベース名を整形
                db_name = Path(file_name).stem.replace(".ris", "").replace(".txt", "")
                f.write(f"{db_name}: (n = {count})\n")
        
        f.write(f"\nDuplicated records: (n = {stats.get('deduplicated_count', 0)})\n")
        f.write(f"Records screened: (n = {stats.get('total_after_dedup', 0)})\n")
    
    print(f"サマリーレポート作成: {report_path}")
    return report_path

def generate_detailed_duplication_report(df_original, df_deduplicated, output_dir):
    """
    重複レコードの詳細レポートを生成する（オプション機能）
    
    Parameters:
    ----------
    df_original : pandas.DataFrame
        重複排除前の元データ
    df_deduplicated : pandas.DataFrame
        重複排除後のデータ
    output_dir : str
        出力先ディレクトリのパス
        
    Returns:
    -------
    str
        生成されたレポートファイルのパス
    """
    if df_original.empty or df_deduplicated.empty:
        return None
    
    # 重複として削除されたレコードを特定
    original_keys = set(df_original['key'])
    deduplicated_keys = set(df_deduplicated['key'])
    removed_keys = original_keys - deduplicated_keys
    
    if not removed_keys:
        return None
    
    # 削除されたレコードのデータフレーム
    df_removed = df_original[df_original['key'].isin(removed_keys)]
    
    # レポートファイルのパス
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    detail_report_path = os.path.join(output_dir, f"duplication_details_{timestamp}.csv")
    
    # CSVとして出力
    df_removed.to_csv(detail_report_path, index=False, encoding='utf-8-sig')
    
    print(f"重複詳細レポート作成: {detail_report_path}")
    return detail_report_path
