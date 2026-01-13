from typing import Dict, Tuple

from .levenshtein import levenshtein
from .context import build_context
from .cosine import cosine_similarity

CONTENT_WEIGHT = 0.6
CONTEXT_WEIGHT = 0.4

def combined_similarity(left_lines: list[str], right_lines: list[str]) -> Dict[Tuple[int, int], float]:
    """
    Return a similarity score for every left/right line pair.

    Uses:
        Levenshtein distance for content similarity
        Cosine similarity for context similarity

    Args:
        left_lines: normalized or raw lines from the left (old) file.
        right_lines: normalized or raw lines from the right (new) file.

    Returns:
        A dictionary mapping (left_index, right_index) -> combined_score
    """

    scores: Dict[Tuple[int, int], float] = {}

    for i, left_line in enumerate(left_lines):
        # Build context once per left line
        left_context = build_context(left_lines, i)

        for j, right_line in enumerate(right_lines):
            # 1. Content similarity (line text)
            content_similarity = levenshtein(left_line, right_line)

            # 2. Context similarity (surrounding lines)
            right_context = build_context(right_lines, j)
            context_similarity = cosine_similarity(left_context, right_context)

            # 3. Weighted combination
            combined = CONTENT_WEIGHT * content_similarity + CONTEXT_WEIGHT * context_similarity

            scores[(i, j)] = combined
    
    return scores
