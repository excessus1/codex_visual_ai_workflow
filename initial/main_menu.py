import os
import sys
from backend.collect_images import run as collect_images_run
from backend.convert_yolo_to_ls import run as convert_yolo_to_ls_run
from backend.download_annotated import run as download_annotated_run
from backend.generate_data_yaml import run as generate_data_yaml_run
from backend.index_predictions_by_class import run as index_predictions_run
from backend.stage_predictions_for_upload import run as stage_predictions_run
from backend.upload_gcs import run as upload_gcs_run
from backend.yolo import run as yolo_run

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "configs")

MENU_OPTIONS = {
    "1": ("Run Training", "train", lambda p: yolo_run(p, mode_override="train")),
    "2": ("Run Image Prediction", "predict", lambda p: yolo_run(p, mode_override="predict")),
    "3": ("Upload to GCS", "upload", upload_gcs_run),
    "4": ("Convert YOLO to Label Studio", "convert", convert_yolo_to_ls_run),
    "5": ("Prepare local download (from labels)", "download", download_annotated_run),
    "6": ("Collect Images from Sources", "collect", collect_images_run),
    "7": ("Stage Predictions for Uploads", "upload", stage_predictions_run),
    "8": ("Download / Organize Annotated", "download", download_annotated_run),
    "9": ("Create data.yaml from classes.txt", "train", generate_data_yaml_run),
    "10": ("Run Video Prediction", "predict", lambda p: yolo_run(p, mode_override="predict")),
    "11": ("Create Video Label Index", "organize", index_predictions_run),
    "0": ("Exit", None, None),
}

def list_json_files(folder_path):
    try:
        files = [f for f in os.listdir(folder_path) if f.endswith(".json")]
        files.sort()
        return files
    except FileNotFoundError:
        print(f"[!] Folder not found: {folder_path}")
        return []

def select_config_file(config_type):
    folder_path = os.path.join(CONFIG_DIR, config_type)
    files = list_json_files(folder_path)

    if not files:
        print(f"[!] No JSON config files found in {folder_path}")
        return None

    print(f"\nAvailable configs in {config_type}/:")
    for i, file in enumerate(files, 1):
        print(f"  {i}. {file}")

    choice = input("\nChoose a config file by number (or 0 to cancel): ")
    if choice == "0":
        return None

    try:
        idx = int(choice) - 1
        return os.path.join(folder_path, files[idx])
    except (ValueError, IndexError):
        print("[!] Invalid selection.")
        return None

def run_backend(func, config_path):
    func(config_path)

def main():
    while True:
        print("\n==== YOLOv8 Main Menu ====")
        for key, (desc, _, _) in MENU_OPTIONS.items():
            print(f"  {key}. {desc}")

        choice = input("\nSelect an option: ").strip()
        if choice not in MENU_OPTIONS:
            print("[!] Invalid option.\n")
            continue

        desc, config_type, func = MENU_OPTIONS[choice]

        if choice == "0":
            print("Goodbye!")
            sys.exit(0)

        if config_type:
            config_file = select_config_file(config_type)
            if config_file and func:
                run_backend(func, config_file)

if __name__ == "__main__":
    main()
