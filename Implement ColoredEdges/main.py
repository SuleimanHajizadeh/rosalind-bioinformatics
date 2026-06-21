# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba6h.txt")
    if not os.path.exists(input_file):
        return []
    with open(input_file, "r") as f:
        content = f.read().strip()
    return content

def parse_genome(genome_str):
    chroms = []
    parts = genome_str.strip().split(")")
    for part in parts:
        part = part.replace("(", "").strip()
        if not part:
            continue
        chroms.append(list(map(int, part.split())))
    return chroms

# Genomun rəngli tillərini tapırıq
# Implement ColoredEdges
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

def main():
    content = read_input()
    if not content:
        return
    genome = parse_genome(content)
    edges = colored_edges(genome)
    
    # Tilləri formatlayırıq: e.g. (2, 4), (3, 6)
    # Format edges
    out_str = ", ".join(f"({u}, {v})" for u, v in edges)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(out_str + "\n")

if __name__ == "__main__":
    main()
