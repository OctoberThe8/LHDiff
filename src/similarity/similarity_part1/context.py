def build_context(lines: list[str], index: int, window: int = 4) -> list[str]:
    """
    Return the surrounding before and after lines of a given 0-based line index, 
    including the line itself.
    
    lines -- list of text lines (for example: from a file)
    index -- 0-based index of the target line
    window -- number of lines to include before and after (default is 4)

    Note: if index is negative, it is clamped to 0, and if it is beyond the last line,
    it is clamped to the final index.
    """
    if index < 0:
        index = 0
    elif index >= len(lines):
        index = len(lines) - 1

    if window < 0:
        raise ValueError("Error: window value must be non-negative.")
    start_index = max(0, index - window)
    end_index = min(len(lines), index + window + 1)

    return lines[start_index:end_index]
