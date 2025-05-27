#!/usr/bin/env python3

import argparse
import os
import concurrent.futures
import threading

log_lock = threading.Lock()
success_count = 0
fail_count = 0

def get_indent_level(line):
    return len(line) - len(line.lstrip(' '))

def convert_with_braces(lines):
    result = []
    indent_stack = [0]

    for i, line in enumerate(lines):
        stripped = line.rstrip()
        curr_indent = get_indent_level(stripped)

        if stripped.strip() == '':
            result.append('')
            continue

        while curr_indent < indent_stack[-1]:
            if result and result[-1].strip() == '':
                result.pop()
            indent_stack.pop()
            result.append(' ' * indent_stack[-1] + '}')

        if curr_indent > indent_stack[-1]:
            result.append(' ' * indent_stack[-1] + '{')
            indent_stack.append(curr_indent)

        result.append(stripped)

    while len(indent_stack) > 1:
        if result and result[-1].strip() == '':
            result.pop()
        indent_stack.pop()
        result.append(' ' * indent_stack[-1] + '}')

    return result

def process_file(input_path):
    global success_count, fail_count
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        clean_lines = [line.rstrip('\n') for line in lines]
        converted = convert_with_braces(clean_lines)
        output_text = '\n'.join(converted) + '\n'

        output_path = os.path.splitext(input_path)[0] + '.braces'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_text)

        with log_lock:
            success_count += 1
    except Exception as e:
        with log_lock:
            fail_count += 1
            with open("braces.log", "a", encoding="utf-8") as log_file:
                log_file.write(f"Failed: {input_path} — {e}\n")

def find_pseudo_files(directory):
    pseudo_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".pseudo"):
                pseudo_files.append(os.path.join(root, file))
    return pseudo_files

def main():
    parser = argparse.ArgumentParser(description="Convert indentation-based pseudo code to brace-style blocks.")
    parser.add_argument('-i', '--input', help='Input pseudo code file')
    parser.add_argument('-o', '--output', help='Output file (optional)')
    parser.add_argument('-d', '--directory', help='Process all .pseudo files in a directory recursively')

    args = parser.parse_args()

    if args.directory:
        pseudo_files = find_pseudo_files(args.directory)
        total_files = len(pseudo_files)

        if os.path.exists("braces.log"):
            os.remove("braces.log")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(process_file, pseudo_files)

        print(f"\nTotal .pseudo files found: {total_files}")
        print(f"Successfully processed: {success_count}")
        print(f"Failed to process: {fail_count}")
        if fail_count > 0:
            print("See 'braces.log' for error details.")
    elif args.input:
        output_path = args.output or os.path.splitext(args.input)[0] + '.braces'
        try:
            process_file(args.input)
            print(f"Processed: {args.input} -> {output_path}")
        except Exception as e:
            print(f"Error processing {args.input}: {e}")
    else:
        print("Error: Either --input or --directory must be specified.")

if __name__ == "__main__":
    main()
