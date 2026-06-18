import os

def reverse_complement(s):
    comp = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return "".join(comp[c] for c in reversed(s))

def solve_gasm(input_path, output_path):
    with open(input_path, 'r') as f:
        reads = [line.strip() for line in f if line.strip()]
        
    if not reads:
        print("No reads found!")
        return
        
    L = len(reads[0])
    
    for k in range(L - 1, 0, -1):
        # Extract all (k+1)-mers from reads and their reverse complements
        edges = set()
        for r in reads:
            r_rc = reverse_complement(r)
            for i in range(len(r) - k):
                edges.add(r[i : i + k + 1])
                edges.add(r_rc[i : i + k + 1])
                
        # Build the de Bruijn graph: nodes are k-mers, edges are (k+1)-mers
        adj = {}
        in_degree = {}
        for edge in edges:
            u = edge[:-1]
            v = edge[1:]
            if u not in adj:
                adj[u] = []
            adj[u].append(v)
            if v not in in_degree:
                in_degree[v] = 0
            in_degree[v] += 1
            if u not in in_degree:
                in_degree[u] = 0
                
        # Check if every node has in-degree exactly 1 and out-degree exactly 1
        valid = True
        for node in in_degree:
            out_deg = len(adj.get(node, []))
            in_deg = in_degree[node]
            if out_deg != 1 or in_deg != 1:
                valid = False
                break
                
        if not valid:
            continue
            
        # Count connected components (cycles)
        visited = set()
        cycles = []
        for start in in_degree:
            if start not in visited:
                cycle = []
                curr = start
                cycle_valid = True
                while curr not in visited:
                    visited.add(curr)
                    cycle.append(curr)
                    # Follow the unique outgoing edge
                    next_nodes = adj.get(curr, [])
                    if not next_nodes:
                        cycle_valid = False
                        break
                    curr = next_nodes[0]
                # Check if it successfully closed back to the start node
                if cycle_valid and curr == start:
                    cycles.append(cycle)
                else:
                    valid = False
                    break
                    
        if valid and len(cycles) == 2:
            print(f"Found k = {k}")
            # Reconstruct the cycle sequence from one of the cycles
            cycle = cycles[0]
            res = ""
            for i in range(len(cycle)):
                next_node = cycle[(i + 1) % len(cycle)]
                res += next_node[-1]
                
            with open(output_path, 'w') as out_f:
                out_f.write(res + '\n')
            print("Successfully wrote genome sequence to output.txt.")
            print(f"Genome length: {len(res)}")
            return
            
    print("Could not find any k that yields exactly 2 directed cycles.")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, 'rosalind_gasm.txt')
    output_path = os.path.join(base_dir, 'output.txt')
    solve_gasm(input_path, output_path)

if __name__ == '__main__':
    main()
