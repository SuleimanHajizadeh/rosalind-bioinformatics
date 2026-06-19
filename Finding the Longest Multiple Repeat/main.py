import sys
import os

# Suffix ağacından ən uzun çoxlu təkrarlanan motifi tapırıq
# Find the longest repeat appearing at least k times using suffix tree data structure


def solve_lrep(input_path, output_path):
    # Suffix ağacı dərin olduqda rekursiya limitini artırırıq
    # Increase recursion depth for deep suffix trees parsing
    sys.setrecursionlimit(200000)

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    if len(lines) < 2:
        return

    s = lines[0]
    k = int(lines[1])

    # Qraf tillərini oxuyuruq
    # Parse parent, child, start_index, and length representation
    adj = {}
    all_nodes = set()
    child_nodes = set()

    for line in lines[2:]:
        parts = line.split()
        if len(parts) != 4:
            continue
        parent, child, start_str, len_str = parts
        start_idx = int(start_str)
        length = int(len_str)

        if parent not in adj:
            adj[parent] = []
        adj[parent].append((child, start_idx, length))

        all_nodes.add(parent)
        all_nodes.add(child)
        child_nodes.add(child)

    # Kök düyünü tapırıq
    # Identify the root node
    roots = all_nodes - child_nodes
    root = list(roots)[0]

    longest_repeat = ""
    longest_len = 0
    leaf_counts = {}

    # DFS vasitəsilə ən azı k sayda yarpaq varisi olan ən uzun yolu tapırıq
    # Run DFS to calculate leaf descendants and track the longest repeat path
    def dfs(node, current_path):
        nonlocal longest_repeat, longest_len

        # Əgər yarpaq düyündürsə (leaf node)
        # Return 1 if current node is a leaf
        if node not in adj or not adj[node]:
            leaf_counts[node] = 1
            return 1

        total_leaves = 0
        for child, start_idx, length in adj[node]:
            edge_str = s[start_idx - 1 : start_idx - 1 + length]
            child_path = current_path + edge_str

            child_leaves = dfs(child, child_path)
            total_leaves += child_leaves

        leaf_counts[node] = total_leaves

        # Şərti yoxlayırıq: varis yarpaq sayı >= k olmalı və '$' olmamalıdır
        # Verify repeat constraints: count >= k and must exclude helper '$' character
        if total_leaves >= k and "$" not in current_path:
            if len(current_path) > longest_len:
                longest_len = len(current_path)
                longest_repeat = current_path

        return total_leaves

    dfs(root, "")

    print(f"Longest Repeat: {longest_repeat} (len={longest_len})")

    with open(output_path, "w") as f:
        f.write(longest_repeat + "\n")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_lrep.txt")
    output_file = os.path.join(script_dir, "output.txt")
    solve_lrep(input_file, output_file)
