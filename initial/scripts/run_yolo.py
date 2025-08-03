import argparse
import json
from backend.yolo import run_prediction, run_training


def load_config(path):
    with open(path, 'r') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Run YOLOv8 training or prediction from JSON config")
    parser.add_argument('--config', required=True, help="Path to JSON config file")
    args = parser.parse_args()

    config = load_config(args.config)
    mode = config.get('mode')

    if mode == 'predict':
        run_prediction(config)
    elif mode == 'train':
        run_training(config)
    else:
        raise ValueError("'mode' must be either 'predict' or 'train'")


if __name__ == '__main__':
    main()
