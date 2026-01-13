from similarity.similarity_part2.simhash import simhash
from similarity.similarity_part2.hamming import hamming_distance

print("Testing Hamming Distance...\n")

h1 = simhash("apple")
h2 = simhash("apples")

print("h1:", h1)
print("h2:", h2)

dist = hamming_distance(h1, h2)
print("Hamming Distance:", dist)

print("Similarity:", 1 - (dist / 64))
