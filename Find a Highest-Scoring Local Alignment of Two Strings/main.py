# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba5f.txt")
    if not os.path.exists(input_file):
        return "", ""
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0], lines[1]

# PAM250 matrisi
# PAM250 scoring matrix mapping
PAM250 = {
    'A': {'A': 2, 'R': -2, 'N': 0, 'D': 0, 'C': -2, 'Q': 0, 'E': 0, 'G': 1, 'H': -1, 'I': -1, 'L': -2, 'K': -1, 'M': -1, 'F': -3, 'P': 1, 'S': 1, 'T': 1, 'W': -6, 'Y': -3, 'V': 0},
    'R': {'A': -2, 'R': 6, 'N': 0, 'D': -1, 'C': -4, 'Q': 1, 'E': -1, 'G': -3, 'H': 2, 'I': -2, 'L': -3, 'K': 3, 'M': 0, 'F': -4, 'P': 0, 'S': 0, 'T': -1, 'W': 2, 'Y': -1, 'V': -2},
    'N': {'A': 0, 'R': 0, 'N': 2, 'D': 2, 'C': -4, 'Q': 1, 'E': 1, 'G': 0, 'H': 2, 'I': -2, 'L': -3, 'K': 1, 'M': -2, 'F': -4, 'P': 0, 'S': 1, 'T': 0, 'W': -4, 'Y': -2, 'V': -2},
    'D': {'A': 0, 'R': -1, 'N': 2, 'D': 4, 'C': -5, 'Q': 2, 'E': 3, 'G': 0, 'H': 1, 'I': -2, 'L': -4, 'K': 0, 'M': -3, 'F': -5, 'P': -1, 'S': 0, 'T': 0, 'W': -7, 'Y': -4, 'V': -2},
    'C': {'A': -2, 'R': -4, 'N': -4, 'D': -5, 'C': 12, 'Q': -5, 'E': -5, 'G': -3, 'H': -3, 'I': -2, 'L': -6, 'K': -5, 'M': -5, 'F': -4, 'P': -3, 'S': 0, 'T': -2, 'W': -8, 'Y': 0, 'V': -2},
    'Q': {'A': 0, 'R': 1, 'N': 1, 'D': 2, 'C': -5, 'Q': 4, 'E': 2, 'G': -1, 'H': 3, 'I': -2, 'L': -2, 'K': 1, 'M': -1, 'F': -5, 'P': 0, 'S': -1, 'T': -1, 'W': -5, 'Y': -4, 'V': -2},
    'E': {'A': 0, 'R': -1, 'N': 1, 'D': 3, 'C': -5, 'Q': 2, 'E': 4, 'G': 0, 'H': 1, 'I': -2, 'L': -3, 'K': 0, 'M': -2, 'F': -5, 'P': -1, 'S': 0, 'T': 0, 'W': -7, 'Y': -4, 'V': -2},
    'G': {'A': 1, 'R': -3, 'N': 0, 'D': 0, 'C': -3, 'Q': -1, 'E': 0, 'G': 5, 'H': -2, 'I': -3, 'L': -4, 'K': -2, 'M': -3, 'F': -5, 'P': 0, 'S': 1, 'T': 0, 'W': -7, 'Y': -5, 'V': -1},
    'H': {'A': -1, 'R': 2, 'N': 2, 'D': 1, 'C': -3, 'Q': 3, 'E': 1, 'G': -2, 'H': 6, 'I': -2, 'L': -2, 'K': 0, 'M': -2, 'F': -2, 'P': 0, 'S': -1, 'T': -1, 'W': -3, 'Y': 0, 'V': -2},
    'I': {'A': -1, 'R': -2, 'N': -2, 'D': -2, 'C': -2, 'Q': -2, 'E': -2, 'G': -3, 'H': -2, 'I': 5, 'L': 2, 'K': -2, 'M': 2, 'F': 1, 'P': -2, 'S': -1, 'T': 0, 'W': -5, 'Y': -1, 'V': 4},
    'L': {'A': -2, 'R': -3, 'N': -3, 'D': -4, 'C': -6, 'Q': -2, 'E': -3, 'G': -4, 'H': -2, 'I': 2, 'L': 6, 'K': -3, 'M': 4, 'F': 2, 'P': -3, 'S': -3, 'T': -2, 'W': -2, 'Y': -1, 'V': 2},
    'K': {'A': -1, 'R': 3, 'N': 1, 'D': 0, 'C': -5, 'Q': 1, 'E': 0, 'G': -2, 'H': 0, 'I': -2, 'L': -3, 'K': 5, 'M': 0, 'F': -5, 'P': -1, 'S': 0, 'T': 0, 'W': -3, 'Y': -4, 'V': -2},
    'M': {'A': -1, 'R': 0, 'N': -2, 'D': -3, 'C': -5, 'Q': -1, 'E': -2, 'G': -3, 'H': -2, 'I': 2, 'L': 4, 'K': 0, 'M': 6, 'F': 2, 'P': -2, 'S': -2, 'T': -1, 'W': -4, 'Y': -2, 'V': 2},
    'F': {'A': -3, 'R': -4, 'N': -4, 'D': -5, 'C': -4, 'Q': -5, 'E': -5, 'G': -5, 'H': -2, 'I': 1, 'L': 2, 'K': -5, 'M': 2, 'F': 9, 'P': -5, 'S': -3, 'T': -3, 'W': 0, 'Y': 7, 'V': -1},
    'P': {'A': 1, 'R': 0, 'N': 0, 'D': -1, 'C': -3, 'Q': 0, 'E': -1, 'G': 0, 'H': 0, 'I': -2, 'L': -3, 'K': -1, 'M': -2, 'F': -5, 'P': 6, 'S': 1, 'T': 0, 'W': -6, 'Y': -5, 'V': -1},
    'S': {'A': 1, 'R': 0, 'N': 1, 'D': 0, 'C': 0, 'Q': -1, 'E': 0, 'G': 1, 'H': -1, 'I': -1, 'L': -3, 'K': 0, 'M': -2, 'F': -3, 'P': 1, 'S': 2, 'T': 1, 'W': -2, 'Y': -3, 'V': -1},
    'T': {'A': 1, 'R': -1, 'N': 0, 'D': 0, 'C': -2, 'Q': -1, 'E': 0, 'G': 0, 'H': -1, 'I': 0, 'L': -2, 'K': 0, 'M': -1, 'F': -3, 'P': 0, 'S': 1, 'T': 3, 'W': -5, 'Y': -3, 'V': 0},
    'W': {'A': -6, 'R': 2, 'N': -4, 'D': -7, 'C': -8, 'Q': -5, 'E': -7, 'G': -7, 'H': -3, 'I': -5, 'L': -2, 'K': -3, 'M': -4, 'F': 0, 'P': -6, 'S': -2, 'T': -5, 'W': 17, 'Y': 0, 'V': -6},
    'Y': {'A': -3, 'R': -1, 'N': -2, 'D': -4, 'C': 0, 'Q': -4, 'E': -4, 'G': -5, 'H': 0, 'I': -1, 'L': -1, 'K': -4, 'M': -2, 'F': 7, 'P': -5, 'S': -3, 'T': -3, 'W': 0, 'Y': 10, 'V': -2},
    'V': {'A': 0, 'R': -2, 'N': -2, 'D': -2, 'C': -2, 'Q': -2, 'E': -2, 'G': -1, 'H': -2, 'I': 4, 'L': 2, 'K': -2, 'M': 2, 'F': -1, 'P': -1, 'S': -1, 'T': 0, 'W': -6, 'Y': -2, 'V': 4}
}

# Smith-Waterman lokal hizalama alqoritmi
# Implement local alignment using Smith-Waterman with sigma = 5 gap penalty and PAM250
def local_alignment(s1, s2):
    sigma = 5
    n, m = len(s1), len(s2)
    dp = [ [0] * (m + 1) for _ in range(n + 1) ]
    
    max_score = 0
    max_pos = (0, 0)
    
    # DP cədvəlini doldururuq (lokal olduqda 0-dan aşağı düşmür)
    # Fill DP table (local score is at least 0)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match_score = PAM250[s1[i-1]][s2[j-1]]
            dp[i][j] = max(
                0,
                dp[i-1][j-1] + match_score,
                dp[i-1][j] - sigma,
                dp[i][j-1] - sigma
            )
            if dp[i][j] > max_score:
                max_score = dp[i][j]
                max_pos = (i, j)
                
    # Ən yüksək xallı mövqedən geriyə izləmə aparırıq
    # Backtrack starting from max score position down to any 0 score cell
    align1, align2 = [], []
    i, j = max_pos
    while i > 0 and j > 0 and dp[i][j] > 0:
        match_score = PAM250[s1[i-1]][s2[j-1]]
        if dp[i][j] == dp[i-1][j-1] + match_score:
            align1.append(s1[i-1])
            align2.append(s2[j-1])
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i-1][j] - sigma:
            align1.append(s1[i-1])
            align2.append("-")
            i -= 1
        else:
            align1.append("-")
            align2.append(s2[j-1])
            j -= 1
            
    align1.reverse()
    align2.reverse()
    
    return max_score, "".join(align1), "".join(align2)

def main():
    s1, s2 = read_input()
    if not s1:
        return
    score, align1, align2 = local_alignment(s1, s2)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(str(score) + "\n")
        f.write(align1 + "\n")
        f.write(align2 + "\n")

if __name__ == "__main__":
    main()
