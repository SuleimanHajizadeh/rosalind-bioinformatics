def calculate_gc_content(sequence):
    """Ardıcıllığın GC faizini hesablayan funksiya"""
    gc_count = sequence.count('G') + sequence.count('C')
    return (gc_count / len(sequence)) * 100

# 1. Faylı oxuyuruq və FASTA formatını parçalayırıq
fasta_dict = {}
current_id = ""

with open("rosalind_gc.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line.startswith(">"):
            # '>' işarəsini silib ID-ni açar (key) kimi saxlayırıq
            current_id = line[1:]
            fasta_dict[current_id] = ""
        else:
            # Eyni ID-yə aid olan alt-alt sətirləri birləşdiririk
            fasta_dict[current_id] += line

# 2. Ən yüksək GC faizini tapırıq
max_id = ""
max_gc = 0.0

for seq_id, sequence in fasta_dict.items():
    gc_content = calculate_gc_content(sequence)
    if gc_content > max_gc:
        max_gc = gc_content
        max_id = seq_id

# 3. Nəticəni ekrana çıxarırıq
print(max_id)
print(f"{max_gc:.6f}")

# 4. Cavabı yeni fayla yazırıq
with open("rosalind_gc_output.txt", "w") as output_file:
    output_file.write(f"{max_id}\n{max_gc:.6f}")