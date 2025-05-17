#!/usr/bin/env python3

import os
import json
import argparse
from pathlib import Path
from tqdm import tqdm
from multiprocessing import Pool
from playwright.sync_api import sync_playwright


def fetch_pseudocode(task):
    name, url, output_path = task
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()

            # 🛠 更稳健的页面加载方式（无networkidle）
            page.goto(url, timeout=20000)
            page.wait_for_selector("section.code-operations", timeout=3000)

            section = page.query_selector("section.code-operations")
            code_block = section.query_selector("div.code-block") if section else None

            if code_block:
                pseudocode = code_block.inner_text()
            else:
                pseudocode = "// ❌ Pseudocode block not found"

            browser.close()

    except Exception as e:
        pseudocode = f"// ❌ Failed to fetch: {url}\n// {str(e)}"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(pseudocode)


def collect_all_intrinsics(node, path_prefix=[]):
    entries = []
    if isinstance(node, list):
        for intrinsic in node:
            name = intrinsic["name"]
            url = intrinsic["url"]
            subdir = Path(*path_prefix)
            entries.append((name, url, subdir))
    elif isinstance(node, dict):
        for key, value in node.items():
            entries.extend(collect_all_intrinsics(value, path_prefix + [key.replace(" ", "_")]))
    return entries


def main():
    parser = argparse.ArgumentParser(description="Fetch ARM intrinsic pseudocode (safe and parallel).")
    parser.add_argument("-i", "--input", required=True, help="Path to advsimd.json")
    parser.add_argument("-o", "--output", required=True, help="Output directory for .pseudo files")
    parser.add_argument("-t", "--threads", type=int, default=4, help="Number of parallel processes")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        data = json.load(f)

    all_intrinsics = collect_all_intrinsics(data)

    tasks = []
    for name, url, subdir in all_intrinsics:
        output_path = Path(args.output) / subdir / f"{name}.pseudo"
        tasks.append((name, url, output_path))

    with Pool(processes=args.threads) as pool:
        list(tqdm(pool.imap_unordered(fetch_pseudocode, tasks), total=len(tasks), desc="🚀 Downloading pseudocode"))


if __name__ == "__main__":
    main()
