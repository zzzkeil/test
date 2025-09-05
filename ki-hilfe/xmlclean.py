from lxml import etree
import re
import pymysql
from datetime import datetime

# --- 1. Config ---
kml_file = "doc.kml"

DB_CONFIG = {
    "host": "localhost",
    "user": "keil",
    "password": "zzz",
    "database": "zzz",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor
}

ns = {"kml": "http://www.opengis.net/kml/2.2"}

# --- 2. Parse and Clean KML ---
tree = etree.parse(kml_file)
root = tree.getroot()

# Regex patterns for cleaning
remove_chars = r"[()\*\[\]≥≳,]"
remove_kw_num = r"\b\d+(\.\d+)?\s*kW\b"
remove_ct_num = r"\b\d+(?:/\d+)?(\.\d+)?\s*ct/kWh\b"
#remove_ct_num = r"\b\d+(\.\d+)?\s*ct/kWh\b"
remove_rp_num = r"\b\d+(?:/\d+)?(\.\d+)?\s*rp/kWh\b"
#remove_rp_num = r"\b\d+(\.\d+)?\s*rp/kWh\b"
remove_kw_unit = r"\bkW\b"
remove_ct_unit = r"\bct/kWh\b"
remove_rp_unit = r"\brp/kWh\b"

for name_el in root.findall(".//kml:name", namespaces=ns):
    if name_el.text:
        text = name_el.text
        text = re.sub(remove_chars, "", text)
        text = re.sub(remove_kw_num, "", text, flags=re.IGNORECASE)
        text = re.sub(remove_ct_num, "", text, flags=re.IGNORECASE)
        text = re.sub(remove_rp_num, "", text, flags=re.IGNORECASE)
        text = re.sub(remove_kw_unit, "", text, flags=re.IGNORECASE)
        text = re.sub(remove_ct_unit, "", text, flags=re.IGNORECASE)
        text = re.sub(remove_rp_unit, "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s+", " ", text)  # collapse spaces
        name_el.text = text.strip()

placemarks = root.findall(".//kml:Placemark", namespaces=ns)

# --- 3. Connect to MariaDB ---
conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS kml_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    longitude DOUBLE,
    latitude DOUBLE,
    imported_at DATETIME,
    UNIQUE KEY unique_coords (longitude, latitude)
)
""")

# --- 4. Insert data ---
for pm in placemarks:
    name = pm.find("kml:name", ns)
    name = name.text if name is not None else None
    
    coords = pm.find(".//kml:coordinates", ns)
    coords = coords.text if coords is not None else None
    
    if coords:
        try:
            lon, lat, *_ = coords.strip().split(",")
            lon = float(lon)
            lat = float(lat)
            
            cursor.execute("""
                INSERT INTO kml_data (name, longitude, latitude, imported_at)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    imported_at = VALUES(imported_at)
            """, (name, lon, lat, datetime.now()))
        except Exception as e:
            print(f"Skipping invalid coords: {coords} ({e})")

conn.commit()
cursor.close()
conn.close()
print("KML data inserted into MariaDB successfully.")
