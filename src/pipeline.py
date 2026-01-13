
#IMPORT STUFF-------------------
import argparse
import os


# Preprocessing step: this normalizes each file (remove spaces, lowercase, strip comments, etc.)
from src.preprocessing.preprocess import normalize_file

# Utilities (unchanged detection)
# If the unchanged_diff module isn't ready yet, we use a dummy fallback.
try:
    from utils.unchanged_diff import find_unchanged_lines
except ImportError:
    # If import fails, just return an empty list so pipeline doesn't crash.
    def find_unchanged_lines(a, b):
        return []   # fallback for now

# Similarity Part 1 (Noor's part)
# These compute Levenshtein, cosine similarity, and build context windows.
from src.similarity.similarity_part1.levenshtein import levenshtein
from src.similarity.similarity_part1.cosine import cosine_similarity
from src.similarity.similarity_part1.context import build_context
from src.similarity.similarity_part1.combined_similarity import combined_similarity


# Similarity Part 2 (Lynn's part)
# This generates the top-k most similar candidates for each line using SimHash + Hamming.
from src.similarity.similarity_part2.top_k import top_k_candidates

# Mapping (Parsia)
# This takes similarity scores + top-k + unchanged matches and decides final mapping.
from src.mapping.mapping import generate_mapping

# Split detection (Hanan)
# This checks if one line on the left actually maps to multiple lines on the right.
from src.split.split_detection import detect_splits

# Gui Part 
from src.gui_output import runLineTracker


# PIPELINE FUNCTION -------------------

def run_pipeline(old_file_path: str, new_file_path: str, top_k_value: int = 15):
    """
    Complete LHDiff pipeline.
    Returns: dict[L_index -> list of R_indexes]

    (My understanding as a student:)
    - This is basically the “main function” for our whole project.
    - Each step prints what it’s doing so we can debug the workflow.
    """

    print("\n=== 1) Preprocessing files ===")
    # Normalize both files into lists of cleaned lines
    left_lines = normalize_file(old_file_path)
    right_lines = normalize_file(new_file_path)

    print(f"Left lines: {len(left_lines)}, Right lines: {len(right_lines)}")


    print("\n=== 2) Detect unchanged lines (fast matches) ===")
    # These are exact unchanged matches detected quickly (like diff)
    unchanged_pairs = find_unchanged_lines(left_lines, right_lines)
    print(f"Found {len(unchanged_pairs)} unchanged lines")


    print("\n=== 3) Similarity Part 1 (Levenshtein + Cosine) ===")
    # Computes detailed similarity scores between all pairs (content + context)
    similarity_scores = combined_similarity(left_lines, right_lines)
    print(f"Generated {len(similarity_scores)} similarity pairs")


    print("\n=== 4) Similarity Part 2 (SimHash Top-K) ===")
    # Get only the top-k most similar right lines for each left line
    # This speeds up the mapping step a lot.
    top_k = top_k_candidates(left_lines, right_lines, k=top_k_value)
    print("Top-K candidates computed")
    print("\nTop-K sample:", list(top_k.items())[:5])
    print("type of top_k:", type(top_k))
    print("Top-K size =", len(top_k), "Expected =", len(left_lines))




    print("\n=== 5) Mapping (Parsia) ===")
    # Combine all similarity info to produce one final line-to-line mapping
    single_mapping = generate_mapping(similarity_scores, top_k, unchanged_pairs)
    print(f"Mapping generated for {len(single_mapping)} left lines")



    print("\n=== 6) Split Detection (Hanan) ===")
    # Detect if some lines were split into multiple lines in the new version
    final_mapping = detect_splits(left_lines, right_lines, single_mapping)


     # Bonus mark 
    # =============================
    from utils.bug_classifier import classify_change
    print("\n=== 6.5) Bug Change Classification (BONUS) ===")

    bug_labels = classify_change(
        old_lines=left_lines,
        new_lines=right_lines,
        mapping=final_mapping
    )

    # Print a readable summary
    counts = {"bug-fix": 0, "bug-introducing": 0, "neutral": 0}
    for label in bug_labels.values():
        counts[label] += 1

    # Include deleted lines explicitly
    for i in range(len(left_lines)):
        if i not in final_mapping:
            final_mapping[i] = []

    print("Bug classification summary:")
    for k, v in counts.items():
        print(f"  {k}: {v}")

    print("\nSample classified changes (first 10):")
    for i, (l_idx, label) in enumerate(bug_labels.items()):
        if i >= 10:
            break
        old_line = left_lines[l_idx]
        mapped = final_mapping.get(l_idx, [])
        new_line = right_lines[mapped[0]] if mapped else "(deleted)"
        print(f"L{l_idx+1}: {label}")
        print(f"  OLD: {old_line}")
        print(f"  NEW: {new_line}")



    # Evaluation (if GT exists)
    # =============================
    from utils.load_ground_truth import load_ground_truth
    from utils.evaluate import evaluate
    import os
    gt_path = None
    base_name = os.path.splitext(os.path.basename(old_file_path))[0]
    base_name = base_name.replace("_1", "")  # GamePanel_1 -> GamePanel

    candidate_gt = f"data/ground_truth/normalized/{base_name}_normalized.xml"

    if os.path.exists(candidate_gt):
        ground_truth = load_ground_truth(candidate_gt)

        # IMPORTANT: evaluate only on GT-defined lines
        filtered_pred = {
            k: v for k, v in final_mapping.items()
            if k in ground_truth
        }

        metrics = evaluate(filtered_pred, ground_truth)

        print("\n=== 7) Evaluation Results ===")
        print(metrics)
    else:
        print("\n(No ground truth found — skipping evaluation)")


    print("\n=== PIPELINE FINISHED ===")
    print("Final Mapping Output:")
    print(final_mapping)

    return final_mapping, left_lines, right_lines



# TESTING ENTRY POINT -------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="LHDiff Pipeline "
    )

    parser.add_argument(
        "--old",
        required=True,
        help="Path to OLD source file"
    )

    parser.add_argument(
        "--new",
        required=True,
        help="Path to NEW source file"
    )

    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch GUI after processing"
    )

    args = parser.parse_args()

    if not os.path.exists(args.old):
        raise FileNotFoundError(f"Old file not found: {args.old}")

    if not os.path.exists(args.new):
        raise FileNotFoundError(f"New file not found: {args.new}")

    final_mapping, left_lines, right_lines = run_pipeline(
        args.old,
        args.new
    )

    print("\nPIPELINE FINISHED")

    if args.gui:
        from src.gui_output import runLineTracker
        print("Opening GUI window...")
        runLineTracker(left_lines, right_lines, final_mapping)
