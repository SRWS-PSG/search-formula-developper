import pandas as pd
import re
from pathlib import Path

def merge_dataframes(list_of_dataframes):
    """
    複数のDataFrameを統合する
    
    Parameters:
    ----------
    list_of_dataframes : list of pandas.DataFrame
        統合するDataFrameのリスト
        
    Returns:
    -------
    pandas.DataFrame
        統合後のDataFrame
    """
    if not list_of_dataframes:
        return pd.DataFrame()
    
    return pd.concat(list_of_dataframes, ignore_index=True)

def normalize_title(title):
    """
    タイトルを正規化する（小文字化、記号の削除など）
    
    Parameters:
    ----------
    title : str
        正規化するタイトル文字列
        
    Returns:
    -------
    str
        正規化されたタイトル文字列
    """
    if pd.isna(title) or title == "":
        return ""
    
    # 小文字化
    normalized = title.lower()
    
    # 先頭と末尾の角括弧を削除
    normalized = re.sub(r'^\[|\]$', '', normalized)
    
    # 先頭と末尾の空白を削除
    normalized = normalized.strip()
    
    # 連続する空白を1つにまとめる
    normalized = re.sub(r'\s+', ' ', normalized)
    
    return normalized

def deduplicate_by_title(df):
    """
    タイトルに基づいて重複を排除する
    
    Parameters:
    ----------
    df : pandas.DataFrame
        重複排除するDataFrame
        
    Returns:
    -------
    tuple
        (重複排除後のDataFrame, 削除された重複レコード数)
    """
    if df.empty or 'title' not in df.columns:
        return df, 0
    
    # タイトルがないレコードは保持（あるいは特定の処理）
    df_with_title = df[df['title'].notna() & (df['title'] != '')].copy()
    df_no_title = df[~(df['title'].notna() & (df['title'] != ''))].copy()
    
    initial_count = len(df_with_title)
    
    if initial_count == 0:
        return df, 0

    # タイトルを正規化して比較用の一時列を作成
    df_with_title['temp_normalized_title'] = df_with_title['title'].apply(normalize_title)
    
    # 重複排除（最初に出現したものを保持）
    df_deduplicated_with_title = df_with_title.drop_duplicates(subset=['temp_normalized_title'], keep='first')
    
    # 削除された重複レコード数を計算
    deduplicated_count = initial_count - len(df_deduplicated_with_title)
    
    # 一時列を削除
    df_deduplicated_with_title = df_deduplicated_with_title.drop(columns=['temp_normalized_title'])
    
    # タイトルがないレコードと結合
    final_df = pd.concat([df_deduplicated_with_title, df_no_title], ignore_index=True)
    
    return final_df, deduplicated_count

def deduplicate_by_doi(df):
    """
    DOIに基づいて重複を排除する
    
    Parameters:
    ----------
    df : pandas.DataFrame
        重複排除するDataFrame
        
    Returns:
    -------
    tuple
        (重複排除後のDataFrame, 削除された重複レコード数)
    """
    if df.empty or 'doi' not in df.columns:
        return df, 0
    
    # DOIがないレコードは保持
    df_with_doi = df[df['doi'].notna() & (df['doi'] != '')].copy()
    df_no_doi = df[~(df['doi'].notna() & (df['doi'] != ''))].copy()
    
    initial_count = len(df_with_doi)
    
    if initial_count == 0:
        return df, 0
    
    # DOIを正規化して比較用の一時列を作成
    df_with_doi['temp_normalized_doi'] = df_with_doi['doi'].str.lower().str.strip()
    
    # 重複排除（最初に出現したものを保持）
    df_deduplicated_with_doi = df_with_doi.drop_duplicates(subset=['temp_normalized_doi'], keep='first')
    
    # 削除された重複レコード数を計算
    deduplicated_count = initial_count - len(df_deduplicated_with_doi)
    
    # 一時列を削除
    df_deduplicated_with_doi = df_deduplicated_with_doi.drop(columns=['temp_normalized_doi'])
    
    # DOIがないレコードと結合
    final_df = pd.concat([df_deduplicated_with_doi, df_no_doi], ignore_index=True)
    
    return final_df, deduplicated_count

def deduplicate_advanced(df):
    """
    複数の条件に基づいて段階的に重複を排除する
    1. DOIに基づく重複排除
    2. タイトルに基づく重複排除
    
    Parameters:
    ----------
    df : pandas.DataFrame
        重複排除するDataFrame
        
    Returns:
    -------
    tuple
        (重複排除後のDataFrame, 削除された重複レコード数の合計)
    """
    if df.empty:
        return df, 0
    
    total_deduplicated = 0
    
    # 1. DOIに基づく重複排除
    df_dedup_doi, doi_dedup_count = deduplicate_by_doi(df)
    total_deduplicated += doi_dedup_count
    
    # 2. タイトルに基づく重複排除
    df_dedup_final, title_dedup_count = deduplicate_by_title(df_dedup_doi)
    total_deduplicated += title_dedup_count
    
    return df_dedup_final, total_deduplicated

def clean_dataframe(df):
    """
    データフレームのクリーニングを行う
    - タイトルや抄録の不要なタグや改行の削除
    - 特殊文字の正規化
    
    Parameters:
    ----------
    df : pandas.DataFrame
        クリーニングするDataFrame
        
    Returns:
    -------
    pandas.DataFrame
        クリーニング後のDataFrame
    """
    if df.empty:
        return df
    
    # 列の存在確認とクリーニング
    for col in ['title', 'abstract', 'journal', 'authors']:
        if col in df.columns:
            # 不要なタグやHTMLエンティティの削除
            df[col] = df[col].astype(str).replace('<[^<]+?>', '', regex=True)
            # 改行コードの削除
            df[col] = df[col].str.replace(r'\n', ' ', regex=True)
            df[col] = df[col].str.replace(r'\r', ' ', regex=True)
            # 連続する空白の単一空白への変換
            df[col] = df[col].str.replace(r'\s+', ' ', regex=True)
    
    return df
