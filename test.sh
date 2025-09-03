#!/bin/bash

URL="https://www.google.com/maps/d/kml?mid=1L-gatZq7W4lZzdrfLLAK3AVUoc8lKNo&femb=1&ll=50.36612061088382%2C10.627823200000002&z=6"
DL_DIR="dl_data"
KMZ_FILE="gerds.kmz"
DEST_DIR="map_data" 

mkdir "$DL_DIR"
wget -q -O "$DL_DIR/$KMZ_FILE" "$URL"
if [ $? -ne 0 ]; then
    echo "Error downloading"
    exit 1
fi

mkdir "$DEST_DIR"
unzip -j "$KMZ_FILE" '*.dml' -d "$DEST_DIR"
if [ $? -ne 0 ]; then
    echo "dml file found or extraction failed."
    rm -f "$KMZ_FILE"
    exit 1
fi

rm -f "$KMZ_FILE"

