# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba9c.txt")
    if not os.path.exists(input_file):
        return ""
    with open(input_file, "r") as f:
        return f.read().strip()

# Sadə Ukkonen və ya trie sıxılması metodu ilə suffix tree qurulması
# Construct suffix tree of a string by compressing a suffix trie
def construct_suffix_tree(text):
    n = len(text)
    # Bütün suffiksləri trie-yə əlavə edirik
    # Add all suffixes to a trie
    trie = {0: {}}
    next_node = 1
    
    for i in range(n):
        curr = 0
        for char in text[i:]:
            if char in trie[curr]:
                curr = trie[curr][char]
            else:
                trie[curr][char] = next_node
                trie[next_node] = {}
                curr = next_node
                next_node += 1
                
    # Budaqlanmayan yolları sıxırıq
    # Compress non-branching paths recursively
    edges = []
    
    def compress(node, path_str):
        if not trie[node]:
            # Yarpaq düyün, yolu əlavə edirik
            # Leaf reached, add path
            edges.append(path_str)
            return
        if len(trie[node]) > 1 or node == 0:
            # Budaqlanma düyünü
            # Branching node
            if path_str:
                edges.append(path_str)
            for char, child in trie[node].items():
                compress(child, char)
        else:
            # Tək uşağı olan düyün - sıxırıq
            # Single child - merge paths
            char = next(iter(trie[node].keys()))
            child = trie[node][char]
            compress(child, path_str + char)
            
    compress(0, "")
    return edges

def main():
    text = read_input()
    if not text:
        return
    edges = construct_suffix_tree(text)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(edges) + "\n")

if __name__ == "__main__":
    main()
