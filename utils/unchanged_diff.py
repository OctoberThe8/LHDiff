# Helper function to calculate diff

def find_unchanged_lines(left_lines, right_lines):
    """
    Simple unchanged detector:
    returns [(L_index, R_index)] pairs
    """
    pairs = []
    right_map = {line: i for i, line in enumerate(right_lines)}

    for lx, line in enumerate(left_lines):
        if line in right_map:
            pairs.append((lx, right_map[line]))

    return pairs
