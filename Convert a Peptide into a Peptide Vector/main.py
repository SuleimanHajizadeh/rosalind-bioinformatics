# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba11c.txt")
    if not os.path.exists(input_file):
        return ""
    with open(input_file, "r") as f:
        return f.read().strip()

# Monoisotopik kütlələr (xəyali X və Z daxil olmaqla)
# Monoisotopic masses mapping (including imaginary X and Z)
MASS_TABLE = {
    'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 'T': 101, 'C': 103, 'I': 113, 'L': 113,
    'N': 114, 'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131, 'H': 137, 'F': 147,
    'R': 156, 'Y': 163, 'W': 186,
    'X': 4, 'Z': 5
}

# Peptidi peptid vektoruna çeviririk
# Convert a Peptide into a Peptide Vector
def peptide_to_vector(peptide):
    # Prefiks kütlələrini hesablayırıq
    # Compute prefix masses
    prefix_masses = []
    curr = 0
    for aa in peptide:
        curr += MASS_TABLE[aa]
        prefix_masses.append(curr)
        
    total_mass = prefix_masses[-1]
    # Kütlə sayı qədər vektor təyin edirik
    # Initialize binary vector representation
    vector = [0] * total_mass
    for m in prefix_masses:
        vector[m - 1] = 1
    return vector

def main():
    peptide = read_input()
    if not peptide:
        return
    result = peptide_to_vector(peptide)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(map(str, result)) + "\n")

if __name__ == "__main__":
    main()
