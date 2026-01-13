import xml.etree.ElementTree as ET
from collections import defaultdict

def load_ground_truth(xml_path: str) -> dict[int, list[int]]:
    """
    Load normalized ground truth XML and return:
    { left_index: [right_index, ...] }
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    gt = defaultdict(list)

    # Find VERSION number 2 (final mapping)
    version2 = None
    for v in root.findall("VERSION"):
        if v.attrib.get("NUMBER") == "2":
            version2 = v
            break

    if version2 is None:
        raise ValueError("No VERSION NUMBER='2' found in ground truth")

    # Parse LOCATION tags
    for loc in version2.findall("LOCATION"):
        orig = int(loc.attrib["ORIG"])
        new  = int(loc.attrib["NEW"])

        # ORIG = -1 means added line and  ignore for mapping evaluation
        if orig >= 0:
            gt[orig].append(new)

    return dict(gt)
