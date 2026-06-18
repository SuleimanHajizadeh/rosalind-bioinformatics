import os
import sys

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

def solve_ctea(input_path, output_path):
    seqs = parse_fasta(input_path)
    if len(seqs) < 2:
        print("Error: Expected at least 2 sequences in the input file.")
        return
        
    s, t = seqs[0], seqs[1]
    print(f"Sequence 1 length: {len(s)}")
    print(f"Sequence 2 length: {len(t)}")
    
    M, N = len(s), len(t)
    MOD = 134217727
    
    # dp[i][j] stores the edit distance of s[0:i] and t[0:j]
    dp = [[0] * (N + 1) for _ in range(M + 1)]
    # paths[i][j] stores the count of optimal alignments of s[0:i] and t[0:j]
    paths = [[0] * (N + 1) for _ in range(M + 1)]
    
    # Base cases
    for i in range(M + 1):
        dp[i][0] = i
        paths[i][0] = 1
    for j in range(N + 1):
        dp[0][j] = j
        paths[0][j] = 1
        
    for i in range(1, M + 1):
        for j in range(1, N + 1):
            cost = 0 if s[i-1] == t[j-1] else 1
            
            diag = dp[i-1][j-1] + cost
            up = dp[i-1][j] + 1
            left = dp[i][j-1] + 1
            
            min_val = min(diag, up, left)
            dp[i][j] = min_val
            
            p_val = 0
            if min_val == diag:
                p_val = (p_val + paths[i-1][j-1]) % MOD
            if min_val == up:
                p_val = (p_val + paths[i-1][j]) % MOD
            if min_val == left:
                p_val = (p_val + paths[i][j-1]) % MOD
                
            paths[i][j] = p_val
            
    ans = paths[M][N]
    print(f"Edit Distance: {dp[M][N]}")
    print(f"Number of optimal alignments: {ans}")
    
    with open(output_path, 'w') as f:
        f.write(str(ans) + '\n')
        
    print(f"Result written to {output_path}")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ctea.txt")
    output_file = os.path.join(script_dir, "output.txt")
    solve_ctea(input_file, output_file)
