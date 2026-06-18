# rosalind_pmch.py
import os
import math

# 1. Faylın yerləşdiyi qovluğu tapırıq və girişi oxuyuruq
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "rosalind_pmch.txt")

# FASTA formatındakı fayldan yalnız RNT ardıcıllığını oxuyuruq
rna_seq = ""
with open(input_path, "r") as file:
    for line in file:
        line = line.strip()
        if not line.startswith(">"):
            rna_seq += line

# 2. 'A' (Adenin) və 'C' (Sitozin) nukleotidlərin sayını tapırıq
# Şərtə görə A-nın sayı U-ya, C-nin sayı isə G-yə bərabərdir (N_A = N_U, N_C = N_G)
n_A = rna_seq.count('A')
n_C = rna_seq.count('C')

# 3. Mümkün olan bütün mükəmməl uyğunlaşmaların (perfect matchings) sayını hesablayırıq
# Hər bir A nukleotidi hər hansı bir U nukleotidi ilə cütləşə bilər (n_A! fərqli üsul)
# Eyni qaydada hər bir C nukleotidi hər hansı bir G nukleotidi ilə cütləşə bilər (n_C! fərqli üsul)
# İki cütləşmə bir-birindən asılı olmadığı üçün ümumi say: n_A! * n_C!
total_matchings = math.factorial(n_A) * math.factorial(n_C)

# 4. Nəticəni həm ekrana çıxarırıq, həm də output.txt faylına yazırıq
print(f"Mükəmməl cütləşmələrin sayı: {total_matchings}")

output_path = os.path.join(script_dir, "output.txt")
with open(output_path, "w") as out_file:
    out_file.write(str(total_matchings) + "\n")
