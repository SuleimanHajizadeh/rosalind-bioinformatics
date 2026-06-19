# 1. Giriş faylını oxuyuruq
# Read DNA sequences from the input file
with open("rosalind_hamm.txt", "r") as file:
    lines = file.read().splitlines()

s = lines[0]
t = lines[1]

# 2. İki ardıcıllıq arasındakı Hemminq məsafəsini (Hamming distance) tapırıq
# Calculate Hamming distance by summing positions with mismatching characters
hamming_distance = sum(1 for x, y in zip(s, t) if x != y)

print(hamming_distance)

# 3. Nəticəni output.txt faylına yazırıq
# Save the hamming distance to output.txt
with open("output.txt", "w") as output_file:
    output_file.write(str(hamming_distance) + "\n")
