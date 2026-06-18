# rosalind_tree.py
import os

# 1. Faylın yerləşdiyi qovluğu tapırıq və girişi oxuyuruq
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "rosalind_tree.txt")

with open(input_path, "r") as file:
    lines = file.read().splitlines()

# Birinci sətir təpə nöqtələrinin (nodes) ümumi sayıdır (n)
n = int(lines[0].strip())

# Qalan dolu sətirlər isə qrafın tilləridir (edges)
edges = [line for line in lines[1:] if line.strip()]
E = len(edges)

# 2. Qrafın ağac (tree) olması üçün lazım olan minimum əlavə til sayını tapırıq
# Hər hansı bir dövrü (cycle) olmayan qrafda Tillərin sayı = Təpələrin sayı - Komponentlərin sayı (E = n - C)
# Ağac tək bir komponentdən ibarət olduğu üçün C = 1 olmalıdır, yəni E = n - 1.
# Bu səbəbdən, əlavə edilməli olan tillərin sayı: C - 1 = n - E - 1
result = n - E - 1

# 3. Nəticəni həm ekrana çıxarırıq, həm də output.txt faylına yazırıq
print(f"Əlavə edilməli olan tillərin sayı (n={n}, E={E}): {result}")

output_path = os.path.join(script_dir, "output.txt")
with open(output_path, "w") as out_file:
    out_file.write(str(result) + "\n")
