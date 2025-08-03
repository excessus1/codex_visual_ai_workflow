#!/bin/bash

# === CONFIG ===
SRC="/mnt/HA_VM/APT_HA/media/blink_organized"
DEST="/mnt/APT_HA_SHARE/media/blink_organized"
LOG="/home/excessus/scripts/bash/apt_ha/logs/push_$(date +%Y%m%d_%H%M%S).log"

{
echo "==== Blink Push to HA Started @ $(date) ===="
echo "Source: $SRC"
echo "Destination: $DEST"
echo

# === SYNC to HA ===
rsync -av --delete "$SRC/" "$DEST/"

echo
echo "==== Push Completed @ $(date) ===="
} >> "$LOG" 2>&1
