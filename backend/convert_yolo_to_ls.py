import json
import logging
import json
import logging
import sys
from pathlib import Path
from .utils import emit_status


def load_classes(class_file):
    with open(class_file, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def convert_yolo_to_ls(cfg):
    label_dir = Path(cfg['labels_dir'])
    image_dir = Path(cfg['image_dir'])
    class_file = Path(cfg['classes_file'])
    output_file = Path(cfg['output_file'])
    image_prefix = cfg.get('image_prefix', 'gs://excessus-home-labelstudio/datasets1/')

    emit_status('start', action='convert_yolo_to_ls', labels_dir=str(label_dir))

    classes = load_classes(class_file)
    label_files = sorted(label_dir.glob('*.txt'))
    tasks = []

    for label_file in label_files:
        image_name = label_file.stem
        image_path_jpg = image_dir / f"{image_name}.jpg"
        image_path_JPG = image_dir / f"{image_name}.JPG"

        if image_path_jpg.exists():
            image_path = image_path_jpg
        elif image_path_JPG.exists():
            image_path = image_path_JPG
        else:
            logging.warning(f"Image not found for label: {label_file.name}")
            continue

        with open(label_file, 'r') as f:
            lines = f.readlines()

        results = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            cls_id, x, y, w, h = map(float, parts)
            label = classes[int(cls_id)]
            results.append({
                "original_width": 9216,
                "original_height": 5184,
                "image_rotation": 0,
                "value": {
                    "x": (x - w / 2) * 100,
                    "y": (y - h / 2) * 100,
                    "width": w * 100,
                    "height": h * 100,
                    "rotation": 0,
                    "rectanglelabels": [label],
                },
                "from_name": "label",
                "to_name": "image",
                "type": "rectanglelabels",
                "origin": "manual",
                "id": None,
            })

        task = {
            "data": {"image": f"{image_prefix}{image_path.name}"},
            "annotations": [{"result": results}],
        }
        tasks.append(task)
        emit_status('converted', label=str(label_file), image=str(image_path))

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(tasks, f, indent=2)

    emit_status('complete', action='convert_yolo_to_ls', tasks=len(tasks), output=str(output_file))
    return tasks


def run(config_path: str) -> None:
    """Load config from ``config_path`` and perform conversion."""
    with open(config_path, "r") as f:
        cfg = json.load(f)
    convert_yolo_to_ls(cfg)


def main(argv: list[str] | None = None) -> None:
    argv = argv or sys.argv[1:]
    if len(argv) != 1:
        print("Usage: python -m backend.convert_yolo_to_ls <config.json>")
        sys.exit(1)
    run(argv[0])


if __name__ == "__main__":
    main()
