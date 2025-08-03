#!/bin/bash

RAW="/mnt/HA_VM/APT_HA/media/blink_raw"
ORG="/mnt/HA_VM/APT_HA/media/blink_organized"
LOG="/home/excessus/scripts/bash/apt_ha/logs/organize_$(date +%Y%m%d_%H%M%S).log"

{
echo "==== Organize Started @ $(date) ===="
echo "Source: $RAW"
echo "Target: $ORG"
echo

find "$RAW" -type f -name "*.mp4" | while read -r file; do
    base=$(basename "$file")
    
    # Extract everything after second underscore
    # Filename format: YYYYMMDD_HHMMSS_camera_name_optional.mp4
    cam_id=$(echo "$base" | sed -E 's/^[^_]+_[^_]+_([^\.]+)\.mp4/\1/')

    if [[ -z "$cam_id" ]]; then
        echo "!! Failed to extract cam ID from $base"
        continue
    fi

    dest="$ORG/$cam_id"
    mkdir -p "$dest"
    mv "$file" "$dest/" && echo "→ Moved $base to $cam_id/"
done

echo
echo "==== Organize Completed @ $(date) ===="
} >> "$LOG" 2>&1
