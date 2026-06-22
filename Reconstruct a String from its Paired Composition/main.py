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
    in_deg = {}
    for r1, r2 in paired_reads:
        prefix = (r1[:-1], r2[:-1])
        suffix = (r1[1:], r2[1:])
        if prefix not in adj:
            adj[prefix] = []
        adj[prefix].append(suffix)
        in_deg[suffix] = in_deg.get(suffix, 0) + 1
        if prefix not in in_deg:
            in_deg[prefix] = 0
    return adj, in_deg

def find_start_node(adj, in_deg):
    out_deg = {u: len(v) for u, v in adj.items()}
    all_nodes = set(out_deg.keys()).union(in_deg.keys())
    start_node = next(iter(all_nodes))
    for u in all_nodes:
        if out_deg.get(u, 0) - in_deg.get(u, 0) == 1:
            return u
    for u in all_nodes:
        if out_deg.get(u, 0) > 0:
            return u
    return start_node

# İkili (paired) oxunuşlara əsasən sətiri tapırıq
# Reconstruct a string from its paired composition
def reconstruct_string_paired(k, d, paired_reads):
    import sys
    sys.setrecursionlimit(50000)
    
    adj, in_deg = paired_de_bruijn(paired_reads)
    start_node = find_start_node(adj, in_deg)
    num_edges = len(paired_reads)
    path = [start_node]
    
    def dfs(curr):
        m = len(path) - 1
        # Pruning check: does path[m] conflict with past choices?
        if m - d - 2 >= 0:
            s1_char = path[m][0][-1]
            target_idx = m - d - 2
            if target_idx < k - 1:
                s2_char = path[0][1][target_idx]
            else:
                s2_char = path[m - d - k][1][-1]
            if s1_char != s2_char:
                return False

        if len(path) == num_edges + 1:
            return True

        if curr not in adj or not adj[curr]:
            return False

        # Try neighbors (make a copy of the list because we mutate it during iteration)
        neighbors = list(adj[curr])
        for nxt in neighbors:
            adj[curr].remove(nxt)
            path.append(nxt)
            if dfs(nxt):
                return True
            path.pop()
            adj[curr].append(nxt)
        return False

    if not dfs(start_node):
        return "No valid path found"

    # Spell the final string
    s1 = path[0][0]
    for node in path[1:]:
        s1 += node[0][-1]
        
    s2 = path[0][1]
    for node in path[1:]:
        s2 += node[1][-1]
        
    return s1 + s2[-(k + d):]

def main():
    k, d, paired_reads = read_input()
    if not paired_reads:
        return
    result = reconstruct_string_paired(k, d, paired_reads)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(result + "\n")
    print("Reconstructed string length:", len(result))

if __name__ == "__main__":
    main()
