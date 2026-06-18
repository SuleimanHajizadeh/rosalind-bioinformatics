# rosalind_orf.py

# 1. DNT Codon Cədvəlini təyin edirik
CODON_TABLE = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
    'TAT': 'Y', 'TAC': 'Y', 'TAA': 'Stop', 'TAG': 'Stop',
    'TGT': 'C', 'TGC': 'C', 'TGA': 'Stop', 'TGG': 'W',
    'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'ATT': 'I', 'AUC': 'I', 'ATA': 'I', 'ATG': 'M',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'
}

def get_reverse_complement(dna_string):
    """DNT sətirinin tərs komplementini tapan funksiya"""
    mapping = str.maketrans("ATCG", "TAGC")
    return dna_string[::-1].translate(mapping)

def find_proteins_from_dna(dna_string, proteins_set):
    """Verilmiş sətirdəki bütün növ ORF-ləri tapıb çoxluğa əlavə edən funksiya"""
    n = len(dna_string)
    
    # Sətir boyu hər bir mümkün Start (ATG) mövqeyini yoxlayırıq
    for i in range(n - 2):
        if dna_string[i:i+3] == "ATG":
            protein = []
            is_valid_orf = False
            
            # Start tapıldıqdan sonra 3-3 (kodon-kodon) addımlayırıq
            for j in range(i, n - 2, 3):
                codon = dna_string[j:j+3]
                amino_acid = CODON_TABLE.get(codon, 'Stop')
                
                if amino_acid == 'Stop':
                    # Əgər rəsmi STOP kodondursa, ORF tamamlanmış sayılır
                    if codon in ['TAA', 'TAG', 'TGA']:
                        is_valid_orf = True
                    break
                protein.append(amino_acid)
                
            if is_valid_orf:
                proteins_set.add("".join(protein))

# 2. FASTA faylından DNT sətirini oxuyuruq
sequences = []
current_seq = ""
with open("rosalind_orf.txt", "r") as file:
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

dna = sequences[0]
distinct_proteins = set()

# 3. Həm düz, həm tərs komplement üzərində axtarış aparırıq
find_proteins_from_dna(dna, distinct_proteins)
find_proteins_from_dna(get_reverse_complement(dna), distinct_proteins)

# 4. Nəticələri ekrana çıxarırıq və fayla yazırıq
with open("rosalind_orf_output.txt", "w") as output_file:
    for p in distinct_proteins:
        print(p)
        output_file.write(p + "\n")