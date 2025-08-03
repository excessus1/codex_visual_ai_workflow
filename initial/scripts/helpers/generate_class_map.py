# generate_class_map.py

import os
import sys
import yaml
import json


def from_yaml(yaml_path, output_path):
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    class_map = {str(i): name for i, name in enumerate(data.get('names', []))}
    with open(output_path, 'w') as out:
        json.dump(class_map, out, indent=2)
    print(f"[INFO] Saved class map from data.yaml to {output_path}")


def from_txt(txt_path, output_path):
    with open(txt_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    class_map = {str(i): name for i, name in enumerate(lines)}
    with open(output_path, 'w') as out:
        json.dump(class_map, out, indent=2)
    print(f"[INFO] Saved class map from classes.txt to {output_path}")


def main():
    if len(sys.argv) < 4:
        print("Usage: python generate_class_map.py <yaml|txt> <input_file> <output_json>")
        sys.exit(1)

    mode, input_file, output_file = sys.argv[1:4]
    if not os.path.isfile(input_file):
        print(f"[ERROR] File not found: {input_file}")
        sys.exit(1)

    if mode == "yaml":
        from_yaml(input_file, output_file)
    elif mode == "txt":
        from_txt(input_file, output_file)
    else:
        print("[ERROR] Mode must be 'yaml' or 'txt'")
        sys.exit(1)


if __name__ == "__main__":
    main()
