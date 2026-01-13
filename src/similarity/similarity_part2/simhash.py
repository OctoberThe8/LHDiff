import re


"""Break a line into simple tokens (only letters, digits, and underscores) """
def tokenize(text: str):
    # This regex finds words like "hello", "var1", "my_function"
    return re.findall(r"[A-Za-z0-9_]+", text)


"""Create a 64-bit SimHash fingerprint for the given line of text."""
def simhash(text: str) -> int:
    tokens = tokenize(text)

    # If line has nothing meaningful, return 0 fingerprint
    if not tokens:
        return 0

    # Start with a 64 length vector of zeros
    # We will gradually push each entry positive or negative
    bit_vector = [0] * 64

    # For every token in the line
    for token in tokens:
        h = hash(token)                # Python's built-in hash of the token

        # we go through all 64 bits of the hash
        for i in range(64):
            bit = (h >> i) & 1         # extract the i-th bit of h

            # If bit is 1 we push vector[i] up else push it down
            bit_vector[i] += 1 if bit else -1

    # Now we convert the sign of bit_vector into actual bits
    fingerprint = 0
    for i in range(64):
        if bit_vector[i] > 0:
            # Set this bit in the final 64-bit fingerprint
            fingerprint |= (1 << i)

    return fingerprint
