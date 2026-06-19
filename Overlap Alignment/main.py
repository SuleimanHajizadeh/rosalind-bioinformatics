#!/usr/bin/env python3
import os
import sys

# Rekursiya limitini artırırıq
# Increase recursion limit
sys.setrecursionlimit(20000)


def solve_oap(s, t):
    m, n = len(s), len(t)

    # S[i][j] dinamik düzülüş cədvəlini qururuq (Overlap Alignment)
    # S[i][j] DP table initialization for overlap alignment
    S = [[0] * (n + 1) for _ in range(m + 1)]

    # Başlanğıc şərtləri təyin edirik (s-in prefiks boşluqları cəriməsizdir)
    # Initialize border values: s prefixes can align to gaps for free
    for i in range(m + 1):
        S[i][0] = 0
    for j in range(n + 1):
        S[0][j] = -2 * j

    # DP cədvəlini doldururuq
    # Fill DP table with match score 1 and mismatch/gap penalty -2
    for i in range(1, m + 1):
        s_i = s[i - 1]
        S_i = S[i]
        S_prev = S[i - 1]
        for j in range(1, n + 1):
            match_score = 1 if s_i == t[j - 1] else -2
            val1 = S_prev[j - 1] + match_score
            val2 = S_prev[j] - 2
            val3 = S_i[j - 1] - 2
            if val1 >= val2 and val1 >= val3:
                S_i[j] = val1
            elif val2 >= val1 and val2 >= val3:
                S_i[j] = val2
            else:
                S_i[j] = val3

    # Son sətirdən ən böyük xalı tapırıq
    # Locate maximum score in the last row
    max_score = float("-inf")
    best_j = -1
    S_m = S[m]
    for j in range(n + 1):
        if S_m[j] > max_score:
            max_score = S_m[j]
            best_j = j

    # Geri izləmə ilə düzülüşləri bərpa edirik
    # Backtrack from ending cell (m, best_j) to reconstruct alignments
    i, j = m, best_j
    align_s, align_t = [], []

    while j > 0:
        if i == 0:
            align_s.append("-")
            align_t.append(t[j - 1])
            j -= 1
        else:
            match_score = 1 if s[i - 1] == t[j - 1] else -2
            if S[i][j] == S[i - 1][j - 1] + match_score:
                align_s.append(s[i - 1])
                align_t.append(t[j - 1])
                i -= 1
                j -= 1
            elif S[i][j] == S[i - 1][j] - 2:
                align_s.append(s[i - 1])
                align_t.append("-")
                i -= 1
            elif S[i][j] == S[i][j - 1] - 2:
                align_s.append("-")
                align_t.append(t[j - 1])
                j -= 1
            else:
                raise ValueError("Reconstruction error")

    align_s = "".join(reversed(align_s))
    align_t = "".join(reversed(align_t))

    return int(max_score), align_s, align_t


def parse_fasta(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    fasta = []
    current_seq = []
    for line in lines:
        if line.startswith(">"):
            if current_seq:
                fasta.append("".join(current_seq))
                current_seq = []
        else:
            current_seq.append(line)
    if current_seq:
        fasta.append("".join(current_seq))
    return fasta


def main():
    input_path = "rosalind_oap.txt"
    output_path = "output.txt"

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    fasta = parse_fasta(input_path)
    s, t = fasta[0], fasta[1]

    score, align_s, align_t = solve_oap(s, t)
    print(f"Overlap Score: {score}")

    with open(output_path, "w") as f:
        f.write(f"{score}\n")
        f.write(f"{align_s}\n")
        f.write(f"{align_t}\n")


if __name__ == "__main__":
    main()
