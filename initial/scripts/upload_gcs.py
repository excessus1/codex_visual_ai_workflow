#!/usr/bin/env python3

import subprocess
import os
import json
import sys

# Flags
DRY_RUN = False  # Set to True to preview without uploading
DELETE_EXTRAS = False  # Set to True if you want to mirror (deletes remote files not in local)

def load_config(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)

def build_rsync_command(local_path, gcs_path):
    cmd = ['gsutil', '-m', 'rsync', '-r']

    if DRY_RUN:
        cmd.append('-n')

    if DELETE_EXTRAS:
        cmd.append('-d')  # Dangerous! Removes files in GCS not present locally

    cmd.extend([local_path, gcs_path])
    return cmd

def upload(config):
    local_path = os.path.expanduser(config['local_path'])
    gcs_path = config['gcs_path']

    print(f"Uploading from:\n  {local_path}\nto:\n  {gcs_path}\n")

    if DRY_RUN:
        print("⚠️  DRY RUN ENABLED – no changes will be made.\n")

    cmd = build_rsync_command(local_path, gcs_path)
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Upload completed.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Upload failed with error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python upload_gcs.py <config.json>")
        sys.exit(1)

    config_path = sys.argv[1]
    config = load_config(config_path)
    upload(config)
