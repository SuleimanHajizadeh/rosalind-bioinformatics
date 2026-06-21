# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba9r.txt")
    if not os.path.exists(input_file):
        return "", [], []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    text = lines[0]
    sa = list(map(int, lines[1].split(",")))
    lcp = list(map(int, lines[2].split(",")))
    return text, sa, lcp

# LCP massivi və Suffix Array vasitəsilə Suffix Tree tillərini tapırıq
# Construct a Suffix Tree from a Suffix Array and LCP array
def suffix_tree_from_sa(text, sa, lcp):
    # Sadə həll üçün suffikslərdən normal sıxılmış ağac qurulmasını tətbiq edə bilərik
    # We construct the suffix tree using the standard suffix tree construction
    n = len(text)
    trie = {0: {}}
    next_node = 1
    
    for idx in sa:
        curr = 0
        for char in text[idx:]:
            if char in trie[curr]:
                curr = trie[curr][char]
            else:
                trie[curr][char] = next_node
                trie[next_node] = {}
                curr = next_node
                next_node += 1
                
    edges = []
    def compress(node, path_str):
        if not trie[node]:
            edges.append(path_str)
            return
        if len(trie[node]) > 1 or node == 0:
            if path_str:
                edges.append(path_str)
            for char, child in trie[node].items():
                compress(child, char)
        else:
            char = next(iter(trie[node].keys()))
            child = trie[node][char]
            compress(child, path_str + char)
            
    compress(0, "")
    return edges

def main():
    text, sa, lcp = read_input()
    if not text:
        return
    edges = suffix_tree_from_sa(text, sa, lcp)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(edges) + "\n")

if __name__ == "__main__":
    main()
