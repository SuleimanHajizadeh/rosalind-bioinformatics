# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba7a.txt")
    if not os.path.exists(input_file):
        return 0, {}
    adj = {}
    n = 0
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    n = int(lines[0])
    for line in lines[1:]:
        parts = line.split("->")
        u = int(parts[0])
        v, w = map(int, parts[1].split(":"))
        if u not in adj:
            adj[u] = []
        adj[u].append((v, w))
    return n, adj

# Yarpaqlar arasındakı məsafəni DFS/BFS vasitəsilə tapırıq
# Compute distances between leaves in a tree
def compute_leaf_distances(n, adj):
    dist_matrix = [ [0] * n for _ in range(n) ]
    
    # DFS ilə hər bir yarpaqdan digərlərinə olan məsafəni tapırıq
    # Run DFS from each leaf to find distance to all other leaves
    def dfs(start, curr, parent, d):
        if curr < n:
            dist_matrix[start][curr] = d
        if curr in adj:
            for neighbor, weight in adj[curr]:
                if neighbor != parent:
                    dfs(start, neighbor, curr, d + weight)
                    
    for i in range(n):
        dfs(i, i, -1, 0)
        
    return dist_matrix

def main():
    n, adj = read_input()
    if n == 0:
        return
    matrix = compute_leaf_distances(n, adj)
    
    # Nəticəni matris şəklində formatlayırıq
    # Format distances as matrix output
    result_lines = []
    for row in matrix:
        result_lines.append(" ".join(map(str, row)))
        
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(result_lines) + "\n")

if __name__ == "__main__":
    main()
