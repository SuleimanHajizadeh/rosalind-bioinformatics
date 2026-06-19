import os
import sys

class Node:
    def __init__(self, name=""):
        self.name = name
        self.children = []
        self.parent = None
        
    def __repr__(self):
        return f"Node({self.name})"

def parse_newick(s):
    s = s.strip()
    if s.endswith(';'):
        s = s[:-1]
        
    stack = []
    current_node = Node()
    
    i = 0
    n = len(s)
    while i < n:
        char = s[i]
        if char == '(':
            new_node = Node()
            current_node.children.append(new_node)
            new_node.parent = current_node
            stack.append(current_node)
            current_node = new_node
            i += 1
        elif char == ',':
            parent = stack[-1]
            new_node = Node()
            parent.children.append(new_node)
            new_node.parent = parent
            current_node = new_node
            i += 1
        elif char == ')':
            current_node = stack.pop()
            i += 1
        else:
            name_chars = []
            while i < n and s[i] not in '(),;':
                name_chars.append(s[i])
                i += 1
            name = ''.join(name_chars).strip()
            if name:
                current_node.name = name
                
    return current_node

def load_input(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    tree_str = lines[0].strip()
    
    sequences = {}
    current_name = None
    current_seq = []
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        if line.startswith('>'):
            if current_name:
                sequences[current_name] = ''.join(current_seq)
            current_name = line[1:].strip()
            current_seq = []
        else:
            current_seq.append(line)
    if current_name:
        sequences[current_name] = ''.join(current_seq)
        
    return tree_str, sequences

def find_reversing_substitutions(root, sequences):
    paths = []
    
    def dfs(node, current_path):
        current_path.append(node)
        if not node.children:
            paths.append(list(current_path))
        else:
            for child in node.children:
                dfs(child, current_path)
        current_path.pop()
        
    dfs(root, [])
    
    L = len(next(iter(sequences.values())))
    results = set()
    
    for path in paths:
        k = len(path) - 1
        for idx in range(L):
            for w_pos in range(1, k + 1):
                w = path[w_pos]
                w_val = sequences[w.name][idx]
                
                v = path[w_pos - 1]
                v_val = sequences[v.name][idx]
                
                if v_val == w_val:
                    continue
                    
                for j in range(w_pos - 2, -1, -1):
                    node_j_val = sequences[path[j].name][idx]
                    if node_j_val == v_val:
                        continue
                    elif node_j_val == w_val:
                        t = path[j+1]
                        results.add((t.name, w.name, idx + 1, w_val, v_val, w_val))
                        break
                    else:
                        break
                        
    formatted = []
    for t_name, w_name, pos, orig, sub, rev in results:
        formatted.append(f"{t_name} {w_name} {pos} {orig}->{sub}->{rev}")
    return formatted

def main():
    input_path = "rosalind_rsub.txt"
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        sys.exit(1)
        
    tree_str, sequences = load_input(input_path)
    root = parse_newick(tree_str)
    
    results = find_reversing_substitutions(root, sequences)
    
    output_path = "output.txt"
    with open(output_path, "w") as out:
        for line in results:
            out.write(line + "\n")
            
    print(f"Successfully processed tree. Found {len(results)} reversing substitutions.")
    print(f"Results written to {output_path}")

if __name__ == '__main__':
    main()
