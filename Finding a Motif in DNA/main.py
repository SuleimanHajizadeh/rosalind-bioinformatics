# 1. Faylı oxuyuruq və sətirlərə parçalayırıq
with open("rosalind_subs.txt", "r") as file:
    lines = file.read().splitlines()

s = lines[0]  # Əsas DNT ardıcıllığı
t = lines[1]  # Axtarılan motif (alt-ardıcıllıq)

positions = []

# 2. Dövr vasitəsilə sətir boyu hərəkət edirik
# len(s) - len(t) + 1 fərqi axtarışın sətirdən kənara çıxmamasını təmin edir
for i in range(len(s) - len(t) + 1):
    # Əgər cari mövqedən başlayan hissə motifə bərabərdirsə
    if s[i:i+len(t)] == t:
        # İndeksləmə 1-dən başladığı üçün i-nin üzərinə 1 gəlirik
        positions.append(i + 1)

# 3. Mövqeləri aralarında boşluq olacaq şəkildə birləşdirib ekrana çıxarırıq
result = " ".join(map(str, positions))
print(result)

# 4. Cavabı yeni bir fayla yazırıq
with open("rosalind_subs_output.txt", "w") as output_file:
    output_file.write(result)