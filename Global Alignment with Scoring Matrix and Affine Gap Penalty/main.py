#!/usr/bin/env python3
import os
import sys

# Increase recursion depth just in case
sys.setrecursionlimit(20000)

blosum62_text = """
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
    lines = [line.strip() for line in blosum62_text.strip().split('\n') if line.strip()]
    labels = "A R N D C Q E G H I L K M F P S T W Y V B Z X *".split()
    matrix = {}
    for line in lines:
        parts = line.split()
        row_label = parts[0]
        scores = [int(x) for x in parts[1:]]
        for col_label, score in zip(labels, scores):
            matrix[(row_label, col_label)] = score
    return matrix

def solve_gaff(s, t, a, b):
    matrix = load_blosum62()
    m, n = len(s), len(t)
    
    # Initialize DP tables
    M = [[float('-inf')] * (n + 1) for _ in range(m + 1)]
    X = [[float('-inf')] * (n + 1) for _ in range(m + 1)]
    Y = [[float('-inf')] * (n + 1) for _ in range(m + 1)]
    
    M[0][0] = 0
    
    # Base cases for X (gap in t, meaning s is aligned with gaps)
    for i in range(1, m + 1):
        X[i][0] = -a - b * (i - 1)
        
    # Base cases for Y (gap in s, meaning t is aligned with gaps)
    for j in range(1, n + 1):
        Y[0][j] = -a - b * (j - 1)
        
    # Fill tables
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            score_match = matrix[(s[i-1], t[j-1])]
            
            # Update M
            M[i][j] = score_match + max(M[i-1][j-1], X[i-1][j-1], Y[i-1][j-1])
            
            # Update X (gap in t, s[i] matched to -)
            X[i][j] = max(M[i-1][j] - a, X[i-1][j] - b)
            
            # Update Y (gap in s, t[j] matched to -)
            Y[i][j] = max(M[i][j-1] - a, Y[i][j-1] - b)
            
    # Find max score and end state
    max_score = max(M[m][n], X[m][n], Y[m][n])
    if max_score == M[m][n]:
        curr_state = 'M'
    elif max_score == X[m][n]:
        curr_state = 'X'
    else:
        curr_state = 'Y'
        
    # Backtracking
    i, j = m, n
    align_s, align_t = [], []
    
    while i > 0 or j > 0:
        if curr_state == 'M':
            align_s.append(s[i-1])
            align_t.append(t[j-1])
            score_match = matrix[(s[i-1], t[j-1])]
            if M[i][j] == score_match + M[i-1][j-1]:
                curr_state = 'M'
            elif M[i][j] == score_match + X[i-1][j-1]:
                curr_state = 'X'
            elif M[i][j] == score_match + Y[i-1][j-1]:
                curr_state = 'Y'
            else:
                raise ValueError("Reconstruction error in state M")
            i -= 1
            j -= 1
        elif curr_state == 'X':
            align_s.append(s[i-1])
            align_t.append('-')
            if X[i][j] == M[i-1][j] - a:
                curr_state = 'M'
            elif X[i][j] == X[i-1][j] - b:
                curr_state = 'X'
            else:
                if j == 0 and X[i][0] == -a - b * (i - 1):
                    curr_state = 'M'
                else:
                    raise ValueError("Reconstruction error in state X")
            i -= 1
        elif curr_state == 'Y':
            align_s.append('-')
            align_t.append(t[j-1])
            if Y[i][j] == M[i][j-1] - a:
                curr_state = 'M'
            elif Y[i][j] == Y[i][j-1] - b:
                curr_state = 'Y'
            else:
                if i == 0 and Y[0][j] == -a - b * (j - 1):
                    curr_state = 'M'
                else:
                    raise ValueError("Reconstruction error in state Y")
            j -= 1
            
    align_s = "".join(reversed(align_s))
    align_t = "".join(reversed(align_t))
    
    return int(max_score), align_s, align_t

def parse_fasta(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
        
    fasta = []
    current_seq = []
    for line in lines:
        if line.startswith('>'):
            if current_seq:
                fasta.append("".join(current_seq))
                current_seq = []
        else:
            current_seq.append(line)
    if current_seq:
        fasta.append("".join(current_seq))
    return fasta

def main():
    input_path = "rosalind_gaff.txt"
    output_path = "output.txt"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return
        
    fasta = parse_fasta(input_path)
    if len(fasta) < 2:
        print("Error: FASTA file must contain at least 2 sequences.")
        return
        
    s, t = fasta[0], fasta[1]
    a = 11
    b = 1
    
    print(f"Aligning string 1 (length {len(s)}) and string 2 (length {len(t)})")
    score, align_s, align_t = solve_gaff(s, t, a, b)
    
    print(f"Maximum alignment score: {score}")
    
    with open(output_path, "w") as f:
        f.write(f"{score}\n")
        f.write(f"{align_s}\n")
        f.write(f"{align_t}\n")
        
    print(f"Results written to {output_path}")

if __name__ == "__main__":
    main()
