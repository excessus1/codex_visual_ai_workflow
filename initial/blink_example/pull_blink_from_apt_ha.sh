#!/bin/bash

# === CONFIG ===
SRC="/mnt/APT_HA_SHARE/media/blink"
DEST="/mnt/HA_VM/APT_HA/media/blink_raw"
LOG="/home/excessus/scripts/bash/apt_ha/logs/pull_$(date +%Y%m%d_%H%M%S).log"
RETENTION_DAYS=10

# === LOG START ===
{
echo "==== Blink Clip Pull Started @ $(date) ===="
echo "Source: $SRC"
echo "Destination: $DEST"
echo "Retention Policy: Keep last $RETENTION_DAYS days"
echo

# === STEP 1: COPY (safe, leave files intact) ===
echo "[*] Pulling new files from HA media/blink to local raw folder..."
rsync -av --ignore-existing "$SRC/" "$DEST/"

# === STEP 2: CLEANUP (delete old files only) ===
echo "[*] Deleting files older than $RETENTION_DAYS days on HA..."
find "$SRC" -type f -name "*.mp4" -mtime +$RETENTION_DAYS -print -delete

echo
echo "==== Pull Completed @ $(date) ===="
} >> "$LOG" 2>&1
