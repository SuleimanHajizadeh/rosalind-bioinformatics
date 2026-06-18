# rosalind_sseq.py
import os

# 1. Faylın yerləşdiyi qovluğu tapırıq və FASTA faylını oxuyuruq
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "rosalind_sseq.txt")

sequences = []
curr_seq = ""

with open(input_path, "r") as file:
    for line in file:
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if curr_seq:
                sequences.append(curr_seq)
                curr_seq = ""
        else:
            curr_seq += line
    if curr_seq:
        sequences.append(curr_seq)

# s və t ardıcıllıqlarını təyin edirik
s = sequences[0]
t = sequences[1]

# 2. t ardıcıllığının s-də alt-ardıcıllıq (subsequence) olaraq yerləşdiyi mövqeləri tapırıq
# Həris (greedy) yanaşma ilə hər bir nukleotidin ən tez rast gəlinən mövqeyini qeyd edirik
indices = []
s_idx = 0

for char in t:
    # Cari nukleotidi s-də axtarırıq (əvvəlki tapılan mövqedən sonrakı hissədə)
    while s_idx < len(s):
        if s[s_idx] == char:
            # Mövqelər 1-əsaslı (1-indexed) olduğu üçün +1 əlavə edirik
            indices.append(s_idx + 1)
            s_idx += 1
            break
        s_idx += 1

# 3. Nəticələri aralarında boşluqla birləşdirib ekrana çıxarırıq və output.txt faylına yazırıq
result_str = " ".join(map(str, indices))
print(result_str)

output_path = os.path.join(script_dir, "output.txt")
with open(output_path, "w") as out_file:
    out_file.write(result_str + "\n")
