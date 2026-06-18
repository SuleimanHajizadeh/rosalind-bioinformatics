import os

def read_input(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines

def build_trie(patterns):
    trie = {1: {}}
    next_node_id = 2
    edges = []
    
    for pattern in patterns:
        curr_node = 1
        for char in pattern:
            if char not in trie[curr_node]:
                trie[curr_node][char] = next_node_id
                trie[next_node_id] = {}
                edges.append((curr_node, next_node_id, char))
                next_node_id += 1
            curr_node = trie[curr_node][char]
            
    return edges

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_trie.txt")
    
    patterns = read_input(input_path)
    print(f"Sətirlərin sayı: {len(patterns)}")
    
    edges = build_trie(patterns)
    
    output_lines = []
    for parent, child, char in edges:
        output_lines.append(f"{parent} {child} {char}")
        
    result_str = "\n".join(output_lines)
    print(f"Trie qrafının tillərinin sayı: {len(edges)}")
    print("İlk 10 til:")
    for line in output_lines[:10]:
        print(line)
        
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        out_file.write(result_str + "\n")

if __name__ == "__main__":
    main()
