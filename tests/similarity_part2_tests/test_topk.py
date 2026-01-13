from similarity.similarity_part2.top_k import top_k_candidates

left = [
    "int x = 5;",
    "return x;"
]

right = [
    "int x = 6;",   # very similar to left[0]
    "float y;",     # unrelated
    "return x;"     # identical to left[1]
]

print("Testing Top-K...\n")
result = top_k_candidates(left, right, k=2)
print(result)
