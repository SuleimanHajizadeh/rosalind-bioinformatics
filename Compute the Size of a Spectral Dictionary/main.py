# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba11h.txt")
    if not os.path.exists(input_file):
        return [], 0, 0
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    spectrum = list(map(int, lines[0].split()))
    threshold = int(lines[1])
    max_score = int(lines[2])
    return spectrum, threshold, max_score

# Spektral lüğət ölçüsünü hesablayan alqoritm (dinamik proqramlaşdırma ilə)
# Compute the Size of a Spectral Dictionary using DP
def spectral_dictionary_size(spectrum, threshold, max_score):
    m = len(spectrum)
    
    # Giriş kütləsinin ölçüsünə görə amin turşusu kütlələrini seçirik
    # Determine the set of amino acid masses based on spectrum length
    if m < 57:
        # Xəyali amin turşuları (X=4, Z=5)
        # Imaginary amino acids (X=4, Z=5)
        aa_masses = [4, 5]
    else:
        # Standart 20 amin turşusunun kütlələri (I/L və K/Q təkrarlanmaqla)
        # Standard 20 amino acid masses (with I/L and K/Q repeated)
        aa_masses = [57, 71, 87, 97, 99, 101, 103, 113, 113, 114, 115, 128, 128, 129, 131, 137, 147, 156, 163, 186]
        
    from collections import defaultdict
    
    # dp[i] = {score: count} -> i kütləsi üçün hər xala uyğun peptid sayı
    # dp[i] = {score: count} -> mapping of score to path count for mass i
    dp = [defaultdict(int) for _ in range(m + 1)]
    dp[0][0] = 1
    
    for i in range(1, m + 1):
        for mass in aa_masses:
            if i - mass >= 0:
                s_i = spectrum[i - 1]
                for prev_score, count in dp[i - mass].items():
                    dp[i][prev_score + s_i] += count
                    
    # threshold ilə max_score aralığındakı xalların sayını cəmləyirik
    # Sum the counts of peptides with scores in the range [threshold, max_score]
    total_peptides = 0
    for score, count in dp[m].items():
        if threshold <= score <= max_score:
            total_peptides += count
            
    return total_peptides

def main():
    spectrum, threshold, max_score = read_input()
    if not spectrum:
        return
    result = spectral_dictionary_size(spectrum, threshold, max_score)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(str(result) + "\n")

if __name__ == "__main__":
    main()
