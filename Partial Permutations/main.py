# rosalind_pper.py
import os

# 1. Faylın yerləşdiyi qovluğu tapırıq və n, k qiymətlərini oxuyuruq
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "rosalind_pper.txt")

with open(input_path, "r") as file:
    n, k = map(int, file.read().split())

# 2. Hissəvi permutasiyaların sayını P(n, k) modul 1,000,000 ilə hesablayırıq
# P(n, k) = n * (n - 1) * ... * (n - k + 1)
# Böyük ədədlərin yaddaşı doldurmaması üçün hər vurma addımında modul alırıq
result = 1
for i in range(k):
    result = (result * (n - i)) % 1000000

# 3. Nəticəni həm ekrana çıxarırıq, həm də output.txt faylına yazırıq
print(f"Hissəvi permutasiyaların sayı (P({n}, {k}) % 1,000,000): {result}")

output_path = os.path.join(script_dir, "output.txt")
with open(output_path, "w") as out_file:
    out_file.write(str(result) + "\n")
