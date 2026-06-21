# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba3h.txt")
    if not os.path.exists(input_file):
        return 0, []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return int(lines[0]), lines[1:]

def de_bruijn_from_kmers(kmers):
    adj = {}
    for kmer in kmers:
        prefix = kmer[:-1]
        suffix = kmer[1:]
        if prefix not in adj:
            adj[prefix] = []
        adj[prefix].append(suffix)
    return adj

def find_start_end(adj):
    out_deg = {u: len(v) for u, v in adj.items()}
    in_deg = {}
    for u in adj:
        for v in adj[u]:
            in_deg[v] = in_deg.get(v, 0) + 1
    all_nodes = set(out_deg.keys()).union(in_deg.keys())
    start_node = next(iter(all_nodes))
    for u in all_nodes:
        if out_deg.get(u, 0) - in_deg.get(u, 0) == 1:
            start_node = u
            break
    return start_node

def find_eulerian_path(adj):
    start_node = find_start_end(adj)
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

# K-merlərə əsasən De Bruijn və Eyler yolu ilə sətiri tapırıq
# Reconstruct a string from its k-mer composition
def reconstruct_string(k, kmers):
    adj = de_bruijn_from_kmers(kmers)
    path = find_eulerian_path(adj)
    # Genom yolundan sətiri qururuq
    # Reconstruct from Eulerian path
    string = path[0]
    for node in path[1:]:
        string += node[-1]
    return string

def main():
    k, kmers = read_input()
    if not kmers:
        return
    result = reconstruct_string(k, kmers)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(result + "\n")

if __name__ == "__main__":
    main()
