#!/usr/bin/env python3

import argparse

def get_indent_level(line):
    return len(line) - len(line.lstrip(' '))

def convert_with_braces(lines):
    result = []
    indent_stack = [0]

    for i, line in enumerate(lines):
        stripped = line.rstrip()
        curr_indent = get_indent_level(stripped)

        # 空行处理
        if stripped.strip() == '':
            result.append('')
            continue

        # 结束代码块时
        while curr_indent < indent_stack[-1]:
            if result and result[-1].strip() == '':
                result.pop()
            indent_stack.pop()
            result.append(' ' * indent_stack[-1] + '}')

        # 开始新代码块时
        if curr_indent > indent_stack[-1]:
            result.append(' ' * indent_stack[-1] + '{')
            indent_stack.append(curr_indent)

        result.append(stripped)

    # 关闭所有未闭合代码块
    while len(indent_stack) > 1:
        if result and result[-1].strip() == '':
            result.pop()
        indent_stack.pop()
        result.append(' ' * indent_stack[-1] + '}')

    return result

def main():
    parser = argparse.ArgumentParser(description="Convert indentation-based pseudo code to brace-style blocks.")
    parser.add_argument('-i', '--input', required=True, help='Input pseudo code file')
    parser.add_argument('-o', '--output', help='Output file (if not provided, prints to stdout)')

    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    clean_lines = [line.rstrip('\n') for line in lines]
    converted = convert_with_braces(clean_lines)

    output_text = '\n'.join(converted) + '\n'

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_text)
    else:
        print(output_text)


if __name__ == "__main__":
    main()
