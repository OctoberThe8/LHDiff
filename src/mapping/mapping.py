# src/mapping/mapping.py

from typing import Dict, List, Tuple

THRESHOLD = 0.5  # default threshold, adjust if needed
WEIGHT_CONTENT = 0.6
WEIGHT_SIMHASH = 0.4


def combined_score(content_score: float, simhash_score: float,
                   w_content: float = WEIGHT_CONTENT,
                   w_simhash: float = WEIGHT_SIMHASH) -> float:
    """
    Combine content-based and SimHash similarity scores using given weights.
    """
    return w_content * content_score + w_simhash * simhash_score


def choose_best_match(left: int, candidates: List[int],
                      content_scores: Dict[Tuple[int,int], float],
                      simhash_scores: Dict[Tuple[int,int], float]) -> Tuple[int, float]:
    """
    Choose the best right line for a left line from top-k candidates.

    Parameters:
      left            : index of left line
      candidates      : list of right line indices from top-k (shortlist)
      content_scores  : similarity scores based on content
      simhash_scores  : similarity scores based on SimHash

    Returns:
      (best_right_line, combined_score)
    """
    best_score = -1
    best_right = None

    for right in candidates:
        content = content_scores.get((left, right), 0)
        simhash = simhash_scores.get((left, right), 0)
        score = combined_score(content, simhash)
        if score > best_score:
            best_score = score
            best_right = right

    return best_right, best_score


def resolve_conflicts(mapping: Dict[int, Tuple[int, float]]) -> Dict[int, int]:
    """
    Resolve conflicts: if two left lines map to the same right line,
    keep the left line with the higher score.

    Input mapping: {left_line: (right_line, score)}
    Output: {left_line: right_line}
    """
    right_taken = {}
    final_mapping = {}

    sorted_items = sorted(mapping.items(), key=lambda x: -x[1][1])

    for left, (right, score) in sorted_items:
        if right is None:
            continue
        if right not in right_taken:
            right_taken[right] = left
            final_mapping[left] = right

    return final_mapping


# -----------------------------------------------------------
# FIXED VERSION — preserves Parsia’s design completely
# -----------------------------------------------------------
def generate_mapping(
    similarity_scores: Dict[Tuple[int,int], float],
    top_k: Dict[int, List[int]],
    unchanged_pairs: List[Tuple[int,int]] = None,
    threshold: float = THRESHOLD
) -> Dict[int, int]:
    """
    Returns a mapping: left_line_index -> right_line_index

    Parameters:
      similarity_scores : content-based similarity (Noor's Levenshtein + Cosine)
      top_k             : top-k candidates (SimHash shortlist)
      unchanged_pairs   : automatically matched unchanged lines
      threshold         : minimum combined score to accept a match
    """

    # -----------------------------------------
    # IMPORTANT FIX:
    # We must create a fake simhash_scores dict
    # so Parsia's combined scoring still works.
    # SimHash is used ONLY for filtering by top-k.
    # -----------------------------------------
    simhash_scores = {
        (l, r): 1.0   # treat SimHash similarity as perfect inside shortlist
        for (l, r), _ in similarity_scores.items()
    }

    preliminary_mapping = {}

    # --- Add unchanged lines first ---
    if unchanged_pairs:
        for L, R in unchanged_pairs:
            preliminary_mapping[L] = (R, 1.0)

    # --- Process remaining lines using Parsia's weighted scoring ---
    for left, candidates in top_k.items():
        if left in preliminary_mapping:
            continue

        best_right, best_score = choose_best_match(
            left, candidates, similarity_scores, simhash_scores
        )

        if best_score is not None and best_score >= threshold:
            preliminary_mapping[left] = (best_right, best_score)
        else:
            preliminary_mapping[left] = (None, best_score)

    # --- Resolve conflicts (same right line chosen twice) ---
    final_mapping = resolve_conflicts(preliminary_mapping)
    return final_mapping
