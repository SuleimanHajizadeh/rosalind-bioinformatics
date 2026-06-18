# 1. Faylı oxuyuruq
with open("rosalind_revc.txt", "r") as file:
    dna = file.read().strip()

# 2. Komplementar hərfləri əvəzləmək üçün lüğət (dictionary) yaradırıq
# Python-da bunun üçün str.maketrans() metodu çox sürətlidir
mapping = str.maketrans("ATCG", "TAGC")

# 3. Əvvəlcə ardıcıllığı tərsinə çeviririk [::-1], sonra komplementlərini tapırıq
reverse_complement = dna[::-1].translate(mapping)

# 4. Cavabı ekrana yazdırırıq və yeni fayla qeyd edirik
print(reverse_complement)

with open("rosalind_revc_output.txt", "w") as output_file:
    output_file.write(reverse_complement)