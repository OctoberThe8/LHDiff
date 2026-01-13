def levenshtein(a: str, b: str) -> float:
    """Return a similarity score (0 to 1) between two lines of text using the Levenshtein distance.
    
    Args:
        a: First line (old version)
        b: Second line (new version)

    Returns:
        A float between 0.0 and 1.0 where:
            1.0 means the lines match
            0.0 means the lines do not match
    """
    old_file_len, new_file_len = len(a), len(b)
    
    # Create the matrix of cells (rows = a prefix, columns = b prefix), initialized to 0
    dynamic_programming = [[0 for _ in range(new_file_len + 1)] for _ in range(old_file_len + 1)]
    
    # Initialize the base cases: cost of converting a prefix to/from the empty string
    for i in range(old_file_len + 1):
        dynamic_programming[i][0] = i   # i deletions to turn first i chars of a into empty
    for j in range(new_file_len + 1):
        dynamic_programming[0][j] = j   # j insertions to turn empty into first j chars of b

    # Fill the dynamic programming matrix
    for i in range(1, old_file_len + 1):
        for j in range(1, new_file_len + 1):
            if a[i - 1] == b[j - 1]:
                # Case 1: match, do nothing
                cost = 0
            else:
                # Case 2: mismatch, a single edit needed
                cost = 1

            dynamic_programming[i][j] = min(
                dynamic_programming[i - 1][j - 1] + cost,    # Replace (or keep if cost = 0)
                dynamic_programming[i][j - 1] + 1,           # Insert
                dynamic_programming[i - 1][j] + 1            # Delete
            )
    distance = dynamic_programming[old_file_len][new_file_len]
    max_len = max(old_file_len, new_file_len)

    if max_len == 0:    # Check if both string are empty
        return 1.0

    return 1 - distance / max_len
