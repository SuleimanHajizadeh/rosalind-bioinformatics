# rosalind_lia.py
import math

# 1. Fayldan k (nəsil) və n (ən azı tələb olunan fərd sayı) qiymətlərini oxuyuruq
with open("rosalind_lia.txt", "r") as file:
    k, n = map(int, file.read().split())

def independent_alleles(k, n):
    # k-cı nəsildəki toplam uşaq sayı
    total_organisms = 2 ** k
    p = 0.25 # Hər bir uşağın Aa Bb olma ehtimalı
    
    # Ən azı n fərd tapmaq ehtimalını hesablamaq üçün, 
    # əvvəlcə uşaq sayının n-dən AZ (0-dan n-1-ə qədər) olma ehtimalını tapıb 1-dən çıxırıq
    prob_less_than_n = 0
    for i in range(n):
        combinations = math.comb(total_organisms, i)
        prob_less_than_n += combinations * (p ** i) * ((1 - p) ** (total_organisms - i))
        
    prob_at_least_n = 1 - prob_less_than_n
    
    # Rosalind cavabı adətən 3 onluq kəsr dəqiqliyi ilə istəyir
    return round(prob_at_least_n, 3)

# 2. Nəticəni hesablayırıq və yazdırırıq
result = independent_alleles(k, n)
print(result)

# 3. Cavabı yeni bir çıxış faylına yazırıq
with open("rosalind_lia_output.txt", "w") as output_file:
    output_file.write(str(result))