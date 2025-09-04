#!/bin/bash

apt install unzip jq

URL="https://www.google.com/maps/d/kml?mid=1L-gatZq7W4lZzdrfLLAK3AVUoc8lKNo&femb=1&ll=50.36612061088382%2C10.627823200000002&z=6"
DL_DIR="dl_data"
KMZ_FILE="gerds.kmz"
MAP_DIR="map_data" 

mkdir "$DL_DIR"
wget -q -O "$DL_DIR/$KMZ_FILE" "$URL"
if [ $? -ne 0 ]; then
    echo "Error downloading"
    exit 1
fi

mkdir "$MAP_DIR"
unzip -j "$DL_DIR/$KMZ_FILE" '*.kml' -d "$MAP_DIR"
if [ $? -ne 0 ]; then
    echo "kml file found or extraction failed."
    rm -f "$KMZ_FILE"
    exit 1
fi

rm -f "$KMZ_FILE"

# sed $DL_DIR/$KMZ_FILE  in name and city line by line als addresses.txt
sed -n 's/.*<name>[^,]*, \(.*\)\[.*<\/name>/\1/p' "$MAP_DIR/doc.kml" | sed 's/ *$//' > "$MAP_DIR/addresses.txt"




# sed $DL_DIR/$KMZ_FILE  in cor. line by line als coordinates.txt for openstreetmap 
#sed -n '/<coordinates>/,/<\/coordinates>/p' "$MAP_DIR/doc.kml" | grep -v coordinates | cut -d',' -f1,2 | tr ',' ' ' | sed 's/^[ \t]*//' > "$MAP_DIR/coordinates.txt"

##openstreetmap test dauer mit max. request limit bei ca. 1500 einträgen ca. 40 min ...  is lang 
#COOR_FILE="$MAP_DIR/coordinates.txt"
#ADDR_FILE="$MAP_DIR/addresses.txt"
#> "$ADDR_FILE"

#while read -r lon lat; do
#    [ -z "$lon" ] && continue
#    response=$(curl -s "https://nominatim.openstreetmap.org/reverse?format=json&lat=$lat&lon=$lon&zoom=18&addressdetails=1" \
#        -H "User-Agent: geo-bash-script/1.0")
#    address=$(echo "$response" | jq -r '.address | "\(.road // ""), \(.house_number // ""), \(.postcode // ""), \(.city // .town // .village // "")"')
#    address=$(echo "$address" | sed 's/, ,/,/g; s/,,/,/g; s/^, //; s/, $//')
#    echo "$address" >> "$ADDR_FILE"
#    sleep 1
#done < "$COOR_FILE"
