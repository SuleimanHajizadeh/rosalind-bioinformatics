import os

# FASTA formatını parçalayırıq
# Parse sequences from FASTA format input


def read_fasta(file_path):
    strings = []
    current_string = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_string:
                    strings.append("".join(current_string))
                    current_string = []
            else:
                current_string.append(line)
        if current_string:
            strings.append("".join(current_string))
    return strings


def align_edit_distance(s, t):
    m = len(s)
    n = len(t)

    # D[i][j] verilmiş prefikslər üçün optimal edit məsafəsini saxlayır
    # D[i][j] will store the edit distance of s[:i] and t[:j]
    D = [[0] * (n + 1) for _ in range(m + 1)]

    # Başlanğıc şərtləri təyin edirik
    # Initialize base cases
    for i in range(m + 1):
        D[i][0] = i
    for j in range(n + 1):
        D[0][j] = j

    # DP cədvəlini doldururuq
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s[i - 1] == t[j - 1] else 1
            D[i][j] = min(
                D[i - 1][j - 1] + cost,  # Əvəzləmə (Match/Mismatch)
                D[i - 1][j] + 1,  # Silmə (Deletion)
                D[i][j - 1] + 1,  # Əlavə etmə (Insertion)
            )

    # Geri izləmə ilə düzülmüş sətirləri bərpa edirik
    # Traceback to reconstruct the aligned strings representation
    s_aligned = []
    t_aligned = []
    i, j = m, n

    while i > 0 or j > 0:
        if i > 0 and j > 0:
            cost = 0 if s[i - 1] == t[j - 1] else 1
            if D[i][j] == D[i - 1][j - 1] + cost:
                s_aligned.append(s[i - 1])
                t_aligned.append(t[j - 1])
                i -= 1
                j -= 1
                continue
        if i > 0 and D[i][j] == D[i - 1][j] + 1:
            s_aligned.append(s[i - 1])
            t_aligned.append("-")
            i -= 1
        elif j > 0 and D[i][j] == D[i][j - 1] + 1:
            s_aligned.append("-")
            t_aligned.append(t[j - 1])
            j -= 1

    s_aligned.reverse()
    t_aligned.reverse()

    return D[m][n], "".join(s_aligned), "".join(t_aligned)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_edta.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    fasta_strings = read_fasta(input_path)
    s, t = fasta_strings[0], fasta_strings[1]

    edit_dist, s_aligned, t_aligned = align_edit_distance(s, t)
    print(f"Edit Distance: {edit_dist}")

    with open(output_path, "w") as out_file:
        out_file.write(f"{edit_dist}\n")
        out_file.write(f"{s_aligned}\n")
        out_file.write(f"{t_aligned}\n")


if __name__ == "__main__":
    main()
