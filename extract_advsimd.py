#!/usr/bin/env python3

import re
import json
import argparse
import html
from bs4 import BeautifulSoup


def clean_html_cell(cell_content):
    """通用字段清洗：清除 <br>、HTML实体、反引号、换行、多余空格"""
    soup = BeautifulSoup(cell_content, "html.parser")

    for br in soup.find_all("br"):
        br.replace_with("; ")

    text = soup.get_text()
    text = html.unescape(text)
    text = text.replace('`', '')
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def clean_intrinsic_signature(cell_content):
    """专用于清洗函数签名：移除 <br> / ; / 多余符号"""
    soup = BeautifulSoup(cell_content, "html.parser")

    for br in soup.find_all("br"):
        br.replace_with(" ")  # 不加分号

    text = soup.get_text()
    text = html.unescape(text)
    text = text.replace('`', '')
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)

    # 修复函数参数前的 ; 问题
    text = re.sub(r'\(\s*;\s*', '(', text)
    text = re.sub(r'\(\s+', '(', text)
    text = text.replace(';', '')
    text = text.replace(',)', ')')
    return text.strip()


def extract_intrinsic_and_url(cell_content):
    """从 HTML 中提取函数名、完整签名和 URL"""
    soup = BeautifulSoup(cell_content, "html.parser")
    code = soup.find('code')
    a_tag = code.find('a') if code else None
    if not a_tag:
        return "", "", ""
    func_name = a_tag.text.strip()
    func_url = a_tag.get('href', '')
    full_signature = clean_intrinsic_signature(code.decode_contents())
    return func_name, full_signature, func_url


def parse_with_structure(md_lines):
    """主解析逻辑：从 Markdown 中提取结构化数据（从 Basic intrinsics 开始）"""
    structured_data = {}
    current_h2 = None
    current_h3 = None
    inside_table = False
    headers = []
    parsing_started = False

    for line in md_lines:
        line = line.strip()

        if line.startswith("## ") and "Basic intrinsics" in line:
            parsing_started = True

        if not parsing_started:
            continue

        if line.startswith("## "):
            current_h2 = line[3:].strip()
            structured_data[current_h2] = {}
            current_h3 = None
            continue

        elif line.startswith("### "):
            current_h3 = line[4:].strip()
            if current_h2:
                structured_data[current_h2][current_h3] = []
            continue

        if line.startswith('|') and 'Intrinsic' in line and 'Instruction' in line:
            inside_table = True
            headers = [h.strip().lower().replace(" ", "_") for h in line.strip('|').split('|')]
            continue

        if inside_table and re.match(r"^\|\s*-+", line):
            continue

        if inside_table and line.startswith('|'):
            columns = [c.strip() for c in line.strip('|').split('|')]
            if len(columns) != len(headers):
                continue
            entry = {}
            for idx, col in enumerate(columns):
                key = headers[idx]
                if key == "intrinsic":
                    name, signature, url = extract_intrinsic_and_url(col)
                    entry["name"] = name
                    entry["intrinsic"] = signature
                    entry["url"] = url
                else:
                    entry[key] = clean_html_cell(col)

            if current_h2:
                if current_h3:
                    structured_data[current_h2][current_h3].append(entry)
                else:
                    structured_data[current_h2].setdefault("__root__", []).append(entry)
            continue

        if inside_table and not line.startswith('|'):
            inside_table = False

    # 删除空章节
    structured_data = {
        h2: h3_data for h2, h3_data in structured_data.items()
        if any(h3_data.values())
    }

    return structured_data


def flatten_structure(structured_data):
    """将嵌套结构转为扁平列表"""
    flat_list = []

    for h2_section in structured_data.values():
        if isinstance(h2_section, list):
            flat_list.extend(h2_section)
        elif isinstance(h2_section, dict):
            for section in h2_section.values():
                flat_list.extend(section)

    return flat_list


def main():
    parser = argparse.ArgumentParser(description="Extract ARM AdvSIMD Intrinsics from Markdown")
    parser.add_argument("-i", "--input", required=True, help="Input markdown file (e.g. advsimd.md)")
    parser.add_argument("-o", "--output", default="simd.json", help="Output JSON file")
    parser.add_argument("--flat", action="store_true", help="Flatten intrinsics to a list")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON with indentation")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        lines = f.readlines()

    structured_data = parse_with_structure(lines)
    output_data = flatten_structure(structured_data) if args.flat else structured_data

    with open(args.output, "w", encoding="utf-8") as f:
        if args.pretty:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        else:
            json.dump(output_data, f, separators=(',', ':'), ensure_ascii=False)

    print(f"✅ 提取完成，输出到 {args.output}，共提取 {len(flatten_structure(structured_data))} 条 intrinsic")


if __name__ == "__main__":
    main()
