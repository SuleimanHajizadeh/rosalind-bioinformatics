import os

# Suffix tree alqoritmi ilə verilmiş mətndən suffix ağacı qururuq
# Build a compressed suffix trie (suffix tree) from the given text


def build_suffix_tree(s):
    # Düyünləri lüğət (dict) olaraq təmsil edirik
    # Represent each node as a dictionary mapping char to edge
    root = {}

    for i in range(len(s)):
        suffix = s[i:]
        node = root
        j = 0
        while j < len(suffix):
            c = suffix[j]
            if c not in node:
                node[c] = [suffix[j:], {}]
                break

            edge_label, children = node[c]
            k = 0
            while k < len(edge_label) and suffix[j + k] == edge_label[k]:
                k += 1

            if k == len(edge_label):
                node = children
                j += k
            else:
                # Eyni olan hissədən sonra tilləri bölürük
                # Split edge_label at mismatch point
                matched = edge_label[:k]
                unmatched_edge = edge_label[k:]
                unmatched_suffix = suffix[j + k :]

                mid_node = {}
                node[c] = [matched, mid_node]

                mid_node[unmatched_edge[0]] = [unmatched_edge, children]
                mid_node[unmatched_suffix[0]] = [unmatched_suffix, {}]
                break
    return root


def collect_edges(node, edges):
    # Suffix ağacındakı bütün tillərin etiketlərini toplayırıq
    # Collect all edge labels recursively from the tree
    for first_char, (edge_label, children) in node.items():
        edges.append(edge_label)
        collect_edges(children, edges)


def solve_suff(input_path, output_path):
    with open(input_path, "r") as f:
        s = f.read().strip()

    if not s.endswith("$"):
        s += "$"

    root = build_suffix_tree(s)

    edges = []
    collect_edges(root, edges)

    # Bütün tillərin etiketlərini fayla yazırıq
    # Write all edge labels to output.txt
    with open(output_path, "w") as f:
        for edge in edges:
            # Sona əlavə edilmiş köməkçi '$' işarəsini təmizləyirik (əgər təkdirsə, yazmırıq)
            # Filter out internal helper suffix character if standalone
            if edge == "$":
                continue
            f.write(edge + "\n")

    print(f"Edges collected: {len(edges)}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_suff.txt")
    output_file = os.path.join(script_dir, "output.txt")
    solve_suff(input_file, output_file)
