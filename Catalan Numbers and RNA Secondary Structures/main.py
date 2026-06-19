import os
import sys

# Rekursiya limitini artırırıq
# Increase recursion limit for processing longer sequences
sys.setrecursionlimit(2000)

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "rosalind_cat.txt")

# 1. FASTA faylını oxuyuruq
# Read and parse the FASTA file
with open(input_path, "r") as file:
    lines = file.read().splitlines()

seq = ""
for line in lines:
    if not line.startswith(">"):
        seq += line

# Komplementar cütləri yoxlamaq üçün funksiya
# Helper function to check base-pairing compatibility
def is_complement(a, b):
    return (a == 'A' and b == 'U') or (a == 'U' and b == 'A') or \
           (a == 'C' and b == 'G') or (a == 'G' and b == 'C')

memo = {}

# Catalan nömrələrini hesablamaq üçün rekursiv funksiya
# Recursive function with memoization to compute Catalan numbers for RNA structures
def catalan(s):
    if len(s) == 0:
        return 1
    if s in memo:
        return memo[s]
    
    total = 0
    # Düzgün cütləşmələri yoxlayaraq alt strukturlara bölürük
    # Split the sequence at compatible base pairings and multiply subproblem counts
    for i in range(1, len(s), 2):
        if is_complement(s[0], s[i]):
            left_seq = s[1:i]
            # U və A/G/C saylarının eyni olub-olmadığını yoxlayırıq (sürətləndirmək üçün)
            # Verify if subproblems can have matching base counts
            if (left_seq.count('A') + left_seq.count('C') == 
                left_seq.count('U') + left_seq.count('G')):
                total = (total + catalan(left_seq) * catalan(s[i+1:])) % 1000000
                
    memo[s] = total
    return total

result = catalan(seq)
print(result)

# Nəticəni output.txt faylına yazırıq
# Write result to output.txt
output_path = os.path.join(script_dir, "output.txt")
with open(output_path, "w") as output_file:
    output_file.write(str(result) + "\n")
