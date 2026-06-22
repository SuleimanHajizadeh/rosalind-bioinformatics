# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba6d.txt")
    if not os.path.exists(input_file):
        return "", ""
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0], lines[1]

# Köməkçi genom parse etmə funksiyaları və 2-break simulyasiyası
# Implement structural functions to find a shortest path of 2-breaks transforming genome P to Q
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
    # Tillərə əsasən genomu bərpa edirik
    # Recover genome from colored edges representation
    adj = {}
    for u, v in edges:
        adj[u] = v
        adj[v] = u
        
    visited = set()
    genome = []
    
    # Bütün mümkün dövrləri (circular chromosomes) izləyirik
    # Traverse circular paths in the edge graph
    for node in sorted(adj.keys()):
        if node not in visited:
            chrom = []
            curr = node
            while curr not in visited:
                visited.add(curr)
                # Müvafiq geni tapırıq
                # Identify synteny block ID
                val = (curr + 1) // 2
                sign = 1 if curr % 2 == 1 else -1
                chrom.append(sign * val)
                
                # Qonşu xromosom tili üzrə hərəkət edirik
                # Move to partner node along the chromosome edge
                if curr % 2 == 1:
                    partner = curr + 1
                else:
                    partner = curr - 1
                visited.add(partner)
                curr = adj[partner]
            # Siyahının sırasını düzəldirik (sintaksis uyğunluğu üçün)
            # Standardize chromosome orientation
            genome.append(chrom)
    return genome

def format_genome(genome):
    result = []
    for chrom in genome:
        items = [f"+{x}" if x > 0 else str(x) for x in chrom]
        result.append("(" + " ".join(items) + ")")
    return "".join(result)

# Q P-yə çevrilənə qədər addım-addım 2-break tətbiq edirik
# Run shortest path transformations
def shortest_rearrangement_path(p_str, q_str):
    p = parse_genome(p_str)
    q = parse_genome(q_str)
    
    edges_p = colored_edges(p)
    edges_q = colored_edges(q)
    
    path = [p_str]
    
    while True:
        # Birləşmiş qrafı qururuq
        # Construct combined graph
        adj_p = {u: v for u, v in edges_p}
        adj_p.update({v: u for u, v in edges_p})
        
        adj_q = {u: v for u, v in edges_q}
        adj_q.update({v: u for u, v in edges_q})
        
        # P ilə Q-nin fərqləndiyi ilk düyünü axtarırıq
        # Find first node u where adj_p[u] != adj_q[u]
        non_trivial_u = None
        for u in adj_p:
            if adj_p[u] != adj_q[u]:
                non_trivial_u = u
                break
                
        if non_trivial_u is None:
            break
            
        u = non_trivial_u
        v = adj_p[u]
        y = adj_q[u]
        z = adj_p[y]
        
        # 2-break tətbiq edib tilləri yeniləyirik
        # Perform 2-break operation: replace (u, v) and (y, z) with (u, y) and (v, z)
        edges_p.remove((u, v) if (u, v) in edges_p else (v, u))
        edges_p.remove((y, z) if (y, z) in edges_p else (z, y))
        edges_p.append((u, y))
        edges_p.append((v, z))
        
        # Sonuncu addım olub olmadığını yoxlayırıq
        # Check if this was the last rearrangement step
        has_diff = False
        adj_p_new = {u: v for u, v in edges_p}
        adj_p_new.update({v: u for u, v in edges_p})
        for node in adj_p_new:
            if adj_p_new[node] != adj_q[node]:
                has_diff = True
                break
                
        if not has_diff:
            path.append(q_str)
        else:
            curr_genome = graph_to_genome(edges_p)
            path.append(format_genome(curr_genome))
            
    return path

def main():
    p_str, q_str = read_input()
    if not p_str:
        return
    result = shortest_rearrangement_path(p_str, q_str)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(result) + "\n")

if __name__ == "__main__":
    main()
