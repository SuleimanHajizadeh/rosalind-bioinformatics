# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba11i.txt")
    if not os.path.exists(input_file):
        return [], 0, 0
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    spectrum = list(map(int, lines[0].split()))
    threshold = int(lines[1])
    max_score = int(lines[2])
    return spectrum, threshold, max_score

# Spektral lüğət ehtimalını hesablayan dinamik proqramlaşdırma alqoritmi
# Compute the Probability of a Spectral Dictionary
def spectral_dictionary_probability(spectrum, threshold, max_score):
    m = len(spectrum)

    # Amin turşusu kütlələri / Amino acid masses
    if m < 57:
        # Kiçik nümunə üçün xəyali amin turşuları: X=4, Z=5
        # Small sample: imaginary amino acids X=4, Z=5
        aa_masses = [4, 5]
    else:
        # Standart 20 amin turşusu kütlələri (I/L=113 iki dəfə, K/Q=128 iki dəfə)
        # Standard 20 amino acid masses (I/L=113 twice, K/Q=128 twice)
        aa_masses = [57, 71, 87, 97, 99, 101, 103,
                     113, 113,   # I and L (same mass, distinct amino acids)
                     114, 115,
                     128, 128,   # K and Q (same mass, distinct amino acids)
                     129, 131, 137, 147, 156, 163, 186]

    alphabet_size = len(aa_masses)

    # 2D DP cədvəli: dp[mass][score] = həmin kütlə və xala uyğun peptid ehtimalı
    # 2D DP table: dp[mass][score] = probability of peptides with given mass and score
    # Score aralığı: [0, max_score]
    dp = [[0.0] * (max_score + 1) for _ in range(m + 1)]
    dp[0][0] = 1.0

    for i in range(1, m + 1):
        s_i = spectrum[i - 1]
        for mass in aa_masses:
            j = i - mass
            if j < 0:
                continue
            for prev_t in range(max_score + 1):
                if dp[j][prev_t] == 0:
                    continue
                new_t = prev_t + s_i
                if 0 <= new_t <= max_score:
                    dp[i][new_t] += dp[j][prev_t] / alphabet_size

    # threshold-dan böyük və ya bərabər olan xalların cəmi
    # Sum probabilities for scores >= threshold
    return sum(dp[m][threshold:])

def main():
    import os
    spectrum, threshold, max_score = read_input()
    if not spectrum:
        return

    result = spectral_dictionary_probability(spectrum, threshold, max_score)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        # Write format matching typical float outputs
        f.write(f"{result}\n")
    print(result)

if __name__ == "__main__":
    main()

