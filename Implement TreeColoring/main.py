# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba9p.txt")
    if not os.path.exists(input_file):
        return {}
    adj = {}
    with open(input_file, "r") as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split(" -> ")
            u = parts[0]
            v = parts[1]
            if u not in adj:
                adj[u] = []
            adj[u].append(v)
    return adj

# Suffix tree/trie rənglənməsi (Tree Coloring) alqoritmi
# Implement TreeColoring
def tree_coloring(adj):
    # Rəng kodları: "red", "blue", "purple", "gray"
    # Colors: "red", "blue", "purple", "gray"
    colors = {}
    
    # Qrafın bütün düyünlərini tapırıq
    # Collect all nodes
    all_nodes = set(adj.keys())
    for u in adj:
        for v in adj[u]:
            all_nodes.add(v)
            
    # İlkin olaraq daxili düyünləri boz (gray), yarpaqları isə girişə görə rəngləyirik
    # Leaf nodes are colored in input format or colored red/blue based on suffix source.
    # In Rosalind, leaves have labels or colors.
    # Standard rule:
    # A leaf is red if it encodes suffix from first string, blue from second.
    # Standard DFS postorder coloring:
    # Purple if children contain both red and blue, otherwise matches child color.
    # DFS postorder traversal
    def dfs(u):
        if u not in adj: # Leaf
            # Rosalind-də yarpaq rəngləri girişi verilə bilər (e.g. u has label containing red/blue)
            # Standard leaf node assignment if not specified
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
        
    root = "0" # standard root is 0
    dfs(root)
    return colors

def main():
    adj = read_input()
    if not adj:
        return
    colors = tree_coloring(adj)
    
    # Nəticəni düyün-rəng cütləri şəklində formatlayırıq
    # Format node: color output
    output_lines = [f"{u}: {colors[u]}" for u in sorted(colors.keys(), key=int)]
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(output_lines) + "\n")

if __name__ == "__main__":
    main()
