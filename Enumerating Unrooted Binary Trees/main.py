import os

def insert_leaf(tree, leaf):
    # tree can be a string (leaf) or a tuple (left, right)
    results = []
    
    # Option 1: insert above the current root
    results.append((tree, leaf))
    
    # Option 2: insert inside the subtrees if current node is internal
    if isinstance(tree, tuple):
        left, right = tree
        # Insert inside left subtree
        for new_left in insert_leaf(left, leaf):
            results.append((new_left, right))
        # Insert inside right subtree
        for new_right in insert_leaf(right, leaf):
            results.append((left, new_right))
            
    return results

def format_tree(tree):
    if isinstance(tree, str):
        return tree
    left, right = tree
    return f"({format_tree(left)},{format_tree(right)})"

def generate_unrooted_trees(taxa):
    if len(taxa) < 3:
        return []
    
    root_taxon = taxa[0]
    other_taxa = taxa[1:]
    
    # Initialize with the first of other_taxa
    trees = [other_taxa[0]]
    
    # Iteratively insert the remaining taxa
    for leaf in other_taxa[1:]:
        new_trees = []
        for t in trees:
            new_trees.extend(insert_leaf(t, leaf))
        trees = new_trees
        
    # Format each tree as Newick: (T)root_taxon;
    newick_trees = []
    for t in trees:
        newick_str = f"({format_tree(t)}){root_taxon};"
        newick_trees.append(newick_str)
        
    return newick_trees

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, 'rosalind_eubt.txt')
    output_path = os.path.join(base_dir, 'output.txt')
    
    with open(input_path, 'r') as f:
        lines = f.read().splitlines()
        
    taxa = lines[0].strip().split()
    
    newick_trees = generate_unrooted_trees(taxa)
    
    with open(output_path, 'w') as f:
        for tree in newick_trees:
            f.write(tree + '\n')
            
    print(f"Generated {len(newick_trees)} trees.")
    for tree in newick_trees[:5]:
        print(tree)
    if len(newick_trees) > 5:
        print("...")

if __name__ == '__main__':
    main()
