# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba9b.txt")
    if not os.path.exists(input_file):
        return "", []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0], lines[1:]

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

# TrieMatching alqoritmi
# Implement TrieMatching
def trie_matching(text, trie):
    positions = []
    for i in range(len(text)):
        # Hər mövqedən başlayaraq trie-də axtarış edirik
        # Search trie starting from index i
        curr_node = 0
        idx = i
        matched = False
        while idx < len(text):
            symbol = text[idx]
            if symbol in trie[curr_node]:
                curr_node = trie[curr_node][symbol]
                # Yarpaq tapılıbsa, bu pattern tapılmış sayılır
                # If leaf reached, match is successful
                if not trie[curr_node]:
                    matched = True
                    break
                idx += 1
            else:
                break
        if matched or (curr_node in trie and not trie[curr_node]):
            positions.append(i)
    return positions

def main():
    text, patterns = read_input()
    if not text:
        return
    trie = construct_trie(patterns)
    result = trie_matching(text, trie)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(map(str, result)) + "\n")

if __name__ == "__main__":
    main()
