import os
import json
import os
import sys
from glob import glob
from .utils import emit_status


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


def index_predictions(cfg):
    root_dir = cfg['source_dir']
    output_path = cfg['output_json']
    class_map_path = cfg['class_map']
    filter_class = cfg.get('filter_class')

    emit_status('start', action='index_predictions')

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
                "class_names": [class_map[cid] for cid in class_ids if cid in class_map],
            }
            index.append(entry)
            emit_status('indexed', file=os.path.basename(txt_file), classes=entry["class_names"])

    with open(output_path, 'w') as f:
        json.dump(index, f, indent=2)

    emit_status('complete', action='index_predictions', entries=len(index), output=output_path)
    return index


def run(config_path: str) -> None:
    with open(config_path, "r") as f:
        cfg = json.load(f)
    index_predictions(cfg)


def main(argv: list[str] | None = None) -> None:
    argv = argv or sys.argv[1:]
    if len(argv) != 1:
        print("Usage: python -m backend.index_predictions_by_class <config.json>")
        sys.exit(1)
    run(argv[0])


if __name__ == "__main__":
    main()
