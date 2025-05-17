import os
import json
import argparse
from pathlib import Path
from tqdm import tqdm
from multiprocessing import Pool
from playwright.sync_api import sync_playwright


def fetch_pseudocode(task):
    name, url, output_path, log_path = task
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=20000)
            page.wait_for_selector("section.code-operations", timeout=3000)
            section = page.query_selector("section.code-operations")
            code_block = section.query_selector("div.code-block") if section else None

            if code_block:
                pseudocode = code_block.inner_text()
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(pseudocode)
                success = True
            else:
                raise ValueError("Pseudocode block not found")

            browser.close()

    except Exception as e:
        with open(log_path, "a") as logf:
            logf.write(f"{name} | {url}\n")
        success = False

    return success

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
    parser = argparse.ArgumentParser(description="Fetch ARM intrinsic pseudocode with stats and logging.")
    parser.add_argument("-i", "--input", required=True, help="Path to advsimd.json")
    parser.add_argument("-o", "--output", required=True, help="Output directory for .pseudo files")
    parser.add_argument("-t", "--threads", type=int, default=4, help="Number of parallel processes")
    parser.add_argument("--limit", type=int, default=None, help="Max number of new files to fetch")
    parser.add_argument("--log", type=str, default="failed.log", help="Failure log path")
    args = parser.parse_args()

    open(args.log, "w").close()  # 清空失败日志

    with open(args.input, "r") as f:
        data = json.load(f)

    all_intrinsics = collect_all_intrinsics(data)
    total = len(all_intrinsics)

    tasks = []
    already_fetched = 0
    for name, url, subdir in all_intrinsics:
        output_path = Path(args.output) / subdir / f"{name}.pseudo"
        if output_path.exists() and output_path.stat().st_size > 0:
            already_fetched += 1
            continue
        tasks.append((name, url, output_path, args.log))

    if args.limit:
        tasks = tasks[:args.limit]

    # 控制台统计信息
    print(f"📦 Total intrinsics in JSON:      {total}")
    print(f"📥 New to fetch this time:        {len(tasks)}")
    print(f"📁 Already fetched locally:       {already_fetched}\n")

    if not tasks:
        print("✅ No new intrinsics to fetch.")
        return

    with Pool(processes=args.threads) as pool:
        results = list(tqdm(pool.imap_unordered(fetch_pseudocode, tasks), total=len(tasks), desc="🚀 Downloading pseudocode"))

    success_count = sum(results)
    fail_count = len(results) - success_count

    print(f"\n✅ Fetched {success_count} successfully")
    print(f"❌ Failed to fetch {fail_count}")
    if fail_count > 0:
        print(f"📄 Failures logged to: {args.log}")


if __name__ == "__main__":
    main()
