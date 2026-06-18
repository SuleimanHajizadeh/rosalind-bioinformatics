class LocalAlignment:
    def __init__(self):
        self.pam = self._get_pam250()

    def _get_pam250(self):
        matrix_str = """
#
# This matrix was produced by "pam" Version 1.0.6 [28-Jul-93]
#
# PAM 250 substitution matrix, scale = ln(2)/3 = 0.231049
#
# Expected score = -0.844, Entropy = 0.354 bits
#
# Lowest score = -8, Highest score = 17
#
   A  R  N  D  C  Q  E  G  H  I  L  K  M  F  P  S  T  W  Y  V  B  Z  X  *
A  2 -2  0  0 -2  0  0  1 -1 -1 -2 -1 -1 -3  1  1  1 -6 -3  0  0  0  0 -8
R -2  6  0 -1 -4  1 -1 -3  2 -2 -3  3  0 -4  0  0 -1  2 -4 -2 -1  0 -1 -8
N  0  0  2  2 -4  1  1  0  2 -2 -3  1 -2 -3  0  1  0 -4 -2 -2  2  1  0 -8
D  0 -1  2  4 -5  2  3  1  1 -2 -4  0 -3 -6 -1  0  0 -7 -4 -2  3  3 -1 -8
C -2 -4 -4 -5 12 -5 -5 -3 -3 -2 -6 -5 -5 -4 -3  0 -2 -8  0 -2 -4 -5 -3 -8
Q  0  1  1  2 -5  4  2 -1  3 -2 -2  1 -1 -5  0 -1 -1 -5 -4 -2  1  3 -1 -8
E  0 -1  1  3 -5  2  4  0  1 -2 -3  0 -2 -5 -1  0  0 -7 -4 -2  3  3 -1 -8
G  1 -3  0  1 -3 -1  0  5 -2 -3 -4 -2 -3 -5  0  1  0 -7 -5 -1  0  0 -1 -8
H -1  2  2  1 -3  3  1 -2  6 -2 -2  0 -2 -2  0 -1 -1 -3  0 -2  1  2 -1 -8
I -1 -2 -2 -2 -2 -2 -2 -3 -2  5  2 -2  2  1 -2 -1  0 -5 -1  4 -2 -2 -1 -8
L -2 -3 -3 -4 -6 -2 -3 -4 -2  2  6 -3  4  2 -3 -3 -2 -2 -1  2 -3 -3 -1 -8
K -1  3  1  0 -5  1  0 -2  0 -2 -3  5  0 -5 -1  0  0 -3 -4 -2  1  0 -1 -8
M -1  0 -2 -3 -5 -1 -2 -3 -2  2  4  0  6  0 -2 -2 -1 -4 -2  2 -2 -2 -1 -8
F -3 -4 -3 -6 -4 -5 -5 -5 -2  1  2 -5  0  9 -5 -3 -3  0  7 -1 -4 -5 -2 -8
P  1  0  0 -1 -3  0 -1  0  0 -2 -3 -1 -2 -5  6  1  0 -6 -5 -1 -1  0 -1 -8
S  1  0  1  0  0 -1  0  1 -1 -1 -3  0 -2 -3  1  2  1 -2 -3 -1  0  0  0 -8
T  1 -1  0  0 -2 -1  0  0 -1  0 -2  0 -1 -3  0  1  3 -5 -3  0  0 -1  0 -8
W -6  2 -4 -7 -8 -5 -7 -7 -3 -5 -2 -3 -4  0 -6 -2 -5 17  0 -6 -5 -6 -4 -8
Y -3 -4 -2 -4  0 -4 -4 -5  0 -1 -1 -4 -2  7 -5 -3 -3  0 10 -2 -3 -4 -2 -8
V  0 -2 -2 -2 -2 -2 -2 -1 -2  4  2 -2  2 -1 -1 -1  0 -6 -2  4 -2 -2 -1 -8
B  0 -1  2  3 -4  1  3  0  1 -2 -3  1 -2 -4 -1  0  0 -5 -3 -2  3  2 -1 -8
Z  0  0  1  3 -5  3  3  0  2 -2 -3  0 -2 -5  0  0 -1 -6 -4 -2  2  3 -1 -8
X  0 -1  0 -1 -3 -1 -1 -1 -1 -1 -1 -1 -1 -2 -1  0  0 -4 -2 -1 -1 -1 -1 -8
* -8 -8 -8 -8 -8 -8 -8 -8 -8 -8 -8 -8 -8 -8 -8 -8 -8 -8 -8 -8 -8 -8 -8  1
"""
        lines = [line.strip() for line in matrix_str.strip().split("\n") if line.strip() and not line.strip().startswith("#")]
        headers = lines[0].split()
        pam = {}
        for line in lines[1:]:
            parts = line.split()
            row_char = parts[0]
            scores = [int(x) for x in parts[1:]]
            for col_char, score in zip(headers, scores):
                pam[(row_char, col_char)] = score
        return pam

    def solve(self, s, t, gap_penalty=5):
        n = len(s)
        m = len(t)
        dp = [[0] * (m + 1) for _ in range(n + 1)]
        
        max_score = 0
        max_i, max_j = 0, 0
        
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                match_score = self.pam.get((s[i-1], t[j-1]), 0)
                score = max(
                    0,
                    dp[i-1][j-1] + match_score,
                    dp[i-1][j] - gap_penalty,
                    dp[i][j-1] - gap_penalty
                )
                dp[i][j] = score
                if score > max_score:
                    max_score = score
                    max_i = i
                    max_j = j
                    
        # Traceback
        curr_i, curr_j = max_i, max_j
        
        while curr_i > 0 and curr_j > 0 and dp[curr_i][curr_j] > 0:
            match_score = self.pam.get((s[curr_i-1], t[curr_j-1]), 0)
            if dp[curr_i][curr_j] == dp[curr_i-1][curr_j-1] + match_score:
                curr_i -= 1
                curr_j -= 1
            elif dp[curr_i][curr_j] == dp[curr_i-1][curr_j] - gap_penalty:
                curr_i -= 1
            elif dp[curr_i][curr_j] == dp[curr_i][curr_j-1] - gap_penalty:
                curr_j -= 1
            else:
                break
                
        sub_s = s[curr_i:max_i]
        sub_t = t[curr_j:max_j]
        return max_score, sub_s, sub_t

def parse_fasta(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    
    entries = content.strip().split(">")
    sequences = []
    for entry in entries:
        if not entry.strip():
            continue
        lines = entry.strip().split("\n")
        seq = "".join(lines[1:]).replace(" ", "").replace("\r", "")
        sequences.append(seq)
    return sequences

def main():
    import os
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(current_dir, "rosalind_loca.txt")
    output_path = os.path.join(current_dir, "output.txt")
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return
        
    sequences = parse_fasta(input_path)
    if len(sequences) < 2:
        print("Error: Input file must contain at least 2 FASTA sequences.")
        return
        
    s, t = sequences[0], sequences[1]
    
    aligner = LocalAlignment()
    score, sub_s, sub_t = aligner.solve(s, t, 5)
    
    print(f"Max Local Alignment Score: {score}")
    print(f"Substring of s: {sub_s}")
    print(f"Substring of t: {sub_t}")
    
    with open(output_path, "w") as f:
        f.write(f"{score}\n")
        f.write(f"{sub_s}\n")
        f.write(f"{sub_t}\n")
        
    print(f"Result successfully written to {output_path}")

if __name__ == "__main__":
    main()
