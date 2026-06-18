import sys
import os

def solve_lrep(input_path, output_path):
    # Set recursion limit high because suffix trees can be deep (up to 30,000+ nodes)
    sys.setrecursionlimit(200000)
    
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} not found.")
        return
        
    with open(input_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
        
    if len(lines) < 2:
        print("Error: Invalid input format. Expected at least string s and threshold k.")
        return
        
    s = lines[0]
    try:
        k = int(lines[1])
    except ValueError:
        print(f"Error: Invalid threshold k: '{lines[1]}'")
        return
        
    print(f"String length: {len(s)}")
    print(f"Threshold k: {k}")
    print(f"Number of edge lines: {len(lines) - 2}")
    
    # adj maps parent -> list of (child, start_index, length)
    # start_index is 1-based.
    adj = {}
    all_nodes = set()
    child_nodes = set()
    
    for idx, line in enumerate(lines[2:], start=3):
        parts = line.split()
        if len(parts) != 4:
            print(f"Warning: line {idx} does not have 4 fields: '{line}'")
            continue
        parent, child, start_str, len_str = parts
        try:
            start_idx = int(start_str)
            length = int(len_str)
        except ValueError:
            print(f"Error: Non-integer edge parameters on line {idx}: '{line}'")
            continue
            
        if parent not in adj:
            adj[parent] = []
        adj[parent].append((child, start_idx, length))
        
        all_nodes.add(parent)
        all_nodes.add(child)
        child_nodes.add(child)
        
    # Find the root node
    roots = all_nodes - child_nodes
    if not roots:
        print("Error: No root found in the tree structure.")
        return
        
    root = list(roots)[0]
    print(f"Root node identified: {root} (Total roots found: {len(roots)})")
    
    # Track the longest repeat matching criteria
    longest_repeat = ""
    longest_len = 0
    
    # Cache leaf counts
    leaf_counts = {}
    
    def dfs(node, current_path):
        nonlocal longest_repeat, longest_len
        
        # If leaf (no children in adj or children list is empty)
        if node not in adj or not adj[node]:
            leaf_counts[node] = 1
            return 1
            
        total_leaves = 0
        for child, start_idx, length in adj[node]:
            # Slice edge string from s using 0-based indexing
            # start_idx is 1-based, so subtract 1
            edge_str = s[start_idx - 1 : start_idx - 1 + length]
            child_path = current_path + edge_str
            
            child_leaves = dfs(child, child_path)
            total_leaves += child_leaves
            
        leaf_counts[node] = total_leaves
        
        # Check if this node has >= k leaf descendants and path does not contain '$'
        if total_leaves >= k and '$' not in current_path:
            if len(current_path) > longest_len:
                longest_len = len(current_path)
                longest_repeat = current_path
                
        return total_leaves

    dfs(root, "")
    
    print(f"Longest repeat found of length {longest_len}")
    
    with open(output_path, 'w') as f:
        f.write(longest_repeat + '\n')
        
    print(f"Result written to {output_path}")

if __name__ == '__main__':
    # Determine the directory of the script to make paths relative to it
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_lrep.txt")
    output_file = os.path.join(script_dir, "output.txt")
    solve_lrep(input_file, output_file)
