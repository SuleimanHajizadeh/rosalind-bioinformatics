# rosalind_cat.py
import os
import sys

# Rekursiya limitini artırırıq ki, uzun sətirlərdə problem olmasın
sys.setrecursionlimit(2000)

# 1. Faylın yerləşdiyi qovluğu tapırıq və FASTA faylını oxuyuruq
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "rosalind_cat.txt")

rna_seq = ""
with open(input_path, "r") as file:
    for line in file:
        line = line.strip()
        if not line.startswith(">"):
            rna_seq += line

# 2. Dinamik Proqramlaşdırma (DP) üçün memoization lüğəti (cache)
memo = {}

# Komplementar cütlükləri təyin edirik
complements = {
    'A': 'U', 'U': 'A',
    'C': 'G', 'G': 'C'
}

def count_noncrossing_matchings(s):
    # Əgər sətir boşdursa, 1 mükəmməl uyğunlaşma var (baza halı)
    if not s:
        return 1
    # Əgər sətir tək sayda nukleotiddən ibarətdirsə, mükəmməl uyğunlaşma mümkün deyil
    if len(s) % 2 != 0:
        return 0
    # Əgər bu alt-sətir artıq hesablanıbsa, cache-dən götürürük
    if s in memo:
        return memo[s]
    
    total = 0
    first_char = s[0]
    
    # Birinci nukleotidi (s[0]) digər cütləşə biləcək s[k] ilə cütləşdiririk.
    # Qrafın kəsişməməsi üçün k mütləq tək ədəd (odd index) olmalıdır.
    for k in range(1, len(s), 2):
        if s[k] == complements.get(first_char, ''):
            # Cütləşmə {0, k} qrafı iki hissəyə ayırır:
            # 1. Daxili hissə (inner): s[1:k]
            # 2. Xarici hissə (outer): s[k+1:]
            # Hər iki hissənin müstəqil şəkildə mükəmməl uyğunlaşma saylarının hasilini tapırıq
            inner_ways = count_noncrossing_matchings(s[1:k])
            outer_ways = count_noncrossing_matchings(s[k+1:])
            
            # Ümumi sayı toplayırıq (mod 1,000,000 ilə)
            total = (total + (inner_ways * outer_ways)) % 1000000
            
    memo[s] = total
    return total

# 3. Hesablamanı aparırıq
result = count_noncrossing_matchings(rna_seq)

# 4. Nəticəni həm ekrana çıxarırıq, həm də output.txt faylına yazırıq
print(f"Kəsişməyən mükəmməl cütləşmələrin sayı (% 1,000,000): {result}")

output_path = os.path.join(script_dir, "output.txt")
with open(output_path, "w") as out_file:
    out_file.write(str(result) + "\n")
