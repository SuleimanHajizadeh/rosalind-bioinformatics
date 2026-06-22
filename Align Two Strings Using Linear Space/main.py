# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba5l.txt")
    if not os.path.exists(input_file):
        return "", ""
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0], lines[1]

BLOSUM62 = {
    'A': {'A': 4, 'C': 0, 'D': -2, 'E': -1, 'F': -2, 'G': 0, 'H': -2, 'I': -1, 'K': -1, 'L': -1, 'M': -1, 'N': -2, 'P': -1, 'Q': -1, 'R': -1, 'S': 1, 'T': 0, 'V': 0, 'W': -3, 'Y': -2},
    'C': {'A': 0, 'C': 9, 'D': -3, 'E': -4, 'F': -2, 'G': -3, 'H': -3, 'I': -1, 'K': -3, 'L': -1, 'M': -1, 'N': -3, 'P': -3, 'Q': -3, 'R': -3, 'S': -1, 'T': -1, 'V': -1, 'W': -2, 'Y': -2},
    'D': {'A': -2, 'C': -3, 'D': 6, 'E': 2, 'F': -3, 'G': -1, 'H': -1, 'I': -3, 'K': -1, 'L': -4, 'M': -3, 'N': 1, 'P': -1, 'Q': 0, 'R': -2, 'S': 0, 'T': -1, 'V': -3, 'W': -4, 'Y': -3},
    'E': {'A': -1, 'C': -4, 'D': 2, 'E': 5, 'F': -3, 'G': -2, 'H': 0, 'I': -3, 'K': 1, 'L': -3, 'M': -2, 'N': 0, 'P': -1, 'Q': 2, 'R': 0, 'S': 0, 'T': -1, 'V': -2, 'W': -3, 'Y': -2},
    'F': {'A': -2, 'C': -2, 'D': -3, 'E': -3, 'F': 6, 'G': -3, 'H': -1, 'I': 0, 'K': -3, 'L': 0, 'M': 0, 'N': -3, 'P': -4, 'Q': -3, 'R': -3, 'S': -2, 'T': -2, 'V': -1, 'W': 1, 'Y': 3},
    'G': {'A': 0, 'C': -3, 'D': -1, 'E': -2, 'F': -3, 'G': 6, 'H': -2, 'I': -4, 'K': -2, 'L': -4, 'M': -3, 'N': 0, 'P': -2, 'Q': -2, 'R': -2, 'S': 0, 'T': -2, 'V': -3, 'W': -2, 'Y': -3},
    'H': {'A': -2, 'C': -3, 'D': -1, 'E': 0, 'F': -1, 'G': -2, 'H': 8, 'I': -3, 'K': -1, 'L': -3, 'M': -2, 'N': 1, 'P': -2, 'Q': 0, 'R': 0, 'S': -1, 'T': -2, 'V': -3, 'W': -2, 'Y': 2},
    'I': {'A': -1, 'C': -1, 'D': -3, 'E': -3, 'F': 0, 'G': -4, 'H': -3, 'I': 4, 'K': -3, 'L': 2, 'M': 1, 'N': -3, 'P': -3, 'Q': -3, 'R': -3, 'S': -2, 'T': -1, 'V': 3, 'W': -3, 'Y': -1},
    'K': {'A': -1, 'C': -3, 'D': -1, 'E': 1, 'F': -3, 'G': -2, 'H': -1, 'I': -3, 'K': 5, 'L': -2, 'M': -1, 'N': 0, 'P': -1, 'Q': 1, 'R': 2, 'S': 0, 'T': -1, 'V': -2, 'W': -3, 'Y': -2},
    'L': {'A': -1, 'C': -1, 'D': -4, 'E': -3, 'F': 0, 'G': -4, 'H': -3, 'I': 2, 'K': -2, 'L': 4, 'M': 2, 'N': -3, 'P': -3, 'Q': -2, 'R': -2, 'S': -2, 'T': -1, 'V': 1, 'W': -2, 'Y': -1},
    'M': {'A': -1, 'C': -1, 'D': -3, 'E': -2, 'F': 0, 'G': -3, 'H': -2, 'I': 1, 'K': -1, 'L': 2, 'M': 5, 'N': -2, 'P': -2, 'Q': 0, 'R': -1, 'S': -1, 'T': -1, 'V': 1, 'W': -1, 'Y': -1},
    'N': {'A': -2, 'C': -3, 'D': 1, 'E': 0, 'F': -3, 'G': 0, 'H': 1, 'I': -3, 'K': 0, 'L': -3, 'M': -2, 'N': 6, 'P': -2, 'Q': 0, 'R': 0, 'S': 1, 'T': 0, 'V': -3, 'W': -4, 'Y': -2},
    'P': {'A': -1, 'C': -3, 'D': -1, 'E': -1, 'F': -4, 'G': -2, 'H': -2, 'I': -3, 'K': -1, 'L': -3, 'M': -2, 'N': -2, 'P': 7, 'Q': -1, 'R': -2, 'S': -1, 'T': -1, 'V': -2, 'W': -4, 'Y': -3},
    'Q': {'A': -1, 'C': -3, 'D': 0, 'E': 2, 'F': -3, 'G': -2, 'H': 0, 'I': -3, 'K': 1, 'L': -2, 'M': 0, 'N': 0, 'P': -1, 'Q': 5, 'R': 1, 'S': 0, 'T': -1, 'V': -2, 'W': -2, 'Y': -1},
    'R': {'A': -1, 'C': -3, 'D': -2, 'E': 0, 'F': -3, 'G': -2, 'H': 0, 'I': -3, 'K': 2, 'L': -2, 'M': -1, 'N': 0, 'P': -2, 'Q': 1, 'R': 5, 'S': -1, 'T': -1, 'V': -3, 'W': -3, 'Y': -2},
    'S': {'A': 1, 'C': -1, 'D': 0, 'E': 0, 'F': -2, 'G': 0, 'H': -1, 'I': -2, 'K': 0, 'L': -2, 'M': -1, 'N': 1, 'P': -1, 'Q': 0, 'R': -1, 'S': 4, 'T': 1, 'V': -2, 'W': -3, 'Y': -2},
    'T': {'A': 0, 'C': -1, 'D': -1, 'E': -1, 'F': -2, 'G': -2, 'H': -2, 'I': -1, 'K': -1, 'L': -1, 'M': -1, 'N': 0, 'P': -1, 'Q': -1, 'R': -1, 'S': 1, 'T': 5, 'V': 0, 'W': -2, 'Y': -2},
    'V': {'A': 0, 'C': -1, 'D': -3, 'E': -2, 'F': -1, 'G': -3, 'H': -3, 'I': 3, 'K': -2, 'L': 1, 'M': 1, 'N': -3, 'P': -2, 'Q': -2, 'R': -3, 'S': -2, 'T': 0, 'V': 4, 'W': -3, 'Y': -1},
    'W': {'A': -3, 'C': -2, 'D': -4, 'E': -3, 'F': 1, 'G': -2, 'H': -2, 'I': -3, 'K': -3, 'L': -2, 'M': -1, 'N': -4, 'P': -4, 'Q': -2, 'R': -3, 'S': -3, 'T': -2, 'V': -3, 'W': 11, 'Y': 2},
    'Y': {'A': -2, 'C': -2, 'D': -3, 'E': -2, 'F': 3, 'G': -3, 'H': 2, 'I': -1, 'K': -2, 'L': -1, 'M': -1, 'N': -2, 'P': -3, 'Q': -1, 'R': -2, 'S': -2, 'T': -2, 'V': -1, 'W': 2, 'Y': 7}
}

# Convert BLOSUM62 to an indexed scoring lookup matrix
ALPHABET = "ARNDCQEGHILKMFPSTWYV"
char_to_idx = {c: i for i, c in enumerate(ALPHABET)}

# Pre-build a 2D array for scoring
score_matrix = [[0]*20 for _ in range(20)]
for c1, row in BLOSUM62.items():
    for c2, val in row.items():
        if c1 in char_to_idx and c2 in char_to_idx:
            score_matrix[char_to_idx[c1]][char_to_idx[c2]] = val

def space_efficient_alignment_scores(s1_idx, s2_idx, sigma=5):
    n, m = len(s1_idx), len(s2_idx)
    prev = [ -i * sigma for i in range(n + 1) ]
    curr = [ 0 ] * (n + 1)
    for j in range(1, m + 1):
        curr[0] = -j * sigma
        s2_char_idx = s2_idx[j-1]
        row = score_matrix[s2_char_idx]
        for i in range(1, n + 1):
            match_score = row[s1_idx[i-1]]
            val_diag = prev[i-1] + match_score
            val_down = prev[i] - sigma
            val_right = curr[i-1] - sigma
            
            if val_diag > val_down:
                if val_diag > val_right:
                    curr[i] = val_diag
                else:
                    curr[i] = val_right
            else:
                if val_down > val_right:
                    curr[i] = val_down
                else:
                    curr[i] = val_right
        prev = curr[:]
    return prev

def align_small(v, w, sigma=5):
    n, m = len(v), len(w)
    dp = [ [0]*(m+1) for _ in range(n+1) ]
    for i in range(n+1):
        dp[i][0] = -i * sigma
    for j in range(m+1):
        dp[0][j] = -j * sigma
        
    for i in range(1, n+1):
        for j in range(1, m+1):
            match_score = score_matrix[v[i-1]][w[j-1]]
            dp[i][j] = max(
                dp[i-1][j-1] + match_score,
                dp[i-1][j] - sigma,
                dp[i][j-1] - sigma
            )
            
    # Traceback
    align1, align2 = [], []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + score_matrix[v[i-1]][w[j-1]]:
            align1.append(ALPHABET[v[i-1]])
            align2.append(ALPHABET[w[j-1]])
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] - sigma:
            align1.append(ALPHABET[v[i-1]])
            align2.append("-")
            i -= 1
        else:
            align1.append("-")
            align2.append(ALPHABET[w[j-1]])
            j -= 1
            
    align1.reverse()
    align2.reverse()
    return "".join(align1), "".join(align2)

def linear_space_alignment_rec(s1_idx, s2_idx, top, bottom, left, right, sigma=5):
    if right - left <= 1 or bottom - top <= 1:
        return align_small(s1_idx[top:bottom], s2_idx[left:right], sigma)
        
    mid_j_rel = (right - left) // 2
    middle = left + mid_j_rel
    
    from_source = space_efficient_alignment_scores(s1_idx[top:bottom], s2_idx[left:middle], sigma)
    to_sink = space_efficient_alignment_scores(s1_idx[top:bottom][::-1], s2_idx[middle:right][::-1], sigma)
    to_sink.reverse()
    
    max_val = -float('inf')
    mid_i_rel = 0
    for i in range(bottom - top + 1):
        val = from_source[i] + to_sink[i]
        if val > max_val:
            max_val = val
            mid_i_rel = i
            
    midNode = top + mid_i_rel
    
    align1_l, align2_l = linear_space_alignment_rec(s1_idx, s2_idx, top, midNode, left, middle, sigma)
    align1_r, align2_r = linear_space_alignment_rec(s1_idx, s2_idx, midNode, bottom, middle, right, sigma)
    
    return align1_l + align1_r, align2_l + align2_r

def linear_space_alignment(s1, s2, sigma=5):
    s1_idx = [char_to_idx[c] for c in s1]
    s2_idx = [char_to_idx[c] for c in s2]
    
    align1, align2 = linear_space_alignment_rec(s1_idx, s2_idx, 0, len(s1), 0, len(s2), sigma)
    
    # Calculate score from alignment
    score = 0
    for c1, c2 in zip(align1, align2):
        if c1 == "-" or c2 == "-":
            score -= sigma
        else:
            score += BLOSUM62[c1][c2]
            
    return score, align1, align2

def main():
    s1, s2 = read_input()
    if not s1:
        return
    score, align1, align2 = linear_space_alignment(s1, s2)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(str(score) + "\n")
        f.write(align1 + "\n")
        f.write(align2 + "\n")

if __name__ == "__main__":
    main()
