# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba5m.txt")
    if not os.path.exists(input_file):
        return "", "", ""
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0], lines[1], lines[2]

# Üç sətir üçün qlobal hizalama (multiple sequence alignment)
# Find a highest-scoring multiple sequence alignment for 3 strings
# Match = 1 if all 3 match, mismatch/gap = 0
def multiple_alignment_3(s1, s2, s3):
    n, m, l = len(s1), len(s2), len(s3)
    
    # 3D DP cədvəli
    # 3D DP table
    dp = [ [ [0] * (l + 1) for _ in range(m + 1) ] for _ in range(n + 1) ]
    backtrack = [ [ [0] * (l + 1) for _ in range(m + 1) ] for _ in range(n + 1) ]
    
    # Sərhəd şərtləri (boundary values)
    # Fill DP boundaries
    for i in range(n + 1):
        for j in range(m + 1):
            for k in range(l + 1):
                if i == 0 and j == 0 and k == 0:
                    continue
                
                scores = []
                # 7 mümkün gəliş istiqaməti var:
                # There are 7 possible incoming directions:
                # 1. Diaqonal (all 3 align)
                val1 = dp[i-1][j-1][k-1] + (1 if s1[i-1] == s2[j-1] == s3[k-1] else 0) if (i > 0 and j > 0 and k > 0) else -float('inf')
                # 2. İki sətir + gap (s1 and s2 align, s3 gap)
                val2 = dp[i-1][j-1][k] if (i > 0 and j > 0) else -float('inf')
                # 3. s1 and s3 align, s2 gap
                val3 = dp[i-1][j][k-1] if (i > 0 and k > 0) else -float('inf')
                # 4. s2 and s3 align, s1 gap
                val4 = dp[i][j-1][k-1] if (j > 0 and k > 0) else -float('inf')
                # 5. s1 oxu, s2 və s3 gap
                val5 = dp[i-1][j][k] if i > 0 else -float('inf')
                # 6. s2 oxu, s1 və s3 gap
                val6 = dp[i][j-1][k] if j > 0 else -float('inf')
                # 7. s3 oxu, s1 və s2 gap
                val7 = dp[i][j][k-1] if k > 0 else -float('inf')
                
                best = max(val1, val2, val3, val4, val5, val6, val7)
                dp[i][j][k] = best
                
                # Backtrack istiqamətini saxlayırıq
                # Store backtrack step
                if best == val1:
                    backtrack[i][j][k] = 1
                elif best == val2:
                    backtrack[i][j][k] = 2
                elif best == val3:
                    backtrack[i][j][k] = 3
                elif best == val4:
                    backtrack[i][j][k] = 4
                elif best == val5:
                    backtrack[i][j][k] = 5
                elif best == val6:
                    backtrack[i][j][k] = 6
                else:
                    backtrack[i][j][k] = 7
                    
    # Hizalanmanı geriyə izləyirik
    # Backtrack 3D table
    a1, a2, a3 = [], [], []
    i, j, k = n, m, l
    while i > 0 or j > 0 or k > 0:
        d = backtrack[i][j][k]
        if d == 1:
            a1.append(s1[i-1])
            a2.append(s2[j-1])
            a3.append(s3[k-1])
            i -= 1
            j -= 1
            k -= 1
        elif d == 2:
            a1.append(s1[i-1])
            a2.append(s2[j-1])
            a3.append("-")
            i -= 1
            j -= 1
        elif d == 3:
            a1.append(s1[i-1])
            a2.append("-")
            a3.append(s3[k-1])
            i -= 1
            k -= 1
        elif d == 4:
            a1.append("-")
            a2.append(s2[j-1])
            a3.append(s3[k-1])
            j -= 1
            k -= 1
        elif d == 5:
            a1.append(s1[i-1])
            a2.append("-")
            a3.append("-")
            i -= 1
        elif d == 6:
            a1.append("-")
            a2.append(s2[j-1])
            a3.append("-")
            j -= 1
        else:
            a1.append("-")
            a2.append("-")
            a3.append(s3[k-1])
            k -= 1
            
    a1.reverse()
    a2.reverse()
    a3.reverse()
    
    return dp[n][m][l], "".join(a1), "".join(a2), "".join(a3)

def main():
    s1, s2, s3 = read_input()
    if not s1:
        return
    score, a1, a2, a3 = multiple_alignment_3(s1, s2, s3)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(str(score) + "\n")
        f.write(a1 + "\n")
        f.write(a2 + "\n")
        f.write(a3 + "\n")

if __name__ == "__main__":
    main()
