import os
import sys

# Oxşar motifləri 1 əvəzləmə fərqi (Hamming distance <= 1) daxilində axtarırıq
# Find all occurrences of a motif in a sequence allowing up to 1 mismatch


def parse_fasta(filepath):
    seqs = []
    curr = []
    with open(filepath) as f:
        for line in f:
            if line.startswith(">"):
                if curr:
                    seqs.append("".join(curr))
                    curr = []
            else:
                curr.append(line.strip())
    if curr:
        seqs.append("".join(curr))
    return seqs


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_ksim.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        lines = f.read().splitlines()

    # Parametrləri oxuyuruq
    # Parse parameters and sequences
    k = int(lines[0].strip())
    s = lines[1].strip()
    t = lines[2].strip()

    M, N = len(s), len(t)
    results = []

    # Sürüşən pəncərə ilə uyğunluqları tapırıq
    # Slide across sequence to find matches with <= k mismatches
    for i in range(M - N + 1):
        sub = s[i : i + N]
        diffs = sum(1 for x, y in zip(sub, t) if x != y)
        if diffs <= k:
            results.append((i + 1, N))

    print(f"Found matches count: {len(results)}")

    with open(output_path, "w") as f:
        for pos, length in results:
            f.write(f"{pos} {length}\n")


if __name__ == "__main__":
    main()
