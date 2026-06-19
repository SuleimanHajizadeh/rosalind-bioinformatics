# 1. Kodon cədvəlini lüğət olaraq təyin edirik
# Standard RNA codon table translation map
CODON_TABLE = {
    "UUU": "F",
    "UUC": "F",
    "UUA": "L",
    "UUG": "L",
    "UCU": "S",
    "UCC": "S",
    "UCA": "S",
    "UCG": "S",
    "UAU": "Y",
    "UAC": "Y",
    "UAA": "Stop",
    "UAG": "Stop",
    "UGU": "C",
    "UGC": "C",
    "UGA": "Stop",
    "UGG": "W",
    "CUU": "L",
    "CUC": "L",
    "CUA": "L",
    "CUG": "L",
    "CCU": "P",
    "CCC": "P",
    "CCA": "P",
    "CCG": "P",
    "CAU": "H",
    "CAC": "H",
    "CAA": "Q",
    "CAG": "Q",
    "CGU": "R",
    "CGC": "R",
    "CGA": "R",
    "CGG": "R",
    "AUU": "I",
    "AUC": "I",
    "AUA": "I",
    "AUG": "M",
    "ACU": "T",
    "ACC": "T",
    "ACA": "T",
    "ACG": "T",
    "AAU": "N",
    "AAC": "N",
    "AAA": "K",
    "AAG": "K",
    "AGU": "S",
    "AGC": "S",
    "AGA": "R",
    "AGG": "R",
    "GUU": "V",
    "GUC": "V",
    "GUA": "V",
    "GUG": "V",
    "GCU": "A",
    "GCC": "A",
    "GCA": "A",
    "GCG": "A",
    "GAU": "D",
    "GAC": "D",
    "GAA": "E",
    "GAG": "E",
    "GGU": "G",
    "GGC": "G",
    "GGA": "G",
    "GGG": "G",
}

# 2. Faylı oxuyuruq
# Read the RNA sequence from the input file
with open("rosalind_prot.txt", "r") as file:
    rna_seq = file.read().strip()

protein_sequence = []

# 3. Ardıcıllığı 3-3 (kodon-kodon) addımlarla gəzirik və protein zəncirini qururuq
# Step through RNA sequence 3 bases at a time and translate codons
for i in range(0, len(rna_seq), 3):
    codon = rna_seq[i : i + 3]
    if len(codon) == 3:
        amino_acid = CODON_TABLE.get(codon, "Stop")
        if amino_acid == "Stop":
            break
        protein_sequence.append(amino_acid)

result = "".join(protein_sequence)
print(result)

# 4. Nəticəni output.txt faylına yazırıq
# Write the protein sequence to output.txt
with open("output.txt", "w") as output_file:
    output_file.write(result + "\n")
