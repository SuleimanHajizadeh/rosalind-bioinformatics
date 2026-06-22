# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba9o.txt")
    if not os.path.exists(input_file):
        return "", [], 0
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    text = lines[0]
    patterns = lines[1].split()
    d = int(lines[2])
    return text, patterns, d

# Təxmini naxış axtarışı üçün Trie qurmaq və axtarmaq
# Build Trie and search for approximate pattern matching
def approximate_pattern_matching_all(text, patterns, d):
    # Trie qurmaq
    # Build Trie
    trie = {}
    for p_idx, pattern in enumerate(patterns):
        node = trie
        for char in pattern:
            if char not in node:
                node[char] = {}
            node = node[char]
        if '$' not in node:
            node['$'] = []
        node['$'].append(p_idx)

    results = []
    text_len = len(text)

    # Hər bir başlanğıc mövqeyi üçün Trie üzərində DFS axtarışı
    # DFS search on Trie for each starting position
    for start_pos in range(text_len):
        def dfs(node, text_idx, mismatches):
            # Əgər cari düyündə naxış bitirsə, uyğunluğu qeyd et
            # If pattern ends at the current node, record the match
            if '$' in node:
                for _ in node['$']:
                    results.append(start_pos)
            
            # Mətnin sonuna çatdıqda axtarışı dayandır
            # Stop search when reaching the end of the text
            if text_idx >= text_len:
                return

            char = text[text_idx]
            
            # 1. Simvol uyğun gəldikdə keçid
            # 1. Transition when character matches
            if char in node:
                dfs(node[char], text_idx + 1, mismatches)
            
            # 2. Simvol uyğun gəlmədikdə (mismatch) keçidlər
            # 2. Transitions when character mismatches
            if mismatches < d:
                for child_char, child_node in node.items():
                    if child_char != char and child_char != '$':
                        dfs(child_node, text_idx + 1, mismatches + 1)

        dfs(trie, start_pos, 0)

    # Mövqeləri artan sıra ilə çeşidləmək (dublikatları saxlayaraq)
    # Sort positions in non-decreasing order (keeping duplicates)
    return sorted(results)

def main():
    text, patterns, d = read_input()
    if not text:
        return
    result = approximate_pattern_matching_all(text, patterns, d)
    
    # Nəticələri fayla yazmaq
    # Write results to file
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(map(str, result)) + "\n")

if __name__ == "__main__":
    main()
