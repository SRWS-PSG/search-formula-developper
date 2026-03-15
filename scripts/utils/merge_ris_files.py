#!/usr/bin/env python3
"""
Merge multiple RIS files and remove duplicates based on ID field
"""

import argparse
from pathlib import Path
from typing import List, Set


def parse_ris_file(filepath: str) -> List[dict]:
    """Parse RIS file into list of record dictionaries (handles both standard and AIO formats)"""
    records = []
    current_record = {}
    current_field = None

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            stripped_line = line.strip()

            # Handle TY tag (with or without indentation)
            if stripped_line.startswith('TY  - ') or stripped_line.startswith('TY  -'):
                current_record = {'TY': stripped_line.split('  - ', 1)[1] if '  - ' in stripped_line else stripped_line[4:].strip()}
                current_field = 'TY'
            # Handle ER tag (with or without hyphen and indentation)
            elif stripped_line.startswith('ER  -') or stripped_line == 'ER':
                if current_record:
                    records.append(current_record)
                    current_record = {}
                    current_field = None
            # Handle field tags (allowing for indentation)
            elif stripped_line and '  ' in stripped_line:
                parts = stripped_line.split('  ', 1)
                if len(parts) == 2 and len(parts[0]) <= 4:
                    tag = parts[0].strip()
                    value = parts[1].lstrip('- ').strip()
                    current_field = tag

                    if tag in current_record:
                        if isinstance(current_record[tag], list):
                            current_record[tag].append(value)
                        else:
                            current_record[tag] = [current_record[tag], value]
                    else:
                        current_record[tag] = value

    # Don't forget last record if file doesn't end with ER
    if current_record:
        records.append(current_record)

    return records


def write_ris_file(records: List[dict], filepath: str):
    """Write records to RIS file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        for record in records:
            # Always start with TY
            f.write(f"TY  - {record.get('TY', 'JOUR')}\n")

            # Write other fields in a consistent order
            field_order = ['ID', 'TI', 'AU', 'AB', 'PY', 'JF', 'JO', 'VL', 'IS', 'SP', 'EP',
                          'DO', 'SN', 'KW', 'UR', 'N1', 'N2']

            for field in field_order:
                if field in record and field != 'TY':
                    values = record[field] if isinstance(record[field], list) else [record[field]]
                    for value in values:
                        f.write(f"{field}  - {value}\n")

            # Write any remaining fields
            for field, value in record.items():
                if field not in field_order and field != 'TY':
                    values = value if isinstance(value, list) else [value]
                    for val in values:
                        f.write(f"{field}  - {val}\n")

            f.write("ER  -\n\n")


def merge_ris_files(input_files: List[str], output_file: str) -> dict:
    """Merge multiple RIS files and remove duplicates"""
    all_records = []
    seen_ids: Set[str] = set()
    stats = {
        'total_input': 0,
        'duplicates': 0,
        'unique': 0
    }

    for input_file in input_files:
        records = parse_ris_file(input_file)
        stats['total_input'] += len(records)

        for record in records:
            record_id = record.get('ID', '')

            if record_id and record_id in seen_ids:
                stats['duplicates'] += 1
                continue

            all_records.append(record)
            if record_id:
                seen_ids.add(record_id)

    stats['unique'] = len(all_records)

    # Write merged file
    write_ris_file(all_records, output_file)

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Merge multiple RIS files and remove duplicates based on ID field"
    )
    parser.add_argument(
        'input_files',
        nargs='+',
        help='Input RIS files to merge'
    )
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output merged RIS file'
    )

    args = parser.parse_args()

    print("Merging RIS files...")
    print(f"Input files: {', '.join(args.input_files)}")
    print(f"Output file: {args.output}")
    print()

    stats = merge_ris_files(args.input_files, args.output)

    print(f"Total input records: {stats['total_input']}")
    print(f"Duplicates removed: {stats['duplicates']}")
    print(f"Unique records: {stats['unique']}")
    print(f"\nMerged file saved: {args.output}")


if __name__ == '__main__':
    main()
