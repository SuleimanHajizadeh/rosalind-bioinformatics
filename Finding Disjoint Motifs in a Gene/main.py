import os

def read_input(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    if not lines:
        raise ValueError("Input file is empty")
    s = lines[0]
    patterns = lines[1:]
    return s, patterns

def can_interweave(s, t, u):
    len_s = len(s)
    len_t = len(t)
    len_u = len(u)
    
    # dp_prev[i][j] will be True if a valid interweaving of prefixes t[:i] and u[:j]
    # can end at the previous character of s.
    dp_prev = [[False] * (len_u + 1) for _ in range(len_t + 1)]
    dp_prev[0][0] = True
    
    for p in range(1, len_s + 1):
        dp_curr = [[False] * (len_u + 1) for _ in range(len_t + 1)]
        dp_curr[0][0] = True  # We can always start a new match at any character
        
        char = s[p - 1]
        for i in range(len_t + 1):
            for j in range(len_u + 1):
                if i == 0 and j == 0:
                    continue
                match_t = False
                if i > 0 and char == t[i - 1]:
                    match_t = dp_prev[i - 1][j]
                match_u = False
                if j > 0 and char == u[j - 1]:
                    match_u = dp_prev[i][j - 1]
                dp_curr[i][j] = match_t or match_u
                
        # If we successfully matched the full patterns t and u, we are done
        if dp_curr[len_t][len_u]:
            return True
        dp_prev = dp_curr
        
    return False

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_itwv.txt")
    
    print(f"Reading input from: {input_path}")
    s, patterns = read_input(input_path)
    print(f"String s length: {len(s)}")
    print(f"Number of patterns n: {len(patterns)}")
    
    n = len(patterns)
    M = [[0] * n for _ in range(n)]
    
    # Fill the matrix, leveraging symmetry (M[i][j] == M[j][i])
    for i in range(n):
        for j in range(i, n):
            res = 1 if can_interweave(s, patterns[i], patterns[j]) else 0
            M[i][j] = res
            M[j][i] = res
            
    print("Computed interweaving matrix:")
    for row in M:
        print(" ".join(map(str, row)))
        
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        for row in M:
            out_file.write(" ".join(map(str, row)) + "\n")
            
    print(f"Results successfully written to: {output_path}")

if __name__ == "__main__":
    main()
