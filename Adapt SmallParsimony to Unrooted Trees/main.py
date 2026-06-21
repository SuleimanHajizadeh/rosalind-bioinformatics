# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba7g.txt")
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

# Small Parsimony-ni unrooted (köksüz) ağac üçün adaptasiya edirik
# Adapt SmallParsimony to Unrooted Trees
def small_parsimony_unrooted(n, adj):
    # Köksüz ağacı köklü etmək üçün ixtiyari bir tilin ortasından kök əlavə edirik
    # Root the tree by adding a temporary root node along any arbitrary edge
    all_nodes = set(adj.keys())
    for u in adj:
        for v in adj[u]:
            all_nodes.add(v)
            
    internal_nodes = [node for node in all_nodes if not (node.isdigit() and int(node) < n)]
    
    # İlk tapılan daxili düyünlər arasındakı tili seçirik
    # Pick a root edge between two internal nodes
    root_edge = None
    for u in adj:
        if u in internal_nodes:
            for v in adj[u]:
                if v in internal_nodes:
                    root_edge = (u, v)
                    break
            if root_edge:
                break
                
    if not root_edge:
        # Əgər daxili tillər yoxdursa, yarpağa birləşən tili seçirik
        # Fallback to any edge if no internal edges exist
        u = next(iter(adj.keys()))
        v = adj[u][0]
        root_edge = (u, v)
        
    u, v = root_edge
    
    # Yeni köklü ağacın qonşuluq qrafını hazırlayırıq
    # Build rooted adjacency list
    rooted_adj = {}
    visited_edges = set()
    
    # Kök düyün təyin edirik
    # Create temporary root node ID
    max_node = max(int(node) for node in all_nodes if node.isdigit())
    temp_root = str(max_node + 1)
    
    # u və v arasına temp_root yerləşdiririk
    # Insert temp_root between u and v
    rooted_adj[temp_root] = [u, v]
    
    # DFS ilə digər tilləri yönləndiririk
    # Direct edges away from temp_root using DFS
    def direct_edges(curr, parent):
        children = []
        for neighbor in adj.get(curr, []):
            # Köksüz qrafda iki tərəfli keçid var
            # Unrooted trees are parsed as bidirectional
            if neighbor != parent:
                # v-dən u-ya və ya u-dan v-yə olan orijinal tili yönləndirmirik
                # Skip the split edge itself
                if (curr == u and neighbor == v) or (curr == v and neighbor == u):
                    continue
                children.append(neighbor)
                direct_edges(neighbor, curr)
        if children:
            rooted_adj[curr] = children
            
    direct_edges(u, temp_root)
    direct_edges(v, temp_root)
    
    # Small Parsimony-ni bu köklü ağac üzərində çağırırıq
    # Call Small Parsimony on the newly rooted tree
    from collections import defaultdict
    # Bizə lazım olan formatda parsimony-ni simulyasiya edirik
    # Parse leaf DNA labels
    leaf_labels = {}
    adj_parsed = {}
    for node in rooted_adj:
        adj_parsed[node] = []
        for child in rooted_adj[node]:
            if not child.isdigit():
                leaf_id = str(len(leaf_labels))
                leaf_labels[leaf_id] = child
                adj_parsed[node].append(leaf_id)
            else:
                adj_parsed[node].append(child)
                
    m = len(next(iter(leaf_labels.values())))
    total_score = 0
    node_sequences = {node: [""] * m for node in adj_parsed}
    for l_id, seq in leaf_labels.items():
        node_sequences[l_id] = list(seq)
        
    alphabet = ['A', 'C', 'G', 'T']
    
    for col in range(m):
        s_table = {}
        backtrack = {}
        postorder = []
        visited = set()
        
        def postorder_dfs(curr_node):
            visited.add(curr_node)
            if curr_node in adj_parsed:
                for child in adj_parsed[curr_node]:
                    if child not in visited:
                        postorder_dfs(child)
            postorder.append(curr_node)
            
        postorder_dfs(temp_root)
        
        for curr_node in postorder:
            s_table[curr_node] = {}
            backtrack[curr_node] = {}
            if curr_node not in adj_parsed:
                char = leaf_labels[curr_node][col]
                for a in alphabet:
                    s_table[curr_node][a] = 0 if a == char else float('inf')
            else:
                children = adj_parsed[curr_node]
                # İki və ya daha çox uşaq ola bilər (kök üçün 2 daxili alt ağac)
                # DP combines scores over all children
                for a in alphabet:
                    cost_sum = 0
                    child_choices = []
                    for child in children:
                        min_c = float('inf')
                        best_c = 'A'
                        for b in alphabet:
                            cost = s_table[child][b] + (0 if a == b else 1)
                            if cost < min_c:
                                min_c = cost
                                best_c = b
                        cost_sum += min_c
                        child_choices.append(best_c)
                    s_table[curr_node][a] = cost_sum
                    backtrack[curr_node][a] = child_choices
                    
        min_val = min(s_table[temp_root].values())
        total_score += min_val
        best_root_char = [a for a in alphabet if s_table[temp_root][a] == min_val][0]
        
        preorder = list(postorder)
        preorder.reverse()
        
        assigned = {temp_root: best_root_char}
        for curr_node in preorder:
            if curr_node in adj_parsed:
                children = adj_parsed[curr_node]
                parent_char = assigned[curr_node]
                choices = backtrack[curr_node][parent_char]
                for child, char in zip(children, choices):
                    assigned[child] = char
                    
        for node in assigned:
            node_sequences[node][col] = assigned[node]
            
    for node in node_sequences:
        node_sequences[node] = "".join(node_sequences[node])
        
    return total_score, adj_parsed, node_sequences, temp_root

def main():
    n, adj = read_input()
    if n == 0:
        return
    score, adj_parsed, node_sequences, temp_root = small_parsimony_unrooted(n, adj)
    
    output_lines = [str(score)]
    def hamming_dist(s1, s2):
        return sum(c1 != c2 for c1, c2 in zip(s1, s2))
        
    # Kökü aradan qaldıraraq tilləri yazırıq
    # Remove the temporary root and print the unrooted tree edges
    edges = []
    visited_edges = set()
    
    # Uşaqlar üzrə gedirik
    # Traverse edges in the tree
    for u in adj_parsed:
        u_seq = node_sequences[u]
        for v in adj_parsed[u]:
            v_seq = node_sequences[v]
            if u == temp_root:
                # Kökü keçirik, uşaqları bir-birinə bağlayırıq
                # Connect temp_root's children directly to bypass temp_root
                left, right = adj_parsed[temp_root][0], adj_parsed[temp_root][1]
                left_seq = node_sequences[left]
                right_seq = node_sequences[right]
                dist = hamming_dist(left_seq, right_seq)
                if (left, right) not in visited_edges and (right, left) not in visited_edges:
                    edges.append(f"{left_seq}->{right_seq}:{dist}")
                    edges.append(f"{right_seq}->{left_seq}:{dist}")
                    visited_edges.add((left, right))
            else:
                dist = hamming_dist(u_seq, v_seq)
                if (u, v) not in visited_edges and (v, u) not in visited_edges:
                    edges.append(f"{u_seq}->{v_seq}:{dist}")
                    edges.append(f"{v_seq}->{u_seq}:{dist}")
                    visited_edges.add((u, v))
                    
    output_lines.extend(edges)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(output_lines) + "\n")

if __name__ == "__main__":
    main()
