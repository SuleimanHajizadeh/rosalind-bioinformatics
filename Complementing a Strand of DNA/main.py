# 1. Faylı oxuyuruq
# Read the DNA sequence from the input file
with open("rosalind_revc.txt", "r") as file:
    dna = file.read().strip()

# 2. Komplementar hərfləri əvəzləmək üçün lüğət yaradırıq
# Create translation table to swap complementary bases
mapping = str.maketrans("ATCG", "TAGC")

# 3. Ardıcıllığı tərsinə çeviririk və komplementlərini tapırıq
# Reverse string and translate to get reverse complement
reverse_complement = dna[::-1].translate(mapping)

print(reverse_complement)

# 4. Cavabı yeni fayla qeyd edirik
# Write the output to output.txt
with open("output.txt", "w") as output_file:
    output_file.write(reverse_complement + "\n")
