import pandas as pd
import os
import rispy
import nbib
import xml.etree.ElementTree as ET
from pathlib import Path
import re
import warnings

# エンコーディングの問題を無視
warnings.filterwarnings("ignore", category=UserWarning)

# --- NBIB処理 ---
def nbib_df_parser(nbib_path):
    """
    NBIBファイルを読み込み、標準化されたDataFrameに変換する
    
    Parameters:
    ----------
    nbib_path : str
        NBIBファイルのパス
        
    Returns:
    -------
    pandas.DataFrame
        Rayyan互換形式のDataFrame
    """
    try:
        # NBIBファイルの読み込み
        entries = nbib.read_file(nbib_path)
        df_raw = pd.DataFrame(entries)
        
        # 最終的な列の順序を定義
        final_columns = [
            "key", "title", "authors", "journal", "issn", "volume", "issue",
            "pages", "year", "publisher", "url", "abstract", "notes", "doi", "keywords"
        ]
        
        # 空のDataFrameを作成（行数は元データに合わせる）
        df_final = pd.DataFrame(index=df_raw.index, columns=final_columns)
        
        # タイトル
        df_final["title"] = df_raw["title"] if "title" in df_raw.columns else ""
        
        # 著者情報の処理
        if "authors" in df_raw.columns:
            df_final["authors"] = df_raw["authors"].apply(
                lambda x: ", ".join([author.get("author_abbreviated", "") for author in x]) if isinstance(x, list) else ""
            )
        else:
            df_final["authors"] = ""
        
        # ジャーナル
        df_final["journal"] = df_raw["journal"] if "journal" in df_raw.columns else ""
        
        # ISSN（電子版を優先）
        df_final["issn"] = df_raw["electronic_issn"] if "electronic_issn" in df_raw.columns else ""
        
        # 巻号・号
        df_final["volume"] = df_raw["journal_volume"] if "journal_volume" in df_raw.columns else ""
        df_final["issue"] = df_raw["journal_issue"] if "journal_issue" in df_raw.columns else ""
        
        # ページ
        df_final["pages"] = df_raw["pages"] if "pages" in df_raw.columns else ""
        
        # 出版年
        if "publication_date" in df_raw.columns:
            df_final["year"] = pd.to_datetime(df_raw["publication_date"], errors="coerce").dt.year.fillna("").astype(str)
        elif "last_revision_date" in df_raw.columns:
            df_final["year"] = pd.to_datetime(df_raw["last_revision_date"], errors="coerce").dt.year.fillna("").astype(str)
        else:
            df_final["year"] = ""
        
        # 出版社
        df_final["publisher"] = df_raw["place_of_publication"] if "place_of_publication" in df_raw.columns else ""
        
        # URL
        if "doi" in df_raw.columns:
            df_final["url"] = df_raw["doi"].apply(
                lambda x: f"https://doi.org/{x}" if pd.notna(x) and str(x).strip() != "" else ""
            )
        else:
            df_final["url"] = ""
        
        # 抄録
        df_final["abstract"] = df_raw["abstract"] if "abstract" in df_raw.columns else ""
        
        # ノート
        df_final["notes"] = ""
        
        # DOI
        df_final["doi"] = df_raw["doi"] if "doi" in df_raw.columns else ""
        
        # キーワード
        if "keywords" in df_raw.columns:
            df_final["keywords"] = df_raw["keywords"]
        elif "descriptors" in df_raw.columns:
            df_final["keywords"] = df_raw["descriptors"]
        else:
            df_final["keywords"] = ""
        
        # key列（一意なID）
        file_stem = Path(nbib_path).stem
        df_final["key"] = [f"NBIB_{file_stem}_{i+1}" for i in range(len(df_final))]
        
        # 欠損値を空文字列に変換
        df_final = df_final.fillna("")
        
        return df_final
    except Exception as e:
        print(f"NBIBファイル処理エラー ({nbib_path}): {str(e)}")
        return pd.DataFrame(columns=final_columns)

def process_nbib_files(nbib_file_paths):
    """
    複数のNBIBファイルを処理し、一つのDataFrameに統合する
    
    Parameters:
    ----------
    nbib_file_paths : list of str
        処理するNBIBファイルのパスリスト
        
    Returns:
    -------
    tuple
        (統合されたDataFrame, ファイルごとの件数を含む辞書)
    """
    all_dfs = []
    counts = {}
    
    for path in nbib_file_paths:
        try:
            df = nbib_df_parser(path)
            if not df.empty:
                all_dfs.append(df)
                file_name = Path(path).name
                counts[file_name] = len(df)
                print(f"  {file_name}: {len(df)}件 読み込み完了")
        except Exception as e:
            print(f"  エラー: {Path(path).name} の処理中にエラーが発生しました - {e}")
    
    if not all_dfs:
        return pd.DataFrame(), counts
    
    return pd.concat(all_dfs, ignore_index=True), counts

# --- RIS処理 ---
def ris_df_parser(ris_path):
    """
    RISファイルを読み込み、標準化されたDataFrameに変換する
    
    Parameters:
    ----------
    ris_path : str
        RISファイルのパス
        
    Returns:
    -------
    pandas.DataFrame
        Rayyan互換形式のDataFrame
    """
    try:
        # ファイルを開いて不要な行を除外
        p = Path(ris_path)
        try:
            # UTF-8で試す
            with p.open(encoding='utf-8', errors='ignore') as f:
                unwanted_prefixes = [
                    "Link to the Ovid Full Text or citation:",
                    "Record #",
                    "Provider:",
                    "Content:"
                ]
                lines = [line for line in f.readlines() if not any(line.startswith(prefix) for prefix in unwanted_prefixes)]
                data = "".join(lines)
        except UnicodeDecodeError:
            # UTF-8で失敗した場合はcp932で試す（日本語Windows環境向け）
            with p.open(encoding='cp932', errors='ignore') as f:
                unwanted_prefixes = [
                    "Link to the Ovid Full Text or citation:",
                    "Record #",
                    "Provider:",
                    "Content:"
                ]
                lines = [line for line in f.readlines() if not any(line.startswith(prefix) for prefix in unwanted_prefixes)]
                data = "".join(lines)

        # RISデータをパース
        entries = rispy.loads(data)
        df_raw = pd.json_normalize(entries)
        
        # 最終的な列の順序を定義
        final_columns = [
            "key", "title", "authors", "journal", "issn", "volume", "issue",
            "pages", "year", "publisher", "url", "abstract", "notes", "doi", "keywords"
        ]
        
        # 空のDataFrameを作成
        df_final = pd.DataFrame(index=df_raw.index, columns=final_columns)
        
        # ファイルタイプの判定
        file_type = "unknown"
        
        if all(col in df_raw.columns for col in ["primary_title", "alternate_title3", "authors", "abstract", "doi", "publication_year", "urls"]):
            file_type = "ProQuest"
        elif all(col in df_raw.columns for col in ["primary_title", "alternate_title3", "first_authors", "notes_abstract", "publication_year", "doi", "url"]):
            file_type = "Mendeley"
        elif all(col in df_raw.columns for col in ["primary_title", "alternate_title3", "authors", "abstract", "publication_year", "doi", "urls"]):
            file_type = "Ovid"
        elif all(col in df_raw.columns for col in ["title", "secondary_title", "authors", "abstract", "doi", "year", "urls"]):
            file_type = "Paperpile/Zotero"
        elif all(col in df_raw.columns for col in ["title", "secondary_title", "authors", "abstract", "doi", "year", "url"]):
            file_type = "Endnote"
        elif all(col in df_raw.columns for col in ["title", "secondary_title", "authors", "abstract", "publication_year", "issn", "urls"]):
            file_type = "Rayyan"
        elif "alternate_title2" in df_raw.columns:
            file_type = "CENTRAL"
        
        # 各ファイルタイプごとのマッピング処理
        if file_type == "ProQuest":
            df_final["title"] = df_raw["primary_title"]
            df_final["journal"] = df_raw["alternate_title3"]
            df_final["authors"] = df_raw["authors"]
            df_final["abstract"] = df_raw["abstract"]
            df_final["doi"] = df_raw["doi"]
            df_final["year"] = df_raw["publication_year"]
            df_final["url"] = df_raw.apply(
                lambda row: f"https://doi.org/{row['doi']}" if pd.notna(row['doi']) and str(row['doi']).strip() != ""
                else (row["urls"] if "urls" in df_raw.columns else ""), 
                axis=1
            )
            df_final["issn"] = df_raw["issn"] if "issn" in df_raw.columns else ""
            df_final["volume"] = df_raw["volume"] if "volume" in df_raw.columns else ""
            df_final["issue"] = df_raw["number"] if "number" in df_raw.columns else ""
            if "start_page" in df_raw.columns:
                df_final["pages"] = df_raw["start_page"]
            else:
                df_final["pages"] = ""
            df_final["publisher"] = df_raw["publisher"] if "publisher" in df_raw.columns else ""
            df_final["notes"] = df_raw["notes"] if "notes" in df_raw.columns else ""
            df_final["keywords"] = df_raw["keywords"] if "keywords" in df_raw.columns else ""
            
        elif file_type == "Mendeley":
            df_final["title"] = df_raw["primary_title"]
            df_final["journal"] = df_raw["alternate_title3"]
            df_final["authors"] = df_raw["first_authors"]
            df_final["abstract"] = df_raw["notes_abstract"]
            df_final["doi"] = df_raw["doi"]
            df_final["year"] = df_raw["publication_year"]
            df_final["url"] = df_raw.apply(
                lambda row: f"https://doi.org/{row['doi']}" if pd.notna(row['doi']) and str(row['doi']).strip() != ""
                else (row["url"] if "url" in df_raw.columns else ""), 
                axis=1
            )
            
        elif file_type == "Ovid":
            df_final["title"] = df_raw["primary_title"]
            df_final["journal"] = df_raw["alternate_title3"]
            df_final["authors"] = df_raw["authors"]
            df_final["abstract"] = df_raw["abstract"]
            df_final["doi"] = df_raw["doi"]
            df_final["year"] = df_raw["publication_year"]
            df_final["url"] = df_raw.apply(
                lambda row: f"https://doi.org/{row['doi']}" if pd.notna(row['doi']) and str(row['doi']).strip() != ""
                else (row["urls"] if "urls" in df_raw.columns else ""), 
                axis=1
            )
            
        elif file_type == "Paperpile/Zotero":
            df_final["title"] = df_raw["title"]
            df_final["journal"] = df_raw["secondary_title"]
            df_final["authors"] = df_raw["authors"]
            df_final["abstract"] = df_raw["abstract"]
            df_final["doi"] = df_raw["doi"]
            df_final["year"] = df_raw["year"]
            df_final["url"] = df_raw.apply(
                lambda row: f"https://doi.org/{row['doi']}" if pd.notna(row['doi']) and str(row['doi']).strip() != ""
                else (row["urls"] if "urls" in df_raw.columns else ""), 
                axis=1
            )
            
        elif file_type == "Endnote":
            df_final["title"] = df_raw["title"]
            df_final["journal"] = df_raw["secondary_title"]
            df_final["authors"] = df_raw["authors"]
            df_final["abstract"] = df_raw["abstract"]
            df_final["doi"] = df_raw["doi"]
            df_final["year"] = df_raw["year"]
            df_final["url"] = df_raw.apply(
                lambda row: f"https://doi.org/{row['doi']}" if pd.notna(row['doi']) and str(row['doi']).strip() != ""
                else (row["url"] if "url" in df_raw.columns else ""), 
                axis=1
            )
            
        elif file_type == "Rayyan":
            df_final["title"] = df_raw["title"]
            df_final["journal"] = df_raw["secondary_title"]
            df_final["authors"] = df_raw["authors"]
            df_final["abstract"] = df_raw["abstract"]
            df_final["doi"] = df_raw["doi"] if "doi" in df_raw.columns else ""
            df_final["year"] = df_raw["publication_year"]
            df_final["url"] = df_raw["urls"] if "urls" in df_raw.columns else ""
            df_final["issn"] = df_raw["issn"] if "issn" in df_raw.columns else ""
            df_final["notes"] = df_raw["notes"] if "notes" in df_raw.columns else ""
            df_final["keywords"] = df_raw["keywords"] if "keywords" in df_raw.columns else ""
            
        elif file_type == "CENTRAL":
            df_final["title"] = df_raw["title"] if "title" in df_raw.columns else ""
            df_final["journal"] = df_raw["alternate_title2"] if "alternate_title2" in df_raw.columns else ""
            df_final["authors"] = df_raw["authors"] if "authors" in df_raw.columns else ""
            df_final["abstract"] = df_raw["abstract"] if "abstract" in df_raw.columns else ""
            df_final["doi"] = df_raw["doi"] if "doi" in df_raw.columns else ""
            
            if "year" in df_raw.columns:
                df_final["year"] = df_raw["year"]
            elif "date" in df_raw.columns:
                try:
                    df_final["year"] = pd.to_datetime(df_raw["date"], errors="coerce").dt.year.fillna("").astype(str)
                except Exception:
                    df_final["year"] = ""
            else:
                df_final["year"] = ""
                
            df_final["volume"] = df_raw["volume"] if "volume" in df_raw.columns else ""
            df_final["issue"] = df_raw["number"] if "number" in df_raw.columns else ""
            
            if "start_page" in df_raw.columns:
                if "end_page" in df_raw.columns:
                    df_final["pages"] = df_raw["start_page"].astype(str) + "-" + df_raw["end_page"].astype(str)
                else:
                    df_final["pages"] = df_raw["start_page"]
            else:
                df_final["pages"] = ""
                
            df_final["publisher"] = df_raw["publisher"] if "publisher" in df_raw.columns else ""
            df_final["url"] = df_raw.apply(
                lambda row: f"https://doi.org/{row['doi']}" if pd.notna(row.get('doi')) and str(row.get('doi', '')).strip() != ""
                else (row.get("urls", "") if "urls" in df_raw.columns else ""), 
                axis=1
            )
            df_final["issn"] = df_raw["issn"] if "issn" in df_raw.columns else ""
            df_final["notes"] = df_raw["custom3"] if "custom3" in df_raw.columns else ""
            df_final["keywords"] = df_raw["keywords"] if "keywords" in df_raw.columns else ""
            
        else:
            # 未知のファイルタイプの場合のフォールバック処理
            df_final["title"] = df_raw["title"] if "title" in df_raw.columns else df_raw["primary_title"] if "primary_title" in df_raw.columns else ""
            df_final["authors"] = df_raw["authors"] if "authors" in df_raw.columns else df_raw["first_authors"] if "first_authors" in df_raw.columns else ""
            df_final["abstract"] = df_raw["abstract"] if "abstract" in df_raw.columns else df_raw["notes_abstract"] if "notes_abstract" in df_raw.columns else ""
            df_final["doi"] = df_raw["doi"] if "doi" in df_raw.columns else ""
            
            # URLの処理（DOIからURLを生成、またはurls/url列から取得）
            if "doi" in df_raw.columns:
                df_final["url"] = df_raw["doi"].apply(
                    lambda x: f"https://doi.org/{x}" if pd.notna(x) and str(x).strip() != "" else ""
                )
            elif "urls" in df_raw.columns:
                df_final["url"] = df_raw["urls"]
            elif "url" in df_raw.columns:
                df_final["url"] = df_raw["url"]
            else:
                df_final["url"] = ""
                
            # ジャーナル名の処理
            if "secondary_title" in df_raw.columns:
                df_final["journal"] = df_raw["secondary_title"]
            elif "alternate_title3" in df_raw.columns:
                df_final["journal"] = df_raw["alternate_title3"]
            elif "alternate_title2" in df_raw.columns:
                df_final["journal"] = df_raw["alternate_title2"]
            else:
                df_final["journal"] = ""
                
            # 発行年の処理
            if "year" in df_raw.columns:
                df_final["year"] = df_raw["year"]
            elif "publication_year" in df_raw.columns:
                df_final["year"] = df_raw["publication_year"]
            else:
                df_final["year"] = ""
                
            # その他のフィールドは空のままにする
            df_final["issn"] = df_raw["issn"] if "issn" in df_raw.columns else ""
            df_final["volume"] = df_raw["volume"] if "volume" in df_raw.columns else ""
            df_final["issue"] = df_raw["number"] if "number" in df_raw.columns else df_raw["issue"] if "issue" in df_raw.columns else ""
            df_final["pages"] = df_raw["pages"] if "pages" in df_raw.columns else ""
            df_final["publisher"] = df_raw["publisher"] if "publisher" in df_raw.columns else ""
            df_final["notes"] = df_raw["notes"] if "notes" in df_raw.columns else ""
            df_final["keywords"] = df_raw["keywords"] if "keywords" in df_raw.columns else ""
        
        # key列に一意なIDを付与
        file_stem = Path(ris_path).stem
        df_final["key"] = [f"RIS_{file_stem}_{i+1}" for i in range(len(df_final))]
        
        # 欠損値を空文字列に変換
        df_final = df_final.fillna("")
        
        return df_final
    
    except Exception as e:
        print(f"RISファイル処理エラー ({ris_path}): {str(e)}")
        return pd.DataFrame(columns=final_columns)

def process_ris_files(ris_file_paths):
    """
    複数のRISファイルを処理し、一つのDataFrameに統合する
    
    Parameters:
    ----------
    ris_file_paths : list of str
        処理するRISファイルのパスリスト
        
    Returns:
    -------
    tuple
        (統合されたDataFrame, ファイルごとの件数を含む辞書)
    """
    all_dfs = []
    counts = {}
    
    for path in ris_file_paths:
        try:
            df = ris_df_parser(path)
            if not df.empty:
                all_dfs.append(df)
                file_name = Path(path).name
                counts[file_name] = len(df)
                print(f"  {file_name}: {len(df)}件 読み込み完了")
        except Exception as e:
            print(f"  エラー: {Path(path).name} の処理中にエラーが発生しました - {e}")
    
    if not all_dfs:
        return pd.DataFrame(), counts
    
    return pd.concat(all_dfs, ignore_index=True), counts

# --- ClinicalTrials.gov CSV処理 ---
def clinicaltrials_csv_parser(csv_path):
    """
    ClinicalTrials.gov CSVファイルを読み込み、標準化されたDataFrameに変換する
    
    Parameters:
    ----------
    csv_path : str
        ClinicalTrials.gov CSVファイルのパス
        
    Returns:
    -------
    pandas.DataFrame
        Rayyan互換形式のDataFrame
    """
    try:
        # CSVファイルの読み込み
        df_ctg_raw = pd.read_csv(csv_path, encoding='utf-8', errors='ignore')
        
        # 最終的な列の順序を定義
        final_columns = [
            "key", "title", "authors", "journal", "issn", "volume", "issue",
            "pages", "year", "publisher", "url", "abstract", "notes", "doi", "keywords"
        ]
        
        # 空のDataFrameを作成
        df_final = pd.DataFrame(index=range(len(df_ctg_raw)), columns=final_columns)
        
        # タイトルとURL
        df_final['title'] = df_ctg_raw.get('Study Title', '')
        df_final['url'] = df_ctg_raw.get('Study URL', '')
        
        # 抄録の作成（複数の列を結合）
        abstract_components = []
        
        if 'Conditions' in df_ctg_raw.columns:
            abstract_components.append("Conditions: " + df_ctg_raw['Conditions'].astype(str))
        
        if 'Interventions' in df_ctg_raw.columns:
            abstract_components.append("Interventions: " + df_ctg_raw['Interventions'].astype(str))
        
        if 'Primary Outcome Measures' in df_ctg_raw.columns:
            abstract_components.append("Primary Outcome Measures: " + df_ctg_raw['Primary Outcome Measures'].astype(str))
        
        if 'Brief Summary' in df_ctg_raw.columns:
            abstract_components.append("Brief Summary: " + df_ctg_raw['Brief Summary'].astype(str))
        
        if 'Sex' in df_ctg_raw.columns:
            abstract_components.append("Sex: " + df_ctg_raw['Sex'].astype(str))
        
        if 'Age' in df_ctg_raw.columns:
            abstract_components.append("Age: " + df_ctg_raw['Age'].astype(str))
        
        if 'Study Type' in df_ctg_raw.columns:
            abstract_components.append("Study Type: " + df_ctg_raw['Study Type'].astype(str))
        
        if 'Study Design' in df_ctg_raw.columns:
            abstract_components.append("Study Design: " + df_ctg_raw['Study Design'].astype(str))
        
        # 抄録の作成
        df_final['abstract'] = " | ".join(abstract_components)
        
        # ジャーナル名はClinicalTrials.govで固定
        df_final['journal'] = "ClinicalTrials.gov"
        
        # 開始日から年を抽出
        if 'Start Date' in df_ctg_raw.columns:
            try:
                df_final['year'] = pd.to_datetime(df_ctg_raw['Start Date'], errors='coerce').dt.year.fillna('').astype(str)
            except Exception:
                df_final['year'] = ""
        
        # その他のフィールドは空文字で埋める
        df_final['authors'] = ""
        df_final['issn'] = ""
        df_final['volume'] = ""
        df_final['issue'] = ""
        df_final['pages'] = ""
        df_final['publisher'] = ""
        df_final['notes'] = ""
        df_final['doi'] = ""
        df_final['keywords'] = ""
        
        # key列に一意なIDを付与
        file_stem = Path(csv_path).stem
        df_final["key"] = [f"CTG_{file_stem}_{i+1}" for i in range(len(df_final))]
        
        # 欠損値を空文字列に変換
        df_final = df_final.fillna("")
        
        return df_final
    
    except Exception as e:
        print(f"ClinicalTrials.gov CSVファイル処理エラー ({csv_path}): {str(e)}")
        return pd.DataFrame(columns=final_columns)

def process_clinicaltrials_files(csv_file_paths):
    """
    複数のClinicalTrials.gov CSVファイルを処理し、一つのDataFrameに統合する
    
    Parameters:
    ----------
    csv_file_paths : list of str
        処理するClinicalTrials.gov CSVファイルのパスリスト
        
    Returns:
    -------
    tuple
        (統合されたDataFrame, ファイルごとの件数を含む辞書)
    """
    all_dfs = []
    counts = {}
    
    for path in csv_file_paths:
        try:
            df = clinicaltrials_csv_parser(path)
            if not df.empty:
                all_dfs.append(df)
                file_name = Path(path).name
                counts[file_name] = len(df)
                print(f"  {file_name}: {len(df)}件 読み込み完了")
        except Exception as e:
            print(f"  エラー: {Path(path).name} の処理中にエラーが発生しました - {e}")
    
    if not all_dfs:
        return pd.DataFrame(), counts
    
    return pd.concat(all_dfs, ignore_index=True), counts

# --- ICTRP XML処理 ---
def ictrp_xml_parser(xml_path):
    """
    ICTRP XMLファイルを読み込み、標準化されたDataFrameに変換する
    
    Parameters:
    ----------
    xml_path : str
        ICTRP XMLファイルのパス
        
    Returns:
    -------
    pandas.DataFrame
        Rayyan互換形式のDataFrame
    """
    try:
        # XMLファイルの解析
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # 抽出する変数
        variables = [
            "TrialID", "Scientific_title", "web_address", "Study_design", 
            "Condition", "Intervention", "Source_Register", "Date_registration"
        ]
        
        # データを抽出して辞書のリストとして保存
        data_list = []
        
        for trial in root.findall(".//Trial"):
            trial_data = {}
            
            for var in variables:
                elem = trial.find(f".//{var}")
                trial_data[var] = elem.text.strip() if elem is not None and elem.text else "unclear"
            
            data_list.append(trial_data)
        
        # DataFrameに変換
        if not data_list:
            return pd.DataFrame()
            
        df_raw = pd.DataFrame(data_list)
        
        # 最終的な列の順序を定義
        final_columns = [
            "key", "title", "authors", "journal", "issn", "volume", "issue",
            "pages", "year", "publisher", "url", "abstract", "notes", "doi", "keywords"
        ]
        
        # 空のDataFrameを作成
        df_final = pd.DataFrame(index=range(len(df_raw)), columns=final_columns)
        
        # タイトルとURL
        df_final['title'] = df_raw.get('Scientific_title', '')
        df_final['url'] = df_raw.get('web_address', '')
        
        # 抄録の作成（条件、介入、研究デザインを結合）
        # 条件とインターベンションを組み合わせて抄録とする
        abstract_parts = []
        
        for idx, row in df_raw.iterrows():
            condition = row.get('Condition', 'unclear')
            intervention = row.get('Intervention', 'unclear')
            design = row.get('Study_design', 'unclear')
            
            parts = []
            if condition != 'unclear':
                parts.append(f'Condition: {condition}')
            if intervention != 'unclear':
                parts.append(f'Intervention: {intervention}')
            if design != 'unclear':
                parts.append(f'Study_design: {design}')
                
            abstract_parts.append(' | '.join(parts))
        
        df_final['abstract'] = abstract_parts
        
        # ジャーナル名はICTRPで固定
        df_final['journal'] = 'ICTRP'
        
        # 登録日から年を抽出
        if 'Date_registration' in df_raw.columns:
            try:
                df_final['year'] = pd.to_datetime(df_raw['Date_registration'], errors='coerce').dt.year.fillna('').astype(str)
            except Exception:
                df_final['year'] = ''
        
        # レジストリソースをISSNとして利用
        df_final['issn'] = df_raw.get('Source_Register', '')
        
        # その他のフィールドは空文字で埋める
        df_final['authors'] = ''
        df_final['volume'] = ''
        df_final['issue'] = ''
        df_final['pages'] = ''
        df_final['publisher'] = ''
        df_final['notes'] = ''
        df_final['doi'] = ''
        df_final['keywords'] = ''
        
        # key列に一意なIDを付与
        file_stem = Path(xml_path).stem
        df_final["key"] = [f"ICTRP_{file_stem}_{i+1}" for i in range(len(df_final))]
        
        # 欠損値を空文字列に変換
        df_final = df_final.fillna("")
        
        return df_final
        
    except Exception as e:
        print(f"ICTRP XMLファイル処理エラー ({xml_path}): {str(e)}")
        return pd.DataFrame(columns=final_columns)

def process_ictrp_files(xml_file_paths):
    """
    複数のICTRP XMLファイルを処理し、一つのDataFrameに統合する
    
    Parameters:
    ----------
    xml_file_paths : list of str
        処理するICTRP XMLファイルのパスリスト
        
    Returns:
    -------
    tuple
        (統合されたDataFrame, ファイルごとの件数を含む辞書)
    """
    all_dfs = []
    counts = {}
    
    for path in xml_file_paths:
        try:
            df = ictrp_xml_parser(path)
            if not df.empty:
                all_dfs.append(df)
                file_name = Path(path).name
                counts[file_name] = len(df)
                print(f"  {file_name}: {len(df)}件 読み込み完了")
        except Exception as e:
            print(f"  エラー: {Path(path).name} の処理中にエラーが発生しました - {e}")
    
    if not all_dfs:
        return pd.DataFrame(), counts
    
    return pd.concat(all_dfs, ignore_index=True), counts
