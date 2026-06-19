import os

# Blosum62 xal matrisinə əsasən sabit boşluq cəriməsi ilə qlobal düzülüşü tapırıq
# Compute global alignment score with constant gap penalty using BLOSUM62


def load_blosum62():
    alphabet = "A R N D C Q E G H I L K M F P S T W Y V".split()
    matrix_raw = [
        [4, -1, -2, -2, 0, -1, -1, 0, -2, -1, -1, -1, -1, -2, -1, 1, 0, -3, -2, 0],
        [-1, 5, 0, -2, -3, 1, 0, -2, 0, -3, -2, 2, -1, -3, -2, -1, -1, -3, -2, -3],
        [-2, 0, 6, 1, -3, 0, 0, 0, 1, -3, -3, 0, -2, -3, -2, 1, 0, -4, -2, -3],
        [-2, -2, 1, 6, -3, 0, 2, -1, -1, -3, -4, -1, -3, -3, -1, 0, -1, -4, -3, -3],
        [0, -3, -3, -3, 9, -3, -4, -3, -3, -1, -1, -3, -1, -2, -3, -1, -1, -2, -2, -1],
        [-1, 1, 0, 0, -3, 5, 2, -2, 0, -3, -2, 1, 0, -3, -1, 0, -1, -2, -1, -2],
        [-1, 0, 0, 2, -4, 2, 5, -2, 0, -3, -3, 1, -2, -3, -1, 0, -1, -3, -2, -2],
        [0, -2, 0, -1, -3, -2, -2, 6, -2, -4, -4, -2, -3, -3, -2, 0, -2, -2, -3, -3],
        [-2, 0, 1, -1, -3, 0, 0, -2, 8, -3, -3, -1, -2, -1, -2, -1, -2, -2, 2, -3],
        [-1, -3, -3, -3, -1, -3, -3, -3, -3, 4, 2, -3, 1, 0, -3, -2, -1, -3, -1, 3],
        [-1, -2, -3, -4, -1, -2, -3, -4, -3, 2, 4, -2, 2, 0, -3, -2, -1, -2, -1, 1],
        [-1, 2, 0, -1, -3, 1, 1, -2, -1, -3, -2, 5, -1, -3, -1, 0, -1, -3, -2, -2],
        [-1, -1, -2, -3, -1, 0, -2, -3, -2, 1, 2, -1, 5, 0, -2, -1, -1, -1, -1, 1],
        [-2, -3, -3, -3, -2, -3, -3, -3, -1, 0, 0, -3, 0, 6, -4, -2, -2, 1, 3, -1],
        [-1, -2, -2, -1, -3, -1, -1, -2, -2, -2, -3, -1, -2, -4, 7, -1, -1, -4, -3, -2],
        [1, -1, 1, 0, -1, 0, 0, 0, -1, -2, -2, 0, -1, -2, -1, 4, 1, -3, -2, -2],
        [0, -1, 0, -1, -2, -1, -1, -2, -2, -1, -2, -1, -1, -3, -1, 1, 5, -2, -2, 0],
        [-3, -3, -4, -4, -2, -2, -3, -2, -2, -5, -2, -3, -4, 1, -4, -3, -2, 11, 2, -3],
        [-2, -2, -2, -3, -2, -1, -2, -3, 2, -1, -1, -2, -1, 3, -3, -2, -2, 2, 7, -1],
        [0, -3, -3, -3, -1, -2, -2, -1, -2, 3, 1, -2, 1, -1, -2, -2, 0, -3, -2, 4],
    ]
    scores = {}
    for r_idx, r in enumerate(alphabet):
        for c_idx, c in enumerate(alphabet):
            scores[(r, c)] = matrix_raw[r_idx][c_idx]
    return scores


def parse_fasta(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    seqs = []
    curr = []
    for line in lines:
        if line.startswith(">"):
            if curr:
                seqs.append("".join(curr))
                curr = []
        else:
            curr.append(line)
    if curr:
        seqs.append("".join(curr))
    return seqs


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_gcon.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    seqs = parse_fasta(input_path)
    s, t = seqs[0], seqs[1]

    M, N = len(s), len(t)
    blosum = load_blosum62()
    # Constant gap penalty of -5
    GAP = -5

    # DP matrisini qururuq
    # DP table initialization
    dp = [[0] * (N + 1) for _ in range(M + 1)]

    # Sətirlərin kənarını doldururuq
    # Fill borders
    for i in range(1, M + 1):
        dp[i][0] = GAP
    for j in range(1, N + 1):
        dp[0][j] = GAP

    # Dinamik proqramlaşdırma
    # Run DP logic
    for i in range(1, M + 1):
        for j in range(1, N + 1):
            cost = blosum[(s[i - 1], t[j - 1])]
            # Qonşu xallara əsasən optimalını tapırıq
            # Score can be diagonal match, or from gap options (constant penalty)
            val = dp[i - 1][j - 1] + cost
            for k in range(i):
                val = max(val, dp[k][j] + GAP)
            for k in range(j):
                val = max(val, dp[i][k] + GAP)
            dp[i][j] = val

    ans = dp[M][N]
    print(f"Global Alignment Score (Constant gap): {ans}")

    with open(output_path, "w") as f:
        f.write(str(ans) + "\n")


if __name__ == "__main__":
    main()
