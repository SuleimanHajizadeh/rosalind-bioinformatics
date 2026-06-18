# rosalind_sign.py
import os
import itertools

# 1. Faylın yerləşdiyi qovluğu tapırıq və n ədədini oxuyuruq
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "rosalind_sign.txt")

# Əgər fayl yoxdursa, istifadəçinin daxil etməsi üçün nümunə kimi n = 2 götürürük
if os.path.exists(input_path):
    with open(input_path, "r") as file:
        n = int(file.read().strip())
else:
    print(f"Məlumat: '{input_path}' faylı tapılmadı. Nümunə olaraq n = 2 üçün hesablanır.")
    n = 2

# 2. 1-dən n-ə qədər olan ədədlərin adi permutasiyalarını tapırıq
numbers = list(range(1, n + 1))
perms = list(itertools.permutations(numbers))

# 3. Hər bir mövqe üçün mümkün olan işarələrin (+1 və ya -1) kombinasiyalarını tapırıq
sign_combinations = list(itertools.product([-1, 1], repeat=n))

# 4. Bütün işarəli permutasiyaları (signed permutations) qururuq
signed_perms = []
for perm in perms:
    for signs in sign_combinations:
        # Hər bir elementi öz işarəsinə vururuq
        signed_perm = [val * sign for val, sign in zip(perm, signs)]
        signed_perms.append(signed_perm)

# 5. Çıxış formatını hazırlayırıq (əvvəlcə ümumi say, sonra hər bir permutasiya)
output_lines = [str(len(signed_perms))]
for sp in signed_perms:
    output_lines.append(" ".join(map(str, sp)))

full_output = "\n".join(output_lines)

# 6. Nəticəni həm ekrana çıxarırıq, həm də output.txt faylına yazırıq
print(f"Ümumi işarəli permutasiya sayı: {len(signed_perms)}")

output_path = os.path.join(script_dir, "output.txt")
with open(output_path, "w") as out_file:
    out_file.write(full_output + "\n")
