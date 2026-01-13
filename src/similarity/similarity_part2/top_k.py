from .simhash import simhash
from .hamming import hamming_distance


"""
For each line in left_lines, return the indexes of the top-k most similar
right-side lines (using SimHash + Hamming distance).
"""
def top_k_candidates(left_lines, right_lines, k=15):

    # Compute SimHash for every line on both sides (preprocessing step)
    left_hashes = [simhash(line) for line in left_lines]
    right_hashes = [simhash(line) for line in right_lines]

    result = {}

    # For every line on the left file
    for i, lh in enumerate(left_hashes):

        similarities = []

        # If the line is empty, put one dummy candidate
        if left_lines[i].strip() == "":
            result[i] = []
            continue

        for j, rh in enumerate(right_hashes):
            dist = hamming_distance(lh, rh)
            score = 1 - (dist / 64)
            similarities.append((score, j))

        similarities.sort(reverse=True)
        top_indexes = [idx for (_, idx) in similarities[:k]]

        result[i] = top_indexes

    return result       
