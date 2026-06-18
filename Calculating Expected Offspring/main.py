# rosalind_iev.py

# 1. Fayldan 6 genotip cütlüyünün sayını oxuyuruq
with open("rosalind_iev.txt", "r") as file:
    counts = list(map(int, file.read().split()))

# 2. Cütlüklər üzrə dominant uşaq sayının çəkiləri (weights)
# Hər cütlüyün 2 uşağı olduğu üçün ehtimalları 2-yə vururuq: [2*1, 2*1, 2*1, 2*0.75, 2*0.5, 2*0]
weights = [2, 2, 2, 1.5, 1, 0]

# 3. Hər bir cütlük sayını öz çəkisinə vurub toplayırıq (Expected Value)
expected_offspring = sum(c * w for c, w in zip(counts, weights))

# 4. Nəticəni ekrana çıxarırıq və yeni fayla yazırıq
print(expected_offspring)

with open("rosalind_iev_output.txt", "w") as output_file:
    output_file.write(str(expected_offspring))