#sed -n 's/.*<name>[^,]*, \(.*\)\[.*<\/name>/\1/p' "$MAP_DIR/doc.kml" | sed 's/ *$//' > "$MAP_DIR/addresses.txt"




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
