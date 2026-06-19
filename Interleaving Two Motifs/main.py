import os

# İki ardıcıllıqdan ortaq ən qısa super ardıcıllığı (Shortest Common Supersequence) hesablayırıq
# Compute the shortest common supersequence interleaving two motifs s and t


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_scsp.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        lines = f.read().splitlines()

    s = lines[0].strip()
    t = lines[1].strip()

    M, N = len(s), len(t)

    # DP matrisi (LCS tapmaq üçün)
    # DP matrix to compute LCS length
    dp = [[0] * (N + 1) for _ in range(M + 1)]

    for i in range(1, M + 1):
        for j in range(1, N + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Geri izləmə (backtracking) edərək super ardıcıllığı qururuq
    # Backtrack to build the shortest common supersequence
    superseq = []
    i, j = M, N
    while i > 0 and j > 0:
        if s[i - 1] == t[j - 1]:
            superseq.append(s[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            superseq.append(s[i - 1])
            i -= 1
        else:
            superseq.append(t[j - 1])
            j -= 1

    while i > 0:
        superseq.append(s[i - 1])
        i -= 1
    while j > 0:
        superseq.append(t[j - 1])
        j -= 1

    superseq.reverse()
    result = "".join(superseq)

    print(f"Supersequence length: {len(result)}")

    with open(output_path, "w") as f:
        f.write(result + "\n")


if __name__ == "__main__":
    main()
