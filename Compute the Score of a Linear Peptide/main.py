# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba4k.txt")
    if not os.path.exists(input_file):
        return "", []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    peptide = lines[0]
    spectrum = list(map(int, lines[1].split()))
    return peptide, spectrum

MASS_TABLE = {
    'A': 71, 'C': 103, 'D': 115, 'E': 129, 'F': 147, 'G': 57, 'H': 137, 'I': 113,
    'K': 128, 'L': 113, 'M': 131, 'N': 114, 'P': 97, 'Q': 128, 'R': 156, 'S': 87,
    'T': 101, 'V': 99, 'W': 186, 'Y': 163
}

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

# Xətti peptidin verilmiş spektrə qarşı olan xalını tapırıq
# Compute the score of a linear peptide against a spectrum
def score_linear_peptide(peptide, spectrum):
    theoretical = linear_spectrum(peptide)
    
    t_counts = {}
    for val in theoretical:
        t_counts[val] = t_counts.get(val, 0) + 1
        
    s_counts = {}
    for val in spectrum:
        s_counts[val] = s_counts.get(val, 0) + 1
        
    score = 0
    for val in t_counts:
        if val in s_counts:
            score += min(t_counts[val], s_counts[val])
    return score

def main():
    peptide, spectrum = read_input()
    if not peptide:
        return
    result = score_linear_peptide(peptide, spectrum)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(str(result) + "\n")

if __name__ == "__main__":
    main()
