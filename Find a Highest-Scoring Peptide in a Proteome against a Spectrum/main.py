# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba11f.txt")
    if not os.path.exists(input_file):
        return "", []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    spectrum = list(map(int, lines[0].split()))
    proteome = lines[1]
    return proteome, spectrum

MASS_TABLE = {
    'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 101, 'C': 103, 'I': 113, 'L': 113,
    'N': 114, 'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131, 'H': 137, 'F': 147,
    'R': 156, 'Y': 163, 'W': 186
}

# Peptidin spektrə görə xalını hesablayırıq
# Score a peptide against a spectrum vector
def score_peptide(peptide, spectrum_vector):
    # Prefiks kütlələrini tapırıq
    # Find prefix masses
    prefix = 0
    score = 0
    for aa in peptide:
        prefix += MASS_TABLE[aa]
        if 0 < prefix <= len(spectrum_vector):
            score += spectrum_vector[prefix - 1]
    return score

# Proteomda ən yüksək xal toplayan peptidi tapırıq
# Find a Highest-Scoring Peptide in a Proteome against a Spectrum
def find_highest_scoring_peptide(proteome, spectrum):
    # Spektrin ümumi kütləsini müəyyən edirik
    # Determine the target mass of the spectrum
    target_mass = len(spectrum)
    
    best_peptide = ""
    max_score = -float('inf')
    
    # Proteomda target_mass kütləsinə malik bütün alt zəncirləri (peptidləri) sürüşən pəncərə ilə yoxlayırıq
    # Check all substrings of the proteome using a sliding window
    # Sürətli olması üçün hər mövqedən kütlə cəmi target_mass olana qədər uzadırıq
    # Expand window at each position until mass matches or exceeds target_mass
    n = len(proteome)
    for i in range(n):
        curr_mass = 0
        j = i
        while j < n and curr_mass < target_mass:
            curr_mass += MASS_TABLE[proteome[j]]
            j += 1
        if curr_mass == target_mass:
            pep = proteome[i:j]
            score = score_peptide(pep, spectrum)
            if score > max_score:
                max_score = score
                best_peptide = pep
                
    return best_peptide

def main():
    proteome, spectrum = read_input()
    if not proteome:
        return
    result = find_highest_scoring_peptide(proteome, spectrum)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(result + "\n")

if __name__ == "__main__":
    main()
