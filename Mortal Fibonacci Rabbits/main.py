# 1. Faylı oxuyuruq
# Read n (months) and m (lifespan) from the input dataset
with open("rosalind_fibd.txt", "r") as file:
    n, m = map(int, file.read().split())

# 2. Fani (mortal) dovşanların sayını hesablayırıq
# Calculate population of rabbits with a finite lifespan of m months
# Hər yaş qrupundakı dovşanları saxlayan siyahı (m-ölçülü)
# Array to keep track of rabbit populations of each age (up to m months old)
ages = [0] * m
ages[0] = 1  # 1-ci ayda 1 yeni doğulmuş dovşan cütü var

# Hər ay üçün populyasiyanı yeniləyirik
# Update population age groups month by month
for month in range(1, n):
    # Yeni doğulanların sayı: 1 aydan böyük olan bütün dovşanların cəmi (indeks 1 və daha böyük)
    # New offspring are born to all rabbits of age >= 1 month
    new_borns = sum(ages[1:])
    
    # Dovşanları 1 ay yaşlandırırıq (sürüşdürürük)
    # Age all rabbits by 1 month
    for i in range(m - 1, 0, -1):
        ages[i] = ages[i-1]
        
    ages[0] = new_borns

# Ümumi dovşan cütlərinin sayını hesablayırıq
# Total rabbit pairs is sum of all age groups
total_rabbits = sum(ages)
print(total_rabbits)

# 3. Cavabı yeni fayla qeyd edirik
# Write result to output.txt
with open("output.txt", "w") as output_file:
    output_file.write(str(total_rabbits) + "\n")
