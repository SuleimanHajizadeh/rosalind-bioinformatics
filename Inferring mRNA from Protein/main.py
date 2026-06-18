# rosalind_mrna.py

# 1. Hər bir amin turşusunun neçə fərqli kodonla kodlaşdırıldığını təyin edirik
CODON_COUNTS = {
    'A': 4, 'C': 2, 'D': 2, 'E': 2, 'F': 2, 'G': 4, 'H': 2, 'I': 3, 'K': 2, 'L': 6,
    'M': 1, 'N': 2, 'P': 4, 'Q': 2, 'R': 6, 'S': 6, 'T': 4, 'V': 4, 'W': 1, 'Y': 2
}

# 2. Giriş faylından zülal ardıcıllığını oxuyuruq
with open("rosalind_mrna.txt", "r") as file:
    protein_seq = file.read().strip()

# 3. Hesablamaya 3 ilə başlayırıq (çünki 3 fərqli STOP kodonu var)
total_combinations = 3

# 4. Hər bir amin turşusu üçün kombinasiyaları vururuq və mod 1,000,000 alırıq
# Hər addımda modulo almaq yaddaşda (memory) böyük rəqəmlərin yaranmasının qarşısını alır
for amino_acid in protein_seq:
    if amino_acid in CODON_COUNTS:
        total_combinations = (total_combinations * CODON_COUNTS[amino_acid]) % 1000000

# 5. Nəticəni ekrana yazdırırıq və çıxış faylına qeyd edirik
print(total_combinations)

with open("rosalind_mrna_output.txt", "w") as output_file:
    output_file.write(str(total_combinations))