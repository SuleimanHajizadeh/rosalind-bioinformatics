#!/usr/bin/env python3
import os

# BLOSUM62 scoring matrix
BLOSUM62_TEXT = """
A  4 -1 -2 -2  0 -1 -1  0 -2 -1 -1 -1 -1 -2 -1  1  0 -3 -2  0 -2 -1 -1 -4
R -1  5  0 -2 -3  1  0 -2  0 -3 -2  2 -1 -3 -2 -1 -1 -3 -2 -3 -1  0 -1 -4
N -2  0  6  1 -3  0  0  0  1 -3 -3  0 -2 -3 -2  1  0 -4 -2 -3  3  0 -1 -4
D -2 -2  1  6 -3  0  2 -1 -1 -3 -4 -1 -3 -3 -1  0 -1 -4 -3 -3  4  1 -1 -4
C  0 -3 -3 -3  9 -3 -4 -3 -3 -1 -1 -3 -1 -2 -3 -1 -1 -2 -2 -1 -3 -3 -2 -4
Q -1  1  0  0 -3  5  2 -2  0 -3 -2  1  0 -3 -1  0 -1 -2 -1 -2  0  3 -1 -4
E -1  0  0  2 -4  2  5 -2  0 -3 -3  1 -2 -3 -1  0 -1 -3 -2 -2  1  4 -1 -4
G  0 -2  0 -1 -3 -2 -2  6 -2 -4 -4 -2 -3 -3 -2  0 -2 -2 -3 -3 -1 -2 -1 -4
H -2  0  1 -1 -3  0  0 -2  8 -3 -3 -1 -2 -1 -2 -1 -2 -2  2 -3  0  0 -1 -4
I -1 -3 -3 -3 -1 -3 -3 -4 -3  4  2 -3  1  0 -3 -2 -1 -3 -1  3 -3 -3 -1 -4
L -1 -2 -3 -4 -1 -2 -3 -4 -3  2  4 -2  2  0 -3 -2 -1 -2 -1  1 -4 -3 -1 -4
K -1  2  0 -1 -3  1  1 -2 -1 -3 -2  5 -1 -3 -1  0 -1 -3 -2 -2  0  1 -1 -4
M -1 -1 -2 -3 -1  0 -2 -3 -2  1  2 -1  5  0 -2 -1 -1 -1 -1  1 -3 -1 -1 -4
F -2 -3 -3 -3 -2 -3 -3 -3 -1  0  0 -3  0  6 -4 -2 -2  1  3 -1 -3 -3 -1 -4
P -1 -2 -2 -1 -3 -1 -1 -2 -2 -3 -3 -1 -2 -4  7 -1 -1 -4 -3 -2 -2 -1 -2 -4
S  1 -1  1  0 -1  0  0  0 -1 -2 -2  0 -1 -2 -1  4  1 -3 -2 -2  0  0  0 -4
T  0 -1  0 -1 -1 -1 -1 -2 -2 -1 -1 -1 -1 -2 -1  1  5 -2 -2  0 -1 -1  0 -4
W -3 -3 -4 -4 -2 -2 -3 -2 -2 -3 -2 -3 -1  1 -4 -3 -2 11  2 -3 -4 -3 -2 -4
Y -2 -2 -2 -3 -2 -1 -2 -3  2 -1 -1 -2 -1  3 -3 -2 -2  2  7 -1 -3 -2 -1 -4
V  0 -3 -3 -3 -1 -2 -2 -3 -3  3  1 -2  1 -1 -2 -2  0 -3 -1  4 -3 -2 -1 -4
B -2 -1  3  4 -3  0  1 -1  0 -3 -4  0 -3 -3 -2  0 -1 -4 -3 -3  4  1 -1 -4
Z -1  0  0  1 -3  3  4 -2  0 -3 -3  1 -1 -3 -1  0 -1 -3 -2 -2  1  4 -1 -4
X -1 -1 -1 -1 -2 -1 -1 -1 -1 -1 -1 -1 -1 -1 -2  0  0 -2 -1 -1 -1 -1 -1 -4
* -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4  1
"""

def load_blosum62():
    labels = "A R N D C Q E G H I L K M F P S T W Y V B Z X *".split()
    matrix = {}
    for line in BLOSUM62_TEXT.strip().split('\n'):
        parts = line.split()
        row_label = parts[0]
        for col_label, score in zip(labels, parts[1:]):
            matrix[(row_label, col_label)] = int(score)
    return matrix

def parse_fasta(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    sequences = []
    for entry in content.strip().split('>'):
        if not entry.strip():
            continue
        lines = entry.strip().split('\n')
        seq = ''.join(lines[1:]).replace(' ', '').replace('\r', '')
        sequences.append(seq)
    return sequences

def solve_laff(s, t, gap_open=11, gap_ext=1):
    """
    Local alignment with affine gap penalty using Smith-Waterman + 3 DP tables.
    
    M[i][j] = best score of alignment ending with s[i-1] aligned to t[j-1]
    X[i][j] = best score of alignment ending with gap in t (s[i-1] aligned to -)
    Y[i][j] = best score of alignment ending with gap in s (t[j-1] aligned to -)
    
    Affine gap cost for a gap of length L = gap_open + gap_ext * (L - 1)
    
    Transitions (local: M can restart from 0):
      M[i][j] = max(0, M[i-1][j-1], X[i-1][j-1], Y[i-1][j-1]) + sub(s[i],t[j])
      X[i][j] = max(M[i-1][j] - gap_open, X[i-1][j] - gap_ext)
      Y[i][j] = max(M[i][j-1] - gap_open, Y[i][j-1] - gap_ext)
    """
    matrix = load_blosum62()
    m, n = len(s), len(t)
    NEG_INF = float('-inf')

    # DP tables
    M = [[0] * (n + 1) for _ in range(m + 1)]
    X = [[NEG_INF] * (n + 1) for _ in range(m + 1)]
    Y = [[NEG_INF] * (n + 1) for _ in range(m + 1)]

    # Traceback: store (state_came_from) at each (i,j,state)
    # state: 'M'=0, 'X'=1, 'Y'=2
    # trace[i][j] = (from_M, from_X, from_Y) each stores the previous state
    trace_M = [[None] * (n + 1) for _ in range(m + 1)]
    trace_X = [[None] * (n + 1) for _ in range(m + 1)]
    trace_Y = [[None] * (n + 1) for _ in range(m + 1)]

    max_score = 0
    max_i, max_j = 0, 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            sub = matrix[(s[i-1], t[j-1])]

            # Best predecessor for M — prefer continuing over restarting (M > X > Y > S)
            cand_M = M[i-1][j-1]
            cand_X = X[i-1][j-1]
            cand_Y = Y[i-1][j-1]
            best_prev = max(0, cand_M, cand_X, cand_Y)
            M[i][j] = best_prev + sub
            if M[i][j] <= 0:
                M[i][j] = 0
                trace_M[i][j] = 'S'  # start fresh (local alignment)
            elif cand_M >= cand_X and cand_M >= cand_Y and cand_M >= 0:
                trace_M[i][j] = 'M'
            elif cand_X >= cand_Y and cand_X >= 0:
                trace_M[i][j] = 'X'
            elif cand_Y >= 0:
                trace_M[i][j] = 'Y'
            else:
                trace_M[i][j] = 'S'  # all predecessors non-positive, restart

            # Best for X (gap in t)
            opt_X_from_M = M[i-1][j] - gap_open if M[i-1][j] != NEG_INF else NEG_INF
            opt_X_from_X = X[i-1][j] - gap_ext  if X[i-1][j] != NEG_INF else NEG_INF
            if opt_X_from_M >= opt_X_from_X:
                X[i][j] = opt_X_from_M
                trace_X[i][j] = 'M'
            else:
                X[i][j] = opt_X_from_X
                trace_X[i][j] = 'X'

            # Best for Y (gap in s)
            opt_Y_from_M = M[i][j-1] - gap_open if M[i][j-1] != NEG_INF else NEG_INF
            opt_Y_from_Y = Y[i][j-1] - gap_ext  if Y[i][j-1] != NEG_INF else NEG_INF
            if opt_Y_from_M >= opt_Y_from_Y:
                Y[i][j] = opt_Y_from_M
                trace_Y[i][j] = 'M'
            else:
                Y[i][j] = opt_Y_from_Y
                trace_Y[i][j] = 'Y'

            # Track best score across all states
            cur_best = max(M[i][j],
                           X[i][j] if X[i][j] != NEG_INF else 0,
                           Y[i][j] if Y[i][j] != NEG_INF else 0)
            if cur_best > max_score:
                max_score = cur_best
                max_i, max_j = i, j

    # Determine which state holds the max score
    if M[max_i][max_j] >= max_score:
        curr_state = 'M'
    elif X[max_i][max_j] >= max_score:
        curr_state = 'X'
    else:
        curr_state = 'Y'

    # Traceback
    i, j = max_i, max_j
    align_s, align_t = [], []

    while True:
        if curr_state == 'M':
            if i == 0 or j == 0 or trace_M[i][j] == 'S':
                break
            align_s.append(s[i-1])
            align_t.append(t[j-1])
            prev = trace_M[i][j]
            i -= 1
            j -= 1
            curr_state = prev
        elif curr_state == 'X':
            if i == 0:
                break
            align_s.append(s[i-1])
            align_t.append('-')
            prev = trace_X[i][j]
            i -= 1
            curr_state = prev
        elif curr_state == 'Y':
            if j == 0:
                break
            align_s.append('-')
            align_t.append(t[j-1])
            prev = trace_Y[i][j]
            j -= 1
            curr_state = prev

    align_s = ''.join(reversed(align_s))
    align_t = ''.join(reversed(align_t))

    # Extract the substrings (without gaps) for output
    sub_s = align_s.replace('-', '')
    sub_t = align_t.replace('-', '')

    return int(max_score), sub_s, sub_t

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, 'rosalind_laff.txt')
    output_path = os.path.join(script_dir, 'output.txt')

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    sequences = parse_fasta(input_path)
    if len(sequences) < 2:
        print("Error: Need at least 2 FASTA sequences.")
        return

    s, t = sequences[0], sequences[1]
    print(f"Aligning s (len={len(s)}) vs t (len={len(t)}) with gap_open=11, gap_ext=1 ...")

    score, sub_s, sub_t = solve_laff(s, t, gap_open=11, gap_ext=1)

    print(f"Score: {score}")
    print(f"s substring: {sub_s}")
    print(f"t substring: {sub_t}")

    with open(output_path, 'w') as f:
        f.write(f"{score}\n{sub_s}\n{sub_t}\n")
    print(f"Written to {output_path}")

if __name__ == '__main__':
    main()
