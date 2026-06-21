# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba7c.txt")
    if not os.path.exists(input_file):
        return 0, []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    n = int(lines[0])
    matrix = []
    for line in lines[1:]:
        matrix.append(list(map(int, line.split())))
    return n, matrix

# Additive Phylogeny alqoritmini tətbiq edirik
# Implement AdditivePhylogeny
def additive_phylogeny(d, n, next_node):
    if n == 2:
        return {0: [(1, d[0][1])], 1: [(0, d[0][1])]}
        
    limb_len = float('inf')
    j = n - 1
    # Limb length tapılması
    # Compute limb length
    for i in range(j):
        for k in range(j):
            if i != j and k != j:
                val = (d[i][j] + d[j][k] - d[i][k]) // 2
                if val < limb_len:
                    limb_len = val
                    
    # Məsafə matrisini yeniləyirik
    # Update distances
    for i in range(j):
        d[i][j] -= limb_len
        d[j][i] = d[i][j]
        
    # j ilə eyni limb-i paylaşan i, k cütünü tapırıq
    # Find i and k sharing paths
    i_near, k_near = 0, 0
    found = False
    for i in range(j):
        for k in range(j):
            if i != j and k != j:
                if d[i][j] + d[j][k] == d[i][k]:
                    i_near, k_near = i, k
                    found = True
                    break
        if found:
            break
            
    x = d[i_near][j]
    
    # Rekursiv olaraq n-1 yarpaqlı ağac qururuq
    # Recurse for n-1 tree
    tree = additive_phylogeny(d, n - 1, next_node)
    
    # i və k arasındakı yolda x məsafəsində yerləşən yeri tapırıq
    # Find path between i and k to insert node v at distance x from i
    path = []
    def find_path(curr, target, parent):
        if curr == target:
            return [curr]
        for neighbor, weight in tree[curr]:
            if neighbor != parent:
                res = find_path(neighbor, target, curr)
                if res:
                    return [curr] + res
        return []
        
    p = find_path(i_near, k_near, -1)
    
    # x məsafəsini yerləşdiririk
    # Locate where to insert the new branching node
    dist = 0
    u, v = -1, -1
    for idx in range(len(p) - 1):
        curr_u = p[idx]
        curr_v = p[idx+1]
        weight = 0
        for neighbor, w in tree[curr_u]:
            if neighbor == curr_v:
                weight = w
                break
        if dist + weight >= x:
            u, v = curr_u, curr_v
            break
        dist += weight
        
    insert_dist = x - dist
    edge_weight = 0
    for neighbor, w in tree[u]:
        if neighbor == v:
            edge_weight = w
            break
            
    v_node = next_node[0]
    
    # Əgər dəqiq bir düyünün üzərinə düşürsə
    # If the distance lands exactly on node v
    if insert_dist == 0:
        v_node = u
    elif insert_dist == edge_weight:
        v_node = v
    else:
        # Yeni düyün yaradaraq qrafı yeniləyirik
        # Insert a new internal node
        next_node[0] += 1
        tree[v_node] = []
        
        # u -> v tilini silirik
        # Remove edge between u and v
        tree[u] = [item for item in tree[u] if item[0] != v]
        tree[v] = [item for item in tree[v] if item[0] != u]
        
        # Yeni tillər əlavə edirik
        # Add new connections
        tree[u].append((v_node, insert_dist))
        tree[v_node].append((u, insert_dist))
        tree[v].append((v_node, edge_weight - insert_dist))
        tree[v_node].append((v, edge_weight - insert_dist))
        
    # j yarpağını v_node düyününə birləşdiririk
    # Connect leaf j to v_node
    if v_node not in tree:
        tree[v_node] = []
    tree[v_node].append((j, limb_len))
    if j not in tree:
        tree[j] = []
    tree[j].append((v_node, limb_len))
    
    return tree

def main():
    n, d = read_input()
    if n == 0:
        return
    next_node = [n]
    tree = additive_phylogeny(d, n, next_node)
    
    # Ağacı formatlayaraq çıxışa veririk
    # Format tree output
    output_lines = []
    for u in sorted(tree.keys()):
        for v, w in sorted(tree[u]):
            output_lines.append(f"{u}->{v}:{w}")
            
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(output_lines) + "\n")

if __name__ == "__main__":
    main()
