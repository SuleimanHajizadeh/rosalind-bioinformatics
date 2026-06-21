# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba6c.txt")
    if not os.path.exists(input_file):
        return "", ""
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0], lines[1]

# Xromosom sintaksisini parse edirik
# Parse chromosome strings into signed integer paths
def parse_genome(genome_str):
    chroms = []
    parts = genome_str.strip().split(")")
    for part in parts:
        part = part.replace("(", "").strip()
        if not part:
            continue
        chroms.append(list(map(int, part.split())))
    return chroms

# Rəngli tilləri (colored edges) qururuq
# Get colored edges of a genome representation
def colored_edges(genome):
    edges = []
    for chrom in genome:
        nodes = []
        for val in chrom:
            if val > 0:
                nodes.extend([2*val - 1, 2*val])
            else:
                nodes.extend([-2*val, -2*val - 1])
        # Dairəvi (circular) xromosom üçün sonuncu tili birinciyə bağlayırıq
        # Connect end to start for circular chromosomes
        n = len(nodes)
        for i in range(1, n, 2):
            if i + 1 < n:
                edges.append((nodes[i], nodes[i+1]))
            else:
                edges.append((nodes[i], nodes[0]))
    return edges

# İki genom arasındakı 2-Break məsafəsini hesablayırıq
# Compute the 2-break distance between a pair of genomes
def two_break_distance(g1_str, g2_str):
    g1 = parse_genome(g1_str)
    g2 = parse_genome(g2_str)
    
    # 2 genom üçün til siyahılarını tapırıq
    # Construct colored edges for both genomes
    edges1 = colored_edges(g1)
    edges2 = colored_edges(g2)
    
    # Birləşmiş qrafın qonşuluq siyahısını qururuq
    # Build combined adjacency list for cycle detection
    adj = {}
    for u, v in edges1 + edges2:
        if u not in adj: adj[u] = []
        if v not in adj: adj[v] = []
        adj[u].append(v)
        adj[v].append(u)
        
    # Tsikllərin (dövrlərin) sayını tapırıq
    # Count the number of disjoint cycles in the graph
    visited = set()
    cycles = 0
    for node in adj:
        if node not in visited:
            cycles += 1
            curr = node
            while curr not in visited:
                visited.add(curr)
                # Növbəti ziyarət olunmamış qonşuya keçirik
                # Move to next unvisited neighbor
                next_node = None
                for neighbor in adj[curr]:
                    if neighbor not in visited:
                        next_node = neighbor
                        break
                if next_node is None:
                    break
                curr = next_node
                
    # 2-break distance düsturu: d(P, Q) = Blocks - Cycles
    # Here, Blocks is total synteny blocks (number of edges in one genome)
    blocks = len(edges1)
    return blocks - cycles

def main():
    g1_str, g2_str = read_input()
    if not g1_str:
        return
    result = two_break_distance(g1_str, g2_str)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(str(result) + "\n")

if __name__ == "__main__":
    main()
