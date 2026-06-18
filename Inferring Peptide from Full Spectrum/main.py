import os

# Monoisotopic masses of the 20 amino acids
AA_MASSES = {
    'A': 71.03711, 'R': 156.10111, 'N': 114.04293, 'D': 115.02694,
    'C': 103.00919, 'E': 129.04259, 'Q': 128.05858, 'G': 57.02146,
    'H': 137.05891, 'I': 113.08406, 'L': 113.08406, 'K': 128.09496,
    'M': 131.04049, 'F': 147.06841, 'P': 97.05276, 'S': 87.03203,
    'T': 101.04768, 'V': 99.06841, 'W': 186.07931, 'Y': 163.06333
}

def read_input(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    if not lines:
        raise ValueError("Input file is empty")
    parent_mass = float(lines[0])
    L = [float(x) for x in lines[1:]]
    return parent_mass, L

def solve_peptide_inference(parent_mass, L):
    tol = 0.01
    used = [False] * len(L)
    pairs = []
    
    # Pair up elements that sum to parent_mass within tolerance
    for i in range(len(L)):
        if used[i]:
            continue
        for j in range(i + 1, len(L)):
            if used[j]:
                continue
            if abs((L[i] + L[j]) - parent_mass) < tol:
                pairs.append((min(L[i], L[j]), max(L[i], L[j])))
                used[i] = True
                used[j] = True
                break
                
    n = len(pairs) - 1
    print(f"Number of complementary pairs found: {len(pairs)}")
    print(f"Expected peptide length n: {n}")
    
    # Represent nodes in the graph
    # Even index 2*i represents pairs[i][0] (smaller element)
    # Odd index 2*i+1 represents pairs[i][1] (larger element)
    num_nodes = 2 * len(pairs)
    nodes = []
    for u, v in pairs:
        nodes.append(u)
        nodes.append(v)
        
    # Build adjacency list: edges represent valid amino acid mass transitions
    adj = {i: [] for i in range(num_nodes)}
    for i in range(num_nodes):
        for j in range(num_nodes):
            diff = nodes[j] - nodes[i]
            if diff > 0:
                for aa, mass in AA_MASSES.items():
                    if abs(diff - mass) < tol:
                        adj[i].append((j, aa))
                        
    # Memoized DFS to find a path of length n
    memo = {}
    
    def dfs(curr_node, visited_pairs):
        if len(visited_pairs) == len(pairs):
            return []
            
        state = (curr_node, frozenset(visited_pairs))
        if state in memo:
            return memo[state]
            
        for next_node, aa in adj[curr_node]:
            next_pair = next_node // 2
            if next_pair not in visited_pairs:
                visited_pairs.add(next_pair)
                res = dfs(next_node, visited_pairs)
                visited_pairs.remove(next_pair)
                if res is not None:
                    memo[state] = [aa] + res
                    return memo[state]
                    
        memo[state] = None
        return None

    # Try starting DFS from each node in the graph
    for start_node in range(num_nodes):
        start_pair = start_node // 2
        res = dfs(start_node, {start_pair})
        if res is not None:
            return "".join(res)
            
    return None

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_full.txt")
    
    print(f"Reading input from: {input_path}")
    parent_mass, L = read_input(input_path)
    print(f"Parent Mass: {parent_mass}")
    print(f"Number of spectrum masses: {len(L)}")
    
    peptide = solve_peptide_inference(parent_mass, L)
    
    if peptide:
        print(f"Inferred Peptide: {peptide}")
        output_path = os.path.join(script_dir, "output.txt")
        with open(output_path, "w") as out_file:
            out_file.write(peptide + "\n")
        print(f"Output written to: {output_path}")
    else:
        print("No valid peptide could be inferred from the given spectrum.")

if __name__ == "__main__":
    main()
