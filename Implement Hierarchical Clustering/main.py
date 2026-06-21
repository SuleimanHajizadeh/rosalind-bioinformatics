# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba8e.txt")
    if not os.path.exists(input_file):
        return 0, []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    n = int(lines[0])
    matrix = []
    for line in lines[1:]:
        matrix.append(list(map(float, line.split())))
    return n, matrix

# İyerarxik klasterləşmə (hierarchical clustering) alqoritmi
# Implement Hierarchical Clustering
def hierarchical_clustering(d, n):
    clusters = {i: [i] for i in range(n)}
    curr_node = n
    active_d = {i: {j: d[i][j] for j in range(n)} for i in range(n)}
    
    steps = []
    while len(clusters) > 1:
        # Ən yaxın iki klasteri tapırıq
        # Find closest pair of clusters
        min_val = float('inf')
        c1, c2 = -1, -1
        keys = list(clusters.keys())
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                k1, k2 = keys[i], keys[j]
                if active_d[k1][k2] < min_val:
                    min_val = active_d[k1][k2]
                    c1, c2 = k1, k2
                    
        # Yeni klaster yaradırıq
        # Create new cluster node
        u = curr_node
        curr_node += 1
        new_cluster = clusters[c1] + clusters[c2]
        clusters[u] = new_cluster
        
        # Add step for output (1-based representation: node IDs list)
        # Rosalind requires output of merged indices (1-based index)
        merged = [x + 1 for x in new_cluster]
        steps.append(" ".join(map(str, merged)))
        
        # Məsafə matrisini yeniləyirik (average distance)
        # Update distances using average linkage
        active_d[u] = {}
        for c in clusters:
            if c != u and c != c1 and c != c2:
                dist = sum(d[i][j] for i in clusters[u] for j in clusters[c]) / (len(clusters[u]) * len(clusters[c]))
                active_d[u][c] = dist
                active_d[c][u] = dist
                
        del clusters[c1]
        del clusters[c2]
        for c in active_d:
            if c1 in active_d[c]: del active_d[c][c1]
            if c2 in active_d[c]: del active_d[c][c2]
        del active_d[c1]
        del active_d[c2]
        
    return steps

def main():
    n, d = read_input()
    if n == 0:
        return
    result = hierarchical_clustering(d, n)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(result) + "\n")

if __name__ == "__main__":
    main()
