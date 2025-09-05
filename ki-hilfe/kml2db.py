import xml.etree.ElementTree as ET
import pymysql
from datetime import datetime
import os

# --- Einstellungen ---
KML_FILE = os.path.join(os.path.dirname(__file__), "doc.kml")
DB_CONFIG = {
    "host": "localhost",
    "user": "deinuser",
    "password": "deinpasswort",
    "database": "deinedatenbank"
}

# --- KML-Datei parsen ---
tree = ET.parse(KML_FILE)
root = tree.getroot()

# Namespace für KML
ns = {"kml": "http://www.opengis.net/kml/2.2"}

placemarks = root.findall(".//kml:Placemark", ns)

# --- Verbindung zur DB ---
conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()

# Tabelle anlegen (falls nicht vorhanden)
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

# --- Daten einfügen oder aktualisieren ---
for pm in placemarks:
    name = pm.find("kml:name", ns).text if pm.find("kml:name", ns) is not None else None
    coords = pm.find(".//kml:coordinates", ns).text if pm.find(".//kml:coordinates", ns) is not None else None
    
    if coords:
        lon, lat, *_ = coords.strip().split(",")
        lon = float(lon)
        lat = float(lat)

        # Insert oder Update falls schon vorhanden
        cursor.execute("""
            INSERT INTO kml_data (name, longitude, latitude, imported_at)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                imported_at = VALUES(imported_at)
        """, (name, lon, lat, datetime.now()))

conn.commit()
cursor.close()
conn.close()
