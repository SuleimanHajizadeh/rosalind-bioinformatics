# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba5d.txt")
    if not os.path.exists(input_file):
        return "", "", {}
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    start = lines[0]
    end = lines[1]
    adj = {}
    for line in lines[2:]:
        parts = line.split("->")
        u = parts[0]
        v, w = parts[1].split(":")
        if u not in adj:
            adj[u] = []
        adj[u].append((v, int(w)))
    return start, end, adj

# Topoloji sıralamanı tapırıq
# Topological sort using DFS
def topological_sort(adj, nodes):
    visited = set()
    order = []
    
    def dfs(u):
        visited.add(u)
        if u in adj:
            for v, _ in adj[u]:
                if v not in visited:
                    dfs(v)
        order.append(u)
        
    for node in nodes:
        if node not in visited:
            dfs(node)
    order.reverse()
    return order

# DAG-da ən uzun yolu tapırıq
# Find the longest path in a DAG
def longest_path_in_dag(start, end, adj):
    # Qrafdakı bütün düyünləri tapırıq
    # Collect all unique nodes
    nodes = set([start, end])
    for u in adj:
        nodes.add(u)
        for v, _ in adj[u]:
            nodes.add(v)
            
    # Topoloji sıralamanı əldə edirik
    # Get topological order
    topo_order = topological_sort(adj, nodes)
    
    # Məsafə və geriyə izləmə cədvəllərini hazırlayırıq
    # Initialize distances and backtrack tables
    dist = {node: -float('inf') for node in nodes}
    dist[start] = 0
    backtrack = {node: None for node in nodes}
    
    for u in topo_order:
        if dist[u] == -float('inf'):
            continue
        if u in adj:
            for v, w in adj[u]:
                if dist[u] + w > dist[v]:
                    dist[v] = dist[u] + w
                    backtrack[v] = u
                    
    # Yolu bərpa edirik
    # Reconstruct the path
    path = []
    curr = end
    while curr is not None:
        path.append(curr)
        curr = backtrack[curr]
    path.reverse()
    
    return dist[end], path

def main():
    start, end, adj = read_input()
    if not start:
        return
    max_d, path = longest_path_in_dag(start, end, adj)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(str(max_d) + "\n")
        f.write("->".join(path) + "\n")

if __name__ == "__main__":
    main()
