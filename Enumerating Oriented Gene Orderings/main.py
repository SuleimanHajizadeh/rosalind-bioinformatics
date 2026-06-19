# rosalind_sign.py
import itertools

# 1. Giriş faylından n ədədini oxuyuruq
# Read n from the dataset file
with open("rosalind_sign.txt", "r") as file:
    n = int(file.read().strip())

# 2. İşarəli permutasiyaları (signed permutations) hesablayırıq
# Compute signed permutations of integers from 1 to n
elements = list(range(1, n + 1))
signed_permutations = []

# Hər bir permutasiya üçün bütün işarə variantlarını (müsbət/mənfi) tapırıq
# For each permutation, apply all combinations of positive/negative signs
for perm in itertools.permutations(elements):
    for signs in itertools.product([-1, 1], repeat=n):
        signed_perm = [val * sign for val, sign in zip(perm, signs)]
        signed_permutations.append(signed_perm)

total_count = len(signed_permutations)
print(total_count)

# 3. Nəticələri output.txt-yə qeyd edirik
# Write the count and signed permutations to output.txt
with open("output.txt", "w") as output_file:
    output_file.write(str(total_count) + "\n")
    for perm in signed_permutations:
        perm_str = " ".join(map(str, perm))
        print(perm_str)
        output_file.write(perm_str + "\n")
