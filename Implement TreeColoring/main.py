# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba9p.txt")
    if not os.path.exists(input_file):
        return {}, {}
    adj = {}
    leaf_colors = {}
    reading_adj = True
    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line == "-":
                reading_adj = False
                continue
            if reading_adj:
                parts = line.split(" -> ")
                u = parts[0]
                v_str = parts[1]
                if v_str == "{}":
                    adj[u] = []
                else:
                    adj[u] = v_str.split(",")
            else:
                parts = line.split(": ")
                node = parts[0]
                color = parts[1]
                leaf_colors[node] = color
    return adj, leaf_colors

# Suffix tree/trie rənglənməsi (Tree Coloring) alqoritmi
# Implement TreeColoring
def tree_coloring(adj, leaf_colors):
    # Rəng kodları: "red", "blue", "purple", "gray"
    # Colors: "red", "blue", "purple", "gray"
    colors = {}
    for node, color in leaf_colors.items():
        colors[node] = color
    
    # Qrafın bütün düyünlərini tapırıq
    # Collect all nodes
    all_nodes = set(adj.keys())
    for u in adj:
        for v in adj[u]:
            all_nodes.add(v)
            
    # Hər bir düyünün giriş dərəcəsini hesablayırıq
    # Calculate in-degree of each node
    in_degree = {n: 0 for n in all_nodes}
    for u in adj:
        for v in adj[u]:
            in_degree[v] += 1
            
    # Kök düyünləri tapırıq
    # Find root nodes
    roots = [n for n in all_nodes if in_degree[n] == 0]
    
    # DFS postorder traversal
    def dfs(u):
        if u not in adj or not adj[u]: # Leaf node
            return colors.get(u, "gray")
            
        child_colors = set()
        for v in adj[u]:
            child_colors.add(dfs(v))
            
        if "purple" in child_colors or ("red" in child_colors and "blue" in child_colors):
            color = "purple"
        elif "red" in child_colors:
            color = "red"
        elif "blue" in child_colors:
            color = "blue"
        else:
            color = "gray"
            
        colors[u] = color
        return color

    for r in roots:
        dfs(r)
        
    return colors

def main():
    adj, leaf_colors = read_input()
    if not adj:
        return
    colors = tree_coloring(adj, leaf_colors)
    
    # Nəticəni düyün-rəng cütləri şəklində formatlayırıq
    # Format node: color output
    output_lines = [f"{u}: {colors[u]}" for u in sorted(colors.keys(), key=int)]
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(output_lines) + "\n")

if __name__ == "__main__":
    main()
