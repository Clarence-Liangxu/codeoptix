#!/usr/bin/env python3

import argparse
import os
import hashlib
from collections import defaultdict

def hash_file(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def find_unique_files_by_content(directory):
    hash_to_files = defaultdict(list)
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.braces'):
                path = os.path.join(root, file)
                try:
                    file_hash = hash_file(path)
                    hash_to_files[file_hash].append(path)
                except Exception as e:
                    print(f"Error reading file {path}: {e}")
    return hash_to_files

def generate_report(hash_groups, report_path):
    with open(report_path, 'w', encoding='utf-8') as f:
        for idx, (file_hash, paths) in enumerate(hash_groups.items(), start=1):
            f.write(f"Group {idx} (Hash: {file_hash}):\n")
            for p in paths:
                f.write(f"  {p}\n")
            f.write('\n')
        f.write(f"Total unique file groups: {len(hash_groups)}\n")

def main():
    parser = argparse.ArgumentParser(description="Group .braces files by content.")
    parser.add_argument('-d', '--directory', required=True, help='Directory to scan for .braces files')
    parser.add_argument('-o', '--output', required=True, help='Output report file')

    args = parser.parse_args()

    hash_groups = find_unique_files_by_content(args.directory)
    generate_report(hash_groups, args.output)

    print(f"Total unique file contents: {len(hash_groups)}")
    print(f"Report saved to: {args.output}")

if __name__ == "__main__":
    main()
