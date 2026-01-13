from utils.convert_ground_truth import convert_ground_truth
import os

PAIRS = [
    # Java
    ("GamePanel", "java"),
    ("Server", "java"),
    ("jsonMapping", "java"),
    ("SchoolNullPointerDemo", "java"),
    ("WebGisApp", "java"),
    ("main", "java"),          # Main2.xml to main_1.java / main_2.java

    # C#
    ("SmartCardReader", "cs"),

    # Python
    ("guessGame", "py"),
    ("llms_eval", "py"),
    ("multithreading", "py"),
    ("multiprocessing_worker", "py"),
    ("random_data_library", "py"),
    ("pyqt_test", "py"),
    ("loo_cross_validation", "py"),
    ("scrolling_background", "py"),

    # C / C++
    ("game", "c"),
    ("proc", "c"),
    ("is_permutation", "cpp"),
    ("urldecoder", "cpp"),
    ("Array_Data", "cpp"),

    # PHP
    ("cart", "php"),
    ("login", "php"),

    # JavaScript
    ("js-array", "js"),
    ("localStorage", "js"),

    # SQL
    ("fizzbuzz_sql_mapping", "sql"),

    # Java (standalone)
    ("Date", "java"),
]

os.makedirs("data/ground_truth/normalized", exist_ok=True)

for name, ext in PAIRS:
    raw_xml = f"data/ground_truth/real/{name}.xml"
    old_src = f"data/old/{name}_1.{ext}"
    new_src = f"data/new/{name}_2.{ext}"
    out_xml = f"data/ground_truth/normalized/{name}_normalized.xml"

    if not os.path.exists(raw_xml):
        print(f"Missing GT: {raw_xml}")
        continue

    if not os.path.exists(old_src) or not os.path.exists(new_src):
        print(f"Missing source for {name}")
        continue

    print(f"🔁 Converting {name}...")
    convert_ground_truth(raw_xml, old_src, new_src, out_xml)
    print(f"Converted XML saved to {out_xml}")

print("All possible ground truth files converted.")
