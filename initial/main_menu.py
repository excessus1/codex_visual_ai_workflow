# /home/excessus/ai_projects/yolov8/main_menu.py

import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "configs")
SCRIPT_DIR = os.path.join(BASE_DIR, "scripts")

MENU_OPTIONS = {
    "1": ("Run Training", "train", "train_yolo.py"),
    "2": ("Run Image Prediction", "predict", "predict_yolo_image.py"),
    "3": ("Upload to GCS", "upload", "upload_gcs.py"),
    "4": ("Convert YOLO to Label Studio", "convert", "convert_yolo_to_ls.py"),
    "5": ("Prepare local download (from labels)", "download", "download_gcs.py"),
    "6": ("Collect Images from Sources", "collect", "collect_images.py"),
    "7": ("Stage Predictions for Uploads", "upload", "stage_predictions_for_upload.py"),
    "8": ("Download / Organize Annotated", "download", "download_annotated.py"),
    "9": ("Create data.yaml from classes.txt", "train", "generate_data_yaml.py"),
    "10": ("Run Video Prediction", "predict", "predict_yolo_video.py"),
    "11": ("Create Video Label Index", "organize", "index_predictions_by_class.py"),
    "0": ("Exit", None, None)
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

def run_script(script_name, config_path=None):
    script_path = os.path.join(SCRIPT_DIR, script_name)
    cmd = ["python3", script_path]
    if config_path:
        cmd.append(config_path)
    
    print(f"\n[+] Running: {' '.join(cmd)}\n")
    subprocess.run(cmd)

def main():
    while True:
        print("\n==== YOLOv8 Main Menu ====")
        for key, (desc, _, _) in MENU_OPTIONS.items():
            print(f"  {key}. {desc}")
        
        choice = input("\nSelect an option: ").strip()
        if choice not in MENU_OPTIONS:
            print("[!] Invalid option.\n")
            continue
        
        desc, config_type, script_name = MENU_OPTIONS[choice]
        
        if choice == "0":
            print("Goodbye!")
            sys.exit(0)
        
        if config_type:
            config_file = select_config_file(config_type)
            if config_file:
                run_script(script_name, config_file)
        else:
            run_script(script_name)

if __name__ == "__main__":
    main()
