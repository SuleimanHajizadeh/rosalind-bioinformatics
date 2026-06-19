#!/usr/bin/env python3
import os

# BLOSUM62 matrisinə əsasən affin boşluq cəriməsi ilə lokal düzülüşü tapırıq
# Compute local alignment score with BLOSUM62 and affine gap penalty (-11 opening, -1 extension)

BLOSUM62_TEXT = (
    "A  4 -1 -2 -2  0 -1 -1  0 -2 -1 -1 -1 -1 -2 -1  1  0 -3 -2  0 -2 -1 -1 -4\n"
    "R -1  5  0 -2 -3  1  0 -2  0 -3 -2  2 -1 -3 -2 -1 -1 -3 -2 -3 -1  0 -1 -4\n"
    "N -2  0  6  1 -3  0  0  0  1 -3 -3  0 -2 -3 -2  1  0 -4 -2 -3  3  0 -1 -4\n"
    "D -2 -2  1  6 -3  0  2 -1 -1 -3 -4 -1 -3 -3 -1  0 -1 -4 -3 -3  4  1 -1 -4\n"
    "C  0 -3 -3 -3  9 -3 -4 -3 -3 -1 -1 -3 -1 -2 -3 -1 -1 -2 -2 -1 -3 -3 -2 -4\n"
    "Q -1  1  0  0 -3  5  2 -2  0 -3 -2  1  0 -3 -1  0 -1 -2 -1 -2  0  3 -1 -4\n"
    "E -1  0  0  2 -4  2  5 -2  0 -3 -3  1 -2 -3 -1  0 -1 -3 -2 -2  1  4 -1 -4\n"
    "G  0 -2  0 -1 -3 -2 -2  6 -2 -4 -4 -2 -3 -3 -2  0 -2 -2 -3 -3 -1 -2 -1 -4\n"
    "H -2  0  1 -1 -3  0  0 -2  8 -3 -3 -1 -2 -1 -2 -1 -2 -2  2 -3  0  0 -1 -4\n"
    "I -1 -3 -3 -3 -1 -3 -3 -4 -3  4  2 -3  1  0 -3 -2 -1 -3 -1  3 -3 -3 -1 -4\n"
    "L -2 -3 -3 -4 -1 -2 -3 -4 -3  2  4 -2  2  0 -3 -2 -1 -2 -1  1 -4 -3 -1 -4\n"
    "K -1  2  0 -1 -3  1  1 -2 -1 -3 -2  5 -1 -3 -1  0 -1 -3 -2 -2 -1  1 -1 -4\n"
    "M -1 -1 -2 -3 -1  0 -2 -3 -2  1  2 -1  5  0 -2 -1 -1 -1 -1  1 -3 -1 -1 -4\n"
    "F -2 -3 -3 -3 -2 -3 -3 -3 -1  0  0 -3  0  6 -4 -2 -2  1  3 -1 -3 -3 -1 -4\n"
    "P -1 -2 -2 -1 -3 -1 -1 -2 -2 -2 -3 -1 -2 -4  7 -1 -1 -4 -3 -2 -2 -1 -2 -4\n"
    "S  1 -1  1  0 -1  0  0  0 -1 -2 -2  0 -1 -2 -1  4  1 -3 -2 -2  0  0  0 -4\n"
    "T  0 -1  0 -1 -2 -1 -1  2 -2 -1 -1 -1 -1 -3 -1  1  5 -2 -2  0 -1 -1  0 -4\n"
    "W -3 -3 -4 -4 -8 -2 -7 -7 -3 -5 -2 -3 -4  1 -6 -2 -5 11  2 -3 -4 -5 -3 -4\n"
    "Y -2 -2 -2 -3 -2 -1 -2 -3  2 -1 -1 -2 -1  3 -3 -2 -2  2  7 -1 -2 -2 -1 -4\n"
    "V  0 -3 -3 -3 -1 -2 -2 -1 -3  3  1 -2  1 -1 -2 -2  0 -3 -1  4 -3 -2 -1 -4"
)



def load_blosum62():
    lines = [line.strip() for line in BLOSUM62_TEXT.strip().split("\n")]
    alphabet = [line.split()[0] for line in lines]
    scores = {}
    for i, line in enumerate(lines):
        vals = list(map(int, line.split()[1:]))
        for j, char in enumerate(alphabet):
            scores[(alphabet[i], char)] = vals[j]
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
    input_path = os.path.join(script_dir, "rosalind_laff.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    seqs = parse_fasta(input_path)
    s, t = seqs[0], seqs[1]

    M, N = len(s), len(t)
    blosum = load_blosum62()

    GAP_OPEN = -11
    GAP_EXT = -1
    INF = float("inf")

    # Smit-Uoterman lokal affin düzülüş matrisləri
    # Smith-Waterman local alignment DP tables for affine gaps
    dp_M = [[0] * (N + 1) for _ in range(M + 1)]
    dp_X = [[-INF] * (N + 1) for _ in range(M + 1)]
    dp_Y = [[-INF] * (N + 1) for _ in range(M + 1)]

    max_score = -1
    max_pos = (0, 0)

    for i in range(1, M + 1):
        for j in range(1, N + 1):
            cost = blosum[(s[i - 1], t[j - 1])]
            dp_M[i][j] = max(
                0,
                dp_M[i - 1][j - 1] + cost,
                dp_X[i - 1][j - 1] + cost,
                dp_Y[i - 1][j - 1] + cost,
            )
            dp_X[i][j] = max(
                dp_M[i - 1][j] + GAP_OPEN, dp_X[i - 1][j] + GAP_EXT
            )
            dp_Y[i][j] = max(
                dp_M[i][j - 1] + GAP_OPEN, dp_Y[i][j - 1] + GAP_EXT
            )

            current_max = max(dp_M[i][j], dp_X[i][j], dp_Y[i][j])
            if current_max > max_score:
                max_score = current_max
                max_pos = (i, j)

    # Geri izləmə ilə lokal zənciri tapırıq
    # Backtrack to locate alignment substrings
    i, j = max_pos
    sub_s = []
    sub_t = []

    while i > 0 and j > 0 and max(dp_M[i][j], dp_X[i][j], dp_Y[i][j]) > 0:
        cost = blosum[(s[i - 1], t[j - 1])]
        if dp_M[i][j] >= dp_X[i][j] and dp_M[i][j] >= dp_Y[i][j]:
            sub_s.append(s[i - 1])
            sub_t.append(t[j - 1])
            i -= 1
            j -= 1
        elif dp_X[i][j] >= dp_Y[i][j]:
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

    print(f"Max Score: {max_score}")

    with open(output_path, "w") as f:
        f.write(f"{max_score}\n")
        f.write(f"{result_s}\n")
        f.write(f"{result_t}\n")


if __name__ == "__main__":
    main()
