import os
import sys

# Newick ağacının düyününü təmsil edən sinif
# Node class for representing Newick tree hierarchy


class Node:
    def __init__(self, name=None):
        self.name = name
        self.children = []


def parse_newick(s):
    # Newick sətirini obyekt strukturuna çeviririk
    # Parse Newick string format to node objects
    s = s.strip()
    if s.endswith(";"):
        s = s[:-1]

    stack = []
    root = Node()
    curr = root
    i = 0
    n = len(s)
    # Ağac düyünlərini gəzirik
    # Traverse tree nodes
    while i < n:
        c = s[i]
        if c == "(":
            new_node = Node()
            curr.children.append(new_node)
            stack.append(curr)
            curr = new_node
            i += 1
        elif c == ",":
            parent = stack[-1]
            new_node = Node()
            parent.children.append(new_node)
            curr = new_node
            i += 1
        elif c == ")":
            curr = stack.pop()
            i += 1
        else:
            name_chars = []
            while i < n and s[i] not in "(),;":
                name_chars.append(s[i])
                i += 1
            name = "".join(name_chars).strip()
            if name:
                curr.name = name
    return root


def build_adjacency_list(root):
    # Ağacdan adj (qonşuluq siyahısı) matrisini qururuq
    # Build bidirectional adjacency list from tree nodes representation
    adj = {}

    def dfs(node):
        if node.name:
            adj.setdefault(node.name, [])
        for child in node.children:
            if child.name:
                adj.setdefault(child.name, [])
            # Düyünləri qarşılıqlı birləşdiririk
            # Connect parent and child nodes
            if node.name and child.name:
                adj[node.name].append(child.name)
                adj[child.name].append(node.name)
            dfs(child)

    dfs(root)
    return adj


def find_distance(adj, u, v):
    # BFS vasitəsilə iki düyün arasındakı ən qısa məsafəni tapırıq
    # Find shortest distance between u and v using BFS
    if u == v:
        return 0
    q = [(u, 0)]
    visited = {u}
    while q:
        curr, dist = q.pop(0)
        for nxt in adj.get(curr, []):
            if nxt == v:
                return dist + 1
            if nxt not in visited:
                visited.add(nxt)
                q.append((nxt, dist + 1))
    return -1


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_nkew.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        sys.exit(1)

    with open(input_path, "r") as f:
        content = f.read().strip()

    blocks = content.split("\n\n")
    results = []

    for block in blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        if len(lines) < 2:
            continue
        tree_str = lines[0]
        u, v = lines[1].split()

        root = parse_newick(tree_str)
        adj = build_adjacency_list(root)
        dist = find_distance(adj, u, v)
        results.append(dist)

    result_str = " ".join(map(str, results))
    print(result_str)

    with open(output_path, "w") as f:
        f.write(result_str + "\n")


if __name__ == "__main__":
    main()
