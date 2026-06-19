import os
import sys

# DNT sətirlərindən prefiks ağacı (Trie) qururuq
# Build a Trie (Prefix Tree) from a set of DNA strings


def read_input(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines


def build_trie(patterns):
    # Düyünləri nömrələyərək Trie qrafını qururuq
    # Construct the trie where each node has a unique identifier
    trie = {1: {}}
    node_count = 1

    for pattern in patterns:
        curr_node = 1
        for char in pattern:
            if char in trie[curr_node]:
                curr_node = trie[curr_node][char]
            else:
                node_count += 1
                trie[curr_node][char] = node_count
                trie[node_count] = {}
                curr_node = node_count
    return trie


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_trie.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        sys.exit(1)

    patterns = read_input(input_path)
    trie = build_trie(patterns)

    # Trie tillərini (keçidləri) output.txt-yə yazırıq
    # Output the adjacency list of transitions to output.txt
    with open(output_path, "w") as out:
        for node, edges in trie.items():
            for char, child in edges.items():
                out.write(f"{node} {child} {char}\n")

    print(f"Nodes in Trie: {len(trie)}")


if __name__ == "__main__":
    main()
