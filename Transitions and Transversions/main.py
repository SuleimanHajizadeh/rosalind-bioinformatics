# rosalind_tran.py
import os

# 1. Faylın yerləşdiyi qovluğu tapırıq və FASTA faylını oxuyuruq
script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "rosalind_tran.txt")

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

s1 = sequences[0]
s2 = sequences[1]

# 2. Keçid (transition) və Transversiya (transversion) saylarını hesablayırıq
transitions = 0
transversions = 0

# Keçid cütlüklərini müəyyən edirik: purinlər (A <-> G) və ya pirimidinlər (C <-> T)
transition_pairs = {
    ('A', 'G'), ('G', 'A'),
    ('C', 'T'), ('T', 'C')
}

for c1, c2 in zip(s1, s2):
    if c1 != c2:
        if (c1, c2) in transition_pairs:
            transitions += 1
        else:
            transversions += 1

# 3. Nisbəti tapırıq və nəticəni həm ekrana çıxarırıq, həm də output.txt faylına yazırıq
ratio = transitions / transversions
print(f"Keçid/Transversiya nisbəti: {ratio}")

output_path = os.path.join(script_dir, "output.txt")
with open(output_path, "w") as out_file:
    out_file.write(str(ratio) + "\n")
