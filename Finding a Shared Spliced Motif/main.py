import os
import sys

# İki ardıcıllıq arasında ən uzun ortaq alt-ardıcıllığı (LCS - Spliced Motif) dinamik proqramlaşdırma ilə tapırıq
# Find the longest common subsequence (LCS) between two sequences to obtain a shared spliced motif


def solve_lcsq(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    # FASTA faylını oxuyuruq
    # Read and parse FASTA records
    with open(input_path, "r") as f:
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

    s, t = seqs[0], seqs[1]
    M, N = len(s), len(t)

    # DP cədvəlini (LCS tapmaq üçün) qururuq
    # DP matrix to compute the longest common subsequence length
    dp = [[0] * (N + 1) for _ in range(M + 1)]

    for i in range(1, M + 1):
        for j in range(1, N + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Geri izləmə (backtracking) edərək alt-ardıcıllığı tapırıq
    # Backtrack to reconstruct the LCS string representation
    lcs = []
    i, j = M, N
    while i > 0 and j > 0:
        if s[i - 1] == t[j - 1]:
            lcs.append(s[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    lcs.reverse()
    result = "".join(lcs)

    with open(output_path, "w") as f:
        f.write(result + "\n")

    print(f"LCS length: {len(result)}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_lcsq.txt")
    output_file = os.path.join(script_dir, "output.txt")
    solve_lcsq(input_file, output_file)
