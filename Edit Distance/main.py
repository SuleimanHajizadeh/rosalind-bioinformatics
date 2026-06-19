import os

# İki FASTA ardıcıllığı arasındakı ən qısa edit məsafəsini (Edit Distance) hesablayırıq
# Compute the minimum edit distance between two sequences from FASTA file


def read_fasta(file_path):
    sequences = []
    current_seq = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
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
    input_path = os.path.join(script_dir, "rosalind_edit.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    seqs = read_fasta(input_path)
    s, t = seqs[0], seqs[1]

    M, N = len(s), len(t)
    # Dinamik proqramlaşdırma cədvəlini (DP table) doldururuq
    # Fill the DP table to find the edit distance
    dp = [[0] * (N + 1) for _ in range(M + 1)]

    for i in range(M + 1):
        dp[i][0] = i
    for j in range(N + 1):
        dp[0][j] = j

    for i in range(1, M + 1):
        for j in range(1, N + 1):
            cost = 0 if s[i - 1] == t[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j - 1] + cost,  # əvəzləmə (substitution)
                dp[i - 1][j] + 1,  # silmə (deletion)
                dp[i][j - 1] + 1,  # əlavə etmə (insertion)
            )

    dist = dp[M][N]
    print(f"Edit Distance: {dist}")

    with open(output_path, "w") as f:
        f.write(str(dist) + "\n")


if __name__ == "__main__":
    main()
