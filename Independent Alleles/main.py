# 1. Giriş faylından k (nəsil sayı) və n (ən azı bu qədər AaBb fərdi olması həddi) oxuyuruq
# Read generation k and threshold n from the dataset file
with open("rosalind_lia.txt", "r") as file:
    line = file.read().strip()
    parts = line.split()
    k = int(parts[0])
    n = int(parts[1])

# 2. k-cı nəsildə fərdlərin ümumi sayını hesablayırıq: 2^k
# Total offspring in the k-th generation is 2^k
total_population = 2**k

# Hər fərdin AaBb genotipinə sahib olma ehtimalı p = 0.25 (Aa x AaBb və Bb x AaBb cütləşməsinə görə)
# Probability of AaBb genotype for any offspring is p = 0.25
p_AaBb = 0.25

# 3. Binomial paylanma vasitəsilə ehtimalı hesablayırıq
# Calculate the probability of having at least n AaBb individuals using binomial probability
import math

# Ən azı n fərd olması ehtimalı = 1 - (n-dən az AaBb olması ehtimalı)
# Probability(at least n) = 1 - sum(Probability(i) for i in range(n))
prob_less_than_n = 0.0
for i in range(n):
    # C(total, i) * p^i * (1-p)^(total - i)
    combinations = math.comb(total_population, i)
    prob_i = combinations * (p_AaBb**i) * ((1 - p_AaBb)**(total_population - i))
    prob_less_than_n += prob_i

probability = 1.0 - prob_less_than_n
result_str = f"{probability:.3f}"
print(result_str)

# 4. Nəticəni output.txt faylına yazırıq
# Write result probability to output.txt
with open("output.txt", "w") as output_file:
    output_file.write(result_str + "\n")
