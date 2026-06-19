# 1. Giriş faylından dominant (k), heterozigot (m) və resessiv (n) fərdlərin sayını oxuyuruq
# Read counts of homozygous dominant (k), heterozygous (m), and homozygous recessive (n)
with open("rosalind_iprb.txt", "r") as file:
    k, m, n = map(int, file.read().split())

# Ümumi populyasiya sayı
# Total population size
total = k + m + n

# 2. Resessiv fenotipə malik uşaq yaranma ehtimalını (prob_recessive) hesablayırıq
# Compute the probability of producing an offspring with homozygous recessive genotype
# Çünki bu ehtimalı tapıb 1-dən çıxmaq dominant fenotipi tapmağın ən asan yoludur
# Calculate probability of recessive outcome and subtract from 1 to get dominant probability
total_pairs = total * (total - 1)

# İki resessiv fərdin cütləşməsi ehtimalı: n/total * (n-1)/(total-1) -> Uşaq 100% resessiv olur (1.0)
prob_n_n = (n * (n - 1)) / total_pairs

# İki heterozigot fərdin cütləşməsi ehtimalı: m/total * (m-1)/(total-1) -> Uşaq 25% resessiv olur (0.25)
prob_m_m = (m * (m - 1)) / total_pairs * 0.25

# Bir heterozigot və bir resessiv fərdin cütləşməsi ehtimalı:
# 2 * (m/total * n/(total-1)) -> Uşaq 50% resessiv olur (0.5)
prob_m_n = (2 * m * n) / total_pairs * 0.5

prob_recessive = prob_n_n + prob_m_m + prob_m_n

# Dominant fenotip ehtimalı: 1 - resessiv fenotip ehtimalı
# Probability of dominant phenotype = 1 - prob_recessive
prob_dominant = 1 - prob_recessive
result_str = f"{prob_dominant:.5f}"
print(result_str)

# 3. Cavabı yeni fayla qeyd edirik
# Write result to output.txt
with open("output.txt", "w") as output_file:
    output_file.write(result_str + "\n")
