# rosalind_corr.py
import os

# 1. Tərs komplement (reverse complement) tapan köməkçi funksiya
def reverse_complement(seq):
    mapping = str.maketrans("ATCG", "TAGC")
    return seq[::-1].translate(mapping)

# 2. İki sətir arasındakı Hamming məsafəsini tapan funksiya
def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

# 3. Giriş faylını oxuyuruq
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "rosalind_corr.txt")

reads = []
curr_seq = ""

with open(input_path, "r") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if curr_seq:
                reads.append(curr_seq)
                curr_seq = ""
        else:
            curr_seq += line
    if curr_seq:
        reads.append(curr_seq)

# 4. Hər bir oxunuşun (read) və onun tərs komplementinin ümumi sayını tapırıq
counts = {}
for r in reads:
    counts[r] = counts.get(r, 0) + 1

# Düzgün və səhv oxunuşları müəyyənləşdiririk
correct_reads = set()
for r in reads:
    rev_r = reverse_complement(r)
    # Əgər oxunuş və ya onun tərs komplementi cəmi 2 və ya daha çox sayda tapılıbsa, o düzgündür
    if counts.get(r, 0) + counts.get(rev_r, 0) >= 2:
        correct_reads.add(r)
        correct_reads.add(rev_r)

# Səhv oxunuşlar (correct_reads çoxluğunda olmayanlar)
incorrect_reads = []
for r in reads:
    if r not in correct_reads:
        incorrect_reads.append(r)

# 5. Səhv oxunuşları düzəldirik
corrections = []
for r in incorrect_reads:
    # Səhv oxunuşun Hamming məsafəsi 1 olan düzgün oxunuşu (və ya onun tərs komplementini) tapırıq
    for c in correct_reads:
        if hamming_distance(r, c) == 1:
            corrections.append(f"{r}->{c}")
            break

# 6. Nəticələri ekrana çıxarırıq və output.txt faylına yazırıq
output_content = "\n".join(corrections)
print(output_content[:1000] + "\n...") # Çox böyük çıxışın qarşısını almaq üçün ekrana qısa yazdırırıq

output_path = os.path.join(script_dir, "output.txt")
with open(output_path, "w") as out_file:
    out_file.write(output_content + "\n")
