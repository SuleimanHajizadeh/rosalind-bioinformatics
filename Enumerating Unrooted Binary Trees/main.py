import os

# Yeni yarpağı ağacın müxtəlif mövqelərinə yerləşdiririk
# Insert a new leaf into all possible edge positions of the tree representation


def insert_leaf(tree, leaf):
    results = []
    # Mövcud kökün üzərində yeni budaq yaradırıq
    # Insert above the current root
    results.append((tree, leaf))

    if isinstance(tree, tuple):
        left, right = tree
        # Sol alt ağaca rekursiv yerləşdiririk
        # Insert inside left subtree
        for new_left in insert_leaf(left, leaf):
            results.append((new_left, right))
        # Sağ alt ağaca rekursiv yerləşdiririk
        # Insert inside right subtree
        for new_right in insert_leaf(right, leaf):
            results.append((left, new_right))

    return results


def format_tree(tree):
    # Ağacı mötərizəli Newick formatında yazırıq
    # Format tree structure to Newick text representation
    if isinstance(tree, str):
        return tree
    left, right = tree
    return f"({format_tree(left)},{format_tree(right)})"


def generate_unrooted_trees(taxa):
    if len(taxa) < 3:
        return []

    root_taxon = taxa[0]
    other_taxa = taxa[1:]

    # İlk digər yarpaq ilə başlayırıq
    # Initialize with the first available leaf node
    trees = [other_taxa[0]]

    # Növbəti yarpaqları növbə ilə ağac variantlarına yerləşdiririk
    # Iteratively insert all remaining taxa leaves
    for leaf in other_taxa[1:]:
        new_trees = []
        for t in trees:
            new_trees.extend(insert_leaf(t, leaf))
        trees = new_trees

    # Nəticələri Newick formatında yığırıq
    # Format each resulting tree to Newick text
    newick_trees = []
    for t in trees:
        newick_str = f"({format_tree(t)}){root_taxon};"
        newick_trees.append(newick_str)

    return newick_trees


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, "rosalind_eubt.txt")
    output_path = os.path.join(base_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        lines = f.read().splitlines()

    taxa = lines[0].strip().split()
    newick_trees = generate_unrooted_trees(taxa)

    with open(output_path, "w") as f:
        for tree in newick_trees:
            f.write(tree + "\n")

    print(f"Generated unrooted trees count: {len(newick_trees)}")


if __name__ == "__main__":
    main()
