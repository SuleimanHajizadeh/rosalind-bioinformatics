# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba7e.txt")
    if not os.path.exists(input_file):
        return 0, []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    n = int(lines[0])
    matrix = []
    for line in lines[1:]:
        matrix.append(list(map(float, line.split())))
    return n, matrix

# Neighbor Joining (Qonşu Birləşmə) alqoritmi
# Implement the Neighbor Joining Algorithm
def neighbor_joining(d, n, active_nodes, next_node):
    if len(active_nodes) == 2:
        u, v = active_nodes[0], active_nodes[1]
        dist = d[u][v]
        return {u: [(v, dist)], v: [(u, dist)]}
        
    # Total distances (Sütün/Sətir cəmləri)
    # Compute sum of distances from node i to all other active nodes
    tot_d = {}
    m = len(active_nodes)
    for u in active_nodes:
        tot_d[u] = sum(d[u][v] for v in active_nodes)
        
    # NJ Matrisini qururuq (Neighbor Joining Matrix)
    # Construct NJ matrix to find closest neighbors
    min_val = float('inf')
    neighbor_u, neighbor_v = -1, -1
    for i in range(m):
        for j in range(i + 1, m):
            u, v = active_nodes[i], active_nodes[j]
            nj_val = (m - 2) * d[u][v] - tot_d[u] - tot_d[v]
            if nj_val < min_val:
                min_val = nj_val
                neighbor_u, neighbor_v = u, v
                
    # Limb length (Limb uzunluğu) hesablayırıq
    # Compute branch lengths from neighbor_u and neighbor_v to new node
    delta = (tot_d[neighbor_u] - tot_d[neighbor_v]) / (m - 2)
    limb_u = (d[neighbor_u][neighbor_v] + delta) / 2.0
    limb_v = (d[neighbor_u][neighbor_v] - delta) / 2.0
    
    # Yeni düyün yaradırıq
    # Create new node
    u_new = next_node[0]
    next_node[0] += 1
    
    # Məsafələr matrisinə yeni düyünü əlavə edirik
    # Add distances of the new node to all active nodes
    d[u_new] = {}
    for w in active_nodes:
        dist = (d[neighbor_u][w] + d[neighbor_v][w] - d[neighbor_u][neighbor_v]) / 2.0
        d[u_new][w] = dist
        d[w][u_new] = dist
    d[u_new][u_new] = 0.0
    
    # Kohne duyunleri cixarib yenisini elave edirik
    # Update active nodes list
    next_active = [w for w in active_nodes if w != neighbor_u and w != neighbor_v] + [u_new]
    
    # Rekursiv olaraq davam edirik
    # Recurse on the updated set of active nodes
    tree = neighbor_joining(d, n, next_active, next_node)
    
    # Yeni düyünü köhnələrə bağlayırıq
    # Connect old neighbors to the new node in the tree structure
    if u_new not in tree:
        tree[u_new] = []
    tree[u_new].append((neighbor_u, limb_u))
    tree[u_new].append((neighbor_v, limb_v))
    
    if neighbor_u not in tree:
        tree[neighbor_u] = []
    tree[neighbor_u].append((u_new, limb_u))
    
    if neighbor_v not in tree:
        tree[neighbor_v] = []
    tree[neighbor_v].append((u_new, limb_v))
    
    return tree

def main():
    n, matrix = read_input()
    if n == 0:
        return
    # Matrisi qonşuluq strukturunda lüğətə yığın
    # Map matrix to dictionary for convenience
    d = {}
    for i in range(n):
        d[i] = {}
        for j in range(n):
            d[i][j] = matrix[i][j]
            
    active_nodes = list(range(n))
    next_node = [n]
    tree = neighbor_joining(d, n, active_nodes, next_node)
    
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
