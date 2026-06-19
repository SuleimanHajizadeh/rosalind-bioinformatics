import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, "rosalind_tran.txt")

sequences = []
curr_seq = ""

# 1. FASTA faylını oxuyuruq
# Parse the FASTA file
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

# 2. Keçid (transition) və transversiya (transversion) saylarını hesablayırıq
# Count transitions and transversions between two sequences of equal length
transitions = 0
transversions = 0

# Purin/Pirimidin keçidlərini müəyyən edən köməkçi çoxluqlar
# Sets of purines and pyrimidines to classify substitutions
purines = {"A", "G"}
pyrimidines = {"C", "T"}

for x, y in zip(s1, s2):
    if x != y:
        # Eyni qrup daxilindəki əvəzlənmələr keçiddir (transition), müxtəlif qruplar arası transversiyadır (transversion)
        # Transition: purine-purine or pyrimidine-pyrimidine. Transversion: purine-pyrimidine.
        if (x in purines and y in purines) or (
            x in pyrimidines and y in pyrimidines
        ):
            transitions += 1
        else:
            transversions += 1

# Nisbəti (ratio) hesablayırıq
# Calculate transitions/transversions ratio
ratio = transitions / transversions
print(f"{ratio:.11f}")

# 3. Nəticəni output.txt faylına yazırıq
# Save the ratio to output.txt
output_path = os.path.join(script_dir, "output.txt")
with open(output_path, "w") as output_file:
    output_file.write(f"{ratio:.11f}\n")
