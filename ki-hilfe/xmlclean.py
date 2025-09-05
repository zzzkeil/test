from lxml import etree

# Input/output path (same file overwrite)
kml_file = "doc.kml"

# Parse KML
tree = etree.parse(kml_file)
root = tree.getroot()
ns = {"kml": "http://www.opengis.net/kml/2.2"}

# 1. Trim whitespace in <name>
for name_el in root.findall(".//kml:name", namespaces=ns):
    if name_el.text:
        name_el.text = name_el.text.strip()

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

# 4. Save back to the same file
tree.write(kml_file, pretty_print=True, xml_declaration=True, encoding="UTF-8")
