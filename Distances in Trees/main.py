import os
from collections import deque

def tokenize(s):
    tokens = []
    i = 0
    while i < len(s):
        if s[i] in '(),;':
            tokens.append(s[i])
            i += 1
        else:
            # Read name
            start = i
            while i < len(s) and s[i] not in '(),;':
                i += 1
            name = s[start:i].strip()
            if name:
                tokens.append(name)
    return tokens

def parse_newick(s):
    tokens = tokenize(s)
    stack = []
    adj = {}
    dummy_count = 0
    
    def get_dummy():
        nonlocal dummy_count
        dummy_count += 1
        return f"__dummy_{dummy_count}__"
        
    def add_edge(u, v):
        if u not in adj: adj[u] = []
        if v not in adj: adj[v] = []
        adj[u].append(v)
        adj[v].append(u)
        
    i = 0
    current_children = []
    while i < len(tokens):
        tok = tokens[i]
        if tok == '(':
            stack.append(current_children)
            current_children = []
            i += 1
        elif tok == ',':
            i += 1
        elif tok == ')':
            parent = None
            if i + 1 < len(tokens) and tokens[i+1] not in '(),;':
                parent = tokens[i+1]
                i += 2
            else:
                parent = get_dummy()
                i += 1
            
            for child in current_children:
                add_edge(parent, child)
                
            if stack:
                prev_children = stack.pop()
                prev_children.append(parent)
                current_children = prev_children
            else:
                current_children = [parent]
        elif tok == ';':
            i += 1
        else:
            current_children.append(tok)
            i += 1
            
    return adj

def bfs_distance(adj, start, target):
    if start == target:
        return 0
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        curr, dist = queue.popleft()
        if curr == target:
            return dist
        for neighbor in adj.get(curr, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return -1

def read_input(file_path):
    trees_and_pairs = []
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f]
    
    i = 0
    while i < len(lines):
        while i < len(lines) and not lines[i]:
            i += 1
        if i >= len(lines):
            break
        tree_str = lines[i]
        i += 1
        while i < len(lines) and not lines[i]:
            i += 1
        if i >= len(lines):
            break
        nodes = lines[i].split()
        i += 1
        if len(nodes) == 2:
            trees_and_pairs.append((tree_str, nodes[0], nodes[1]))
    return trees_and_pairs

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_nwck.txt")
    
    pairs = read_input(input_path)
    distances = []
    
    for idx, (tree_str, x, y) in enumerate(pairs, 1):
        adj = parse_newick(tree_str)
        dist = bfs_distance(adj, x, y)
        print(f"Ağac {idx}: {x} - {y} məsafəsi = {dist}")
        distances.append(dist)
        
    result_str = " ".join(map(str, distances))
    print(f"Yekun nəticə: {result_str}")
    
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        out_file.write(result_str + "\n")

if __name__ == "__main__":
    main()
