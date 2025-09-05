from lxml import etree
import re

# Input/output path (overwrite same file)
kml_file = "/mnt/data/doc.kml"

# Parse KML
tree = etree.parse(kml_file)
root = tree.getroot()
ns = {"kml": "http://www.opengis.net/kml/2.2"}

# Regex patterns
remove_chars = r"[()\*\[\]≥,]"               # unwanted characters
remove_kw_num = r"\b\d+(\.\d+)?\s*kW\b"      # numbers followed by kW
remove_ct_num = r"\b\d+(\.\d+)?\s*ct/kWh\b"  # numbers followed by ct/kWh
remove_kw_unit = r"\bkW\b"                   # standalone kW
remove_ct_unit = r"\bct/kWh\b"               # standalone ct/kWh

# 1. Clean <name> tags
for name_el in root.findall(".//kml:name", namespaces=ns):
    if name_el.text:
        text = name_el.text
        # Remove unwanted chars
        text = re.sub(remove_chars, "", text)
        # Remove numbers + units
        text = re.sub(remove_kw_num, "", text, flags=re.IGNORECASE)
        text = re.sub(remove_ct_num, "", text, flags=re.IGNORECASE)
        # Remove units alone
        text = re.sub(remove_kw_unit, "", text, flags=re.IGNORECASE)
        text = re.sub(remove_ct_unit, "", text, flags=re.IGNORECASE)
        # Collapse multiple spaces
        text = re.sub(r"\s+", " ", text)
        # Trim spaces
        name_el.text = text.strip()

# 2. Remove unused <Style> elements
style_refs = set()
for style_url in root.findall(".//kml:styleUrl", namespaces=ns):
    if style_url.text:
        style_refs.add(style_url.text.replace("#", "").strip())

for style in root.findall(".//kml:Style", namespaces=ns):
    style_id = style.attrib.get("id")
    if style_id and style_id not in style_refs:
        parent = style.getparent()
        parent.remove(style)

# 3. Remove empty <description> tags
for desc in root.findall(".//kml:description", namespaces=ns):
    if desc.text is None or not desc.text.strip():
        parent = desc.getparent()
        parent.remove(desc)

# 4. Save back to same file
tree.write(kml_file, pretty_print=True, xml_declaration=True, encoding="UTF-8")

print(f"KML file cleaned (names sanitized, units removed, unused styles removed, empty descriptions removed). Saved to: {kml_file}")
