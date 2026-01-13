import math
from collections import Counter

def _context_to_counts(context: list[str]) -> Counter:
    """
    Convert context lines to a token-frequency vector for cosine similarity.
    """

    return Counter(" ".join(context).split())

def cosine_similarity(context1: list[str], context2: list[str]) -> float:
    """
    Return a cosine similarity score (0 to 1) between two contexts.

    context1 -- list of lines around a target line (left file)
    context2 -- list of lines around a target line (right file)
    """

    vector1 = _context_to_counts(context1)
    vector2 = _context_to_counts(context2)
    
    # Check if both contexts are empty, treat them as maximally similar
    if not vector1 and not vector2:
        return 1.0
    
    # Take the dot product on the union of tokens
    all_tokens = set(vector1) | set(vector2)
    dot_product = sum(vector1[token] * vector2[token] for token in all_tokens)

    # Euclidean norms of frequency vectors
    norm1 = math.sqrt(sum(count * count for count in vector1.values()))
    norm2 = math.sqrt(sum(count * count for count in vector2.values()))

    # Handle division by zero if one vector has no non-zero tokens
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)
