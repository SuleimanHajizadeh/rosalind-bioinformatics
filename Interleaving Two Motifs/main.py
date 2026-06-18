import os

def read_input(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0], lines[1]

def shortest_common_supersequence(s, t):
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
        
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1)
                
    # Backtrack to reconstruct the SCS
    scs_chars = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and s[i - 1] == t[j - 1]:
            scs_chars.append(s[i - 1])
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j - 1] < dp[i - 1][j]):
            scs_chars.append(t[j - 1])
            j -= 1
        else:
            scs_chars.append(s[i - 1])
            i -= 1
            
    return "".join(reversed(scs_chars))

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_scsp.txt")
    
    s, t = read_input(input_path)
    print(f"s sətiri: {s} (Uzunluq: {len(s)})")
    print(f"t sətiri: {t} (Uzunluq: {len(t)})")
    
    result = shortest_common_supersequence(s, t)
    print(f"Yekun SCS uzunluğu: {len(result)}")
    print(f"SCS: {result}")
    
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        out_file.write(result + "\n")

if __name__ == "__main__":
    main()
