# 1. Faylı oxuyuruq
# Read DNA string from the input file
with open("rosalind_rna.txt", "r") as file:
    dna = file.read().strip()

# 2. 'T' hərflərini 'U' ilə əvəz edərək RNT zəncirini tapırıq
# Transcribe DNA to RNA by replacing 'T' with 'U'
rna = dna.replace("T", "U")

print(rna)

# 3. Nəticəni output.txt faylına yazırıq
# Save the transcribed RNA sequence to output.txt
with open("output.txt", "w") as output_file:
    output_file.write(rna + "\n")
