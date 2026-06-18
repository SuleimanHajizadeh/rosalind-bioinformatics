# rosalind_grph.py

# 1. FASTA formatlı rosalind_grph.txt faylını oxuyuruq
sequences = {}
current_id = ""

with open("rosalind_grph.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line.startswith(">"):
            current_id = line[1:]
            sequences[current_id] = ""
        else:
            sequences[current_id] += line

k = 3
edges = []

# 2. İkiqat dövrlə bütün sətirlərin prefiks və suffiks uyğunluğunu yoxlayırıq
for id1, seq1 in sequences.items():
    suffix = seq1[-k:] # sətirin son k simvolu
    
    for id2, seq2 in sequences.items():
        if id1 == id2:  # Özü-özünə ilgək (loop) olmasının qarşısını alırıq
            continue
            
        prefix = seq2[:k]  # sətirin ilk k simvolu
        
        # Əgər suffiks prefiksə bərabərdirsə, kənarı siyahıya əlavə edirik
        if suffix == prefix:
            edges.append(f"{id1} {id2}")

# 3. Nəticələri ekrana çıxarırıq və yeni fayla yazırıq
output_content = "\n".join(edges)
print(output_content)

with open("rosalind_grph_output.txt", "w") as out_file:
    out_file.write(output_content)