import requests
import pymysql
import time

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

cursor.execute("""
    SELECT id, latitude, longitude 
    FROM pois 
    WHERE streetname IS NULL 
       OR housenumber IS NULL 
       OR postalcode IS NULL 
       OR city IS NULL
""")
pois = cursor.fetchall()
print(f"Found {len(pois)} POIs to update.")

for idx, poi in enumerate(pois, start=1):
    lat, lon, pois_id = pois["latitude"], pois["longitude"], pois["id"]
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&addressdetails=1"

    try:
        response = requests.get(url, headers={"User-Agent": "poi-updater/1.0 (your_email@example.com)"}, timeout=10)
        data = response.json()

        address = data.get("address", {})
        street = address.get("road")
        house = address.get("house_number")
        postal = address.get("postcode")
        city = address.get("city") or address.get("town") or address.get("village") or address.get("hamlet")

        if not street and not house and not postal and not city:
            print(f"⚠️ No address found for POI {pois_id}, skipping...")
            continue

        cursor.execute("""
            UPDATE pois
            SET streetname=%s, housenumber=%s, postalcode=%s, city=%s
            WHERE id=%s
        """, (street, house, postal, city, poi_id))

        if idx % 50 == 0:  # commit every 50 updates
            conn.commit()

        print(f"✅ Updated POI {pois_id}: {street} {house}, {postal} {city}")
        time.sleep(1)

    except Exception as e:
        print(f"❌ Error updating POI {pois_id}: {e}")

conn.commit()
cursor.close()
conn.close()
print("All updates done.")
