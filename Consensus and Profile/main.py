import os

script_dir = os.path.dirname(os.path.abspath(__file__))

sequences = []
current_seq = ""

# 1. FASTA formatlı faylı oxuyuruq
# Read DNA sequences from FASTA format file
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

n = len(sequences)
l = len(sequences[0])

# Profil matrisini (profile matrix) qururuq
# Initialize and populate the profile matrix for A, C, G, T
profile = {
    'A': [0] * l,
    'C': [0] * l,
    'G': [0] * l,
    'T': [0] * l
}

for i in range(l):
    for seq in sequences:
        profile[seq[i]][i] += 1

# 3. Konsensus ardıcıllığı (consensus sequence) müəyyən edirik
# Reconstruct consensus sequence by taking max frequency nucleotide at each position
consensus = []
for i in range(l):
    max_count = -1
    max_char = ''
    for char in ['A', 'C', 'G', 'T']:
        if profile[char][i] > max_count:
            max_count = profile[char][i]
            max_char = char
    consensus.append(max_char)

consensus_str = "".join(consensus)
print(consensus_str)

# 4. Profil matrisini yazdırırıq və fayla qeyd edirik
# Write consensus sequence and profile matrix to output.txt
output_path = os.path.join(script_dir, "output.txt")
with open(output_path, "w") as output_file:
    output_file.write(consensus_str + "\n")
    for char in ['A', 'C', 'G', 'T']:
        counts_str = " ".join(map(str, profile[char]))
        row = f"{char}: {counts_str}"
        print(row)
        output_file.write(row + "\n")
