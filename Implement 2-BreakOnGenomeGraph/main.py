# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba6j.txt")
    if not os.path.exists(input_file):
        return [], 0, 0, 0, 0
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # Tilləri oxuyuruq
    # Parse edges
    edges_str = lines[0].replace("(", "").replace(")", "")
    parts = edges_str.split(",")
    edges = []
    for i in range(0, len(parts), 2):
        edges.append((int(parts[i].strip()), int(parts[i+1].strip())))
        
    # 2-break indekslərini oxuyuruq
    # Parse indices for the 2-break: i, j, k, l
    i, j, k, l = map(int, lines[1].split(","))
    return edges, i, j, k, l

# Genom qrafında 2-break əməliyyatını simulyasiya edirik
# Implement 2-BreakOnGenomeGraph
def two_break_on_genome_graph(edges, i, j, k, l):
    # (i, j) və (k, l) tillərini silib yerinə (i, k) və (j, l) əlavə edirik
    # Remove edges (i, j) and (k, l) and add (i, k) and (j, l)
    new_edges = []
    for u, v in edges:
        if (u == i and v == j) or (u == j and v == i):
            continue
        if (u == k and v == l) or (u == l and v == k):
            continue
        new_edges.append((u, v))
        
    new_edges.append((i, k))
    new_edges.append((j, l))
    return new_edges

def main():
    edges, i, j, k, l = read_input()
    if not edges:
        return
    result_edges = two_break_on_genome_graph(edges, i, j, k, l)
    
    # Nəticəni formatlayırıq
    # Format output edges
    out_str = ", ".join(f"({u}, {v})" for u, v in result_edges)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(out_str + "\n")

if __name__ == "__main__":
    main()
