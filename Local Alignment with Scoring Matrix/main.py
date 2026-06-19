import os
import sys

# Lokal düzülüşün xal matrisi və cədvəli üçün köməkçi sinif
# Local alignment structure utilizing dynamic programming and BLOSUM62/PAM250 matrices


class PAM250:
    def __init__(self):
        # PAM250 matrisini təyin edirik
        # Define PAM250 substitution matrix values
        self.alphabet = "A R N D C Q E G H I L K M F P S T W Y V".split()
        matrix_raw = [
            [2, -2, 0, 0, -2, 0, 0, 1, -1, -1, -2, -1, -1, -3, 1, 1, 1, -6, -3, 0],
            [-2, 6, 0, -1, -4, 1, -1, -3, 2, -2, -3, 3, 0, -4, 0, 0, -1, 2, -4, -2],
            [0, 0, 2, 2, -4, 1, 1, 0, 2, -2, -3, 1, -2, -4, 0, 1, 0, -4, -2, -2],
            [0, -1, 2, 4, -5, 2, 3, 1, 1, -2, -4, 0, -3, -6, -1, 0, 0, -7, -4, -2],
            [-2, -4, -4, -5, 12, -5, -5, -3, -3, -2, -6, -5, -5, -4, -3, 0, -2, -8, 0, -2],
            [0, 1, 1, 2, -5, 4, 3, -1, 3, -2, -2, 1, -1, -5, 0, -1, -1, -5, -4, -2],
            [0, -1, 1, 3, -5, 3, 4, 0, 1, -2, -3, 0, -2, -5, -1, 0, 0, -7, -4, -2],
            [1, -3, 0, 1, -3, -1, 0, 5, -2, -3, -4, -2, -3, -5, 0, 1, 0, -7, -5, -1],
            [-1, 2, 2, 1, -3, 3, 1, -2, 6, -2, -2, 0, -2, -2, 0, -1, -1, -3, 0, -2],
            [-1, -2, -2, -2, -2, -2, -2, -3, -2, 5, 2, -2, 2, 1, -2, -1, 0, -5, -1, 4],
            [-2, -3, -3, -4, -6, -2, -3, -4, -2, 2, 6, -3, 4, 2, -3, -3, -2, -2, -1, 2],
            [-1, 3, 1, 0, -5, 1, 0, -2, 0, -2, -3, 5, 0, -5, -1, 0, -1, -3, -4, -2],
            [-1, 0, -2, -3, -5, -1, -2, -3, -2, 2, 4, 0, 6, 0, -2, -2, -1, -4, -2, 2],
            [-3, -4, -4, -6, -4, -5, -5, -5, -2, 1, 2, -5, 0, 9, -5, -3, -3, 0, 7, -1],
            [1, 0, 0, -1, -3, 0, -1, 0, 0, -2, -3, -1, -2, -5, 6, 1, 0, -6, -5, -1],
            [1, 0, 1, 0, 0, -1, 0, 1, -1, -1, -3, 0, -2, -3, 1, 2, 1, -2, -3, -1],
            [1, -1, 0, 0, -2, -1, 0, 0, -1, 0, -2, -1, -1, -3, 0, 1, 3, -5, -3, 0],
            [-6, 2, -4, -7, -8, -5, -7, -7, -3, -5, -2, -3, -4, 0, -6, -2, -5, 17, 0, -6],
            [-3, -4, -2, -4, 0, -4, -4, -5, 0, -1, -1, -4, -2, 7, -5, -3, -3, 0, 10, -2],
            [0, -2, -2, -2, -2, -2, -2, -1, -2, 4, 2, -2, 2, -1, -1, -1, 0, -6, -2, 4],
        ]
        self.scores = {}
        for r_idx, r in enumerate(self.alphabet):
            for c_idx, c in enumerate(self.alphabet):
                self.scores[(r, c)] = matrix_raw[r_idx][c_idx]


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
    input_path = os.path.join(script_dir, "rosalind_loca.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    seqs = parse_fasta(input_path)
    s, t = seqs[0], seqs[1]

    pam = PAM250()
    M, N = len(s), len(t)
    dp = [[0] * (N + 1) for _ in range(M + 1)]

    max_val = -1
    max_pos = (0, 0)

    # Dinamik proqramlaşdırma ilə Smit-Uoterman (Smith-Waterman) lokal düzülüş matrisini doldururuq
    # Fill Smith-Waterman DP table with PAM250 scores and constant gap penalty of -5
    for i in range(1, M + 1):
        for j in range(1, N + 1):
            match_score = pam.scores[(s[i - 1], t[j - 1])]
            dp[i][j] = max(
                0,
                dp[i - 1][j - 1] + match_score,
                dp[i - 1][j] - 5,
                dp[i][j - 1] - 5,
            )
            if dp[i][j] > max_val:
                max_val = dp[i][j]
                max_pos = (i, j)

    # Geri izləmə (backtracking) ilə ən yaxşı lokal düzülüş zəncirini tapırıq
    # Backtrack to find the optimal local alignment substrings
    i, j = max_pos
    sub_s = []
    sub_t = []

    while i > 0 and j > 0 and dp[i][j] > 0:
        match_score = pam.scores[(s[i - 1], t[j - 1])]
        if dp[i][j] == dp[i - 1][j - 1] + match_score:
            sub_s.append(s[i - 1])
            sub_t.append(t[j - 1])
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i - 1][j] - 5:
            sub_s.append(s[i - 1])
            sub_t.append("-")
            i -= 1
        else:
            sub_s.append("-")
            sub_t.append(t[j - 1])
            j -= 1

    sub_s.reverse()
    sub_t.reverse()

    result_s = "".join(sub_s).replace("-", "")
    result_t = "".join(sub_t).replace("-", "")

    print(f"Max Score: {max_val}")

    with open(output_path, "w") as f:
        f.write(f"{max_val}\n")
        f.write(f"{result_s}\n")
        f.write(f"{result_t}\n")


if __name__ == "__main__":
    main()
