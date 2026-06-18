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

def edit_distance(s, t):
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
        
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s[i-1] == t[j-1] else 1
            dp[i][j] = min(
                dp[i-1][j] + 1,      # Deletion
                dp[i][j-1] + 1,      # Insertion
                dp[i-1][j-1] + cost  # Substitution
            )
            
    return dp[m][n]

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_edit.txt")
    
    sequences = read_fasta(input_path)
    if len(sequences) < 2:
        print("Faylda ən azı 2 ardıcıllıq olmalıdır.")
        return
        
    s, t = sequences[0], sequences[1]
    print(f"s sətirinin uzunluğu: {len(s)}")
    print(f"t sətirinin uzunluğu: {len(t)}")
    
    dist = edit_distance(s, t)
    print(f"Edit məsafəsi (Edit Distance) = {dist}")
    
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        out_file.write(str(dist) + "\n")

if __name__ == "__main__":
    main()
