import os
from src.pipeline import run_pipeline

OLD_DIR = "data/old"
NEW_DIR = "data/new"

results = []

for fname in sorted(os.listdir(OLD_DIR)):
    if not "_1." in fname:
        continue

    base = fname.replace("_1", "").split(".")[0]

    old_path = os.path.join(OLD_DIR, fname)

    # try to find matching _2 file
    new_file = None
    for f in os.listdir(NEW_DIR):
        if f.startswith(base) and "_2." in f:
            new_file = f
            break

    if not new_file:
        print(f"No matching NEW file for {base}")
        continue

    new_path = os.path.join(NEW_DIR, new_file)

    print("\n" + "=" * 60)
    print(f"Running LHDiff on: {base}")
    print("=" * 60)

    final_mapping, left_lines, right_lines = run_pipeline(
        old_path,
        new_path
    )

print("\nBatch evaluation finished")
