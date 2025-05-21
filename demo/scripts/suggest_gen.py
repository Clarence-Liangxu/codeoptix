import argparse
import os
import re

# 硬编码可扩展的建议模板
SUGGESTIONS = {
    "vaddq_s8": {
        "type": "int8_t",
        "lanes": 16,
        "code": [
            "int8x16_t va = vld1q_s8(a);",
            "int8x16_t vb = vld1q_s8(b);",
            "int8x16_t vc = vaddq_s8(va, vb);",
            "vst1q_s8(c, vc);"
        ]
    },
    # 可添加更多 intrinsic 建议模板
}

def generate_suggestion(csv_file, output_file=None):
    if not os.path.exists(csv_file):
        print(f"[✗] Match file not found: {csv_file}")
        return

    with open(csv_file) as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        print("[!] Match file is empty.")
        return

    results = []
    for line in lines:
        func, loop, typ, intrinsic = line.split("\t")
        entry = SUGGESTIONS.get(intrinsic)
        if not entry:
            results.append(f"⚠ 未知 intrinsic: {intrinsic}，请手动处理")
            continue

        results.append(f"函数 {func} 中的循环 {loop} 可替换为 {intrinsic} 实现：\n建议代码：")
        results.extend([f"  {stmt}" for stmt in entry["code"]])
        results.append("")

    output = "\n".join(results)

    if output_file:
        with open(output_file, "w") as f:
            f.write(output)
        print(f"[✔] 建议已写入 {output_file}")
    else:
        print(output)

def main():
    parser = argparse.ArgumentParser(description="Generate SIMD optimization suggestions")
    parser.add_argument("-i", "--input", required=True, help="Path to match_<intrinsic>.csv")
    parser.add_argument("-o", "--output", help="Optional output file for suggestions")
    args = parser.parse_args()

    generate_suggestion(args.input, args.output)

if __name__ == "__main__":
    main()
