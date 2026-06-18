# rosalind_prob.py
import os
import math

# 1. Faylın yerləşdiyi qovluğu tapırıq və girişi oxuyuruq
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "rosalind_prob.txt")

with open(input_path, "r") as file:
    lines = file.read().splitlines()
    s = lines[0].strip()
    A = list(map(float, lines[1].split()))

# 2. DNT sətirində GC və AT nukleotidlərinin sayını təyin edirik
n_gc = s.count('G') + s.count('C')
n_at = s.count('A') + s.count('T')

# 3. Hər bir GC-kontent ehtimalı üçün s sətirinin yaranma ehtimalının log10-nu hesablayırıq
# GC nukleotidi üçün ehtimal: x / 2
# AT nukleotidi üçün ehtimal: (1 - x) / 2
# log10(P) = n_gc * log10(x/2) + n_at * log10((1-x)/2)
B = []
for x in A:
    prob_gc = x / 2
    prob_at = (1 - x) / 2
    log_prob = n_gc * math.log10(prob_gc) + n_at * math.log10(prob_at)
    # Rosalind cavabı adətən 3 onluq kəsr dəqiqliyi ilə yuvarlaqlaşdırır
    B.append(f"{log_prob:.3f}")

# 4. Nəticələri aralarında boşluqla birləşdirib ekrana və output.txt faylına yazırıq
result_str = " ".join(B)
print(result_str)

output_path = os.path.join(script_dir, "output.txt")
with open(output_path, "w") as out_file:
    out_file.write(result_str + "\n")
