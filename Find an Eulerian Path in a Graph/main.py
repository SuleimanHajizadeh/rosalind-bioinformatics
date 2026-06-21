# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba3g.txt")
    if not os.path.exists(input_file):
        return {}
    adj = {}
    with open(input_file, "r") as f:
        for line in f:
            if not line.strip():
                continue
            node, neighbors = line.strip().split(" -> ")
            adj[node] = neighbors.split(",")
    return adj

# Giriş-çıxış dərəcələrinə əsasən başlanğıc və son düyünləri tapırıq
# Find start and end nodes of the Eulerian path by calculating in-degrees and out-degrees
def find_start_end(adj):
    out_deg = {u: len(v) for u, v in adj.items()}
    in_deg = {}
    for u in adj:
        for v in adj[u]:
            in_deg[v] = in_deg.get(v, 0) + 1
            
    all_nodes = set(out_deg.keys()).union(in_deg.keys())
    start_node = next(iter(all_nodes))
    end_node = start_node
    
    for u in all_nodes:
        in_d = in_deg.get(u, 0)
        out_d = out_deg.get(u, 0)
        if out_d - in_d == 1:
            start_node = u
        elif in_d - out_d == 1:
            end_node = u
            
    return start_node, end_node

# Qrafda Eyler yolunu tapırıq
# Find an Eulerian path in a graph
def find_eulerian_path(adj):
    start_node, end_node = find_start_end(adj)
    
    # Keçici olaraq son nöqtədən başlanğıca til əlavə edib Eyler dövrünə çevirə bilərik,
    # ya da birbaşa Hierholzer alqoritmini başlanğıc düyündən başladaraq işlədə bilərik
    # We run Hierholzer starting from the start_node
    stack = [start_node]
    path = []
    adj_copy = {u: list(v) for u, v in adj.items()}
    
    while stack:
        u = stack[-1]
        if adj_copy.get(u):
            v = adj_copy[u].pop()
            stack.append(v)
        else:
            path.append(stack.pop())
            
    path.reverse()
    return path

def main():
    adj = read_input()
    if not adj:
        return
    result = find_eulerian_path(adj)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("->".join(result) + "\n")

if __name__ == "__main__":
    main()
