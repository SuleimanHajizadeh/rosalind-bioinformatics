import os


def build_suffix_tree(s):
    """
    Build a compressed suffix trie (suffix tree) naively in O(n^2).
    Each node is represented as a dict mapping first_char -> [edge_label, children_dict].
    Since s ends with '$' (unique), no suffix is a prefix of another.
    """
    root = {}

    for i in range(len(s)):
        suffix = s[i:]
        node = root
        j = 0
        while j < len(suffix):
            c = suffix[j]
            if c not in node:
                # Remaining suffix becomes a new leaf edge
                node[c] = [suffix[j:], {}]
                break

            edge_label, children = node[c]
            # Find longest common prefix of edge_label and suffix[j:]
            k = 0
            while k < len(edge_label) and suffix[j + k] == edge_label[k]:
                k += 1

            if k == len(edge_label):
                # Fully matched this edge — continue down the tree
                node = children
                j += k
            else:
                # Partial match — split the edge
                common   = edge_label[:k]
                rest_old = edge_label[k:]
                rest_new = suffix[j + k:]

                internal = {}
                internal[rest_old[0]] = [rest_old, children]
                if rest_new:
                    internal[rest_new[0]] = [rest_new, {}]
                node[c] = [common, internal]
                break

    return root


def collect_edges(node):
    """DFS to collect all edge labels in the suffix tree."""
    result = []
    for label, children in node.values():
        result.append(label)
        result.extend(collect_edges(children))
    return result


def solve_suff(input_path, output_path):
    with open(input_path, 'r') as f:
        s = f.read().strip()

    # Ensure the string ends with '$'
    if not s.endswith('$'):
        s += '$'

    tree  = build_suffix_tree(s)
    edges = collect_edges(tree)

    result = '\n'.join(edges)
    with open(output_path, 'w') as f:
        f.write(result + '\n')

    print(result)


if __name__ == '__main__':
    base = os.path.dirname(os.path.abspath(__file__))
    solve_suff(
        os.path.join(base, 'rosalind_suff.txt'),
        os.path.join(base, 'output.txt'),
    )
