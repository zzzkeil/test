import requests
import pymysql
import time

# 🔹 Database connection
DB_CONFIG = {
    "host": "localhost",
    "user": "",
    "password": "",
    "database": "",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor
}

conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()

# 🔹 Fetch POIs that don’t have an address yet
cursor.execute("""
    SELECT id, latitude, longitude 
    FROM poi 
    WHERE streetname IS NULL 
    OR housenumber IS NULL 
    OR postalcode IS NULL 
    OR city IS NULL
""")
pois = cursor.fetchall()

print(f"Found {len(pois)} POIs to update.")

for poi in pois:
    lat, lon, poi_id = poi["latitude"], poi["longitude"], poi["id"]
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&addressdetails=1"

    try:
        response = requests.get(url, headers={"User-Agent": "poi-updater"})
        data = response.json()

        address = data.get("address", {})
        street = address.get("road")
        house = address.get("house_number")
        postal = address.get("postcode")
        city = (
            address.get("city") 
            or address.get("town") 
            or address.get("village")
            or address.get("hamlet")
        )

        # 🔹 Update DB
        update_sql = """
        UPDATE poi
        SET streetname=%s, housenumber=%s, postalcode=%s, city=%s
        WHERE id=%s
        """
        cursor.execute(update_sql, (street, house, postal, city, poi_id))
        conn.commit()

        print(f"✅ Updated POI {poi_id}: {street} {house}, {postal} {city}")

        # 🔹 Be nice to OSM servers (rate limit)
        time.sleep(1)

    except Exception as e:
        print(f"❌ Error updating POI {poi_id}: {e}")

cursor.close()
conn.close()
print("All updates done.")
