import os
from itertools import combinations


def solve_qrt(input_path, output_path):
    with open(input_path, 'r') as f:
        lines = [line.rstrip('\n') for line in f if line.strip()]

    taxa = lines[0].split()
    n = len(taxa)

    seen = set()   # canonical quartet keys for deduplication
    quartets = []  # ordered list of (pair_a, pair_b) for output

    for row in lines[1:]:
        A = [taxa[i] for i in range(n) if i < len(row) and row[i] == '0']
        B = [taxa[i] for i in range(n) if i < len(row) and row[i] == '1']

        if len(A) < 2 or len(B) < 2:
            continue

        for pair_a in combinations(A, 2):
            for pair_b in combinations(B, 2):
                # Canonical key: frozenset of frozensets (order-independent)
                key = frozenset([frozenset(pair_a), frozenset(pair_b)])
                if key not in seen:
                    seen.add(key)
                    quartets.append((pair_a, pair_b))

    lines_out = []
    for (a1, a2), (b1, b2) in quartets:
        lines_out.append(f"{{{a1}, {a2}}} {{{b1}, {b2}}}")

    result = '\n'.join(lines_out)
    with open(output_path, 'w') as f:
        f.write(result + '\n')

    print(result)


if __name__ == '__main__':
    base = os.path.dirname(os.path.abspath(__file__))
    solve_qrt(
        os.path.join(base, 'rosalind_qrt.txt'),
        os.path.join(base, 'output.txt'),
    )
