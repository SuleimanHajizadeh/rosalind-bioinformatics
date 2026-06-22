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


# === Variant A: 20 amin turşusu, xal aşağı hedd yoxdur (cari yanaşma) ===
# 20 amino acids (I/L both 113, K/Q both 128), no lower score bound
def solve_20aa_unbounded(spectrum, threshold, max_score):
    from collections import defaultdict
    aa_masses = _get_masses(len(spectrum))
    m = len(spectrum)
    dp = [defaultdict(int) for _ in range(m + 1)]
    dp[0][0] = 1
    for i in range(1, m + 1):
        s_i = spectrum[i - 1]
        for mass in aa_masses:
            if i - mass >= 0:
                for prev_score, count in list(dp[i - mass].items()):
                    new_score = prev_score + s_i
                    if new_score <= max_score:
                        dp[i][new_score] += count
    return sum(c for s, c in dp[m].items() if threshold <= s <= max_score)


# === Variant B: 18 unikal kütlə, xal aşağı hedd yoxdur ===
# 18 unique amino acid masses (I=L treated as same, K=Q treated as same)
def solve_18aa_unbounded(spectrum, threshold, max_score):
    from collections import defaultdict
    aa_masses = _get_masses_18(len(spectrum))
    m = len(spectrum)
    dp = [defaultdict(int) for _ in range(m + 1)]
    dp[0][0] = 1
    for i in range(1, m + 1):
        s_i = spectrum[i - 1]
        for mass in aa_masses:
            if i - mass >= 0:
                for prev_score, count in list(dp[i - mass].items()):
                    new_score = prev_score + s_i
                    if new_score <= max_score:
                        dp[i][new_score] += count
    return sum(c for s, c in dp[m].items() if threshold <= s <= max_score)


# === Variant C: 20 amin turşusu, xal [0, max_score] arasinda ===
# 20 amino acids, score bounded to [0, max_score] — "table height" interpretation
def solve_20aa_bounded(spectrum, threshold, max_score):
    aa_masses = _get_masses(len(spectrum))
    m = len(spectrum)
    dp = [[0] * (max_score + 1) for _ in range(m + 1)]
    dp[0][0] = 1
    for i in range(1, m + 1):
        s_i = spectrum[i - 1]
        for mass in aa_masses:
            j = i - mass
            if j < 0:
                continue
            for t in range(max_score + 1):
                if dp[j][t] == 0:
                    continue
                new_t = t + s_i
                if 0 <= new_t <= max_score:
                    dp[i][new_t] += dp[j][t]
    return sum(dp[m][threshold:max_score + 1])


# === Variant D: 18 unikal kütlə, xal [0, max_score] arasinda ===
# 18 unique masses, score bounded to [0, max_score]
def solve_18aa_bounded(spectrum, threshold, max_score):
    aa_masses = _get_masses_18(len(spectrum))
    m = len(spectrum)
    dp = [[0] * (max_score + 1) for _ in range(m + 1)]
    dp[0][0] = 1
    for i in range(1, m + 1):
        s_i = spectrum[i - 1]
        for mass in aa_masses:
            j = i - mass
            if j < 0:
                continue
            for t in range(max_score + 1):
                if dp[j][t] == 0:
                    continue
                new_t = t + s_i
                if 0 <= new_t <= max_score:
                    dp[i][new_t] += dp[j][t]
    return sum(dp[m][threshold:max_score + 1])


def _get_masses(m):
    """20 amin turşusu kütlələri (kiçik m üçün xəyali)"""
    if m < 57:
        return [4, 5]  # imaginary X=4, Z=5
    # Standard 20 (I/L=113 twice, K/Q=128 twice)
    return [57, 71, 87, 97, 99, 101, 103, 113, 113, 114, 115,
            128, 128, 129, 131, 137, 147, 156, 163, 186]


def _get_masses_18(m):
    """18 unikal amin turşusu kütlələri"""
    if m < 57:
        return [4, 5]  # imaginary X=4, Z=5
    # 18 unique masses
    return [57, 71, 87, 97, 99, 101, 103, 113, 114, 115,
            128, 129, 131, 137, 147, 156, 163, 186]


def main():
    import os
    spectrum, threshold, max_score = read_input()
    if not spectrum:
        print("Dataset tapılmadı!")
        return

    print(f"Spectrum uzunluğu: {len(spectrum)}, threshold: {threshold}, max_score: {max_score}")
    print()

    results = {
        "A: 20aa, aşağı hədd yox  (ƏN GÜCLÜ EHTIMAL)": solve_20aa_unbounded(spectrum, threshold, max_score),
        "B: 18aa, aşağı hədd yox ": solve_18aa_unbounded(spectrum, threshold, max_score),
        "C: 20aa, xal [0..max]   ": solve_20aa_bounded(spectrum, threshold, max_score),
        "D: 18aa, xal [0..max]   ": solve_18aa_bounded(spectrum, threshold, max_score),
    }

    for label, val in results.items():
        print(f"  {label}: {val}")

    # Əsas cavabı output.txt-ə yazırıq (Variant A - ən doğru ehtimal)
    best = results["A: 20aa, aşağı hədd yox  (ƏN GÜCLÜ EHTIMAL)"]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(str(best) + "\n")
    print(f"\noutput.txt → {best}")


if __name__ == "__main__":
    main()
