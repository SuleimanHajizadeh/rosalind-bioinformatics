# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba5i.txt")
    if not os.path.exists(input_file):
        return "", ""
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0], lines[1]

# Overlap Alignment alqoritmini təyin edirik
# Implement Overlap Alignment: align suffix of s1 with prefix of s2
# Match = 1, Mismatch = -2, Gap = -2
def overlap_alignment(s1, s2):
    n, m = len(s1), len(s2)
    dp = [ [0] * (m + 1) for _ in range(n + 1) ]
    
    # s1 prefiksi ödənişsiz buraxıla bilər, ona görə birinci sütun 0-dır
    # First column is 0 as we can skip prefix of s1
    # s2 prefiksi silinərsə gap cəriməsi hesablanır
    # First row has gap penalties
    for j in range(1, m + 1):
        dp[0][j] = -2 * j
        
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 1 if s1[i-1] == s2[j-1] else -2
            dp[i][j] = max(
                dp[i-1][j-1] + cost,
                dp[i-1][j] - 2,
                dp[i][j-1] - 2
            )
            
    # Son sətirdən ən yaxşı xalı tapırıq (s1-in sonuna çatdığımız üçün)
    # Find the maximum score in the last row
    max_score = -float('inf')
    max_j = 0
    for j in range(1, m + 1):
        if dp[n][j] > max_score:
            max_score = dp[n][j]
            max_j = j
            
    # Geriyə izləmə (backtrack)
    # Backtrack starting from (n, max_j) until i or j hit 0
    align1, align2 = [], []
    i, j = n, max_j
    while i > 0 and j > 0:
        cost = 1 if s1[i-1] == s2[j-1] else -2
        if dp[i][j] == dp[i-1][j-1] + cost:
            align1.append(s1[i-1])
            align2.append(s2[j-1])
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i-1][j] - 2:
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
    score, align1, align2 = overlap_alignment(s1, s2)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(str(score) + "\n")
        f.write(align1 + "\n")
        f.write(align2 + "\n")

if __name__ == "__main__":
    main()
