import itertools

# 1. Giriş faylından n rəqəmini oxuyuruq
# Read integer n from the input dataset file
with open("rosalind_perm.txt", "r") as file:
    n = int(file.read().strip())

# 2. itertools vasitəsilə 1-dən n-ə qədər olan rəqəmlərin permutasiyalarını tapırıq
# Generate all permutations of integers from 1 to n
permutations_list = list(itertools.permutations(range(1, n + 1)))

# Permutasiyaların ümumi sayını tapırıq
# Total permutations count
total_permutations = len(permutations_list)
print(total_permutations)

# 3. Nəticələri output.txt faylına yazırıq
# Write the total count and permutations list to output.txt
with open("output.txt", "w") as output_file:
    output_file.write(str(total_permutations) + "\n")
    for perm in permutations_list:
        perm_str = " ".join(map(str, perm))
        print(perm_str)
        output_file.write(perm_str + "\n")
