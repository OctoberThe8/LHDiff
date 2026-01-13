import os
from src.pipeline import run_pipeline
from utils.load_mutation_ground_truth import load_mutation_ground_truth
from utils.evaluate import evaluate

BASE_MUTATION_DIR = "data/mutations/sampleX"
GT_PATH = "data/ground_truth/mutations/sampleX_gt.xml"

ORIGINAL = os.path.join(BASE_MUTATION_DIR, "original.txt")

MUTATIONS = [
    "insert.txt",
    "delete.txt",
    "modify.txt",
    "rename.txt",
    "split.txt",
    "merge.txt",
    "move.txt",
    "whitespace.txt",
]

def main():
    if not os.path.exists(ORIGINAL):
        raise FileNotFoundError("original.txt not found")

    if not os.path.exists(GT_PATH):
        raise FileNotFoundError("Mutation ground truth not found")

    ground_truth = load_mutation_ground_truth(GT_PATH)

    print("\nMUTATION EVALUATION\n")

    for mutation in MUTATIONS:
        mutated = os.path.join(BASE_MUTATION_DIR, mutation)

        if not os.path.exists(mutated):
            print(f"Skipping missing mutation: {mutation}")
            continue

        print(f"--- Testing mutation: {mutation} ---")

        predicted, _, _ = run_pipeline(
            ORIGINAL,
            mutated,
            top_k_value=15
        )

        # Evaluate only GT-covered lines
        filtered_pred = {
            k: v for k, v in predicted.items()
            if k in ground_truth
        }

        metrics = evaluate(filtered_pred, ground_truth)
        print(metrics)
        print()

if __name__ == "__main__":
    main()
