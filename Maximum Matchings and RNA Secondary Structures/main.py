import os
import math

# Maksimal mümkün RNT ikili cütləşmələrinin sayını hesablayırıq
# Compute the maximum number of matchings of base pairings (A-U and C-G)


def read_fasta(file_path):
    seq = ""
    with open(file_path, "r") as f:
        for line in f:
            if not line.startswith(">"):
                seq += line.strip()
    return seq


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_mmch.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    seq = read_fasta(input_path)

    # Hər bir əsas nukleotidin tezliyini sayırıq
    # Count frequencies of A, U, C, G
    a = seq.count("A")
    u = seq.count("U")
    c = seq.count("C")
    g = seq.count("G")

    # Maksimal cütləri (Permutasiya vasitəsilə) hesablayırıq
    # Calculate permutations for pairing max(A, U) elements with min(A, U) elements
    ans = math.perm(max(a, u), min(a, u)) * math.perm(max(c, g), min(c, g))
    print(ans)

    with open(output_path, "w") as f:
        f.write(str(ans) + "\n")


if __name__ == "__main__":
    main()
