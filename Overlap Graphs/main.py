import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "rosalind_grph.txt")

sequences = {}
current_id = ""

# 1. FASTA formatlı rosalind_grph.txt faylını oxuyuruq
# Parse FASTA records and store them in a dictionary
with open(input_path, "r") as file:
    for line in file:
        line = line.strip()
        if line.startswith(">"):
            current_id = line[1:]
            sequences[current_id] = ""
        else:
            sequences[current_id] += line

k = 3
edges = []

# 2. Hər bir cütü yoxlayaraq O_3 overlap qrafını qururuq
# Compare suffix of one sequence with prefix of another to build O_3 overlap graph
for id1, seq1 in sequences.items():
    suffix = seq1[-k:]  # sətirin son k simvolu
    
    for id2, seq2 in sequences.items():
        if id1 == id2:  # Özü-özünə ilgək (loop) olmasının qarşısını alırıq
            continue
            
        prefix = seq2[:k]  # sətirin ilk k simvolu
        
        # Əgər suffiks prefiksə bərabərdirsə, tili siyahıya əlavə edirik
        # If suffix of seq1 equals prefix of seq2, record edge (id1, id2)
        if suffix == prefix:
            edges.append((id1, id2))

# 3. Cavabları yazdırırıq və output.txt faylına qeyd edirik
# Write edges list to output.txt
output_path = os.path.join(script_dir, "output.txt")
with open(output_path, "w") as output_file:
    for u, v in edges:
        edge_str = f"{u} {v}"
        print(edge_str)
        output_file.write(edge_str + "\n")
