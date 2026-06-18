# rosalind_inod.py
import os

# 1. Faylın yerləşdiyi qovluğu tapırıq və n (yarpaq sayını) oxuyuruq
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "rosalind_inod.txt")

with open(input_path, "r") as file:
    n = int(file.read().strip())

# 2. Köksüz binar ağacda daxili təpələrin (internal nodes) sayını tapırıq
# Yarpaqların sayı n olarsa, daxili təpələrin sayı həmişə: I = n - 2 olur.
# İsbatı:
# Təpələrin cəmi: V = n + I
# Tillərin cəmi: E = V - 1 = n + I - 1
# Qraf xassəsinə görə dərəcələrin cəmi 2E-yə bərabərdir: n * 1 + I * 3 = 2 * (n + I - 1)
# n + 3I = 2n + 2I - 2  =>  I = n - 2
result = n - 2

# 3. Nəticəni həm ekrana çıxarırıq, həm də output.txt faylına yazırıq
print(f"Daxili təpələrin sayı (n={n}): {result}")

output_path = os.path.join(script_dir, "output.txt")
with open(output_path, "w") as out_file:
    out_file.write(str(result) + "\n")
