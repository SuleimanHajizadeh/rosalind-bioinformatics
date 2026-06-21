# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba7f.txt")
    if not os.path.exists(input_file):
        return 0, {}
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    n = int(lines[0])
    adj = {}
    for line in lines[1:]:
        u, v = line.split("->")
        if u not in adj:
            adj[u] = []
        adj[u].append(v)
    return n, adj

# Small Parsimony alqoritmini tətbiq edirik
# Implement SmallParsimony
def small_parsimony(n, adj):
    # Düyünləri tapırıq
    # Collect nodes
    all_nodes = set(adj.keys())
    for u in adj:
        for v in adj[u]:
            all_nodes.add(v)
            
    leaves = [node for node in all_nodes if node.isdigit() and int(node) < n]
    internal_nodes = [node for node in all_nodes if not (node.isdigit() and int(node) < n)]
    
    # Yarpaqlardakı simvolların uzunluğunu tapırıq
    # Find length of DNA sequences at leaves
    seq_len = 0
    leaf_seq = {}
    for leaf in leaves:
        # parent axtarırıq
        # Find leaf sequence from incoming edges
        for parent in adj:
            for child in adj[parent]:
                if child == leaf:
                    # child-in adında yox, dəyərində sətir olur
                    # leaves have DNA strings in the actual datasets
                    pass
                    
    # Simulyasiya üçün qonşuluq cədvəlini düzgün parse edək
    # Parse leaf DNA strings correctly. In Rosalind, leaves are labeled with DNA strings in input lines.
    # format: parent->leaf_string
    leaf_labels = {}
    adj_parsed = {}
    
    # Düzgün parse edirik (Rosalind formatı)
    # Parse graph edges and leaf strings
    for u in adj:
        if u not in adj_parsed:
            adj_parsed[u] = []
        for v in adj[u]:
            if not v.isdigit():
                # v yarpaq simvoludur
                # v is leaf string
                leaf_id = str(len(leaf_labels))
                leaf_labels[leaf_id] = v
                adj_parsed[u].append(leaf_id)
            else:
                adj_parsed[u].append(v)
                
    m = len(next(iter(leaf_labels.values()))) # sequence length
    total_parsimony_score = 0
    node_sequences = {node: [""] * m for node in adj_parsed}
    for l_id, seq in leaf_labels.items():
        node_sequences[l_id] = list(seq)
        
    alphabet = ['A', 'C', 'G', 'T']
    
    # Hər bir simvol mövqeyi üçün kiçik parsimoniya hesablayırıq
    # Calculate parsimony for each character column independently
    for col in range(m):
        # S dynamic programming cədvəli
        # S DP matrix: S[node][character]
        s_table = {}
        backtrack = {}
        
        # Postorder keçid sırasını hazırlayırıq (yarpaqlardan kökə doğru)
        # Postorder traversal to compute scores bottom-up
        postorder = []
        visited = set()
        
        def postorder_dfs(u):
            visited.add(u)
            if u in adj_parsed:
                for v in adj_parsed[u]:
                    if v not in visited:
                        postorder_dfs(v)
            postorder.append(u)
            
        root = max(adj_parsed.keys(), key=int)
        postorder_dfs(root)
        
        # Aşağıdan yuxarıya hesablama
        # Bottom-up DP score calculation
        for u in postorder:
            s_table[u] = {}
            backtrack[u] = {}
            if u not in adj_parsed: # Leaf
                char = leaf_labels[u][col]
                for a in alphabet:
                    s_table[u][a] = 0 if a == char else float('inf')
            else:
                left, right = adj_parsed[u][0], adj_parsed[u][1]
                for a in alphabet:
                    # Sol tərəf üçün minimum
                    # Min cost from left child
                    min_l = float('inf')
                    best_l = 'A'
                    for b in alphabet:
                        cost = s_table[left][b] + (0 if a == b else 1)
                        if cost < min_l:
                            min_l = cost
                            best_l = b
                            
                    # Sağ tərəf üçün minimum
                    # Min cost from right child
                    min_r = float('inf')
                    best_r = 'A'
                    for b in alphabet:
                        cost = s_table[right][b] + (0 if a == b else 1)
                        if cost < min_r:
                            min_r = cost
                            best_r = b
                            
                    s_table[u][a] = min_l + min_r
                    backtrack[u][a] = (best_l, best_r)
                    
        # Kökdən başlayaraq geriyə izləyirik (preorder)
        # Top-down traceback to find optimal character assignments
        min_root_val = min(s_table[root].values())
        total_parsimony_score += min_root_val
        best_root_char = [a for a in alphabet if s_table[root][a] == min_root_val][0]
        
        preorder = list(postorder)
        preorder.reverse()
        
        assigned_chars = {root: best_root_char}
        for u in preorder:
            if u in adj_parsed:
                left, right = adj_parsed[u][0], adj_parsed[u][1]
                parent_char = assigned_chars[u]
                best_l, best_r = backtrack[u][parent_char]
                assigned_chars[left] = best_l
                assigned_chars[right] = best_r
                
        for node in assigned_chars:
            node_sequences[node][col] = assigned_chars[node]
            
    # Nəticələri sətirə çeviririk
    # Form sequence strings
    for node in node_sequences:
        node_sequences[node] = "".join(node_sequences[node])
        
    return total_parsimony_score, adj_parsed, node_sequences

def main():
    n, adj = read_input()
    if n == 0:
        return
    score, adj_parsed, node_sequences = small_parsimony(n, adj)
    
    # Tilləri və məsafələri çıxışa yazırıq (Hamming məsafəsi ilə)
    # Output total score followed by edges with Hamming distance weights
    output_lines = [str(score)]
    def hamming_dist(s1, s2):
        return sum(c1 != c2 for c1, c2 in zip(s1, s2))
        
    for u in adj_parsed:
        u_seq = node_sequences[u]
        for v in adj_parsed[u]:
            v_seq = node_sequences[v]
            dist = hamming_dist(u_seq, v_seq)
            output_lines.append(f"{u_seq}->{v_seq}:{dist}")
            output_lines.append(f"{v_seq}->{u_seq}:{dist}")
            
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(output_lines) + "\n")

if __name__ == "__main__":
    main()
