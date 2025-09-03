#!/bin/bash

apt install unzip jq

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
unzip -j "$DL_DIR/$KMZ_FILE" '*.kml' -d "$DEST_DIR"
if [ $? -ne 0 ]; then
    echo "kml file found or extraction failed."
    rm -f "$KMZ_FILE"
    exit 1
fi

rm -f "$KMZ_FILE"


# sed $DL_DIR/$KMZ_FILE  in cor. line by line als coordinates.txt



#openstreetmap test

OPENSMIN_FILE="coordinates.txt"           
OPENSMOUT_FILE="addresses.txt"

get_address() {
    local lat="$1"
    local lon="$2"
    response=$(curl -s "https://nominatim.openstreetmap.org/reverse?lat=$lat&lon=$lon&format=json&addressdetails=1")
    address=$(echo "$response" | jq -r '.display_name')
    if [ "$address" != "null" ]; then
        echo "$address"
    else
        echo "Address not found for coordinates: $lat, $lon"
    fi
}

echo "Processing coordinates..."

while IFS=',' read -r lat lon; do
    address=$(get_address "$lat" "$lon")
    echo "$address" >> "$OPENSMOUT_FILE"
    sleep 1
done < "$OPENSMIN_FILE"

echo "Address list saved to: $OPENSMOUT_FILE"
