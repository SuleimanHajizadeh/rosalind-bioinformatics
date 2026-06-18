import os
import sys

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

def parse_fasta(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return []
        
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
        
    seqs = []
    curr = []
    for line in lines:
        if line.startswith('>'):
            if curr:
                seqs.append("".join(curr))
                curr = []
        else:
            curr.append(line)
    if curr:
        seqs.append("".join(curr))
    return seqs

def global_alignment_with_constant_gap(v, w, scoring_matrix, sigma):
    import numpy as np
    
    # S_lower: ending in a gap in v
    # S_upper: ending in a gap in w
    # S_middle: total optimal score
    S_lower = np.full((len(v)+1, len(w)+1), -float('inf'))
    S_middle = np.full((len(v)+1, len(w)+1), -float('inf'))
    S_upper = np.full((len(v)+1, len(w)+1), -float('inf'))
    
    S_middle[0][0] = 0
    
    for i in range(1, len(v)+1):
        S_lower[i][0] = -sigma
        S_middle[i][0] = -sigma
        
    for j in range(1, len(w)+1):
        S_upper[0][j] = -sigma
        S_middle[0][j] = -sigma
        
    for i in range(1, len(v)+1):
        for j in range(1, len(w)+1):
            S_lower[i][j] = max(S_lower[i-1][j], S_middle[i-1][j] - sigma)
            S_upper[i][j] = max(S_upper[i][j-1], S_middle[i][j-1] - sigma)
            S_middle[i][j] = max(S_lower[i][j],
                                 S_middle[i-1][j-1] + scoring_matrix[(v[i-1], w[j-1])],
                                 S_upper[i][j])
            
    return S_middle[len(v)][len(w)]

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, 'rosalind_gcon.txt')
    output_path = os.path.join(base_dir, 'output.txt')
    
    seqs = parse_fasta(input_path)
    if len(seqs) < 2:
        print("Error: Expected at least 2 sequences.")
        return
        
    v, w = seqs[0], seqs[1]
    matrix = load_blosum62()
    
    score = global_alignment_with_constant_gap(v, w, matrix, 5)
    ans = int(score)
    
    with open(output_path, 'w') as f:
        f.write(str(ans) + '\n')
        
    print(f"Alignment score: {ans}")

if __name__ == '__main__':
    main()
