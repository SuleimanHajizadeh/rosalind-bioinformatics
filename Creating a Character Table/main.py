import os

class Node:
    def __init__(self, label=None):
        self.label = label
        self.children = []
        self.leaves = set()

def tokenize(s):
    s = s.strip()
    if s.endswith(';'):
        s = s[:-1]
    tokens = []
    i = 0
    while i < len(s):
        if s[i] in '(),':
            tokens.append(s[i])
            i += 1
        else:
            start = i
            while i < len(s) and s[i] not in '(),;':
                i += 1
            name = s[start:i].strip()
            if name:
                tokens.append(name)
    return tokens

def parse_tree(tokens):
    stack = [Node()]
    for token in tokens:
        if token == '(':
            new_node = Node()
            stack[-1].children.append(new_node)
            stack.append(new_node)
        elif token == ')':
            stack.pop()
        elif token == ',':
            pass
        else:
            leaf_node = Node(label=token)
            stack[-1].children.append(leaf_node)
    return stack[0].children[0]

def collect_leaves(node, all_nodes):
    all_nodes.append(node)
    if not node.children:
        node.leaves = {node.label}
    else:
        for child in node.children:
            collect_leaves(child, all_nodes)
            node.leaves.update(child.leaves)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_ctbl.txt")
    
    with open(input_path, "r") as f:
        newick_str = f.read().strip()
        
    print("Parsing tree...")
    tokens = tokenize(newick_str)
    root = parse_tree(tokens)
    
    all_nodes = []
    collect_leaves(root, all_nodes)
    
    all_leaves = sorted(list(root.leaves))
    n = len(all_leaves)
    print(f"Total number of species (taxa): {n}")
    
    splits = set()
    for node in all_nodes:
        if node == root:
            continue
        S = node.leaves
        if 2 <= len(S) <= n - 2:
            # Canonicalize split:
            # Ensure the first leaf in the sorted list is always '0' (or '1' consistently).
            # Here, we ensure the first leaf is mapped to '0'.
            first_leaf = all_leaves[0]
            invert = (first_leaf in S)
            row = []
            for leaf in all_leaves:
                is_in = leaf in S
                row.append('0' if is_in == invert else '1')
            splits.add(''.join(row))
            
    print(f"Number of nontrivial splits: {len(splits)}")
    
    # Sort splits for deterministic output, though Rosalind accepts any order of rows.
    sorted_splits = sorted(list(splits))
    
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        for split in sorted_splits:
            out_file.write(split + "\n")
            
    print(f"Character table written to: {output_path}")

if __name__ == "__main__":
    main()
