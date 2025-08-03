# index_predictions_by_class.py

import os
import sys
import json
import argparse
from glob import glob


def load_class_map(path):
    with open(path, 'r') as f:
        return {int(k): v for k, v in json.load(f).items()}


def parse_txt_file(path):
    class_ids = set()
    with open(path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if parts:
                class_ids.add(int(parts[0]))
    return list(class_ids)


def build_index(config):
    root_dir = config['source_dir']
    output_path = config['output_json']
    class_map_path = config['class_map']
    filter_class = config.get('filter_class')

    class_map = load_class_map(class_map_path)
    reverse_class_map = {v: k for k, v in class_map.items()}
    class_filter_id = reverse_class_map.get(filter_class) if filter_class else None

    index = []

    for labels_dir in glob(os.path.join(root_dir, 'predict*/labels')):
        predict_dir = os.path.dirname(labels_dir)
        video_file = next((f for f in os.listdir(predict_dir) if f.endswith('.avi')), None)
        if not video_file:
            continue

        full_video_path = os.path.join(os.path.basename(predict_dir), video_file)

        for txt_file in glob(os.path.join(labels_dir, '*.txt')):
            class_ids = parse_txt_file(txt_file)
            if not class_ids:
                continue

            if class_filter_id is not None and class_filter_id not in class_ids:
                continue

            entry = {
                "video": full_video_path,
                "frame_label": os.path.join(os.path.basename(predict_dir), 'labels', os.path.basename(txt_file)),
                "class_ids": class_ids,
                "class_names": [class_map[cid] for cid in class_ids if cid in class_map]
            }
            index.append(entry)

    with open(output_path, 'w') as f:
        json.dump(index, f, indent=2)
    print(f"[INFO] Saved index with {len(index)} entries to {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 predict_yolo.py <config_file.json>")
        sys.exit(1)

    config_path = sys.argv[1]
    if not os.path.isfile(config_path):
        print(f"[ERROR] Config file not found: {config_path}")
        sys.exit(1)

    with open(config_path, 'r') as f:
        cfg = json.load(f)

    build_index(cfg)


if __name__ == "__main__":
    main()
