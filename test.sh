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


#clean up kml file
sed -i -E 's/<!\[CDATA\[//g; s/\]\]>//g' doc.kml
sed -i ':a;N;$!ba;s/<name>\([^<]*\)\n<\/name>/<name>\1<\/name>/g' doc.kml
sed ':a;N;$!ba;s/<name>\([^<]*\)\n<\/name>/<name>\1<\/name>/g' doc.kml > fixed_doc.kml



#sed ':a;N;$!ba;s/\(<[^>]*>\)\([^<]*[^]]\)\n<\/\([^>]*\)>/\1\2<\/\3>/g' doc.kml > 1fixed_doc.kml




#  $DL_DIR/$KMZ_FILE cleanup
#sed -n 's:.*<name>\(.*\)</name>.*:\1:p' "$MAP_DIR/doc.kml" > "$MAP_DIR/addresses.txt"
#sed -Ei 's/.*kWh,//; s/.*<!\[CDATA\[//' "$MAP_DIR/addresses.txt"






# proper json file ?
#sed -E 's/^[^,]+, *//; s/ *[[].*[]]$//; s/ *[(].*[)]$//' "$MAP_DIR/addresses.txt" > "$MAP_DIR/addresses.json"


