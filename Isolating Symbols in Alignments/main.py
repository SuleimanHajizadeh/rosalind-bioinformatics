import os
import sys

def parse_fasta(filepath):
    sequences = []
    current_seq = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if current_seq:
                    sequences.append(''.join(current_seq))
                    current_seq = []
            else:
                current_seq.append(line)
        if current_seq:
            sequences.append(''.join(current_seq))
    return sequences

def main():
    input_path = "rosalind_osym.txt"
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        sys.exit(1)

    sequences = parse_fasta(input_path)
    if len(sequences) < 2:
        print("Error: Could not find at least two sequences in the input FASTA file.")
        sys.exit(1)

    s = sequences[0]
    t = sequences[1]

    m = len(s)
    n = len(t)
    print(f"Loaded s (length {m}) and t (length {n}). Running alignment analysis...")

    MATCH = 1
    MISMATCH = -1
    GAP = -1

    def score(a, b):
        return MATCH if a == b else MISMATCH

    # fwd[i][j] is the global alignment score of s[0..i-1] and t[0..j-1]
    fwd = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        fwd[i][0] = i * GAP
    for j in range(n + 1):
        fwd[0][j] = j * GAP

    for i in range(1, m + 1):
        s_char = s[i-1]
        for j in range(1, n + 1):
            fwd[i][j] = max(
                fwd[i-1][j-1] + (MATCH if s_char == t[j-1] else MISMATCH),
                fwd[i-1][j] + GAP,
                fwd[i][j-1] + GAP
            )

    # bwd[i][j] is the global alignment score of s[i..m-1] and t[j..n-1]
    bwd = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        bwd[i][n] = (m - i) * GAP
    for j in range(n + 1):
        bwd[m][j] = (n - j) * GAP

    for i in range(m - 1, -1, -1):
        s_char = s[i]
        for j in range(n - 1, -1, -1):
            bwd[i][j] = max(
                bwd[i+1][j+1] + (MATCH if s_char == t[j] else MISMATCH),
                bwd[i+1][j] + GAP,
                bwd[i][j+1] + GAP
            )

    # Compute M[j][k] and its sum
    sum_M = 0
    for j in range(m):
        s_char = s[j]
        for k in range(n):
            val = fwd[j][k] + (MATCH if s_char == t[k] else MISMATCH) + bwd[j+1][k+1]
            sum_M += val

    global_score = fwd[m][n]

    # Write output to output.txt
    output_path = "output.txt"
    with open(output_path, "w") as out:
        out.write(f"{global_score}\n")
        out.write(f"{sum_M}\n")

    print(f"Successfully wrote solution to {output_path}")
    print(f"Global Alignment Score: {global_score}")
    print(f"Sum of M matrix: {sum_M}")

if __name__ == '__main__':
    main()
