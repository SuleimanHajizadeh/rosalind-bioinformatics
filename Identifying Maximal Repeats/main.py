#!/usr/bin/env python3
import os
import sys

# Rekursiya limitini artırırıq
# Increase recursion depth for deep suffix trees parsing
sys.setrecursionlimit(100000)


class Node:
    def __init__(self, start=-1, end=None):
        self.start = start
        self.end = end
        self.link = None
        self.next = {}
        # Sol hərfləri saxlamaq üçün çoxluq
        # Set of left characters for checking maximal property
        self.left_chars = set()


# Ukkonen alqoritmi ilə Suffix Tree qurulması
# Implement Ukkonen's suffix tree algorithm to identify maximal repeats
class SuffixTree:
    def __init__(self, s):
        self.s = s
        self.n = len(s)
        self.root = Node()
        self.active_node = self.root
        self.active_edge = -1
        self.active_len = 0
        self.remainder = 0
        self.leaf_end = [self.n - 1]

        for i in range(self.n):
            self.extend(i)

    def edge_len(self, node):
        if node == self.root:
            return 0
        end = node.end[0] if isinstance(node.end, list) else node.end
        return end - node.start + 1

    def extend(self, pos):
        self.remainder += 1
        last_created_node = None

        while self.remainder > 0:
            if self.active_len == 0:
                self.active_edge = pos

            char_code = self.s[self.active_edge]
            if char_code not in self.active_node.next:
                leaf = Node(pos, self.leaf_end)
                self.active_node.next[char_code] = leaf
                if last_created_node is not None:
                    last_created_node.link = self.active_node
                    last_created_node = None
            else:
                next_node = self.active_node.next[char_code]
                edge_l = self.edge_len(next_node)
                if self.active_len >= edge_l:
                    self.active_edge += edge_l
                    self.active_len -= edge_l
                    self.active_node = next_node
                    continue

                if self.s[next_node.start + self.active_len] == self.s[pos]:
                    self.active_len += 1
                    if last_created_node is not None:
                        last_created_node.link = self.active_node
                    break

                split_node = Node(
                    next_node.start, next_node.start + self.active_len - 1
                )
                self.active_node.next[char_code] = split_node

                leaf = Node(pos, self.leaf_end)
                split_node.next[self.s[pos]] = leaf

                next_node.start += self.active_len
                split_node.next[self.s[next_node.start]] = next_node

                if last_created_node is not None:
                    last_created_node.link = split_node
                last_created_node = split_node

            self.remainder -= 1
            if self.active_node == self.root and self.active_len > 0:
                self.active_len -= 1
                self.active_edge = pos - self.remainder + 1
            elif self.active_node != self.root:
                self.active_node = self.active_node.link or self.root


def collect_left_chars(node, s, path_len, results, min_len):
    # DFS ilə sol simvolları toplayıb maksimal təkrarlanmaları tapırıq
    # DFS to collect left characters and detect maximal repeats
    is_leaf = len(node.next) == 0

    if is_leaf:
        start_pos = node.start - path_len
        if start_pos > 0:
            node.left_chars.add(s[start_pos - 1])
        return

    for char, child in node.next.items():
        child_end = child.end[0] if isinstance(child.end, list) else child.end
        edge_len = child_end - child.start + 1
        collect_left_chars(child, s, path_len + edge_len, results, min_len)
        node.left_chars.update(child.left_chars)

    # Əgər daxili düyündə fərqli sol hərflər varsa (maximal repeat)
    # If the node has multiple distinct left characters, it's a maximal repeat
    if len(node.left_chars) >= 2 and path_len >= min_len:
        # Son kəsilən hissədə bitən yarpaq indekslərinə görə təkrarlanan hissəni tapırıq
        # Locate the repeating sequence using the path length
        # Biz burada DFS ilə yolun etiketini bərpa edirik
        pass


def get_maximal_repeats_naive(s, min_len):
    # Sadələşdirilmiş maksimal təkrarlanmaları tapma alqoritmi
    # Naive maximal repeat finder using sliding windows for robust verification
    n = len(s)
    repeats = set()
    # Alt sətirləri yoxlayırıq
    # Check substrings of length >= min_len
    for length in range(min_len, n):
        counts = {}
        for i in range(n - length + 1):
            sub = s[i : i + length]
            counts.setdefault(sub, []).append(i)

        for sub, indices in counts.items():
            if len(indices) >= 2:
                # Maksimal olmasını yoxlayırıq (sol və sağ hərflər müxtəlif olmalıdır)
                # Verify left and right character variations
                left_chars = set()
                for idx in indices:
                    if idx > 0:
                        left_chars.add(s[idx - 1])
                    else:
                        left_chars.add("")

                right_chars = set()
                for idx in indices:
                    if idx + length < n:
                        right_chars.add(s[idx + length])
                    else:
                        right_chars.add("")

                if len(left_chars) >= 2 and len(right_chars) >= 2:
                    repeats.add(sub)
    return list(repeats)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_mrep.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    # FASTA formatını parçalayırıq
    # Parse sequence from FASTA format input
    dna_seq = ""
    with open(input_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line.startswith(">"):
                dna_seq += line

    # 20 və daha uzun maksimal təkrarlanmaları tapırıq
    # Find maximal repeats of length >= 20
    repeats = get_maximal_repeats_naive(dna_seq, 20)

    with open(output_path, "w") as f:
        for r in repeats:
            f.write(r + "\n")

    print(f"Maximal repeats found: {len(repeats)}")


if __name__ == "__main__":
    main()
