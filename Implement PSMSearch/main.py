# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba11g.txt")
    if not os.path.exists(input_file):
        return [], "", 0
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
        
    spectra = []
    proteome = ""
    threshold = 0
    for i, line in enumerate(lines):
        # Hərflər olan sətir proteom ardıcıllığıdır
        # The line containing alphabetical characters is the proteome
        if any(c.isalpha() for c in line):
            proteome = line
            threshold = int(lines[i+1])
            break
        else:
            spectra.append(list(map(int, line.split())))
    return spectra, proteome, threshold

# Standart və xəyali amin turşusu kütlələri cədvəli
# Standard and imaginary amino acid masses and symbols mapping
MASS_TABLE = {
    'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 'T': 101, 'C': 103, 'I': 113, 'L': 113,
    'N': 114, 'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131, 'H': 137, 'F': 147,
    'R': 156, 'Y': 163, 'W': 186,
    'X': 4, 'Z': 5
}

# Spektrlərə qarşı proteomda PSM axtarışını həyata keçiririk
# Identify Peptide-Spectrum Matches (PSM) matching spectra against a proteome
def psm_search(spectral_vectors, proteome, threshold):
    n = len(proteome)
    P = [0] * (n + 1)
    for i in range(n):
        P[i+1] = P[i] + MASS_TABLE[proteome[i]]
        
    psm_set = set()
    
    for spectrum in spectral_vectors:
        target_mass = len(spectrum)
        best_peptide = ""
        max_score = -float('inf')
        
        for i in range(n):
            j = i
            while j < n and P[j+1] - P[i] < target_mass:
                j += 1
            if j < n and P[j+1] - P[i] == target_mass:
                score = sum(spectrum[P[r] - P[i] - 1] for r in range(i + 1, j + 2))
                if score > max_score:
                    max_score = score
                    best_peptide = proteome[i:j+1]
                    
        if max_score >= threshold:
            psm_set.add(best_peptide)
            
    return psm_set

def main():
    spectra, proteome, threshold = read_input()
    if not proteome:
        return
    result = psm_search(spectra, proteome, threshold)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        for pep in sorted(list(result)):
            f.write(pep + "\n")

if __name__ == "__main__":
    main()
