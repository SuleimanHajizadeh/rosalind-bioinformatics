# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba6i.txt")
    if not os.path.exists(input_file):
        return []
    with open(input_file, "r") as f:
        content = f.read().strip()
        # tilləri parse edirik (e.g. (2, 4), (3, 6))
        # parse edge pairs
        content = content.replace("(", "").replace(")", "")
        parts = content.split(",")
        edges = []
        for i in range(0, len(parts), 2):
            if i+1 < len(parts):
                edges.append((int(parts[i].strip()), int(parts[i+1].strip())))
        return edges

# Til qrafından genom strukturunu tapırıq
# Implement GraphToGenome
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
                
                # Keçidi edirik
                # Move to next node
                if curr % 2 == 1:
                    partner = curr + 1
                else:
                    partner = curr - 1
                visited.add(partner)
                curr = adj[partner]
            genome.append(chrom)
    return genome

def main():
    edges = read_input()
    if not edges:
        return
    genome = graph_to_genome(edges)
    
    # Genomu formatlayırıq
    # Format the resulting genome string
    result = []
    for chrom in genome:
        items = [f"+{x}" if x > 0 else str(x) for x in chrom]
        result.append("(" + " ".join(items) + ")")
    out_str = "".join(result)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(out_str + "\n")

if __name__ == "__main__":
    main()
