import os
import argparse
import subprocess
import sys

def run_cmd(cmd, cwd=None):
    print(f"[+] $ {' '.join(cmd)}")
    result = subprocess.run(cmd, text=True, capture_output=True, cwd=cwd)
    if result.returncode != 0:
        print(result.stderr)
        sys.exit(1)
    return result.stdout

def main():
    parser = argparse.ArgumentParser(description="End-to-end pipeline: pseudo → .dl → facts → csv → suggestion")
    parser.add_argument("--pseudo", required=True, help="Path to .pseudo file")
    parser.add_argument("--json", required=True, help="Path to advsimd.json")
    parser.add_argument("--source", required=True, help="C file for fact extraction")
    parser.add_argument("--exporter", required=True, help="Path to FactExporter binary")
    args = parser.parse_args()

    base = os.path.splitext(os.path.basename(args.pseudo))[0]
    dl_file = f"rules/{base}.dl"
    csv_file = f"out/match_{base}.csv"
    suggestion_file = f"suggestions/{base}.txt"

    # Step 1: .pseudo → .dl
    run_cmd([
        sys.executable, "scripts/generate_dl_from_intrinsic.py",
        "-j", args.json,
        "-p", args.pseudo,
        "-o", "rules",
        "-g"
    ])

    # Step 2: 源码 → .facts
    os.makedirs("facts", exist_ok=True)
    run_cmd([args.exporter, args.source, "--", "-std=c++17"])

    # Step 3: .dl + .facts → .csv
    run_cmd([
        sys.executable, "scripts/run_souffle.py",
        "-d", dl_file,
        "-f", "facts",
        "-o", "out"
    ])

    # Step 4: .csv → 建议
    os.makedirs("suggestions", exist_ok=True)
    run_cmd([
        sys.executable, "scripts/suggest_gen.py",
        "-i", csv_file,
        "-o", suggestion_file
    ])

    print(f"[✔] 优化建议输出到：{suggestion_file}")

if __name__ == "__main__":
    main()
