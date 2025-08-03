import shutil
import logging
from pathlib import Path
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
