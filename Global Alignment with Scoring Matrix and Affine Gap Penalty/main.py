import os

# BLOSUM62 matrisinə əsasən affin boşluq cəriməsi ilə qlobal düzülüş xalını tapırıq
# Compute global alignment score with BLOSUM62 and affine gap penalty (-11 opening, -1 extension)


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
    input_path = os.path.join(script_dir, "rosalind_gaff.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    seqs = parse_fasta(input_path)
    s, t = seqs[0], seqs[1]

    M, N = len(s), len(t)
    blosum = load_blosum62()

    # Gap open and gap extend penalties
    GAP_OPEN = -11
    GAP_EXT = -1
    INF = float("inf")

    # M: match, X: gap in s, Y: gap in t matrices
    # Initialize DP tables
    dp_M = [[-INF] * (N + 1) for _ in range(M + 1)]
    dp_X = [[-INF] * (N + 1) for _ in range(M + 1)]
    dp_Y = [[-INF] * (N + 1) for _ in range(M + 1)]

    # Base cases
    dp_M[0][0] = 0
    for i in range(1, M + 1):
        dp_X[i][0] = GAP_OPEN + (i - 1) * GAP_EXT
    for j in range(1, N + 1):
        dp_Y[0][j] = GAP_OPEN + (j - 1) * GAP_EXT

    # Dinamik proqramlaşdırma
    # Run DP loops for affine gaps
    for i in range(1, M + 1):
        for j in range(1, N + 1):
            cost = blosum[(s[i - 1], t[j - 1])]
            dp_M[i][j] = cost + max(
                dp_M[i - 1][j - 1], dp_X[i - 1][j - 1], dp_Y[i - 1][j - 1]
            )
            dp_X[i][j] = max(
                dp_M[i - 1][j] + GAP_OPEN,
                dp_X[i - 1][j] + GAP_EXT,
                dp_Y[i - 1][j] + GAP_OPEN,
            )
            dp_Y[i][j] = max(
                dp_M[i][j - 1] + GAP_OPEN,
                dp_X[i][j - 1] + GAP_OPEN,
                dp_Y[i][j - 1] + GAP_EXT,
            )

    ans = max(dp_M[M][N], dp_X[M][N], dp_Y[M][N])
    print(f"Global Alignment Score (Affine gaps): {ans}")

    with open(output_path, "w") as f:
        f.write(str(ans) + "\n")


if __name__ == "__main__":
    main()
