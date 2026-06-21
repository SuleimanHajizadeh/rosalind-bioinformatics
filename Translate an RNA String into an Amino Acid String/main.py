# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba4a.txt")
    if not os.path.exists(input_file):
        return ""
    with open(input_file, "r") as f:
        return f.read().strip()

# Kodon cədvəlini hazırlayırıq
# RNA Codon Table
CODON_TABLE = {
    'AAA':'K', 'AAC':'N', 'AAG':'K', 'AAU':'N', 'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACU':'T',
    'AGA':'R', 'AGC':'S', 'AGG':'R', 'AGU':'S', 'AUA':'I', 'AUC':'I', 'AUG':'M', 'AUU':'I',
    'CAA':'Q', 'CAC':'H', 'CAG':'Q', 'CAU':'H', 'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCU':'P',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGU':'R', 'CUA':'L', 'CUC':'L', 'CUG':'L', 'CUU':'L',
    'GAA':'E', 'GAC':'D', 'GAG':'E', 'GAU':'D', 'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCU':'A',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGU':'G', 'GUA':'V', 'GUC':'V', 'GUG':'V', 'GUU':'V',
    'UAC':'Y', 'UAU':'Y', 'UCA':'S', 'UCC':'S', 'UCG':'S', 'UCU':'S', 'UGC':'C', 'UGG':'W',
    'UGU':'C', 'UUA':'L', 'UUG':'L', 'UUU':'F', 'UAA':'Stop', 'UAG':'Stop', 'UGA':'Stop'
}

# RNT ardıcıllığını amin turşusu ardıcıllığına tərcümə edirik
# Translate an RNA string into an amino acid string
def translate_rna(rna):
    peptide = []
    for i in range(0, len(rna), 3):
        codon = rna[i:i+3]
        if len(codon) < 3:
            break
        aa = CODON_TABLE.get(codon, "")
        if aa == "Stop":
            break
        peptide.append(aa)
    return "".join(peptide)

def main():
    rna = read_input()
    if not rna:
        return
    result = translate_rna(rna)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(result + "\n")

if __name__ == "__main__":
    main()
