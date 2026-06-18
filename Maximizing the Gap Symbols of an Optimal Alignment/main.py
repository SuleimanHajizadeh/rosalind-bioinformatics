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

def lcs_length(s, t):
    m, n = len(s), len(t)
    if m < n:
        s, t = t, s
        m, n = n, m
        
    prev = [0] * (n + 1)
    curr = [0] * (n + 1)
    
    for i in range(1, m + 1):
        s_char = s[i-1]
        for j in range(1, n + 1):
            if s_char == t[j-1]:
                curr[j] = prev[j-1] + 1
            else:
                curr[j] = prev[j] if prev[j] > curr[j-1] else curr[j-1]
        prev, curr = curr, prev
    return prev[n]

def main():
    input_path = "rosalind_mgap.txt"
    output_path = "output.txt"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return
        
    seqs = read_fasta(input_path)
    if len(seqs) < 2:
        print("Error: Input file must contain at least two sequences in FASTA format.")
        return
        
    s = seqs[0]
    t = seqs[1]
    
    print(f"Sequence 1 length: {len(s)}")
    print(f"Sequence 2 length: {len(t)}")
    
    lcs_len = lcs_length(s, t)
    print(f"LCS length: {lcs_len}")
    
    max_gaps = len(s) + len(t) - 2 * lcs_len
    print(f"Maximum gaps: {max_gaps}")
    
    with open(output_path, 'w') as f:
        f.write(str(max_gaps) + "\n")
    print(f"Result written to {output_path}")

if __name__ == "__main__":
    main()
