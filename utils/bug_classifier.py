"""
Bug change classifier for (BONUS FEATURE)

This module classifies line-level changes as:
- bug-fix
- bug-introducing
- neutral

The classification is heuristic-based and relies on:
- mapping structure
- change type (insert / delete / modify)
- safety-related keywords

"""

from typing import Dict, List

BUG_FIX_KEYWORDS = {
    "if", "null", "none", "try", "catch", "except",
    "assert", "check", "validate", "error", "return",
    "raise", "throw", "fail", "exit",
    "len(", "size(", "index",
    "==", "!=", "<=", ">=",
}


BUG_INTRO_KEYWORDS = {
    "delete", "remove"
}


def classify_change(
    old_lines: List[str],
    new_lines: List[str],
    mapping: Dict[int, List[int]]
) -> Dict[int, str]:
    """
    Classify each changed line as:
    - bug-fix
    - bug-introducing
    - neutral

    Returns:
        Dict[left_line_index -> label]
    """

    labels: Dict[int, str] = {}

    for l_idx, r_idxs in mapping.items():
        # Deleted line
        if not r_idxs:
            old_line = old_lines[l_idx].lower()
            if any(k in old_line for k in BUG_FIX_KEYWORDS):
                labels[l_idx] = "bug-introducing"
            else:
                labels[l_idx] = "neutral"
            continue

        # Insert / split
        if len(r_idxs) > 1:
            labels[l_idx] = "bug-fix"
            continue

        # One-to-one mapping (modify or unchanged)
        r_idx = r_idxs[0]

        old_line = old_lines[l_idx].lower()
        new_line = new_lines[r_idx].lower()

        if old_line == new_line:
            labels[l_idx] = "neutral"
            continue

        # Bug-fix heuristic
        if any(k in new_line for k in BUG_FIX_KEYWORDS):
            labels[l_idx] = "bug-fix"
        # Bug-introducing heuristic
        elif any(k in old_line for k in BUG_FIX_KEYWORDS) and not any(
            k in new_line for k in BUG_FIX_KEYWORDS
        ):
            labels[l_idx] = "bug-introducing"
        else:
            labels[l_idx] = "neutral"

    return labels
