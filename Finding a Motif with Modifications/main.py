import sys
import os

# FASTA formatını parçalayırıq
# Parse sequences from FASTA format input


def parse_fasta(filepath):
    sequences = []
    current_seq = []
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_seq:
                    sequences.append("".join(current_seq))
                    current_seq = []
            else:
                current_seq.append(line)
        if current_seq:
            sequences.append("".join(current_seq))
    return sequences


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_sims.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        sys.exit(1)

    sequences = parse_fasta(input_path)
    s, t = sequences[0], sequences[1]
    n, m = len(s), len(t)

    MATCH = 1
    MISMATCH = -1
    GAP = -1

    # dp[i][j] s-in i sonluğu ilə t-nin j prefiksinin optimal düzülüş xalını saxlayır
    # dp[i][j] will store optimal score aligning a suffix of s[0:i] to t[0:j]
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Başlanğıc şərtləri təyin edirik
    # Initialize boundary conditions: s can start match anywhere for free
    for i in range(n + 1):
        dp[i][0] = 0
    for j in range(1, m + 1):
        dp[0][j] = dp[0][j - 1] + GAP

    # Dinamik proqramlaşdırma ilə cədvəli doldururuq (Fitting Alignment)
    # Fill DP table for fitting alignment
    for i in range(1, n + 1):
        s_char = s[i - 1]
        for j in range(1, m + 1):
            t_char = t[j - 1]
            match_score = MATCH if s_char == t_char else MISMATCH

            score_diag = dp[i - 1][j - 1] + match_score
            score_up = dp[i - 1][j] + GAP
            score_left = dp[i][j - 1] + GAP

            dp[i][j] = max(score_diag, score_up, score_left)

    # s üzrə ən optimal bitmə mövqeyini tapırıq
    # Find the optimal ending position in s
    opt_score = -float("inf")
    opt_i = -1
    for i in range(n + 1):
        if dp[i][m] > opt_score:
            opt_score = dp[i][m]
            opt_i = i

    # Geri izləmə ilə optimal düzülüşü bərpa edirik
    # Backtrack to reconstruct the aligned sequences
    align_s = []
    align_t = []
    i, j = opt_i, m
    while j > 0:
        match_score = MATCH if s[i - 1] == t[j - 1] else MISMATCH
        if i > 0 and dp[i][j] == dp[i - 1][j - 1] + match_score:
            align_s.append(s[i - 1])
            align_t.append(t[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + GAP:
            align_s.append(s[i - 1])
            align_t.append("-")
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + GAP:
            align_s.append("-")
            align_t.append(t[j - 1])
            j -= 1
        else:
            break

    align_s.reverse()
    align_t.reverse()

    aligned_s = "".join(align_s)
    aligned_t = "".join(align_t)

    with open(output_path, "w") as out:
        out.write(f"{opt_score}\n")
        out.write(f"{aligned_s}\n")
        out.write(f"{aligned_t}\n")

    print(f"Optimal Score: {opt_score}")


if __name__ == "__main__":
    main()
