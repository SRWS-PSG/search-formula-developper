#!/usr/bin/env python3
"""
RIS File Deduplication Script

複数のRISファイルを読み込み、タイトルのExact Matchで重複を削除し、
統合されたRISファイルを出力するスクリプト。

Usage:
    python deduplicate_ris.py --input file1.ris file2.ris --output merged.ris --log dedup_log.txt
"""

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class RISRecord:
    """RISレコードを表すデータクラス"""
    raw_lines: list[str] = field(default_factory=list)
    tags: dict = field(default_factory=dict)
    source_file: str = ""
    
    def get_title(self) -> Optional[str]:
        """タイトルを取得（TI または T1 タグ）"""
        return self.tags.get("TI") or self.tags.get("T1")
    
    def to_ris_string(self) -> str:
        """RIS形式の文字列に変換"""
        return "\n".join(self.raw_lines)


class RISParser:
    """RISファイルパーサー"""
    
    # RISタグの正規表現（タグ名 + 区切り + 値）
    TAG_PATTERN = re.compile(r'^([A-Z][A-Z0-9]{0,3})\s{0,2}-\s{0,2}(.*)$')
    
    def __init__(self):
        self.records: list[RISRecord] = []
    
    def parse_file(self, filepath: Path) -> list[RISRecord]:
        """RISファイルをパースしてレコードのリストを返す"""
        records = []
        current_record = None
        current_lines = []
        
        # エンコーディングを試行
        encodings = ['utf-8', 'utf-8-sig', 'cp1252', 'latin-1']
        content = None
        
        for encoding in encodings:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            raise ValueError(f"ファイルを読み込めませんでした: {filepath}")
        
        lines = content.splitlines()
        
        for line in lines:
            line = line.rstrip('\r\n')
            
            match = self.TAG_PATTERN.match(line)
            if match:
                tag, value = match.groups()
                
                if tag == "TY":
                    # 新しいレコードの開始
                    if current_record is not None:
                        records.append(current_record)
                    current_record = RISRecord(source_file=str(filepath))
                    current_lines = [line]
                    current_record.tags["TY"] = value.strip()
                    
                elif tag == "ER":
                    # レコードの終了
                    if current_record is not None:
                        current_lines.append(line)
                        current_record.raw_lines = current_lines
                        records.append(current_record)
                        current_record = None
                        current_lines = []
                        
                elif current_record is not None:
                    current_lines.append(line)
                    # 複数値タグの場合は最初の値を保持
                    if tag not in current_record.tags:
                        current_record.tags[tag] = value.strip()
            else:
                # タグのない行（継続行など）
                if current_record is not None:
                    current_lines.append(line)
        
        # 最後のレコード（ERタグなしで終わる場合）
        if current_record is not None:
            current_record.raw_lines = current_lines
            records.append(current_record)
        
        return records


class TitleNormalizer:
    """タイトル正規化クラス"""
    
    # 角括弧とその内容を削除する正規表現
    BRACKET_PATTERN = re.compile(r'\[.*?\]')
    # 複数スペースを単一スペースに
    MULTI_SPACE_PATTERN = re.compile(r'\s+')
    
    @classmethod
    def normalize(cls, title: Optional[str]) -> str:
        """タイトルを正規化"""
        if not title:
            return ""
        
        # 角括弧とその内容を削除
        normalized = cls.BRACKET_PATTERN.sub('', title)
        # 小文字化
        normalized = normalized.lower()
        # 複数スペースを単一スペースに
        normalized = cls.MULTI_SPACE_PATTERN.sub(' ', normalized)
        # 前後の空白を除去
        normalized = normalized.strip()
        
        return normalized


@dataclass
class DuplicateInfo:
    """重複情報を保持するデータクラス"""
    original_title: str
    normalized_title: str
    sources: list[tuple[str, RISRecord]] = field(default_factory=list)  # (source_file, record)


class DeduplicationEngine:
    """重複削除エンジン"""
    
    def __init__(self, strategy: str = "keep-first"):
        self.strategy = strategy
        self.title_to_records: dict[str, list[tuple[str, RISRecord]]] = defaultdict(list)
        self.all_records: list[tuple[str, RISRecord]] = []
    
    def add_records(self, records: list[RISRecord], source_file: str):
        """レコードを追加"""
        for record in records:
            title = record.get_title()
            if title:
                normalized = TitleNormalizer.normalize(title)
                self.title_to_records[normalized].append((source_file, record))
                self.all_records.append((source_file, record))
    
    def find_duplicates(self) -> list[DuplicateInfo]:
        """重複を検出"""
        duplicates = []
        
        for normalized_title, records in self.title_to_records.items():
            if len(records) > 1:
                # 最初のレコードから元のタイトルを取得
                original_title = records[0][1].get_title() or ""
                dup_info = DuplicateInfo(
                    original_title=original_title,
                    normalized_title=normalized_title,
                    sources=records
                )
                duplicates.append(dup_info)
        
        return duplicates
    
    def get_unique_records(self) -> list[RISRecord]:
        """ユニークなレコードを取得（keep-first戦略）"""
        seen_titles = set()
        unique_records = []
        
        for source_file, record in self.all_records:
            title = record.get_title()
            if not title:
                # タイトルがないレコードはそのまま含める
                unique_records.append(record)
                continue
            
            normalized = TitleNormalizer.normalize(title)
            if normalized not in seen_titles:
                seen_titles.add(normalized)
                unique_records.append(record)
        
        return unique_records


class RISWriter:
    """RISファイル書き出しクラス"""
    
    @staticmethod
    def write(records: list[RISRecord], filepath: Path):
        """レコードをRIS形式で書き出し"""
        with open(filepath, 'w', encoding='utf-8') as f:
            for i, record in enumerate(records):
                f.write(record.to_ris_string())
                f.write("\n")
                # レコード間に空行を追加（最後のレコード以外）
                if i < len(records) - 1:
                    f.write("\n")


class DeduplicationLogger:
    """ログ出力クラス"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.log_lines: list[str] = []
    
    def log(self, message: str, print_to_console: bool = True):
        """ログメッセージを追加"""
        self.log_lines.append(message)
        if print_to_console and self.verbose:
            print(message)
    
    def generate_report(
        self,
        input_files: list[Path],
        file_record_counts: dict[str, int],
        duplicates: list[DuplicateInfo],
        output_count: int,
        output_file: Path
    ) -> str:
        """レポートを生成"""
        lines = []
        separator = "=" * 80
        
        lines.append(separator)
        lines.append("RIS Deduplication Log")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(separator)
        lines.append("")
        
        # 入力ファイル情報
        lines.append("INPUT FILES:")
        total_input = 0
        for i, filepath in enumerate(input_files, 1):
            count = file_record_counts.get(str(filepath), 0)
            total_input += count
            lines.append(f"  [{i}] {filepath.name}: {count} records")
        lines.append(f"  TOTAL INPUT: {total_input} records")
        lines.append("")
        
        # 重複削除結果
        duplicates_removed = total_input - output_count
        lines.append("DEDUPLICATION RESULTS:")
        lines.append(f"  Unique records: {output_count}")
        lines.append(f"  Duplicates removed: {duplicates_removed}")
        lines.append("")
        
        # 重複ペアの詳細
        if duplicates:
            lines.append("DUPLICATE PAIRS:")
            for dup in duplicates:
                # タイトルを短縮
                title_display = dup.original_title[:70] + "..." if len(dup.original_title) > 70 else dup.original_title
                lines.append(f"  [{title_display}]")
                sources = [Path(s[0]).stem for s in dup.sources]
                lines.append(f"    - Found in: {', '.join(sources)}")
                lines.append(f"    - Kept: {sources[0]} (first occurrence)")
                lines.append("")
        
        # 出力情報
        lines.append("OUTPUT:")
        lines.append(f"  File: {output_file.name}")
        lines.append(f"  Records: {output_count}")
        lines.append(separator)
        
        return "\n".join(lines)
    
    def save_log(self, filepath: Path, report: str):
        """ログをファイルに保存"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)


def main():
    parser = argparse.ArgumentParser(
        description="RISファイルの重複削除ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  python deduplicate_ris.py --input file1.ris file2.ris --output merged.ris
  python deduplicate_ris.py -i *.ris -o output.ris -l log.txt -v
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        nargs='+',
        required=True,
        type=Path,
        help='入力RISファイル（複数可）'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=Path,
        default=Path('deduplicated.ris'),
        help='出力RISファイル（デフォルト: deduplicated.ris）'
    )
    
    parser.add_argument(
        '-l', '--log',
        type=Path,
        default=Path('dedup_log.txt'),
        help='ログファイルパス（デフォルト: dedup_log.txt）'
    )
    
    parser.add_argument(
        '-s', '--strategy',
        choices=['keep-first'],
        default='keep-first',
        help='重複時の保持戦略（デフォルト: keep-first）'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='詳細出力を有効化'
    )
    
    args = parser.parse_args()
    
    # ロガー初期化
    logger = DeduplicationLogger(verbose=args.verbose)
    
    # 入力ファイルの存在確認
    for filepath in args.input:
        if not filepath.exists():
            print(f"エラー: ファイルが見つかりません: {filepath}", file=sys.stderr)
            sys.exit(1)
    
    print(f"処理開始: {len(args.input)} ファイル")
    
    # RISパーサーとエンジン初期化
    ris_parser = RISParser()
    engine = DeduplicationEngine(strategy=args.strategy)
    file_record_counts: dict[str, int] = {}
    
    # ファイルを順次読み込み
    for filepath in args.input:
        print(f"  読み込み中: {filepath.name}...", end=" ")
        try:
            records = ris_parser.parse_file(filepath)
            file_record_counts[str(filepath)] = len(records)
            engine.add_records(records, str(filepath))
            print(f"{len(records)} records")
        except Exception as e:
            print(f"エラー: {e}", file=sys.stderr)
            sys.exit(1)
    
    # 重複検出
    print("重複検出中...")
    duplicates = engine.find_duplicates()
    
    # ユニークレコード取得
    unique_records = engine.get_unique_records()
    
    # 出力
    print(f"出力中: {args.output}...")
    RISWriter.write(unique_records, args.output)
    
    # レポート生成
    report = logger.generate_report(
        input_files=args.input,
        file_record_counts=file_record_counts,
        duplicates=duplicates,
        output_count=len(unique_records),
        output_file=args.output
    )
    
    # ログ保存
    logger.save_log(args.log, report)
    
    # サマリー出力
    total_input = sum(file_record_counts.values())
    print("")
    print("=" * 60)
    print(f"入力: {total_input} records")
    print(f"重複: {len(duplicates)} タイトル ({total_input - len(unique_records)} records)")
    print(f"出力: {len(unique_records)} records")
    print(f"ログ: {args.log}")
    print("=" * 60)


if __name__ == "__main__":
    main()
