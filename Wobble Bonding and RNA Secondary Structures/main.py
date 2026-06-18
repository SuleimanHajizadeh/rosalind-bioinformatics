import os
import sys

def solve_rnas(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} not found.")
        return
        
    with open(input_path, 'r') as f:
        s = f.read().strip()
        
    print(f"RNA String length: {len(s)}")
    
    valid_pairs = {('A', 'U'), ('U', 'A'), ('C', 'G'), ('G', 'C'), ('U', 'G'), ('G', 'U')}
    
    memo = {}
    
    def count_matchings(i, j):
        if j - i < 4:
            return 1
        if (i, j) in memo:
            return memo[(i, j)]
            
        # Option 1: s[j] is unpaired
        res = count_matchings(i, j - 1)
        
        # Option 2: s[j] is paired with s[k] for k in [i, j - 4]
        for k in range(i, j - 3):
            if (s[k], s[j]) in valid_pairs:
                res += count_matchings(i, k - 1) * count_matchings(k + 1, j - 1)
                
        memo[(i, j)] = res
        return res
        
    total_matchings = count_matchings(0, len(s) - 1)
    print(f"Total valid matchings: {total_matchings}")
    
    with open(output_path, 'w') as f:
        f.write(str(total_matchings) + '\n')
        
    print(f"Result written to {output_path}")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_rnas.txt")
    output_file = os.path.join(script_dir, "output.txt")
    solve_rnas(input_file, output_file)
