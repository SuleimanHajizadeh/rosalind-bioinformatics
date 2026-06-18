# rosalind_revp.py

def complement(base):
    mapping = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return mapping.get(base, base)

def reverse_complement(s):
    # DNT-ni tərsinə çevirib hər bir bazın komplementini tapırıq
    return "".join(complement(base) for base in reversed(s))

def is_reverse_palindrome(s):
    return s == reverse_complement(s)

# 1. FASTA faylını oxuyuruq
with open("rosalind_revp.txt", "r") as file:
    lines = file.readlines()

dna_string = "".join([line.strip() for line in lines if not line.startswith(">")])
n = len(dna_string)

# 2. 4 ilə 12 uzunluqları arasında yoxlama aparırıq
results = []
for length in range(4, 13):
    for i in range(n - length + 1):
        substring = dna_string[i : i + length]
        if is_reverse_palindrome(substring):
            # Mövqe 1-əsaslı olduğu üçün i+1
            results.append(f"{i + 1} {length}")

# 3. Nəticəni ekrana çıxarırıq
for r in results:
    print(r)