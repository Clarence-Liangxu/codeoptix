import json
import argparse
import re
import os

def extract_intrinsic_name(pseudo_path):
    return os.path.splitext(os.path.basename(pseudo_path))[0]

def parse_json_metadata(json_path, intrinsic_name, debug=False):
    with open(json_path) as f:
        data = json.load(f)

    def warn(msg):
        if debug:
            print(f"[WARN] {msg}")

    for category in data.values():
        entries = []
        if isinstance(category, list):
            entries = category
        elif isinstance(category, dict):
            for sublist in category.values():
                if isinstance(sublist, list):
                    entries.extend(sublist)

        for item in entries:
            if item.get("name") == intrinsic_name:
                signature = item.get("intrinsic", "")
                if not signature:
                    warn(f"Missing 'intrinsic' field for {intrinsic_name}")

                # 推断 element_type
                element_type = "UNKNOWN"
                if "s8" in intrinsic_name:
                    element_type = "int8_t"
                elif "s16" in intrinsic_name:
                    element_type = "int16_t"
                elif "s32" in intrinsic_name:
                    element_type = "int32_t"
                elif "s64" in intrinsic_name:
                    element_type = "int64_t"
                elif "u8" in intrinsic_name:
                    element_type = "uint8_t"
                elif "u16" in intrinsic_name:
                    element_type = "uint16_t"
                elif "u32" in intrinsic_name:
                    element_type = "uint32_t"
                elif "u64" in intrinsic_name:
                    element_type = "uint64_t"
                elif "f32" in intrinsic_name:
                    element_type = "float"
                elif "f64" in intrinsic_name:
                    element_type = "double"
                else:
                    warn(f"Unable to infer element_type from name: {intrinsic_name}")

                # ✅ 使用正则准确提取 xN
                match = re.search(r"x(\d+)", signature)
                if match:
                    vector_size = int(match.group(1))
                else:
                    vector_size = 2
                    warn(f"Unable to infer vector_size from signature: '{signature}', defaulting to 2")

                if debug:
                    print(f"\n[DEBUG] Inferred metadata:")
                    print(f"{'-'*40}")
                    print(f"name         : {intrinsic_name}")
                    print(f"element_type : {element_type}")
                    print(f"vector_size  : {vector_size}")
                    print(f"intrinsic    : {intrinsic_name}")
                    print(f"{'-'*40}")

                return {
                    "name": intrinsic_name,
                    "element_type": element_type,
                    "vector_size": vector_size,
                    "intrinsic": intrinsic_name
                }

    raise ValueError(f"[ERROR] {intrinsic_name} not found in JSON metadata.")

def parse_pseudocode(pseudo_path, debug=False):
    with open(pseudo_path) as f:
        text = f.read()

    if debug:
        print(f"\n[DEBUG] Parsed pseudocode ({pseudo_path}):\n{'='*40}\n{text.strip()}\n{'='*40}")

    if "+ element2" in text and "for e = 0 to elements-1" in text:
        return {
            "operation": "+",
            "loop": True
        }
    else:
        raise ValueError("Unsupported pseudocode structure.")

def generate_dl(metadata, output_dir, pseudo_path, debug=False):
    element_type = metadata["element_type"]
    lanes = metadata["vector_size"]
    intrinsic = metadata["intrinsic"]
    predicate = f"match_{intrinsic}"

    rule = f""".decl {predicate}(func: symbol, loop: symbol, type: symbol, intrinsic: symbol)
.output {predicate}

{predicate}(F, L, "{element_type}", "{intrinsic}") :-
    loop_stmt(F, L),
    array_assign(F, _, C, A, B, "+"),
    array_type(C, "{element_type}"),
    array_type(A, "{element_type}"),
    array_type(B, "{element_type}"),
    loop_length(F, L, {lanes}).
"""

    pseudo_basename = os.path.splitext(os.path.basename(pseudo_path))[0]
    output_path = os.path.join(output_dir, f"{pseudo_basename}.dl")
    os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w") as f:
        f.write(rule)

    print(f"[✔] Datalog rule written to {output_path}")

    if debug:
        print(f"\n[DEBUG] Datalog rule content:\n{'='*40}\n{rule.strip()}\n{'='*40}")

def main():
    parser = argparse.ArgumentParser(description="Generate Datalog rule from pseudo + JSON metadata")
    parser.add_argument("-j", "--json", required=True, help="Path to intrinsics metadata JSON")
    parser.add_argument("-p", "--pseudo", required=True, help="Path to .pseudo file")
    parser.add_argument("-o", "--output", required=True, help="Output directory for .dl file")
    parser.add_argument("-g", "--debug", action="store_true", help="Enable debug mode with warnings and verbose output")
    args = parser.parse_args()

    intrinsic_name = extract_intrinsic_name(args.pseudo)
    metadata = parse_json_metadata(args.json, intrinsic_name, args.debug)
    _ = parse_pseudocode(args.pseudo, debug=args.debug)
    generate_dl(metadata, args.output, args.pseudo, debug=args.debug)

if __name__ == "__main__":
    main()

