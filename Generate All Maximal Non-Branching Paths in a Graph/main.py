# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba3m.txt")
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

# Qrafın dərəcələrini təyin edirik
# Get degrees of the graph
def get_degrees(adj):
    in_deg = {}
    out_deg = {u: len(v) for u, v in adj.items()}
    for u in adj:
        for v in adj[u]:
            in_deg[v] = in_deg.get(v, 0) + 1
            if v not in out_deg:
                out_deg[v] = 0
        if u not in in_deg:
            in_deg[u] = 0
    return in_deg, out_deg

# Bütün maksimal budaqlanmayan yolları tapırıq
# Generate all maximal non-branching paths in a graph
def maximal_non_branching_paths(adj):
    in_deg, out_deg = get_degrees(adj)
    paths = []
    
    # 1-dən çox olan budaqlardan başlayaraq yolları qururuq
    # Build paths starting from branching nodes
    for v in in_deg:
        if not (in_deg[v] == 1 and out_deg[v] == 1):
            if out_deg[v] > 0:
                for w in adj[v]:
                    path = [v, w]
                    while in_deg.get(w, 0) == 1 and out_deg.get(w, 0) == 1:
                        w = adj[w][0]
                        path.append(w)
                    paths.append(path)
                    
    # Təcrid olunmuş dövrləri (isolated cycles) axtarırıq
    # Find isolated cycles
    visited = set()
    for p in paths:
        for node in p:
            visited.add(node)
            
    for v in in_deg:
        if v not in visited and in_deg[v] == 1 and out_deg[v] == 1:
            cycle = [v]
            w = adj[v][0]
            while w != v:
                cycle.append(w)
                visited.add(w)
                w = adj[w][0]
            cycle.append(v)
            paths.append(cycle)
            
    return paths

def main():
    adj = read_input()
    if not adj:
        return
    paths = maximal_non_branching_paths(adj)
    
    # Yolları tələb olunan formatda çıxışa veririk
    # Format the outputs
    result_lines = []
    for p in paths:
        result_lines.append(" -> ".join(p))
        
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(result_lines) + "\n")

if __name__ == "__main__":
    main()
