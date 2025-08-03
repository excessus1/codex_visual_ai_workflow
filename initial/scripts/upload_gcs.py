#!/usr/bin/env python3

import json
import sys
from backend.upload_gcs import upload


def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python upload_gcs.py <config.json>")
        sys.exit(1)

    config_path = sys.argv[1]
    config = load_config(config_path)
    upload(config)
