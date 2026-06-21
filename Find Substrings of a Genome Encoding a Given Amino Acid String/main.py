# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba4b.txt")
    if not os.path.exists(input_file):
        return "", ""
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0], lines[1]

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

def translate_rna(rna):
    peptide = []
    for i in range(0, len(rna), 3):
        codon = rna[i:i+3]
        if len(codon) < 3:
            break
        aa = CODON_TABLE.get(codon, "")
        if aa == "Stop":
            peptide.append("*")
        else:
            peptide.append(aa)
    return "".join(peptide)

# DNT-ni RNT-yə çeviririk
# Transcribe DNA to RNA
def dna_to_rna(dna):
    return dna.replace('T', 'U')

# RNT-ni DNT-yə çeviririk
# Transcribe RNA to DNA
def rna_to_dna(rna):
    return rna.replace('U', 'T')

# Tərs komplement tapırıq
# Reverse complement
def reverse_complement(dna):
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return "".join(complement[base] for base in reversed(dna))

# Verilmiş peptidi kodlaşdıran DNT alt zəncirlərini tapırıq
# Find substrings of a genome encoding a given amino acid string
def find_encoding_substrings(dna, peptide):
    k = len(peptide) * 3
    results = []
    for i in range(len(dna) - k + 1):
        sub = dna[i:i+k]
        
        # İrəli oxunuş (Forward strand)
        rna_f = dna_to_rna(sub)
        pep_f = translate_rna(rna_f)
        if pep_f == peptide:
            results.append(sub)
            continue
            
        # Geri oxunuş (Reverse strand)
        rc_sub = reverse_complement(sub)
        rna_r = dna_to_rna(rc_sub)
        pep_r = translate_rna(rna_r)
        if pep_r == peptide:
            results.append(sub)
            
    return results

def main():
    dna, peptide = read_input()
    if not dna:
        return
    result = find_encoding_substrings(dna, peptide)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(result) + "\n")

if __name__ == "__main__":
    main()
