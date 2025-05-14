#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
システマティックレビュー検索結果処理ツール

指定されたディレクトリ内の検索結果ファイル（RIS, NBIB, ClinicalTrials.gov CSV, ICTRP XML）を
自動的に処理し、データをマージ、重複排除を行い、Rayyanレビュー用のCSVファイルとして出力します。
また、各ファイルの件数などの統計情報も表示します。

使用方法:
    python search_results_processor.py --input-dir <検索結果ディレクトリ> [オプション]

オプション:
    --input-dir          検索結果ファイルがあるディレクトリ（必須）
    --output-dir         出力先ディレクトリ（デフォルト: input-dir/processed）
    --split-size         分割CSVファイルの最大レコード数（デフォルト: 500）
    --test-size          テストレビュー用のレコード数（デフォルト: 50）
    --include-duplicates 重複レコードの詳細を出力する（デフォルト: False）
    --no-zip             圧縮ZIPファイルを作成しない（デフォルト: 圧縮する）
    --verbose            詳細なログを出力する（デフォルト: False）
"""

import argparse
import os
import sys
import glob
from pathlib import Path

# 自作モジュールのインポート
from modules import file_handlers, data_processing, output_generator

def parse_arguments():
    """コマンドライン引数を解析する"""
    parser = argparse.ArgumentParser(description="検索結果ファイルを処理しRayyan用CSVに変換するツール")
    
    # 必須引数
    parser.add_argument("--input-dir", required=True, help="検索結果ファイルが置かれているディレクトリ")
    
    # オプション引数
    parser.add_argument("--output-dir", default=None, help="出力先ディレクトリ（デフォルト：input-dir/processed）")
    parser.add_argument("--split-size", type=int, default=500, help="分割するCSVファイルの最大レコード数（デフォルト：500）")
    parser.add_argument("--test-size", type=int, default=50, help="テストレビュー用のレコード数（デフォルト：50）")
    parser.add_argument("--include-duplicates", action="store_true", help="重複レコードの詳細を出力する")
    parser.add_argument("--no-zip", action="store_true", help="圧縮ZIPファイルを作成しない")
    parser.add_argument("--verbose", action="store_true", help="詳細なログを出力する")
    
    return parser.parse_args()

def find_files(input_dir):
    """
    入力ディレクトリ内のファイルを種類別に検索する
    
    Parameters:
    ----------
    input_dir : str
        検索対象のディレクトリパス
        
    Returns:
    -------
    dict
        ファイルタイプごとのパスリストを含む辞書
    """
    # ファイルパスを格納する辞書
    files = {
        "nbib": [],
        "ris": [],
        "clinical_trials": [],
        "ictrp": []
    }
    
    # NBIBファイル（PubMedからのエクスポート）
    nbib_files = glob.glob(os.path.join(input_dir, "*.nbib"))
    files["nbib"] = nbib_files
    
    # RISファイル（文献管理ソフトからのエクスポート）
    ris_files = glob.glob(os.path.join(input_dir, "*.ris")) + glob.glob(os.path.join(input_dir, "*.txt"))
    # ClinicalTrials.govやICTRPのファイルと誤認しないようにフィルタリング
    files["ris"] = [f for f in ris_files if not ("clinicaltrials" in f.lower() or "ictrp" in f.lower())]
    
    # ClinicalTrials.gov CSVファイル
    clinical_trials_files = glob.glob(os.path.join(input_dir, "*clinicaltrials*.csv"))
    files["clinical_trials"] = clinical_trials_files
    
    # ICTRP XMLファイル
    ictrp_files = glob.glob(os.path.join(input_dir, "*ictrp*.xml"))
    files["ictrp"] = ictrp_files
    
    return files

def process_files(args):
    """
    ファイルを処理し、結果を出力する
    
    Parameters:
    ----------
    args : argparse.Namespace
        コマンドライン引数
        
    Returns:
    -------
    tuple
        (処理結果のデータフレーム, 統計情報を含む辞書)
    """
    # 入力ディレクトリの確認
    input_dir = os.path.abspath(args.input_dir)
    if not os.path.isdir(input_dir):
        print(f"エラー: 指定された入力ディレクトリが存在しません: {input_dir}")
        sys.exit(1)
    
    # 出力ディレクトリの設定
    if args.output_dir:
        output_dir = os.path.abspath(args.output_dir)
    else:
        output_dir = os.path.join(input_dir, "processed")
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"入力ディレクトリ: {input_dir}")
    print(f"出力ディレクトリ: {output_dir}")
    
    # ファイルを種類別に検索
    files = find_files(input_dir)
    
    # 各ファイルタイプごとの件数
    file_counts = {}
    
    # データフレームを格納するリスト
    all_dataframes = []
    
    # 1. NBIBファイルの処理
    if files["nbib"]:
        print(f"\nNBIBファイルを処理中（{len(files['nbib'])}件）...")
        df_nbib, counts_nbib = file_handlers.process_nbib_files(files["nbib"])
        if not df_nbib.empty:
            all_dataframes.append(df_nbib)
        file_counts.update(counts_nbib)
    
    # 2. RISファイルの処理
    if files["ris"]:
        print(f"\nRISファイルを処理中（{len(files['ris'])}件）...")
        df_ris, counts_ris = file_handlers.process_ris_files(files["ris"])
        if not df_ris.empty:
            all_dataframes.append(df_ris)
        file_counts.update(counts_ris)
    
    # 3. ClinicalTrials.gov CSVファイルの処理
    if files["clinical_trials"]:
        print(f"\nClinicalTrials.gov CSVファイルを処理中（{len(files['clinical_trials'])}件）...")
        df_ct, counts_ct = file_handlers.process_clinicaltrials_files(files["clinical_trials"])
        if not df_ct.empty:
            all_dataframes.append(df_ct)
        file_counts.update(counts_ct)
    
    # 4. ICTRP XMLファイルの処理
    if files["ictrp"]:
        print(f"\nICTRP XMLファイルを処理中（{len(files['ictrp'])}件）...")
        df_ictrp, counts_ictrp = file_handlers.process_ictrp_files(files["ictrp"])
        if not df_ictrp.empty:
            all_dataframes.append(df_ictrp)
        file_counts.update(counts_ictrp)
    
    # ファイルが見つからない場合
    if not all_dataframes:
        print("処理対象のファイルが見つかりませんでした。")
        sys.exit(1)
    
    # 5. データの統合
    print("\nデータを統合中...")
    merged_df = data_processing.merge_dataframes(all_dataframes)
    total_before_dedup = len(merged_df)
    print(f"統合後のレコード数: {total_before_dedup}")
    
    # 元のデータフレームを保存（重複詳細レポート用）
    original_df = merged_df.copy() if args.include_duplicates else None
    
    # 6. データクリーニング
    merged_df = data_processing.clean_dataframe(merged_df)
    
    # 7. 重複排除
    print("\n重複を排除中...")
    deduplicated_df, duplicated_count = data_processing.deduplicate_advanced(merged_df)
    total_after_dedup = len(deduplicated_df)
    print(f"重複排除後のレコード数: {total_after_dedup}")
    print(f"削除された重複レコード数: {duplicated_count}")
    
    # 8. CSVファイルへの出力
    print("\nCSVファイルを出力中...")
    output_generator.export_to_rayyan_csv(
        deduplicated_df, 
        output_dir, 
        test_size=args.test_size, 
        split_size=args.split_size
    )
    
    # 9. 統計情報の生成
    stats = {
        "initial_counts": file_counts,
        "total_before_dedup": total_before_dedup,
        "deduplicated_count": duplicated_count,
        "total_after_dedup": total_after_dedup
    }
    
    print("\n統計情報を生成中...")
    output_generator.generate_summary_report(stats, output_dir)
    
    # 10. 重複詳細レポートの生成（オプション）
    if args.include_duplicates and original_df is not None:
        print("\n重複詳細レポートを生成中...")
        output_generator.generate_detailed_duplication_report(original_df, deduplicated_df, output_dir)
    
    return deduplicated_df, stats

def main():
    """メイン関数"""
    # バージョン情報
    version = "1.0.0"
    print(f"システマティックレビュー検索結果処理ツール v{version}")
    print("=" * 50)
    
    # コマンドライン引数の解析
    args = parse_arguments()
    
    try:
        # ファイルの処理
        df_result, stats = process_files(args)
        
        print("\n処理が完了しました。")
        print(f"総レコード数: {stats['total_before_dedup']}")
        print(f"重複排除後のレコード数: {stats['total_after_dedup']}")
        print(f"出力先ディレクトリ: {os.path.abspath(args.output_dir) if args.output_dir else os.path.join(os.path.abspath(args.input_dir), 'processed')}")
        
    except Exception as e:
        print(f"処理中にエラーが発生しました: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
