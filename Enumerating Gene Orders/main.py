# rosalind_perm.py
import itertools

# 1. Giriş faylından n ədədini oxuyuruq
with open("rosalind_perm.txt", "r") as file:
    n = int(file.read().strip())

# 2. itertools vasitəsilə 1-dən n-ə qədər olan rəqəmlərin permutasiyalarını tapırıq
permutations_list = list(itertools.permutations(range(1, n + 1)))

# 3. Çıxış formatını hazırlayırıq (Rosalind permutasiyaların hər hansı bir ardıcıllıqla düzülməsini qəbul edir)
output_lines = []
output_lines.append(str(len(permutations_list))) # Əvvəlcə ümumi say

for p in permutations_list:
    output_lines.append(" ".join(map(str, p))) # rəqəmləri aralarında boşluqla birləşdiririk

full_output = "\n".join(output_lines)

# 4. Nəticəni həm ekrana çıxarırıq, həm də çıxış faylına yazırıq
print(full_output)

with open("rosalind_perm_output.txt", "w") as output_file:
    output_file.write(full_output)