# rosalind_pmch.py
import os
import math

# RNT ardıcıllığında mükəmməl ikili cütləşmələrin (perfect matchings) sayını tapırıq
# Compute the number of perfect matchings of base pairings (A-U and C-G) in RNA sequence

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "rosalind_pmch.txt")

# FASTA formatındakı fayldan yalnız RNT ardıcıllığını oxuyuruq
# Parse FASTA file to load RNA string
rna_seq = ""
with open(input_path, "r") as file:
    for line in file:
        line = line.strip()
        if not line.startswith(">"):
            rna_seq += line

# A-lar və C-lər sayını tapırıq (mükəmməl cütləşmə üçün A=U və C=G olmalıdır)
# Count A and C occurrences
a = rna_seq.count("A")
c = rna_seq.count("C")

# Mükəmməl cütlərin sayı: a! * c!
# Number of perfect matchings is a! * c!
ans = math.factorial(a) * math.factorial(c)
print(ans)

# Nəticəni output.txt faylına yazırıq
# Save results to output.txt
output_path = os.path.join(script_dir, "output.txt")
with open(output_path, "w") as output_file:
    output_file.write(str(ans) + "\n")
