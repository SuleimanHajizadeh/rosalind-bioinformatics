"""
Rosalind: Quartet Distance (QRTD)

For two UNROOTED BINARY TREES T1 and T2 on n taxa:
  dq(T1, T2) = q(T1) + q(T2) - 2*q(T1, T2)

Since both trees are binary, EVERY 4-subset is resolved, so:
  q(T1) = q(T2) = C(n, 4)
  dq = 2*C(n,4) - 2*q(T1,T2)

ALGORITHM for q(T1,T2) in O(n^2):
Root both trees at the SAME LEAF r (lexicographically first taxon).
For each internal node u in T1 (with left/right child subtrees L1,R1):
  For each internal node v in T2 (with left/right child subtrees L2,R2):
    Let S1=L1∪R1, S2=L2∪R2, S1^c = complement of S1 (in all leaves except r),
        S2^c = complement of S2.
    a = |S1 ∩ S2|,  b = |S1 ∩ S2^c|,  c = |S1^c ∩ S2|,  d = |S1^c ∩ S2^c|
    Non-root quartets: C(a,2)*C(d,2) + C(b,2)*C(c,2)
    Root-involving:   (|L1∩L2|*|R1∩R2| + |L1∩R2|*|R1∩L2|) * d
    Total contribution += above sum.
"""

import sys
from math import comb


# ---------------------------------------------------------------------------
# Newick parser
# ---------------------------------------------------------------------------

def parse_newick(s: str):
    """Parse Newick. Returns root as dict {name, children: [...]}."""
    s = s.strip().rstrip(';').strip()
    pos = [0]

    def parse_node():
        node = {'name': None, 'children': []}
        if pos[0] < len(s) and s[pos[0]] == '(':
            pos[0] += 1
            node['children'].append(parse_node())
            while pos[0] < len(s) and s[pos[0]] == ',':
                pos[0] += 1
                node['children'].append(parse_node())
            assert pos[0] < len(s) and s[pos[0]] == ')'
            pos[0] += 1
        label = []
        while pos[0] < len(s) and s[pos[0]] not in (',', ')', '(', ';'):
            if s[pos[0]] == ':':
                pos[0] += 1
                while pos[0] < len(s) and s[pos[0]] not in (',', ')', '(', ';'):
                    pos[0] += 1
                break
            label.append(s[pos[0]])
            pos[0] += 1
        lbl = ''.join(label).strip()
        if lbl:
            node['name'] = lbl
        return node

    return parse_node()


# ---------------------------------------------------------------------------
# Build adjacency list from Newick (treating as unrooted)
# ---------------------------------------------------------------------------

def build_adj(node, adj, node_list):
    """Build undirected adjacency. Returns node's integer ID."""
    nid = len(node_list)
    node_list.append(node['name'])  # None for internal, name for leaf
    adj[nid] = []
    for child in node['children']:
        cid = build_adj(child, adj, node_list)
        adj[nid].append(cid)
        adj[cid].append(nid)
    return nid


# ---------------------------------------------------------------------------
# Root the unrooted tree at a specific leaf and collect internal nodes.
# Each internal node gets: (left_mask, right_mask) of its two child subtrees.
# Also compute S_mask = left | right, Sc_mask = all_nonroot_mask ^ S_mask.
# ---------------------------------------------------------------------------

def collect_internal_nodes(adj, node_names, leaf_idx, root_leaf_id):
    """
    DFS from root_leaf_id's neighbor. Computes subtree bitmasks.
    Returns list of (L_mask, R_mask) for each non-root internal node.
    """
    # The rooted root = the unique neighbor of root_leaf_id
    assert len(adj[root_leaf_id]) == 1, "Root leaf should have exactly 1 neighbor"
    rooted_root = adj[root_leaf_id][0]

    # Subtree bitmask: leaves below this node (excluding root_leaf_id direction)
    subtree_mask = {}
    internal_nodes = []  # list of (L_mask, R_mask)

    def dfs(nid, parent_id):
        name = node_names[nid]
        children = [nb for nb in adj[nid] if nb != parent_id]

        if not children:
            # Leaf node
            idx = leaf_idx.get(name, -1)
            mask = (1 << idx) if idx >= 0 else 0
            subtree_mask[nid] = mask
            return mask

        # Internal node: should have exactly 2 children in a rooted binary tree
        assert len(children) == 2, (
            f"Expected 2 children for internal node {name}, got {len(children)}"
        )
        c1, c2 = children
        m1 = dfs(c1, nid)
        m2 = dfs(c2, nid)
        mask = m1 | m2
        subtree_mask[nid] = mask
        # Record this internal node: (left_mask, right_mask)
        # We do not record the rooted_root because its incoming edge is not internal
        if nid != rooted_root:
            internal_nodes.append((m1, m2))
        return mask

    dfs(rooted_root, root_leaf_id)
    return internal_nodes


# ---------------------------------------------------------------------------
# Compute q(T1, T2)
# ---------------------------------------------------------------------------

def compute_shared_q(nodes1, nodes2, all_mask):
    """
    nodes1: list of (L1, R1) masks from T1 internal nodes (non-root).
    nodes2: list of (L2, R2) masks from T2 internal nodes (non-root).
    all_mask: bitmask of all leaves.

    For each pair of internal edges (e1, e2):
      Let F2 = L1, F3 = R1, F1 = all_mask ^ (F2 | F3)
      Let G2 = L2, G3 = R2, G1 = all_mask ^ (G2 | G3)
      c_F1G1 = popcount(F1 & G1)
      c_F2G2 = popcount(F2 & G2)
      c_F3G3 = popcount(F3 & G3)
      c_F2G3 = popcount(F2 & G3)
      c_F3G2 = popcount(F3 & G2)
      shared += C(c_F1G1, 2) * (c_F2G2 * c_F3G3 + c_F2G3 * c_F3G2)
    """
    shared = 0
    for (L1, R1) in nodes1:
        F2 = L1
        F3 = R1
        F1 = all_mask ^ (F2 | F3)
        for (L2, R2) in nodes2:
            G2 = L2
            G3 = R2
            G1 = all_mask ^ (G2 | G3)

            c_F1G1 = bin(F1 & G1).count('1')
            if c_F1G1 >= 2:
                c_F2G2 = bin(F2 & G2).count('1')
                c_F3G3 = bin(F3 & G3).count('1')
                c_F2G3 = bin(F2 & G3).count('1')
                c_F3G2 = bin(F3 & G2).count('1')
                shared += comb(c_F1G1, 2) * (c_F2G2 * c_F3G3 + c_F2G3 * c_F3G2)

    return shared


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    data = sys.stdin.read().split('\n')
    taxa_list = data[0].strip().split()
    taxa_set = set(taxa_list)
    t1_str = data[1].strip()
    t2_str = data[2].strip()

    n = len(taxa_set)
    sorted_taxa = sorted(taxa_set)
    leaf_idx = {leaf: i for i, leaf in enumerate(sorted_taxa)}

    # Root leaf: lexicographically first taxon
    root_leaf = sorted_taxa[0]

    # Bitmask of ALL leaves
    all_mask = (1 << n) - 1

    # Parse trees
    tree1 = parse_newick(t1_str)
    tree2 = parse_newick(t2_str)

    # Build adjacency lists
    adj1, nodes1_names = {}, []
    build_adj(tree1, adj1, nodes1_names)
    adj2, nodes2_names = {}, []
    build_adj(tree2, adj2, nodes2_names)

    # Find the root leaf node ID in each adjacency
    def find_leaf_id(node_names, leaf_name):
        for i, name in enumerate(node_names):
            if name == leaf_name:
                return i
        raise ValueError(f"Leaf {leaf_name} not found")

    root1_id = find_leaf_id(nodes1_names, root_leaf)
    root2_id = find_leaf_id(nodes2_names, root_leaf)

    # Collect internal nodes with their child subtree bitmasks
    int_nodes1 = collect_internal_nodes(adj1, nodes1_names, leaf_idx, root1_id)
    int_nodes2 = collect_internal_nodes(adj2, nodes2_names, leaf_idx, root2_id)

    # Compute shared quartets
    shared = compute_shared_q(int_nodes1, int_nodes2, all_mask)

    # Quartet distance
    dq = 2 * comb(n, 4) - 2 * shared
    print(dq)


if __name__ == '__main__':
    main()
