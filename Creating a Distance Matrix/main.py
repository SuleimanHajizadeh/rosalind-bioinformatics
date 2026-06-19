import os

# FASTA faylından məsafə matrisini (distance matrix) hesablayırıq
# Parse FASTA records and calculate p-distance matrix for a set of DNA sequences


def read_fasta(file_path):
    seqs = []
    curr = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
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
    input_path = os.path.join(script_dir, "rosalind_pdst.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    seqs = read_fasta(input_path)
    n = len(seqs)
    L = len(seqs[0])

    # Məsafələri (p-distance) hesablayırıq
    # Compute p-distances pairwise
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            diffs = sum(1 for k in range(L) if seqs[i][k] != seqs[j][k])
            matrix[i][j] = diffs / L

    # Nəticəni output.txt faylına yazırıq
    # Write distance matrix formatted with 5 decimal places to output.txt
    with open(output_path, "w") as f:
        for row in matrix:
            row_str = " ".join(f"{val:.5f}" for val in row)
            print(row_str)
            f.write(row_str + "\n")


if __name__ == "__main__":
    main()
