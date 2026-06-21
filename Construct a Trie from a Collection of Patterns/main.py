# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba9a.txt")
    if not os.path.exists(input_file):
        return []
    with open(input_file, "r") as f:
        return [line.strip() for line in f if line.strip()]

# Sətirlər toplusundan Trie ağacı qururuq
# Construct a trie from a collection of patterns
def construct_trie(patterns):
    trie = {0: {}}
    next_node = 1
    
    for pattern in patterns:
        curr_node = 0
        for symbol in pattern:
            if symbol in trie[curr_node]:
                curr_node = trie[curr_node][symbol]
            else:
                trie[curr_node][symbol] = next_node
                trie[next_node] = {}
                curr_node = next_node
                next_node += 1
    return trie

def main():
    patterns = read_input()
    if not patterns:
        return
    trie = construct_trie(patterns)
    
    # Tilləri formatlayırıq: parent->child:symbol
    # Format edge output
    output_lines = []
    for parent in sorted(trie.keys()):
        for symbol, child in sorted(trie[parent].items(), key=lambda x: x[1]):
            output_lines.append(f"{parent}->{child}:{symbol}")
            
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(output_lines) + "\n")

if __name__ == "__main__":
    main()
