import requests
import xml.etree.ElementTree as ET
import pymysql
from datetime import datetime

# --- Einstellungen ---
KML_URL = "doc.kml"
DB_CONFIG = {
    "host": "localhost",
    "user": "deinuser",
    "password": "deinpasswort",
    "database": "deinedatenbank"
}

# --- KML abrufen ---
response = requests.get(KML_URL)
with open("data.kml", "wb") as f:
    f.write(response.content)

# --- XML parsen ---
tree = ET.parse("data.kml")
root = tree.getroot()

# KML-Namespace (wichtig, sonst findet er die Tags nicht)
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
    imported_at DATETIME
)
""")

# --- Daten einfügen ---
for pm in placemarks:
    name = pm.find("kml:name", ns).text if pm.find("kml:name", ns) is not None else None
    coords = pm.find(".//kml:coordinates", ns).text if pm.find(".//kml:coordinates", ns) is not None else None
    
    if coords:
        lon, lat, *_ = coords.strip().split(",")
        cursor.execute("""
            INSERT INTO kml_data (name, longitude, latitude, imported_at)
            VALUES (%s, %s, %s, %s)
        """, (name, float(lon), float(lat), datetime.now()))

conn.commit()
cursor.close()
conn.close()
