def hamming_distance(h1: int, h2: int) -> int:
    """Count how many bits differ between two 64-bit numbers."""

    # XOR: bits become 1 only when h1 and h2 differ
    x = h1 ^ h2

    count = 0

    # Loop runs once per 1-bit in x
    # (Brian Kernighan’s bit trick)
    while x:
        count += 1                       # found a differing bit
        x &= x - 1                       # remove the lowest 1-bit

    return count                          # total number of different bits
