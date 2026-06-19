#!/usr/bin/env python3
import os
import sys

# Düyünlərin dərinliyi çox olduqda rekursiya limitini artırırıq
# Increase recursion depth for deep tree structures
sys.setrecursionlimit(20000)


def tokenize(s):
    # Newick sətirini tokenlərə ayırırıq
    # Tokenize the Newick tree string
    s = s.replace(" ", "").replace("\n", "").replace("\r", "")
    tokens = []
    i = 0
    n = len(s)
    while i < n:
        if s[i] in "(),;":
            tokens.append(s[i])
            i += 1
        else:
            j = i
            while j < n and s[j] not in "(),;":
                j += 1
            tokens.append(s[i:j])
            i = j
    return tokens


def parse(tokens):
    # Tokenlərdən ağacın düyünlərini rekursiv olaraq qururuq
    # Parse tokens into tree structure recursively
    def parse_node(index):
        if index >= len(tokens):
            raise ValueError("Tokenlərin sonu gözlənilməz bitdi.")
        if tokens[index] == "(":
            children = []
            index += 1
            while True:
                child, index = parse_node(index)
                children.append(child)
                if index >= len(tokens):
                    raise ValueError("Mötərizə xətası.")
                if tokens[index] == ")":
                    index += 1
                    break
                elif tokens[index] == ",":
                    index += 1
                else:
                    raise ValueError(f"Xətalı token: {tokens[index]}")
            name = ""
            if index < len(tokens) and tokens[index] not in "(),;":
                name = tokens[index]
                index += 1
            return {"children": children, "name": name}, index
        else:
            name = tokens[index]
            return {"children": [], "name": name}, index + 1

    tree, next_index = parse_node(0)
    return tree


def get_post_order(node, post_order, parent_map):
    # Ağacı post-order ardıcıllığı ilə gəzirik
    # Traverse tree in post-order sequence
    for child in node["children"]:
        parent_map[id(child)] = node
        get_post_order(child, post_order, parent_map)
    post_order.append(node)


def solve_alph(tree_str, fasta):
    tree = parse(tokenize(tree_str))

    post_order = []
    parent_map = {}
    get_post_order(tree, post_order, parent_map)

    node_to_idx = {id(node): i for i, node in enumerate(post_order)}

    states = ["A", "C", "G", "T", "-"]
    state_to_idx = {s: i for i, s in enumerate(states)}

    first_leaf = list(fasta.keys())[0]
    L = len(fasta[first_leaf])

    internal_seqs = {
        node["name"]: [] for node in post_order if node["children"]
    }

    total_cost = 0

    def cost(s1, s2):
        return 0 if s1 == s2 else 1

    # Hər bir sütun üzrə Sankoff alqoritmini tətbiq edirik
    # Apply Sankoff's algorithm for parsimonious tree reconstruction column-by-column
    for col in range(L):
        dp = [[float("inf")] * 5 for _ in range(len(post_order))]

        for idx, node in enumerate(post_order):
            if not node["children"]:
                char = fasta[node["name"]][col]
                if char in state_to_idx:
                    dp[idx][state_to_idx[char]] = 0
            else:
                for s in range(5):
                    sum_min_child = 0
                    for child in node["children"]:
                        child_idx = node_to_idx[id(child)]
                        min_child_cost = min(
                            dp[child_idx][sc] + cost(states[s], states[sc])
                            for sc in range(5)
                        )
                        sum_min_child += min_child_cost
                    dp[idx][s] = sum_min_child

        root_idx = len(post_order) - 1
        min_root_cost = min(dp[root_idx])
        total_cost += min_root_cost

        assigned = [None] * len(post_order)
        best_root_states = [
            s for s in range(5) if dp[root_idx][s] == min_root_cost
        ]
        assigned[root_idx] = best_root_states[0]

        # Geri izləmə ilə daxili düyünlərin simvollarını bərpa edirik
        # Backtrack to assign states to internal nodes
        for idx in reversed(range(len(post_order) - 1)):
            node = post_order[idx]
            parent = parent_map[id(node)]
            parent_idx = node_to_idx[id(parent)]
            s_p = assigned[parent_idx]

            best_s = None
            min_val = float("inf")
            for s in range(5):
                val = dp[idx][s] + cost(states[s_p], states[s])
                if val < min_val:
                    min_val = val
                    best_s = s
            assigned[idx] = best_s

        for idx, node in enumerate(post_order):
            if node["children"]:
                internal_seqs[node["name"]].append(states[assigned[idx]])

    for name in internal_seqs:
        internal_seqs[name] = "".join(internal_seqs[name])

    return total_cost, internal_seqs


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_alph.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        return

    tree_str = lines[0]
    fasta_lines = lines[1:]

    fasta = {}
    current_key = None
    for line in fasta_lines:
        if line.startswith(">"):
            current_key = line[1:]
            fasta[current_key] = []
        else:
            fasta[current_key].append(line)

    for k in fasta:
        fasta[k] = "".join(fasta[k])

    cost, internal_seqs = solve_alph(tree_str, fasta)
    print(f"Düzülüşün minimal xalı (dH): {cost}")

    with open(output_path, "w") as f:
        f.write(f"{cost}\n")
        for name in sorted(internal_seqs.keys()):
            f.write(f">{name}\n")
            f.write(f"{internal_seqs[name]}\n")


if __name__ == "__main__":
    main()
