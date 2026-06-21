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
    'A': {'A': 4, 'R': -1, 'N': -2, 'D': -2, 'C': 0, 'Q': -1, 'E': -1, 'G': 0, 'H': -2, 'I': -1, 'L': -1, 'K': -1, 'M': -1, 'F': -2, 'P': -1, 'S': 1, 'T': 0, 'W': -3, 'Y': -2, 'V': 0},
    'R': {'A': -1, 'R': 5, 'N': 0, 'D': -2, 'C': -3, 'Q': 1, 'E': -1, 'G': -2, 'H': 0, 'I': -3, 'L': -2, 'K': 2, 'M': -1, 'F': -3, 'P': -2, 'S': -1, 'T': -1, 'W': -3, 'Y': -2, 'V': -3},
    'N': {'A': -2, 'R': 0, 'N': 6, 'D': 1, 'C': -3, 'Q': 0, 'E': 0, 'G': 0, 'H': 1, 'I': -3, 'L': -3, 'K': 0, 'M': -2, 'F': -3, 'P': -2, 'S': 1, 'T': 0, 'W': -4, 'Y': -2, 'V': -3},
    'D': {'A': -2, 'R': -2, 'N': 1, 'D': 6, 'C': -3, 'Q': 0, 'E': 2, 'G': -1, 'H': -1, 'I': -3, 'L': -4, 'K': -1, 'M': -3, 'F': -3, 'P': -1, 'S': 0, 'T': -1, 'W': -4, 'Y': -3, 'V': -3},
    'C': {'A': 0, 'R': -3, 'N': -3, 'D': -3, 'C': 9, 'Q': -3, 'E': -4, 'G': -3, 'H': -3, 'I': -1, 'L': -1, 'K': -3, 'M': -1, 'F': -2, 'P': -3, 'S': -1, 'T': -1, 'W': -2, 'Y': -2, 'V': -1},
    'Q': {'A': -1, 'R': 1, 'N': 0, 'D': 0, 'C': -3, 'Q': 5, 'E': 2, 'G': -2, 'H': 0, 'I': -3, 'L': -2, 'K': 1, 'M': 0, 'F': -3, 'P': -1, 'S': 0, 'T': -1, 'W': -2, 'Y': -1, 'V': -2},
    'E': {'A': -1, 'R': -1, 'N': 0, 'D': 2, 'C': -4, 'Q': 2, 'E': 5, 'G': -2, 'H': 0, 'I': -3, 'L': -3, 'K': 1, 'M': -2, 'F': -3, 'P': -1, 'S': 0, 'T': -1, 'W': -3, 'Y': -2, 'V': -2},
    'G': {'A': 0, 'R': -2, 'N': 0, 'D': -1, 'C': -3, 'Q': -2, 'E': -2, 'G': 6, 'H': -2, 'I': -4, 'L': -4, 'K': -2, 'M': -3, 'F': -3, 'P': -2, 'S': 0, 'T': -2, 'W': -2, 'Y': -3, 'V': -3},
    'H': {'A': -2, 'R': 0, 'N': 1, 'D': -1, 'C': -3, 'Q': 0, 'E': 0, 'G': -2, 'H': 8, 'I': -3, 'L': -3, 'K': -1, 'M': -2, 'F': -1, 'P': -2, 'S': -1, 'T': -2, 'W': -2, 'Y': 2, 'V': -3},
    'I': {'A': -1, 'R': -3, 'N': -3, 'D': -3, 'C': -1, 'Q': -3, 'E': -3, 'G': -4, 'H': -3, 'I': 4, 'L': 2, 'K': -3, 'M': 1, 'F': 0, 'P': -3, 'S': -2, 'T': -1, 'W': -3, 'Y': -1, 'V': 3},
    'L': {'A': -1, 'R': -2, 'N': -3, 'D': -4, 'C': -1, 'Q': -2, 'E': -3, 'G': -4, 'H': -3, 'I': 2, 'L': 4, 'K': -3, 'M': 2, 'F': 0, 'P': -3, 'S': -2, 'T': -1, 'W': -2, 'Y': -1, 'V': 1},
    'K': {'A': -1, 'R': 2, 'N': 0, 'D': -1, 'C': -3, 'Q': 1, 'E': 1, 'G': -2, 'H': -1, 'I': -3, 'L': -3, 'K': 5, 'M': -1, 'F': -3, 'P': -1, 'S': 0, 'T': -1, 'W': -3, 'Y': -2, 'V': -3},
    'M': {'A': -1, 'R': -1, 'N': -2, 'D': -3, 'C': -1, 'Q': 0, 'E': -2, 'G': -3, 'H': -2, 'I': 1, 'L': 2, 'K': -1, 'M': 5, 'F': 0, 'P': -2, 'S': -1, 'T': -1, 'W': -1, 'Y': -1, 'V': 1},
    'F': {'A': -2, 'R': -3, 'N': -3, 'D': -3, 'C': -2, 'Q': -3, 'E': -3, 'G': -3, 'H': -1, 'I': 0, 'L': 0, 'K': -3, 'M': 0, 'F': 6, 'P': -4, 'S': -2, 'T': -2, 'W': 1, 'Y': 3, 'V': -1},
    'P': {'A': -1, 'R': -2, 'N': -2, 'D': -1, 'C': -3, 'Q': -1, 'E': -1, 'G': -2, 'H': -2, 'I': -3, 'L': -3, 'K': -1, 'M': -2, 'F': -4, 'P': 7, 'S': -1, 'T': -1, 'W': -4, 'Y': -3, 'V': -2},
    'S': {'A': 1, 'R': -1, 'N': 1, 'D': 0, 'C': -1, 'Q': 0, 'E': 0, 'G': 0, 'H': -1, 'I': -2, 'L': -2, 'K': 0, 'M': -1, 'F': -2, 'P': -1, 'S': 4, 'T': 1, 'W': -3, 'Y': -2, 'V': 0},
    'T': {'A': 0, 'R': -1, 'N': 0, 'D': -1, 'C': -1, 'Q': -1, 'E': -1, 'G': -2, 'H': -2, 'I': -1, 'L': -1, 'K': -1, 'M': -1, 'F': -2, 'P': -1, 'S': 1, 'T': 5, 'W': -3, 'Y': -2, 'V': 0},
    'W': {'A': -3, 'R': -3, 'N': -4, 'D': -4, 'C': -2, 'Q': -2, 'E': -3, 'G': -2, 'H': -2, 'I': -3, 'L': -2, 'K': -3, 'M': -1, 'F': 1, 'P': -4, 'S': -3, 'T': -3, 'W': 11, 'Y': 2, 'V': -3},
    'Y': {'A': -2, 'R': -2, 'N': -2, 'D': -3, 'C': -2, 'Q': -1, 'E': -2, 'G': -3, 'H': 2, 'I': -1, 'L': -1, 'K': -2, 'M': -1, 'F': 3, 'P': -3, 'S': -2, 'T': -2, 'W': 2, 'Y': 7, 'V': -1},
    'V': {'A': 0, 'R': -3, 'N': -3, 'D': -3, 'C': -1, 'Q': -2, 'E': -2, 'G': -3, 'H': -3, 'I': 3, 'L': 1, 'K': -3, 'M': 1, 'F': -1, 'P': -2, 'S': 0, 'T': 0, 'W': -3, 'Y': -1, 'V': 4}
}

def space_efficient_alignment_scores(s1, s2, sigma=5):
    n, m = len(s1), len(s2)
    prev = [ -i * sigma for i in range(n + 1) ]
    curr = [ 0 for _ in range(n + 1) ]
    for j in range(1, m + 1):
        curr[0] = -j * sigma
        for i in range(1, n + 1):
            match_score = BLOSUM62[s1[i-1]][s2[j-1]]
            curr[i] = max(
                prev[i-1] + match_score,
                prev[i] - sigma,
                curr[i-1] - sigma
            )
        prev = list(curr)
    return prev

def find_middle_edge(s1, s2, sigma=5):
    n, m = len(s1), len(s2)
    mid_j = m // 2
    from_source = space_efficient_alignment_scores(s1, s2[:mid_j], sigma)
    to_sink = space_efficient_alignment_scores(s1[::-1], s2[mid_j:][::-1], sigma)
    to_sink.reverse()
    max_val = -float('inf')
    mid_i = 0
    for i in range(n + 1):
        val = from_source[i] + to_sink[i]
        if val > max_val:
            max_val = val
            mid_i = i
            
    if mid_i == n:
        next_i, next_j = mid_i, mid_j + 1
    else:
        diag = from_source[mid_i] + BLOSUM62[s1[mid_i]][s2[mid_j]] + to_sink[mid_i+1] if mid_j < m else -float('inf')
        down = from_source[mid_i] - sigma + to_sink[mid_i+1]
        right = from_source[mid_i] - sigma + to_sink[mid_i] if mid_j < m else -float('inf')
        best = max(diag, down, right)
        if best == diag:
            next_i, next_j = mid_i + 1, mid_j + 1
        elif best == down:
            next_i, next_j = mid_i + 1, mid_j
        else:
            next_i, next_j = mid_i, mid_j + 1
    return (mid_i, mid_j), (next_i, next_j)

# Hirschberg alqoritmi ilə yaddaşa qənaət edən qlobal hizalanma
# Align two strings in linear space using Hirschberg's algorithm (divide and conquer)
def linear_space_alignment(s1, s2, sigma=5):
    n, m = len(s1), len(s2)
    
    # Əsas hallar (Base cases)
    # Base cases for recursion
    if m == 0:
        return -n * sigma, s1, "-" * n
    if n == 0:
        return -m * sigma, "-" * m, s2
    if m == 1:
        # Smith-Waterman / Needleman-Wunsch standart kiçik hizalanma
        # Run standard alignment for small instances
        dp = [ [-i*sigma] for i in range(n + 1) ]
        dp[0].append(-sigma)
        for i in range(1, n + 1):
            cost = BLOSUM62[s1[i-1]][s2[0]]
            val = max(
                dp[i-1][0] + cost,
                dp[i-1][1] - sigma,
                dp[i][0] - sigma
            )
            dp[i].append(val)
        score = dp[n][1]
        
        # Hizalanmanı qururuq
        # Reconstruct path
        a1, a2 = [], []
        i, j = n, 1
        while i > 0 or j > 0:
            if i > 0 and j > 0 and dp[i][j] == dp[i-1][0] + BLOSUM62[s1[i-1]][s2[0]]:
                a1.append(s1[i-1])
                a2.append(s2[0])
                i -= 1
                j -= 1
            elif i > 0 and dp[i][j] == dp[i-1][j] - sigma:
                a1.append(s1[i-1])
                a2.append("-")
                i -= 1
            else:
                a1.append("-")
                a2.append(s2[0])
                j -= 1
        a1.reverse()
        a2.reverse()
        return score, "".join(a1), "".join(a2)
        
    # Böl və idarə et (Divide and Conquer)
    # Recursively split along the middle edge
    (mid_i, mid_j), (next_i, next_j) = find_middle_edge(s1, s2, sigma)
    
    # Sol tərəf üçün rekursiya
    # Recursion on the left half
    score_l, align1_l, align2_l = linear_space_alignment(s1[:mid_i], s2[:mid_j], sigma)
    
    # Orta tili əlavə edirik
    # Add the middle edge itself
    mid_align1 = ""
    mid_align2 = ""
    edge_score = 0
    if next_i == mid_i + 1 and next_j == mid_j + 1:
        mid_align1 = s1[mid_i]
        mid_align2 = s2[mid_j]
        edge_score = BLOSUM62[s1[mid_i]][s2[mid_j]]
    elif next_i == mid_i + 1 and next_j == mid_j:
        mid_align1 = s1[mid_i]
        mid_align2 = "-"
        edge_score = -sigma
    else:
        mid_align1 = "-"
        mid_align2 = s2[mid_j]
        edge_score = -sigma
        
    # Sağ tərəf üçün rekursiya
    # Recursion on the right half
    score_r, align1_r, align2_r = linear_space_alignment(s1[next_i:], s2[next_j:], sigma)
    
    total_score = score_l + edge_score + score_r
    return total_score, align1_l + mid_align1 + align1_r, align2_l + mid_align2 + align2_r

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
