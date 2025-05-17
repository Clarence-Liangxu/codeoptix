#!/usr/bin/env python3

import os
import json
import asyncio
import argparse
from pathlib import Path
from tqdm.asyncio import tqdm
from playwright.async_api import async_playwright


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


async def fetch_single(page, name, url, output_path, fail_log_path):
    try:
        await page.goto(url, timeout=20000)
        await page.wait_for_selector("section.code-operations", timeout=3000)
        section = await page.query_selector("section.code-operations")
        code_block = await section.query_selector("div.code-block") if section else None
        if not code_block:
            raise ValueError("Missing pseudocode block")

        pseudocode = await code_block.inner_text()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(pseudocode)
        return True

    except Exception as e:
        async with asyncio.Lock():
            with open(fail_log_path, "a") as logf:
                logf.write(f"{name} | {url}\n")
        return False


async def run(args):
    with open(args.input, "r") as f:
        data = json.load(f)
    all_intrinsics = collect_all_intrinsics(data)

    tasks = []
    already_fetched = 0
    for name, url, subdir in all_intrinsics:
        output_path = Path(args.output) / subdir / f"{name}.pseudo"
        if output_path.exists() and output_path.stat().st_size > 0:
            already_fetched += 1
            continue
        tasks.append((name, url, output_path))

    print(f"📦 Total intrinsics in JSON:      {len(all_intrinsics)}")
    print(f"📥 New to fetch (available):      {len(tasks)}")
    print(f"📁 Already fetched locally:       {already_fetched}\n")

    if not tasks or args.limit == 0:
        print("✅ No new intrinsics to fetch.")
        return

    success_count = 0
    fail_count = 0
    open(args.log, "w").close()

    sem = asyncio.Semaphore(args.concurrency)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        progress = tqdm(total=args.limit, desc="🚀 Downloading pseudocode")

        async def worker(name, url, output_path):
            nonlocal success_count, fail_count
            async with sem:
                if success_count >= args.limit:
                    return
                ok = await fetch_single(page, name, url, output_path, args.log)
                if ok:
                    success_count += 1
                    progress.update(1)
                else:
                    fail_count += 1

        for name, url, output_path in tasks:
            if success_count >= args.limit:
                break
            await worker(name, url, output_path)

        await browser.close()
        progress.close()

    print(f"\n✅ Fetched {success_count} successfully")
    print(f"❌ Failed to fetch {fail_count}")
    if fail_count > 0:
        print(f"📄 Failures logged to: {args.log}")


def main():
    parser = argparse.ArgumentParser(description="Async fetch of ARM intrinsics pseudocode.")
    parser.add_argument("-i", "--input", required=True, help="Input advsimd.json file")
    parser.add_argument("-o", "--output", required=True, help="Output directory")
    parser.add_argument("--limit", type=int, default=20, help="Number of successful fetches")
    parser.add_argument("--concurrency", type=int, default=4, help="Concurrent fetches at a time")
    parser.add_argument("--log", type=str, default="failed.log", help="Log file for failures")
    args = parser.parse_args()
    asyncio.run(run(args))


if __name__ == "__main__":
    main()
