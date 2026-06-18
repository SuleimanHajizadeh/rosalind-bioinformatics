import sys
import os

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
    input_path = "rosalind_sims.txt"
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        sys.exit(1)

    sequences = parse_fasta(input_path)
    if len(sequences) < 2:
        print("Error: Could not find at least two sequences in the input FASTA file.")
        sys.exit(1)

    s = sequences[0]
    t = sequences[1]

    n, m = len(s), len(t)
    print(f"Loaded s (length {n}) and t (length {m}). Running fitting alignment...")

    # Scoring parameters
    MATCH = 1
    MISMATCH = -1
    GAP = -1

    # DP table of size (n+1) x (m+1)
    # dp[i][j] will store the optimal score aligning a suffix of s[0:i] to t[0:j]
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Initialize boundary conditions
    # j = 0: aligning a suffix of s to empty t -> score is 0 (free to start anywhere)
    for i in range(n + 1):
        dp[i][0] = 0

    # i = 0: aligning empty prefix of s to non-empty prefix of t -> must penalize gaps in s
    for j in range(1, m + 1):
        dp[0][j] = dp[0][j-1] + GAP

    # Fill the DP table
    for i in range(1, n + 1):
        s_char = s[i-1]
        for j in range(1, m + 1):
            t_char = t[j-1]
            match_score = MATCH if s_char == t_char else MISMATCH
            
            score_diag = dp[i-1][j-1] + match_score
            score_up = dp[i-1][j] + GAP
            score_left = dp[i][j-1] + GAP
            
            dp[i][j] = max(score_diag, score_up, score_left)

    # Find the optimal ending position in s
    opt_score = -float('inf')
    opt_i = -1
    for i in range(n + 1):
        if dp[i][m] > opt_score:
            opt_score = dp[i][m]
            opt_i = i

    print(f"Optimal Score: {opt_score} ending at s index {opt_i}")

    # Backtrack to reconstruct alignment
    align_s = []
    align_t = []
    i, j = opt_i, m
    while j > 0:
        match_score = MATCH if s[i-1] == t[j-1] else MISMATCH
        if i > 0 and dp[i][j] == dp[i-1][j-1] + match_score:
            align_s.append(s[i-1])
            align_t.append(t[j-1])
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] + GAP:
            align_s.append(s[i-1])
            align_t.append('-')
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j-1] + GAP:
            align_s.append('-')
            align_t.append(t[j-1])
            j -= 1
        else:
            # Should not happen, but safeguard
            break

    align_s.reverse()
    align_t.reverse()

    aligned_s = ''.join(align_s)
    aligned_t = ''.join(align_t)

    # Write to output.txt
    with open("output.txt", "w") as out:
        out.write(f"{opt_score}\n")
        out.write(f"{aligned_s}\n")
        out.write(f"{aligned_t}\n")

    print("Successfully wrote solution to output.txt")

if __name__ == '__main__':
    main()
