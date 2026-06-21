# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba5h.txt")
    if not os.path.exists(input_file):
        return "", ""
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0], lines[1]

# Fitting Alignment alqoritmini təyin edirik
# Implement Fitting Alignment: fit s2 (shorter string) into s1 (longer string)
# Match = 1, Mismatch = -1, Gap = -1
def fitting_alignment(s1, s2):
    n, m = len(s1), len(s2)
    dp = [ [0] * (m + 1) for _ in range(n + 1) ]
    
    # s2 tamamilə uyğunlaşmalıdır, ona görə s2 üçün gap cərimələri başlanğıcda təyin edilir
    # s2 must align completely, so initialize columns with gap penalties
    for j in range(1, m + 1):
        dp[0][j] = -j
    # s1-in ixtiyari yerindən başlaya bilərik, ona görə dp[i][0] = 0 olaraq qalır
    # We can start anywhere in s1, so row 0 stays 0
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 1 if s1[i-1] == s2[j-1] else -1
            dp[i][j] = max(
                dp[i-1][j-1] + cost,
                dp[i-1][j] - 1,
                dp[i][j-1] - 1
            )
            
    # dp[i][m] cərgəsindən ən böyük xalı tapırıq (s2 bitdiyi üçün)
    # Find the maximum score in the last column
    max_score = -float('inf')
    max_i = 0
    for i in range(1, n + 1):
        if dp[i][m] > max_score:
            max_score = dp[i][m]
            max_i = i
            
    # Geriyə izləmə (backtrack) aparırıq
    # Backtrack starting from (max_i, m) until j hits 0
    align1, align2 = [], []
    i, j = max_i, m
    while j > 0:
        cost = 1 if s1[i-1] == s2[j-1] else -1
        if i > 0 and dp[i][j] == dp[i-1][j-1] + cost:
            align1.append(s1[i-1])
            align2.append(s2[j-1])
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j] - 1:
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
    score, align1, align2 = fitting_alignment(s1, s2)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(str(score) + "\n")
        f.write(align1 + "\n")
        f.write(align2 + "\n")

if __name__ == "__main__":
    main()
