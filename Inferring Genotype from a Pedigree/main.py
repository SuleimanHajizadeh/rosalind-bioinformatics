#!/usr/bin/env python3
import os
import sys

# Pedigri ağacında fərdlərin ehtimallarına görə genotip paylanmasını tapırıq
# Compute the probability of dominant and recessive genotypes using a pedigree structure


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_mend.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        sys.exit(1)

    with open(input_path, "r") as f:
        tree_str = f.read().strip()

    # Newick sətirini tokenlərə ayırırıq
    # Tokenize tree string
    if tree_str.endswith(";"):
        tree_str = tree_str[:-1]

    tokens = []
    i = 0
    n = len(tree_str)
    while i < n:
        if tree_str[i] in "(),":
            tokens.append(tree_str[i])
            i += 1
        else:
            start = i
            while i < n and tree_str[i] not in "(),":
                i += 1
            name = tree_str[start:i].strip()
            if name:
                tokens.append(name)

    # Rekursiv olaraq ehtimalları hesablayırıq
    # Recursively calculate genotype probabilities
    # Genotiplər: [AA, Aa, aa]
    # Genotypes order: [AA, Aa, aa]
    stack = []

    def combine(p1, p2):
        # İki valideynin ehtimallarından uşağın ehtimalını tapırıq
        # Compute child genotype probability from parent probabilities
        AA = p1[0] * p2[0] + 0.5 * (p1[0] * p2[1] + p1[1] * p2[0]) + 0.25 * (p1[1] * p2[1])
        Aa = (
            p1[0] * p2[2]
            + p1[2] * p2[0]
            + 0.5 * (p1[0] * p2[1] + p1[1] * p2[0])
            + 0.5 * (p1[1] * p2[1])
            + 0.5 * (p1[1] * p2[2] + p1[2] * p2[1])
        )
        aa = p1[2] * p2[2] + 0.5 * (p1[1] * p2[2] + p1[2] * p2[1]) + 0.25 * (p1[1] * p2[1])
        return [AA, Aa, aa]

    # Post-order yığın emalı
    # Process tokens using stack hierarchy
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t == "(":
            i += 1
        elif t == ",":
            i += 1
        elif t == ")":
            # İki valideyn alt-düyününü yığından götürüb birləşdiririk
            # Pop parents and combine probabilities
            p2 = stack.pop()
            p1 = stack.pop()
            stack.append(combine(p1, p2))
            i += 1
        else:
            # Yarpaq düyünlərin (leaf nodes) genotipini oxuyuruq
            # Identify leaf genotypes AA, Aa, or aa
            if t == "AA":
                stack.append([1.0, 0.0, 0.0])
            elif t == "Aa":
                stack.append([0.0, 1.0, 0.0])
            elif t == "aa":
                stack.append([0.0, 0.0, 1.0])
            i += 1

    ans = stack[0]
    result = f"{ans[0]:.3f} {ans[1]:.3f} {ans[2]:.3f}"
    print(result)

    with open(output_path, "w") as f:
        f.write(result + "\n")


if __name__ == "__main__":
    main()
