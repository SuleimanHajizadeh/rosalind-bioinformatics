# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba7d.txt")
    if not os.path.exists(input_file):
        return 0, []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    n = int(lines[0])
    matrix = []
    for line in lines[1:]:
        matrix.append(list(map(float, line.split())))
    return n, matrix

# UPGMA alqoritmi ilə filogenetik ağac qururuq
# Implement UPGMA hierarchical clustering algorithm for phylogeny
def upgma(d, n):
    clusters = {i: [i] for i in range(n)}
    age = {i: 0.0 for i in range(n)}
    tree = {i: [] for i in range(n)}
    
    curr_node = n
    active_d = {i: {j: d[i][j] for j in range(n)} for i in range(n)}
    
    while len(clusters) > 1:
        # Ən kiçik məsafəli iki klasteri tapırıq
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
                    
        # Yeni düyün yaradırıq
        # Create a new parent node
        u = curr_node
        curr_node += 1
        age[u] = min_val / 2.0
        
        # Klasterləri birləşdiririk
        # Merge clusters and add tree edges
        tree[u] = []
        for child in [c1, c2]:
            tree[child].append((u, age[u] - age[child]))
            tree[u].append((child, age[u] - age[child]))
            
        new_cluster = clusters[c1] + clusters[c2]
        clusters[u] = new_cluster
        
        # Məsafələri yeniləyirik
        # Compute average distance from new cluster to all other clusters
        active_d[u] = {}
        for c in clusters:
            if c != u and c != c1 and c != c2:
                # UPGMA orta məsafə düsturu
                # UPGMA average distance formula
                num = sum(d[i][j] for i in clusters[u] for j in clusters[c])
                denom = len(clusters[u]) * len(clusters[c])
                dist = num / denom
                active_d[u][c] = dist
                active_d[c][u] = dist
                
        # Köhnə klasterləri silirik
        # Remove old merged clusters
        del clusters[c1]
        del clusters[c2]
        for c in active_d:
            if c1 in active_d[c]: del active_d[c][c1]
            if c2 in active_d[c]: del active_d[c][c2]
        del active_d[c1]
        del active_d[c2]
        
    return tree

def main():
    n, d = read_input()
    if n == 0:
        return
    tree = upgma(d, n)
    
    # Tilləri formatlayırıq
    # Format tree output
    output_lines = []
    for u in sorted(tree.keys()):
        for v, w in sorted(tree[u]):
            output_lines.append(f"{u}->{v}:{w:.3f}")
            
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(output_lines) + "\n")

if __name__ == "__main__":
    main()
