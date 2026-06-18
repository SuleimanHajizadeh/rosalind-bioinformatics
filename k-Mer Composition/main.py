# rosalind_kmer.py
import os
import itertools

# 1. Faylın yerləşdiyi qovluğu tapırıq və FASTA faylını oxuyuruq
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "rosalind_kmer.txt")

dna_seq = ""
with open(input_path, "r") as file:
    for line in file:
        line = line.strip()
        if not line.startswith(">"):
            dna_seq += line

# 2. Bütün mümkün 4-merləri leksikoqrafik ardıcıllıqla (A, C, G, T) generasiya edirik
# Ümumi kombinasiya sayı: 4^4 = 256
bases = ['A', 'C', 'G', 'T']
kmers = [''.join(p) for p in itertools.product(bases, repeat=4)]

# Tezlikləri saxlamaq üçün lüğət yaradırıq
kmer_counts = {kmer: 0 for kmer in kmers}

# 3. DNT sətiri boyunca sürüşən pəncərə (sliding window) ilə hər bir 4-merin sayını hesablayırıq
k = 4
for i in range(len(dna_seq) - k + 1):
    current_kmer = dna_seq[i:i+k]
    if current_kmer in kmer_counts:
        kmer_counts[current_kmer] += 1

# 4. Sayları leksikoqrafik sırada aralarında boşluqla birləşdiririk
result_list = [str(kmer_counts[kmer]) for kmer in kmers]
result_str = " ".join(result_list)

# 5. Nəticəni həm ekrana çıxarırıq, həm də output.txt faylına yazırıq
print(result_str[:200] + " ...") # Ekrana çıxışın çox böyük olmaması üçün qısaldırıq

output_path = os.path.join(script_dir, "output.txt")
with open(output_path, "w") as out_file:
    out_file.write(result_str + "\n")
