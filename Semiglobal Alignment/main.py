import sys
import os
import array

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
    input_path = "rosalind_smgb.txt"
    output_path = "output.txt"

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        sys.exit(1)

    sequences = parse_fasta(input_path)
    s, t = sequences[0], sequences[1]
    n, m = len(s), len(t)

    MATCH = 1
    MISMATCH = -1
    GAP = -1

    row_len = m + 1

    # Yaddaşa qənaət etmək üçün 1D massivlərdən (Flat arrays) istifadə edirik
    # Flattened arrays to minimize memory footprint during dynamic programming
    dp = array.array("h", [0] * ((n + 1) * (m + 1)))
    trace = bytearray((n + 1) * (m + 1))

    # Dinamik proqramlaşdırma (Semiglobal Alignment)
    # Fill DP table: prefix gaps in s and t are free (0 penalty)
    for i in range(1, n + 1):
        s_char = s[i - 1]
        i_offset = i * row_len
        prev_i_offset = (i - 1) * row_len

        for j in range(1, m + 1):
            t_char = t[j - 1]
            match_score = MATCH if s_char == t_char else MISMATCH

            score_diag = dp[prev_i_offset + (j - 1)] + match_score
            score_up = dp[prev_i_offset + j] + GAP
            score_left = dp[i_offset + (j - 1)] + GAP

            val = max(score_diag, score_up, score_left)
            dp[i_offset + j] = val

            # Geri izləmə yönü: 1 = diaqonal, 2 = yuxarı, 3 = sol
            # Backtrack direction code: 1 = diag, 2 = up, 3 = left
            if val == score_diag:
                trace[i_offset + j] = 1
            elif val == score_up:
                trace[i_offset + j] = 2
            else:
                trace[i_offset + j] = 3

    # Son sətir və ya sütundan ən böyük xalı tapırıq (sufiks boşluqları cəriməsizdir)
    # Locate maximum score in last row or last column (suffix gaps are free)
    opt_score = -float("inf")
    opt_i = -1
    opt_j = -1

    n_offset = n * row_len
    for j in range(m + 1):
        val = dp[n_offset + j]
        if val > opt_score:
            opt_score = val
            opt_i = n
            opt_j = j

    for i in range(n + 1):
        val = dp[i * row_len + m]
        if val > opt_score:
            opt_score = val
            opt_i = i
            opt_j = m

    # Geri izləmə ilə semiqlobal düzülüşü bərpa edirik
    # Backtrack to reconstruct the aligned sequences
    align_s = []
    align_t = []

    # 1. Pulsuz sufiks boşluqlarını əlavə edirik
    # Append suffix gaps
    if opt_i < n and opt_j == m:
        for k in range(n - 1, opt_i - 1, -1):
            align_s.append(s[k])
            align_t.append("-")
    elif opt_j < m and opt_i == n:
        for k in range(m - 1, opt_j - 1, -1):
            align_s.append("-")
            align_t.append(t[k])

    # 2. Düzülüş sahəsini geri izləyirik
    # Backtrack alignment matrix region
    i, j = opt_i, opt_j
    while i > 0 and j > 0:
        dir_code = trace[i * row_len + j]
        if dir_code == 1:
            align_s.append(s[i - 1])
            align_t.append(t[j - 1])
            i -= 1
            j -= 1
        elif dir_code == 2:
            align_s.append(s[i - 1])
            align_t.append("-")
            i -= 1
        elif dir_code == 3:
            align_s.append("-")
            align_t.append(t[j - 1])
            j -= 1
        else:
            break

    # 3. Pulsuz prefiks boşluqlarını əlavə edirik
    # Append prefix gaps
    if i > 0 and j == 0:
        for k in range(i - 1, -1, -1):
            align_s.append(s[k])
            align_t.append("-")
    elif j > 0 and i == 0:
        for k in range(j - 1, -1, -1):
            align_s.append("-")
            align_t.append(t[k])

    align_s.reverse()
    align_t.reverse()
    aligned_s = "".join(align_s)
    aligned_t = "".join(align_t)

    print(f"Optimal Score: {opt_score}")

    with open(output_path, "w") as out:
        out.write(f"{opt_score}\n")
        out.write(f"{aligned_s}\n")
        out.write(f"{aligned_t}\n")


if __name__ == "__main__":
    main()
