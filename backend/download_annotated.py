import os
import sys
import json
import shutil
import logging
from pathlib import Path
from datetime import datetime
from .utils import emit_status


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def copy_matching_images(labels_dir, images_dir, output_dir):
    labels_dir = Path(labels_dir)
    images_dir = Path(images_dir)
    output_images = Path(output_dir) / "images"
    output_labels = Path(output_dir) / "labels"

    ensure_dir(output_images)
    ensure_dir(output_labels)

    label_files = list(labels_dir.glob("*.txt"))
    count = 0
    missing = 0
    renamed = 0

    emit_status('start', action='download_annotated', labels=len(label_files))

    for label_file in label_files:
        original_stem = label_file.stem
        base = original_stem.split("__", 1)[1] if "__" in original_stem else original_stem

        candidates = list(images_dir.glob(f"{base}.*"))
        img_file = next((c for c in candidates if c.suffix.lower() in ['.jpg', '.jpeg']), None)

        if img_file and img_file.exists():
            new_label_name = img_file.stem + ".txt"
            new_label_path = output_labels / new_label_name

            shutil.copy(img_file, output_images / img_file.name)
            shutil.copy(label_file, new_label_path)

            log_entry = f"[COPY] {img_file.name} and {new_label_name}"
            if new_label_name != label_file.name:
                renamed += 1
                log_entry += f" (renamed from {label_file.name})"

            logging.info(log_entry)
            count += 1
            emit_status('copied', image=str(img_file), label=new_label_name)
        else:
            logging.warning(f"[MISSING] No image found for label {label_file.name}")
            missing += 1
            emit_status('missing', label=str(label_file))

    emit_status('complete', action='download_annotated', copied=count, renamed=renamed, missing=missing)
    return {
        'copied': count,
        'renamed': renamed,
        'missing': missing,
    }


def download_annotated(cfg):
    labels_dir = cfg.get("labels_dir")
    images_dir = cfg.get("images_dir")
    output_dir = cfg.get("output_dir")
    return copy_matching_images(labels_dir, images_dir, output_dir)


def setup_logging(log_dir: Path) -> Path:
    """Configure logging for download operation and return the log file path."""
    ensure_dir(log_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = log_dir / f"download_annotated_{timestamp}.log"
    logging.basicConfig(
        filename=log_path,
        filemode="w",
        level=logging.INFO,
        format='[%(levelname)s] %(message)s',
    )
    return log_path


def run(config_path: str) -> None:
    """Entry point to download annotated images using a JSON config file."""
    with open(config_path, "r") as f:
        cfg = json.load(f)

    data_dir = Path(os.getenv("DATA_DIR", "."))
    log_path = setup_logging(data_dir / "logs" / "download")
    print(f"[INFO] Log written to {log_path}\n")
    download_annotated(cfg)


def main(argv: list[str] | None = None) -> None:
    argv = argv or sys.argv[1:]
    if len(argv) != 1:
        print("Usage: python -m backend.download_annotated <config.json>")
        sys.exit(1)
    run(argv[0])


if __name__ == "__main__":
    main()
