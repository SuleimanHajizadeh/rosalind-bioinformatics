# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba4j.txt")
    if not os.path.exists(input_file):
        return ""
    with open(input_file, "r") as f:
        return f.read().strip()

MASS_TABLE = {
    'A': 71, 'C': 103, 'D': 115, 'E': 129, 'F': 147, 'G': 57, 'H': 137, 'I': 113,
    'K': 128, 'L': 113, 'M': 131, 'N': 114, 'P': 97, 'Q': 128, 'R': 156, 'S': 87,
    'T': 101, 'V': 99, 'W': 186, 'Y': 163
}

# Xətti peptidin nəzəri spektrini tapırıq
# Generate the theoretical spectrum of a linear peptide
def linear_spectrum(peptide):
    masses = [MASS_TABLE[aa] for aa in peptide]
    n = len(peptide)
    prefix_mass = [0] * (n + 1)
    for i in range(n):
        prefix_mass[i+1] = prefix_mass[i] + masses[i]
        
    spectrum = [0]
    for length in range(1, n + 1):
        for start in range(n - length + 1):
            spectrum.append(prefix_mass[start+length] - prefix_mass[start])
            
    spectrum.sort()
    return spectrum

def main():
    peptide = read_input()
    if not peptide:
        return
    result = linear_spectrum(peptide)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(map(str, result)) + "\n")

if __name__ == "__main__":
    main()
