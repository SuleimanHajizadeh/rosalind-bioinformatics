import os
import sys

# Rekursiya limitini artırırıq
# Increase recursion limit
sys.setrecursionlimit(2000)

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "rosalind_motz.txt")

# FASTA faylını oxuyuruq
# Parse sequence from FASTA format input
with open(input_path, "r") as file:
    lines = file.read().splitlines()

seq = ""
for line in lines:
    if not line.startswith(">"):
        seq += line.strip()

# Komplementar cütləri yoxlamaq üçün köməkçi funksiya
# Check if two nucleotides can pair
def is_complement(a, b):
    return (a == 'A' and b == 'U') or (a == 'U' and b == 'A') or \
           (a == 'C' and b == 'G') or (a == 'G' and b == 'C')

memo = {}

# Motzkin nömrələrini hesablamaq üçün rekursiv funksiya (RNT strukturlarında)
# Compute Motzkin numbers of RNA secondary structures with base crossings allowed
def motzkin(s):
    if len(s) <= 1:
        return 1
    if s in memo:
        return memo[s]
    
    # 1. Birinci nukleotidin cütləşmədiyi hal (motzkin(s[1:]))
    # Option 1: First nucleotide does not pair
    total = motzkin(s[1:]) % 1000000
    
    # 2. Birinci nukleotidin digər uyğun nukleotidlərlə cütləşdiyi hallar
    # Option 2: First nucleotide pairs with a compatible downstream nucleotide
    for i in range(1, len(s)):
        if is_complement(s[0], s[i]):
            total = (total + motzkin(s[1:i]) * motzkin(s[i+1:])) % 1000000
            
    memo[s] = total
    return total

result = motzkin(seq)
print(result)

# Nəticəni output.txt faylına yazırıq
# Save the final count to output.txt
output_path = os.path.join(script_dir, "output.txt")
with open(output_path, "w") as output_file:
    output_file.write(str(result) + "\n")
