# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba3k.txt")
    if not os.path.exists(input_file):
        return []
    with open(input_file, "r") as f:
        return [line.strip() for line in f if line.strip()]

def de_bruijn_from_kmers(kmers):
    adj = {}
    for kmer in kmers:
        prefix = kmer[:-1]
        suffix = kmer[1:]
        if prefix not in adj:
            adj[prefix] = []
        adj[prefix].append(suffix)
    return adj

# Giriş və çıxış dərəcələrini tapırıq
# Compute in-degrees and out-degrees
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

# K-mer oxunuşlarından kontiqlər yaradırıq
# Generate contigs from a collection of reads
def generate_contigs(kmers):
    adj = de_bruijn_from_kmers(kmers)
    in_deg, out_deg = get_degrees(adj)
    
    # Budaqlanmayan (non-branching) yolları axtarırıq
    # Find all maximal non-branching paths
    paths = []
    
    for v in in_deg:
        if not (in_deg[v] == 1 and out_deg[v] == 1):
            if out_deg[v] > 0:
                for w in adj[v]:
                    path = [v, w]
                    while in_deg[w] == 1 and out_deg[w] == 1:
                        w = adj[w][0]
                        path.append(w)
                    paths.append(path)
                    
    # Həmçinin təcrid olunmuş tsiklləri tapırıq
    # Also find isolated cycles
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
            
    contigs = []
    for p in paths:
        contig = p[0]
        for node in p[1:]:
            contig += node[-1]
        contigs.append(contig)
    contigs.sort()
    return contigs

def main():
    kmers = read_input()
    if not kmers:
        return
    result = generate_contigs(kmers)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(result) + "\n")

if __name__ == "__main__":
    main()
