# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba3j.txt")
    if not os.path.exists(input_file):
        return 0, 0, []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    k, d = map(int, lines[0].split())
    paired_reads = []
    for line in lines[1:]:
        paired_reads.append(line.split("|"))
    return k, d, paired_reads

# Paired reads üçün De Bruijn qrafını qururuq
# Construct De Bruijn graph from paired kmers
def paired_de_bruijn(paired_reads):
    adj = {}
    for r1, r2 in paired_reads:
        prefix = (r1[:-1], r2[:-1])
        suffix = (r1[1:], r2[1:])
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
        if adj_copy.get(u, []):
            v = adj_copy[u].pop()
            stack.append(v)
        else:
            path.append(stack.pop())
    path.reverse()
    return path

# İkili (paired) oxunuşlara əsasən sətiri tapırıq
# Reconstruct a string from its paired composition
def reconstruct_string_paired(k, d, paired_reads):
    adj = paired_de_bruijn(paired_reads)
    path = find_eulerian_path(adj)
    
    # Eyler yolundan sətirləri bərpa edirik
    # Restore strings from path
    s1 = path[0][0]
    for node in path[1:]:
        s1 += node[0][-1]
        
    s2 = path[0][1]
    for node in path[1:]:
        s2 += node[1][-1]
        
    # İki ardıcıllığı birləşdiririk
    # Combine the two paths taking the gap d into account
    overlap = len(s1) - (k + d)
    if s1[overlap:] == s2[:-overlap]:
        return s1 + s2[-overlap:]
    return s1 + s2

def main():
    k, d, paired_reads = read_input()
    if not paired_reads:
        return
    result = reconstruct_string_paired(k, d, paired_reads)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(result + "\n")

if __name__ == "__main__":
    main()
