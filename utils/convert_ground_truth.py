import xml.etree.ElementTree as ET
from src.preprocessing.preprocess import normalize_file_with_index_map


def convert_ground_truth(raw_xml_path, old_file, new_file, output_path):
    # Normalize both files + get mapping tables
    norm_old, map_old = normalize_file_with_index_map(old_file)
    norm_new, map_new = normalize_file_with_index_map(new_file)

    #Load XML
    tree = ET.parse(raw_xml_path)
    root = tree.getroot()

    #Convert each LOCATION element
    for version in root.findall("VERSION"):
        for loc in version.findall("LOCATION"):

            raw_orig = int(loc.get("ORIG"))
            raw_new  = int(loc.get("NEW"))

            # find normalized index for raw_orig
            norm_orig = next((n for n, r in map_old.items() if r == raw_orig), -1)
            norm_new_idx = next((n for n, r in map_new.items() if r == raw_new), -1)

            loc.set("ORIG", str(norm_orig))
            loc.set("NEW",  str(norm_new_idx))

    # Write normalized version
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"Converted XML saved to {output_path}")
