# rosalind_cons.py
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

sequences = []
current_seq = ""

# 1. FASTA formatlı rosalind_cons.txt faylını oxuyuruq
input_path = os.path.join(script_dir, "rosalind_cons.txt")
with open(input_path, "r") as file:
    for line in file:
        line = line.strip()
        if line.startswith(">"):
            if current_seq:
                sequences.append(current_seq)
                current_seq = ""
        else:
            current_seq += line
    if current_seq:
        sequences.append(current_seq)

n = len(sequences[0])
bases = ['A', 'C', 'G', 'T']
profile = {base: [0] * n for base in bases}

# 2. Profil matrisini dəqiqliklə qururuq
for seq in sequences:
    for i, base in enumerate(seq):
        profile[base][i] += 1

# 3. Konsensus ardıcıllığını tapırıq
consensus = []
for i in range(n):
    max_base = ""
    max_count = -1
    for base in bases:
        if profile[base][i] > max_count:
            max_count = profile[base][i]
            max_base = base
    consensus.append(max_base)

consensus_str = "".join(consensus)

# 4. Rosalind-in qəbul etdiyi təmiz formatda birbaşa fayla qeyd edirik
output_path = os.path.join(script_dir, "rosalind_cons_output.txt")
with open(output_path, "w") as out_file:
    out_file.write(consensus_str + "\n")
    for base in bases:
        counts_str = " ".join(map(str, profile[base]))
        out_file.write(f"{base}: {counts_str}\n")

print(f"Uğurlu! Tam və təmiz nəticə '{output_path}' faylına yazıldı.")