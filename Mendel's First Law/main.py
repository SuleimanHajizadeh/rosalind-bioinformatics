# 1. Fayldan k, m, n qiymətlərini oxuyuruq
with open("rosalind_iprb.txt", "r") as file:
    k, m, n = map(int, file.read().split())

# Toplam fərdlərin sayı
total = k + m + n

# Seçilə biləcək bütün mümkün cütlüklərin sayı
total_pairs = total * (total - 1)

# Resessiv (aa) nəsil verə biləcək cütlüklərin ehtimalları:
# aa x aa -> 100% resessiv nəsil yaradır (1.0)
prob_aa_aa = (n * (n - 1)) / total_pairs * 1.0

# Aa x aa və ya aa x Aa -> 50% resessiv nəsil yaradır (0.5)
prob_Aa_aa = (m * n + n * m) / total_pairs * 0.5

# Aa x Aa -> 25% resessiv nəsil yaradır (0.25)
prob_Aa_Aa = (m * (m - 1)) / total_pairs * 0.25

# Toplam resessiv nəsil ehtimalı
prob_recessive = prob_aa_aa + prob_Aa_aa + prob_Aa_Aa

# Dominant fenotip ehtimalı = 1 - resessiv ehtimalı
prob_dominant = 1 - prob_recessive

# 2. Nəticəni ekrana çıxarırıq (Rosalind 5 nöqtədən sonra 5 rəqəm qəbul edir)
print(f"{prob_dominant:.5f}")

# 3. Cavabı yeni fayla qeyd edirik
with open("rosalind_iprb_output.txt", "w") as output_file:
    output_file.write(f"{prob_dominant:.5f}")