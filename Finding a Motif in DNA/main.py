# 1. Giriş faylını oxuyuruq və sətirlərə parçalayırıq
# Read DNA string and substring motif from the input file
with open("rosalind_subs.txt", "r") as file:
    lines = file.read().splitlines()

s = lines[0]
t = lines[1]

positions = []
# 2. s sətri boyu sürüşərək t motifinin mövqelərini tapırıq
# Scan s to locate all occurrences of motif t (1-based index)
for i in range(len(s) - len(t) + 1):
    if s[i:i+len(t)] == t:
        positions.append(i + 1)

result_str = " ".join(map(str, positions))
print(result_str)

# 3. Mövqeləri output.txt faylına yazırıq
# Write result coordinates to output.txt
with open("output.txt", "w") as output_file:
    output_file.write(result_str + "\n")
