# 1. Faylı oxuyuruq və sətirlərə parçalayırıq
with open("rosalind_hamm.txt", "r") as file:
    lines = file.read().splitlines()

# Sətirlərin boş olub-olmadığını yoxlayırıq və s və t dəyişənlərinə mənimsədirik
s = lines[0]
t = lines[1]

# 2. zip() funksiyası ilə hər iki ardıcıllığı eyni anda gəzirik
# Fərqli olan hər bir mövqe üçün 1 qaytarırıq və sum() ilə toplayırıq
hamming_distance = sum(1 for char_s, char_t in zip(s, t) if char_s != char_t)

# 3. Nəticəni ekrana çıxarırıq
print(hamming_distance)

# 4. Cavabı yeni bir fayla yazırıq
with open("rosalind_hamm_output.txt", "w") as output_file:
    output_file.write(str(hamming_distance))