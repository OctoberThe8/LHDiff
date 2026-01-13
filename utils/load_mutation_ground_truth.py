import xml.etree.ElementTree as ET

def load_mutation_ground_truth(xml_path: str) -> dict[int, list[int]]:
    """
    Loads mutation ground truth.
    Expected format:
      <TEST>
        <LOCATION ORIG="i" NEW="j"/>
      </TEST>
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    mapping = {}

    for loc in root.findall("LOCATION"):
        orig = int(loc.attrib["ORIG"])
        new = int(loc.attrib["NEW"])

        if orig == -1:
            continue  # insertion, no left-side mapping

        mapping.setdefault(orig, []).append(new)

    return mapping
