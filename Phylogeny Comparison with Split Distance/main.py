#!/usr/bin/env python3
import os
import sys

# Rekursiya limitini artırırıq
# Increase recursion limit
sys.setrecursionlimit(20000)


def tokenize(s):
    s = s.replace(" ", "").replace("\n", "").replace("\r", "")
    tokens = []
    i = 0
    n = len(s)
    while i < n:
        if s[i] in "(),;":
            tokens.append(s[i])
            i += 1
        else:
            start = i
            while i < n and s[i] not in "(),;":
                i += 1
            name = s[start:i].strip()
            if name:
                tokens.append(name)
    return tokens


# İki ağac arasındakı split məsafəsini (split distance) hesablayırıq
# Compute split distance between two phylogenetic trees
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_spd.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    # Ağacları oxuyuruq
    # Read the trees representation
    pass
