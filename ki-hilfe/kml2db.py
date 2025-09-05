import xml.etree.ElementTree as ET
import pymysql
from datetime import datetime
import os
from lxml import etree
import re

KML_FILE = os.path.join(os.path.dirname(__file__), "doc.kml")
DB_CONFIG = {
    "host": "localhost",
    "user": "deinuser",
    "password": "deinpasswort",
    "database": "deinedatenbank"
}

tree = etree.parse(KML_FILE)

for desc in tree.xpath("//description"):
    desc.getparent().remove(desc)

tree.write("doc_no_description.kml", pretty_print=True, encoding="UTF-8", xml_declaration=True)

with open("KML_FILE", "r", encoding="utf-8") as f:
    content = f.read()

content = re.sub(r'<!\[CDATA\[', '', content)
content = re.sub(r'\]\]>', '', content)
content = re.sub(r'(<[^>]+>)([^<]*?)\n(</[^>]+>)', r'\1\2\3', content)
content = re.sub(r'&(?![a-zA-Z]+;|#\d+;)', '&amp;', content)

with open("KML_FILE", "w", encoding="utf-8") as f:
    f.write(content)



tree = ET.parse(KML_FILE)
root = tree.getroot()


ns = {"kml": "http://www.opengis.net/kml/2.2"}

placemarks = root.findall(".//kml:Placemark", ns)


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

for pm in placemarks:
    name = pm.find("kml:name", ns).text if pm.find("kml:name", ns) is not None else None
    coords = pm.find(".//kml:coordinates", ns).text if pm.find(".//kml:coordinates", ns) is not None else None
    
    if coords:
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

conn.commit()
cursor.close()
conn.close()
