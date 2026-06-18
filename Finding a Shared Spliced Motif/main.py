import os

def read_fasta(file_path):
    sequences = []
    current_seq = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if current_seq:
                    sequences.append("".join(current_seq))
                    current_seq = []
            else:
                current_seq.append(line)
        if current_seq:
            sequences.append("".join(current_seq))
    return sequences

def lcs(s, t):
    m, n = len(s), len(t)
    # 2D DP cədvəli yaradırıq
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                
    # LCS ardıcıllığını geriyə doğru izləyərək tapırıq
    lcs_chars = []
    i, j = m, n
    while i > 0 and j > 0:
        if s[i - 1] == t[j - 1]:
            lcs_chars.append(s[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
            
    # Tərsinə çeviririk, çünki sondan başlamışdıq
    return "".join(reversed(lcs_chars))

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_lcsq.txt")
    
    sequences = read_fasta(input_path)
    if len(sequences) < 2:
        print("Faylda ən azı 2 ardıcıllıq olmalıdır.")
        return
        
    s, t = sequences[0], sequences[1]
    result = lcs(s, t)
    
    print("Ən Uzun Ortaq Alt-ardıcıllıq (LCS) Uzunluğu:", len(result))
    print("LCS:", result)
    
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        out_file.write(result + "\n")

if __name__ == "__main__":
    main()
