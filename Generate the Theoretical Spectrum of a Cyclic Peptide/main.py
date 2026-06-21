# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba4c.txt")
    if not os.path.exists(input_file):
        return ""
    with open(input_file, "r") as f:
        return f.read().strip()

# Monoizotopik kütlə cədvəli
# Monoisotopic mass table for amino acids
MASS_TABLE = {
    'A': 71, 'C': 103, 'D': 115, 'E': 129, 'F': 147, 'G': 57, 'H': 137, 'I': 113,
    'K': 128, 'L': 113, 'M': 131, 'N': 114, 'P': 97, 'Q': 128, 'R': 156, 'S': 87,
    'T': 101, 'V': 99, 'W': 186, 'Y': 163
}

# Tsiklik (dairəvi) peptidin nəzəri spektrini qururuq
# Generate the theoretical spectrum of a cyclic peptide
def cyclic_spectrum(peptide):
    # Kütlələrin siyahısını hazırlayırıq
    # Get mass list
    masses = [MASS_TABLE[aa] for aa in peptide]
    n = len(peptide)
    
    # Kütlələrin prefiks cəmlərini tapırıq
    # Prefix sums
    prefix_mass = [0] * (n + 1)
    for i in range(n):
        prefix_mass[i+1] = prefix_mass[i] + masses[i]
        
    total_mass = prefix_mass[n]
    spectrum = [0, total_mass]
    
    # Subpeptidlərin kütlələrini hesablayırıq
    # Subpeptides masses
    for length in range(1, n):
        for start in range(n):
            if start + length <= n:
                spectrum.append(prefix_mass[start+length] - prefix_mass[start])
            else:
                spectrum.append(total_mass - (prefix_mass[start] - prefix_mass[start + length - n]))
                
    spectrum.sort()
    return spectrum

def main():
    peptide = read_input()
    if not peptide:
        return
    result = cyclic_spectrum(peptide)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(map(str, result)) + "\n")

if __name__ == "__main__":
    main()
