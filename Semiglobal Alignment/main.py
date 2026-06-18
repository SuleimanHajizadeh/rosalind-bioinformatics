import sys
import os
import array

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
    input_path = "rosalind_smgb.txt"
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
    print(f"Loaded s (length {n}) and t (length {m}). Running semiglobal alignment...")

    # Scoring parameters
    MATCH = 1
    MISMATCH = -1
    GAP = -1

    # Row length for 1D indexing
    row_len = m + 1

    # Flat arrays to save memory:
    # dp: signed 16-bit integers (2 bytes per cell). For 10000x10000 -> 200 MB.
    # trace: 8-bit unsigned integers (1 byte per cell). For 10000x10000 -> 100 MB.
    dp = array.array('h', [0] * ((n + 1) * (m + 1)))
    trace = bytearray((n + 1) * (m + 1))

    # Initialize boundary conditions:
    # Prefix gaps in t (first column) are free -> dp[i][0] = 0
    # Prefix gaps in s (first row) are free -> dp[0][j] = 0
    # Flat array starts initialized to 0, so they are already 0.
    
    # Fill the DP table
    for i in range(1, n + 1):
        s_char = s[i-1]
        i_offset = i * row_len
        prev_i_offset = (i-1) * row_len
        
        for j in range(1, m + 1):
            t_char = t[j-1]
            match_score = MATCH if s_char == t_char else MISMATCH
            
            score_diag = dp[prev_i_offset + (j-1)] + match_score
            score_up = dp[prev_i_offset + j] + GAP
            score_left = dp[i_offset + (j-1)] + GAP
            
            val = max(score_diag, score_up, score_left)
            dp[i_offset + j] = val
            
            # Traceback code: 1 = diag, 2 = up, 3 = left
            if val == score_diag:
                trace[i_offset + j] = 1
            elif val == score_up:
                trace[i_offset + j] = 2
            else:
                trace[i_offset + j] = 3

    # Find the maximum score in the last row or last column (suffix gaps are free)
    opt_score = -float('inf')
    opt_i = -1
    opt_j = -1

    # Last row: i = n
    n_offset = n * row_len
    for j in range(m + 1):
        val = dp[n_offset + j]
        if val > opt_score:
            opt_score = val
            opt_i = n
            opt_j = j

    # Last column: j = m
    for i in range(n + 1):
        val = dp[i * row_len + m]
        if val > opt_score:
            opt_score = val
            opt_i = i
            opt_j = m

    print(f"Optimal Score: {opt_score} at cell ({opt_i}, {opt_j})")

    # Backtrack to reconstruct alignment
    align_s = []
    align_t = []

    # 1. Append suffix gaps (free)
    if opt_i < n and opt_j == m:
        for k in range(n - 1, opt_i - 1, -1):
            align_s.append(s[k])
            align_t.append('-')
    elif opt_j < m and opt_i == n:
        for k in range(m - 1, opt_j - 1, -1):
            align_s.append('-')
            align_t.append(t[k])

    # 2. Alignment region backtracking
    i, j = opt_i, opt_j
    while i > 0 and j > 0:
        dir_code = trace[i * row_len + j]
        if dir_code == 1:
            align_s.append(s[i-1])
            align_t.append(t[j-1])
            i -= 1
            j -= 1
        elif dir_code == 2:
            align_s.append(s[i-1])
            align_t.append('-')
            i -= 1
        elif dir_code == 3:
            align_s.append('-')
            align_t.append(t[j-1])
            j -= 1
        else:
            # Should not happen
            break

    # 3. Append prefix gaps (free)
    if i > 0 and j == 0:
        for k in range(i - 1, -1, -1):
            align_s.append(s[k])
            align_t.append('-')
    elif j > 0 and i == 0:
        for k in range(j - 1, -1, -1):
            align_s.append('-')
            align_t.append(t[k])

    # Reverse and join
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
