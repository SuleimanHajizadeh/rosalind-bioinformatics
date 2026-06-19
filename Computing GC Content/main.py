# Ardıcıllığın GC faizini hesablayan funksiya
# Calculate the GC percentage of a DNA sequence
def calculate_gc_content(sequence):
    gc_count = sequence.count('G') + sequence.count('C')
    return (gc_count / len(sequence)) * 100

# 1. Faylı oxuyuruq və FASTA formatını parçalayırıq
# Read the file and parse FASTA records
fasta_dict = {}
current_id = ""

with open("rosalind_gc.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line.startswith(">"):
            current_id = line[1:]
            fasta_dict[current_id] = ""
        else:
            fasta_dict[current_id] += line

# 2. Hər bir ardıcıllığın GC faizini hesablayıb ən böyüyünü tapırıq
# Find the sequence with the highest GC content
max_id = ""
max_gc = -1.0

for seq_id, sequence in fasta_dict.items():
    gc = calculate_gc_content(sequence)
    if gc > max_gc:
        max_gc = gc
        max_id = seq_id

print(max_id)
print(f"{max_gc:.6f}")

# 3. Nəticəni output.txt faylına yazırıq
# Write output to output.txt
with open("output.txt", "w") as output_file:
    output_file.write(f"{max_id}\n{max_gc:.6f}\n")
