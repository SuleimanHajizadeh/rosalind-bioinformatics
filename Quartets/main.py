import os
from itertools import combinations

# Kvartetləri (splits) analiz edib uyğun cütləri çıxarırıq
# Generate quartets from the given species splits


def solve_qrt(input_path, output_path):
    with open(input_path, "r") as f:
        lines = [line.rstrip("\n") for line in f if line.strip()]

    taxa = lines[0].split()
    n = len(taxa)

    seen = set()
    quartets = []

    # Hər bölünmə sətri üçün elementləri A və B olaraq qruplaşdırırıq
    # Parse each split row: group species into set A ('0') and set B ('1')
    for row in lines[1:]:
        A = [taxa[i] for i in range(n) if i < len(row) and row[i] == "0"]
        B = [taxa[i] for i in range(n) if i < len(row) and row[i] == "1"]

        if len(A) < 2 or len(B) < 2:
            continue

        # İki tərəfdən cütləri seçib kvartetləri toplayırıq
        # Take combinations of pairs from both groups to build quartets
        for pair_a in combinations(A, 2):
            for pair_b in combinations(B, 2):
                key = frozenset([frozenset(pair_a), frozenset(pair_b)])
                if key not in seen:
                    seen.add(key)
                    quartets.append((pair_a, pair_b))

    # Nəticələri formatlayıb output.txt-ə yazırıq
    # Format and write results to output.txt
    lines_out = []
    for pair_a, pair_b in quartets:
        lines_out.append(f"{{ {pair_a[0]}, {pair_a[1]} }} {{ {pair_b[0]}, {pair_b[1]} }}")

    with open(output_path, "w") as f:
        f.write("\n".join(lines_out) + "\n")

    print(f"Total quartets generated: {len(quartets)}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_qrt.txt")
    output_file = os.path.join(script_dir, "output.txt")
    solve_qrt(input_file, output_file)
