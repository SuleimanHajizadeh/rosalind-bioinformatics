# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba5n.txt")
    if not os.path.exists(input_file):
        return {}
    adj = {}
    with open(input_file, "r") as f:
        for line in f:
            if not line.strip():
                continue
            u, v = line.strip().split(" -> ")
            if u not in adj:
                adj[u] = []
            adj[u].append(v)
    return adj

# DFS vasitəsilə topoloji sıralamanı tapırıq
# Find a topological ordering of a DAG using DFS
def topological_ordering(adj):
    nodes = set(adj.keys())
    for u in adj:
        for v in adj[u]:
            nodes.add(v)
            
    visited = set()
    order = []
    
    def dfs(u):
        visited.add(u)
        if u in adj:
            for v in adj[u]:
                if v not in visited:
                    dfs(v)
        order.append(u)
        
    for node in sorted(nodes):
        if node not in visited:
            dfs(node)
            
    order.reverse()
    return order

def main():
    adj = read_input()
    if not adj:
        return
    result = topological_ordering(adj)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(", ".join(result) + "\n")

if __name__ == "__main__":
    main()
