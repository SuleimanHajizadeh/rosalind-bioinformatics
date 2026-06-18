import itertools

# 1. Read input from the file
with open("rosalind_lexf.txt", "r") as file:
    lines = file.readlines()
    # First line contains the alphabet symbols
    alphabet = lines[0].split()
    # Second line contains the length n
    n = int(lines[1].strip())

# 2. Generate lexicographically ordered strings
# itertools.product generates products in the order of the input alphabet
# Since we need lexicographical order, we ensure the alphabet is sorted
alphabet.sort()
kmers = itertools.product(alphabet, repeat=n)

# 3. Output the results
for kmer in kmers:
    print("".join(kmer))