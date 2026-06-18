import os

# Monoisotopik kütlə cədvəli
AMINO_ACID_MASSES = {
    'A': 71.03711,
    'C': 103.00919,
    'D': 115.02694,
    'E': 129.04259,
    'F': 147.06841,
    'G': 57.02146,
    'H': 137.05891,
    'I': 113.08406,
    'K': 128.09496,
    'L': 113.08406,
    'M': 131.04049,
    'N': 114.04293,
    'P': 97.05276,
    'Q': 128.05858,
    'R': 156.10111,
    'S': 87.03203,
    'T': 101.04768,
    'V': 99.06841,
    'W': 186.07931,
    'Y': 163.06333
}

def find_amino_acid(mass, tolerance=0.01):
    for aa, aa_mass in AMINO_ACID_MASSES.items():
        if abs(mass - aa_mass) <= tolerance:
            return aa
    return '?'

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_spec.txt")
    
    with open(input_path, "r") as f:
        masses = [float(line.strip()) for line in f if line.strip()]
        
    protein = []
    for i in range(1, len(masses)):
        diff = masses[i] - masses[i-1]
        aa = find_amino_acid(diff)
        protein.append(aa)
        
    result = "".join(protein)
    print(f"Tapılan protein ({len(result)} aa): {result}")
    
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        out_file.write(result + "\n")

if __name__ == "__main__":
    main()
