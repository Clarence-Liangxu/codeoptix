import argparse
import os
import subprocess

def run_souffle(dl_file, fact_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    cmd = ["souffle", dl_file, "-F", fact_dir, "-D", out_dir]
    print(f"[+] Running Soufflé: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("[!] Soufflé execution failed:")
        print(result.stderr)
        return

    print("[✔] Soufflé analysis complete.\n")

    basename = os.path.splitext(os.path.basename(dl_file))[0]
    output_csv = os.path.join(out_dir, f"match_{basename}.csv")

    if os.path.exists(output_csv):
        print(f"[✓] Match result found in {output_csv}:\n")
        with open(output_csv) as f:
            print(f.read())
    else:
        print(f"[✗] No match result found: {output_csv} not generated.")

def main():
    parser = argparse.ArgumentParser(description="Run Soufflé analysis and display result")
    parser.add_argument("-d", "--dl", required=True, help="Path to .dl rule file")
    parser.add_argument("-f", "--facts", required=True, help="Directory containing .facts files")
    parser.add_argument("-o", "--out", required=True, help="Output directory for Soufflé .csv files")
    args = parser.parse_args()

    run_souffle(args.dl, args.facts, args.out)

if __name__ == "__main__":
    main()
