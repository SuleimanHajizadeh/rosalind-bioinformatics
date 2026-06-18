#!/usr/bin/env python3
import os
import sys

# Increase recursion depth for deep tree structures
sys.setrecursionlimit(20000)

def tokenize(s):
    s = s.replace(" ", "").replace("\n", "").replace("\r", "")
    tokens = []
    i = 0
    n = len(s)
    while i < n:
        if s[i] in "(),;":
            tokens.append(s[i])
            i += 1
        else:
            j = i
            while j < n and s[j] not in "(),;":
                j += 1
            tokens.append(s[i:j])
            i = j
    return tokens

def parse(tokens):
    def parse_node(index):
        if index >= len(tokens):
            raise ValueError("Unexpected end of tokens")
        if tokens[index] == '(':
            children = []
            index += 1
            while True:
                child, index = parse_node(index)
                children.append(child)
                if index >= len(tokens):
                    raise ValueError("Expected ',' or ')', got end of tokens")
                if tokens[index] == ')':
                    index += 1
                    break
                elif tokens[index] == ',':
                    index += 1
                else:
                    raise ValueError(f"Expected ',' or ')', got {tokens[index]}")
            name = ""
            if index < len(tokens) and tokens[index] not in "(),;":
                name = tokens[index]
                index += 1
            return {"children": children, "name": name}, index
        else:
            name = tokens[index]
            return {"children": [], "name": name}, index + 1
            
    tree, next_index = parse_node(0)
    return tree

def get_node_leaves(node, leaves_map):
    if not node["children"]:
        leaves = {node["name"]}
    else:
        leaves = set()
        for child in node["children"]:
            leaves.update(get_node_leaves(child, leaves_map))
    leaves_map[id(node)] = leaves
    return leaves

def get_nontrivial_splits(tree, all_leaves, ref_taxon):
    leaves_map = {}
    get_node_leaves(tree, leaves_map)
    
    splits = set()
    n = len(all_leaves)
    
    def collect_splits(node, is_root=False):
        if not is_root:
            S_u = leaves_map[id(node)]
            if 2 <= len(S_u) <= n - 2:
                if ref_taxon in S_u:
                    split = frozenset(all_leaves - S_u)
                else:
                    split = frozenset(S_u)
                splits.add(split)
        for child in node["children"]:
            collect_splits(child, is_root=False)
            
    collect_splits(tree, is_root=True)
    return splits

def main():
    input_path = "rosalind_sptd.txt"
    output_path = "output.txt"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return
        
    with open(input_path, 'r') as f:
        # Filter out empty lines
        lines = [line.strip() for line in f if line.strip()]
        
    if len(lines) < 3:
        print("Error: Input file must contain taxa line and two trees.")
        return
        
    taxa = lines[0].split()
    newick1 = lines[1]
    newick2 = lines[2]
    
    print(f"Number of taxa: {len(taxa)}")
    all_leaves = set(taxa)
    ref_taxon = taxa[0]
    
    print("Parsing tree 1...")
    tree1 = parse(tokenize(newick1))
    print("Parsing tree 2...")
    tree2 = parse(tokenize(newick2))
    
    print("Collecting nontrivial splits for tree 1...")
    splits1 = get_nontrivial_splits(tree1, all_leaves, ref_taxon)
    print("Collecting nontrivial splits for tree 2...")
    splits2 = get_nontrivial_splits(tree2, all_leaves, ref_taxon)
    
    s = len(splits1.intersection(splits2))
    n = len(taxa)
    distance = 2 * (n - 3) - 2 * s
    print(f"Shared nontrivial splits: {s}")
    print(f"Split distance: {distance}")
    
    with open(output_path, 'w') as f:
        f.write(str(distance) + "\n")
    print(f"Result written to {output_path}")

if __name__ == "__main__":
    main()
