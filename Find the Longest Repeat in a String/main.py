# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba9d.txt")
    if not os.path.exists(input_file):
        return ""
    with open(input_file, "r") as f:
        return f.read().strip()

def construct_suffix_trie(text):
    trie = {0: {}}
    next_node = 1
    for i in range(len(text)):
        curr = 0
        for char in text[i:]:
            if char in trie[curr]:
                curr = trie[curr][char]
            else:
                trie[curr][char] = next_node
                trie[next_node] = {}
                curr = next_node
                next_node += 1
    return trie

# Suffix tree/trie-də ən uzun təkrarlanan alt sətiri (longest repeat) tapırıq
# Find the longest repeat in a string
def longest_repeat(text):
    trie = construct_suffix_trie(text + "$")
    
    # Ən çox daxili budaqlanan və yarpaq olmayan yollar ən uzun təkrarı verir
    # Internal nodes with branching paths correspond to repeated substrings
    best = ""
    
    # DFS ilə bütün ağacı gəzirik və ən uzun təkrarlanan yolları tapırıq
    # DFS search for deepest internal node
    stack = [(0, "")]
    while stack:
        node, path = stack.pop()
        if len(trie[node]) >= 2:
            if len(path) > len(best):
                best = path
        for char, child in trie[node].items():
            if char != "$":
                stack.append((child, path + char))
    return best

def main():
    text = read_input()
    if not text:
        return
    result = longest_repeat(text)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(result + "\n")

if __name__ == "__main__":
    main()
