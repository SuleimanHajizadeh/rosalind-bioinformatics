import os
import glob
from Bio import SeqIO
from io import StringIO


def count_approx(query, text, max_dist=3):
    """Count positions where query matches text window with ≤ max_dist substitutions."""
    k = len(query)
    if k > len(text):
        return 0
    count = 0
    for i in range(len(text) - k + 1):
        d = 0
        for j in range(k):
            if query[j] != text[i + j]:
                d += 1
                if d > max_dist:
                    break
        if d <= max_dist:
            count += 1
    return count


def find_and_count_repeat(s, t, min_len=32, max_len=40, max_dist=3):
    """
    Find repeat r of length 32-40 bp that appears most frequently
    (with ≤ max_dist substitutions) in both s and t.
    Returns (r, count_in_s, count_in_t).
    """
    best_r = None
    best_cs = 0
    best_ct = 0
    best_total = 0

    for k in range(min_len, max_len + 1):
        for i in range(len(s) - k + 1):
            kmer = s[i:i + k]

            # Quick pre-check: does this kmer appear at all in t?
            found_in_t = False
            for j in range(len(t) - k + 1):
                d = 0
                for c in range(k):
                    if kmer[c] != t[j + c]:
                        d += 1
                        if d > max_dist:
                            break
                if d <= max_dist:
                    found_in_t = True
                    break

            if not found_in_t:
                continue

            cs = count_approx(kmer, s, max_dist)
            ct = count_approx(kmer, t, max_dist)

            if cs >= 2 and ct >= 2:
                total = cs + ct
                if total > best_total:
                    best_total = total
                    best_cs = cs
                    best_ct = ct
                    best_r = kmer

    return best_r, best_cs, best_ct


def solve(input_text):
    records = list(SeqIO.parse(StringIO(input_text), 'fasta'))
    s = str(records[0].seq)
    t = str(records[1].seq)
    r, cs, ct = find_and_count_repeat(s, t)
    return r, cs, ct


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_files = glob.glob(os.path.join(script_dir, 'rosalind_*.txt'))

    if not dataset_files:
        print("Error: No rosalind_*.txt dataset file found.")
        return

    dataset_file = dataset_files[0]
    print(f"Using dataset: {dataset_file}")

    with open(dataset_file, 'r') as f:
        input_text = f.read()

    r, cs, ct = solve(input_text)
    result = f"{cs} {ct}"
    print(f"Repeat r ({len(r)} bp): {r}")
    print(f"Result: {result}")

    output_file = os.path.join(script_dir, 'output.txt')
    with open(output_file, 'w') as f:
        f.write(result + '\n')
    print(f"Output written to: {output_file}")


if __name__ == '__main__':
    # Verify with sample data (note: sample has short strings ~100 bp, repeat ~34 bp)
    sample_text = """>Rosalind_12
GACTCCTTTGTTTGCCTTAAATAGATACATATTTACTCTTGACTCTTTTGTTGGCCTTAAATAGATACATATTTGTGCGACTCCACGAGTGATTCGTA
>Rosalind_37
ATGGACTCCTTTGTTTGCCTTAAATAGATACATATTCAACAAGTGTGCACTTAGCCTTGCCGACTCCTTTGTTTGCCTTAAATAGATACATATTTG"""

    r, cs, ct = solve(sample_text)
    print(f"Sample: {cs} {ct} (expected: 2 2) | r={r}")
    print()

    main()
