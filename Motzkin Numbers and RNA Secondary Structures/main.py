import os
import sys

# Rekursiya limitini artırırıq
sys.setrecursionlimit(2000)

def read_fasta(file_path):
    seq = ""
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line.startswith(">"):
                seq += line
    return seq

def solve_motzkin(seq):
    memo = {}
    
    # Tamamlayıcı cütlər
    pairs = {('A', 'U'), ('U', 'A'), ('G', 'C'), ('C', 'G')}
    
    def dp(i, j):
        # Əgər alt-ardıcıllıq boşdursa və ya 1 elementlidirsə, yalnız 1 cütləşmə (boş cütləşmə) var
        if i >= j:
            return 1
        if (i, j) in memo:
            return memo[(i, j)]
            
        # 1-ci Hal: seq[i] elementi heç bir cütləşmədə iştirak etmir
        ans = dp(i + 1, j)
        
        # 2-ci Hal: seq[i] elementi seq[k] ilə cütləşir (i < k <= j)
        for k in range(i + 1, j + 1):
            if (seq[i], seq[k]) in pairs:
                ans += dp(i + 1, k - 1) * dp(k + 1, j)
                ans %= 1000000
                
        memo[(i, j)] = ans
        return ans

    return dp(0, len(seq) - 1)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_motz.txt")
    
    seq = read_fasta(input_path)
    print(f"RNT ardıcıllığı uzunluğu: {len(seq)}")
    
    ans = solve_motzkin(seq)
    print(f"Mümkün strukturların sayı (modulo 1,000,000) = {ans}")
    
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        out_file.write(str(ans) + "\n")

if __name__ == "__main__":
    main()
