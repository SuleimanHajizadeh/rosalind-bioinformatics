# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba7b.txt")
    if not os.path.exists(input_file):
        return 0, 0, []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    n = int(lines[0])
    j = int(lines[1])
    matrix = []
    for line in lines[2:]:
        matrix.append(list(map(int, line.split())))
    return n, j, matrix

# j yarpağının limb uzunluğunu (limb length) hesablayırıq
# Compute limb length of leaf j using the distance matrix
def compute_limb_length(n, j, d):
    min_length = float('inf')
    for i in range(n):
        for k in range(n):
            if i != j and k != j:
                # Limb length formulu: (D_i,j + D_j,k - D_i,k) / 2
                # Limb length formula
                length = (d[i][j] + d[j][k] - d[i][k]) // 2
                if length < min_length:
                    min_length = length
    return min_length

def main():
    n, j, d = read_input()
    if n == 0:
        return
    result = compute_limb_length(n, j, d)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(str(result) + "\n")

if __name__ == "__main__":
    main()
