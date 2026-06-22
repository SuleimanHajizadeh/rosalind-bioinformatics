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


def spectral_dictionary_size(spectrum, threshold, max_score):
    """
    Spektral lüğət ölçüsünü hesabla.
    DP cədvəli [0, max_score] aralığındadır — mənfi xallar göz ardı edilir.
    20 amin turşusu işlədilir (I/L hər ikisi=113, K/Q hər ikisi=128).

    Compute spectral dictionary size.
    DP table is bounded to [0, max_score] — negative scores are discarded.
    Uses all 20 amino acids (I and L both=113, K and Q both=128).
    """
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

    # 2D DP cədvəli: dp[mass][score] = həmin kütlə + xala uyğun peptid sayı
    # 2D DP table: dp[mass][score] = count of peptides with given mass and score
    # Score aralığı: [0, max_score] — cədvəlin hündürlüyü max_score-dur
    dp = [[0] * (max_score + 1) for _ in range(m + 1)]
    dp[0][0] = 1

    for i in range(1, m + 1):
        s_i = spectrum[i - 1]   # i-ci nodun spektral çəkisi
        for mass in aa_masses:
            j = i - mass        # əvvəlki kütlə mövqeyi
            if j < 0:
                continue
            for prev_t in range(max_score + 1):
                if dp[j][prev_t] == 0:
                    continue
                new_t = prev_t + s_i
                # Yalnız [0, max_score] aralığındakı xalları saxla
                # Only keep scores within [0, max_score]
                if 0 <= new_t <= max_score:
                    dp[i][new_t] += dp[j][prev_t]

    # threshold ilə max_score arasındakı xalların cəmi
    # Sum counts for scores in [threshold, max_score]
    return sum(dp[m][threshold:max_score + 1])


def main():
    import os
    spectrum, threshold, max_score = read_input()
    if not spectrum:
        return

    result = spectral_dictionary_size(spectrum, threshold, max_score)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(str(result) + "\n")
    print(result)


if __name__ == "__main__":
    main()
