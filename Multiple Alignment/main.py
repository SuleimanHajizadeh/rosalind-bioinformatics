#!/usr/bin/env python3
import os

def read_fasta(file_path):
    sequences = []
    current_seq = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if current_seq:
                    sequences.append("".join(current_seq))
                    current_seq = []
            else:
                current_seq.append(line)
        if current_seq:
            sequences.append("".join(current_seq))
    return sequences

def solve_mult(seqs):
    s1, s2, s3, s4 = seqs
    n1, n2, n3, n4 = len(s1), len(s2), len(s3), len(s4)
    
    # 4D DP table initialized to -infinity
    dp = [[[[ -float('inf') for _ in range(n4 + 1)] 
             for _ in range(n3 + 1)] 
            for _ in range(n2 + 1)] 
           for _ in range(n1 + 1)]
    
    parent = [[[[ None for _ in range(n4 + 1)] 
                for _ in range(n3 + 1)] 
               for _ in range(n2 + 1)] 
              for _ in range(n1 + 1)]
              
    dp[0][0][0][0] = 0
    
    transitions = []
    for d1 in (0, 1):
        for d2 in (0, 1):
            for d3 in (0, 1):
                for d4 in (0, 1):
                    if d1 == 0 and d2 == 0 and d3 == 0 and d4 == 0:
                        continue
                    transitions.append((d1, d2, d3, d4))
                    
    for i1 in range(n1 + 1):
        for i2 in range(n2 + 1):
            for i3 in range(n3 + 1):
                for i4 in range(n4 + 1):
                    if i1 == 0 and i2 == 0 and i3 == 0 and i4 == 0:
                        continue
                        
                    best_score = -float('inf')
                    best_trans = None
                    
                    for d1, d2, d3, d4 in transitions:
                        p1, p2, p3, p4 = i1 - d1, i2 - d2, i3 - d3, i4 - d4
                        if p1 < 0 or p2 < 0 or p3 < 0 or p4 < 0:
                            continue
                            
                        c1 = s1[p1] if d1 else '-'
                        c2 = s2[p2] if d2 else '-'
                        c3 = s3[p3] if d3 else '-'
                        c4 = s4[p4] if d4 else '-'
                        
                        delta = 0
                        chars = [c1, c2, c3, c4]
                        for a in range(4):
                            for b in range(a + 1, 4):
                                if chars[a] != chars[b]:
                                    delta -= 1
                                    
                        score = dp[p1][p2][p3][p4] + delta
                        if score > best_score:
                            best_score = score
                            best_trans = (d1, d2, d3, d4)
                            
                    dp[i1][i2][i3][i4] = best_score
                    parent[i1][i2][i3][i4] = best_trans
                    
    curr = (n1, n2, n3, n4)
    aligned1, aligned2, aligned3, aligned4 = [], [], [], []
    
    while curr != (0, 0, 0, 0):
        d1, d2, d3, d4 = parent[curr[0]][curr[1]][curr[2]][curr[3]]
        p1, p2, p3, p4 = curr[0] - d1, curr[1] - d2, curr[2] - d3, curr[3] - d4
        
        c1 = s1[p1] if d1 else '-'
        c2 = s2[p2] if d2 else '-'
        c3 = s3[p3] if d3 else '-'
        c4 = s4[p4] if d4 else '-'
        
        aligned1.append(c1)
        aligned2.append(c2)
        aligned3.append(c3)
        aligned4.append(c4)
        
        curr = (p1, p2, p3, p4)
        
    aligned1.reverse()
    aligned2.reverse()
    aligned3.reverse()
    aligned4.reverse()
    
    return dp[n1][n2][n3][n4], "".join(aligned1), "".join(aligned2), "".join(aligned3), "".join(aligned4)

def main():
    input_path = "rosalind_mult.txt"
    output_path = "output.txt"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return
        
    seqs = read_fasta(input_path)
    if len(seqs) < 4:
        print("Error: Input file must contain at least 4 sequences in FASTA format.")
        return
        
    score, a1, a2, a3, a4 = solve_mult(seqs)
    print("Maximum Score:", score)
    print(a1)
    print(a2)
    print(a3)
    print(a4)
    
    with open(output_path, 'w') as f:
        f.write(f"{score}\n")
        f.write(f"{a1}\n")
        f.write(f"{a2}\n")
        f.write(f"{a3}\n")
        f.write(f"{a4}\n")
    print(f"Results written to {output_path}")

if __name__ == "__main__":
    main()
