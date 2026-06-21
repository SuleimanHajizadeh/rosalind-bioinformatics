# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba5b.txt")
    if not os.path.exists(input_file):
        return 0, 0, [], []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    n, m = map(int, lines[0].split())
    
    # Cənub matrisini (down edges) oxuyuruq
    # Parse down (Southward) edges
    down = []
    for i in range(1, n + 1):
        down.append(list(map(int, lines[i].split())))
        
    # Şərq matrisini (right edges) oxuyuruq
    # Parse right (Eastward) edges
    right = []
    for i in range(n + 2, n + 2 + n + 1):
        right.append(list(map(int, lines[i].split())))
    return n, m, down, right

# Manhetten şəbəkəsində ən uzun yolun uzunluğunu tapırıq
# Find the length of a longest path in a Manhattan-like grid
def manhattan_tourist(n, m, down, right):
    dp = [ [0] * (m + 1) for _ in range(n + 1) ]
    
    # Birinci sütun
    # Initialize the first column
    for i in range(1, n + 1):
        dp[i][0] = dp[i-1][0] + down[i-1][0]
        
    # Birinci sətir
    # Initialize the first row
    for j in range(1, m + 1):
        dp[0][j] = dp[0][j-1] + right[0][j-1]
        
    # Dinamik proqramlaşdırma ilə digər hücrələri doldururuq
    # Fill remaining DP table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = max(dp[i-1][j] + down[i-1][j], dp[i][j-1] + right[i][j-1])
            
    return dp[n][m]

def main():
    n, m, down, right = read_input()
    if n == 0:
        return
    result = manhattan_tourist(n, m, down, right)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(str(result) + "\n")

if __name__ == "__main__":
    main()
