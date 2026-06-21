# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba6k.txt")
    if not os.path.exists(input_file):
        return "", 0, 0, 0, 0
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    genome = lines[0]
    i, j, k, l = map(int, lines[1].split(","))
    return genome, i, j, k, l

def parse_genome(genome_str):
    chroms = []
    parts = genome_str.strip().split(")")
    for part in parts:
        part = part.replace("(", "").strip()
        if not part:
            continue
        chroms.append(list(map(int, part.split())))
    return chroms

def colored_edges(genome):
    edges = []
    for chrom in genome:
        nodes = []
        for val in chrom:
            if val > 0:
                nodes.extend([2*val - 1, 2*val])
            else:
                nodes.extend([-2*val, -2*val - 1])
        n = len(nodes)
        for i in range(1, n, 2):
            if i + 1 < n:
                edges.append((nodes[i], nodes[i+1]))
            else:
                edges.append((nodes[i], nodes[0]))
    return edges

def graph_to_genome(edges):
    adj = {}
    for u, v in edges:
        adj[u] = v
        adj[v] = u
    visited = set()
    genome = []
    for node in sorted(adj.keys()):
        if node not in visited:
            chrom = []
            curr = node
            while curr not in visited:
                visited.add(curr)
                val = (curr + 1) // 2
                sign = 1 if curr % 2 == 0 else -1
                chrom.append(sign * val)
                if curr % 2 == 1:
                    partner = curr + 1
                else:
                    partner = curr - 1
                visited.add(partner)
                curr = adj[partner]
            genome.append(chrom)
    return genome

# Genom səviyyəsində 2-break əməliyyatını tətbiq edirik
# Implement 2-BreakOnGenome
def two_break_on_genome(genome_str, i, j, k, l):
    genome = parse_genome(genome_str)
    edges = colored_edges(genome)
    
    # 2-break edirik
    # Apply 2-break on edges
    new_edges = []
    for u, v in edges:
        if (u == i and v == j) or (u == j and v == i):
            continue
        if (u == k and v == l) or (u == l and v == k):
            continue
        new_edges.append((u, v))
    new_edges.append((i, k))
    new_edges.append((j, l))
    
    # Tillərdən yeni genomu bərpa edirik
    # Reconstruct genome from updated edges
    new_genome = graph_to_genome(new_edges)
    return new_genome

def main():
    genome_str, i, j, k, l = read_input()
    if not genome_str:
        return
    result_genome = two_break_on_genome(genome_str, i, j, k, l)
    
    # Genomu formatlayırıq
    # Format genome string
    result = []
    for chrom in result_genome:
        items = [f"+{x}" if x > 0 else str(x) for x in chrom]
        result.append("(" + " ".join(items) + ")")
    out_str = "".join(result)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(out_str + "\n")

if __name__ == "__main__":
    main()
