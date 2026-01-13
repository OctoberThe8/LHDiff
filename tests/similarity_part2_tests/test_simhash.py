from similarity.similarity_part2.simhash import simhash

print("Testing SimHash...\n")

#Test identical lines
h1 = simhash("hello world")
h2 = simhash("hello world")
print("Hash1:", h1)
print("Hash2:", h2)
print("Identical:", h1 == h2)

#Test small change
h3 = simhash("hello worlx")
print("\nHash3:", h3)

print("Difference between h1 and h3:", bin(h1 ^ h3))
