# 1. Fayldan 6 genotip cütlüyünün sayını oxuyuruq
# Read counts of 6 genotype pairings from the input file
with open("rosalind_iev.txt", "r") as file:
    counts = list(map(int, file.read().split()))

# 2. Cütlüklər üzrə dominant uşaq sayının çəkiləri
# Weights of dominant offspring per pairing (multiplied by 2 as each pair has 2 offspring)
weights = [2, 2, 2, 1.5, 1, 0]

# 3. Gözlənilən dominant uşaqların sayını hesablayırıq
# Calculate total expected number of dominant offspring
expected_dominant = sum(c * w for c, w in zip(counts, weights))

print(expected_dominant)

# 4. Nəticəni output.txt faylına yazırıq
# Write the result to output.txt
with open("output.txt", "w") as output_file:
    output_file.write(str(expected_dominant) + "\n")
