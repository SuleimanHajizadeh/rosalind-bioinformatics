import os
import glob
from Bio import SeqIO
from Bio.Align import PairwiseAligner
from io import StringIO


def pairwise_distance(seq1, seq2):
    """Compute normalized global alignment distance between two sequences."""
    aligner = PairwiseAligner()
    aligner.mode = 'global'
    # Default: match=1, mismatch=-1, no gap penalties (like globalxx)
    aligner.match_score = 1
    aligner.mismatch_score = -1
    aligner.open_gap_score = -1
    aligner.extend_gap_score = -0.5
    score = aligner.score(seq1, seq2)
    max_len = max(len(seq1), len(seq2))
    # Normalize to [0,1] where 0=identical, 1=completely different
    return 1.0 - score / max_len


def solve(input_text: str) -> str:
    records = list(SeqIO.parse(StringIO(input_text), 'fasta'))
    n = len(records)
    ids = [r.id for r in records]
    seqs = [str(r.seq) for r in records]

    # Compute pairwise distances and accumulate total distance per sequence
    total_distances = [0.0] * n

    for i in range(n):
        for j in range(i + 1, n):
            dist = pairwise_distance(seqs[i], seqs[j])
            total_distances[i] += dist
            total_distances[j] += dist

    # The outlier has the highest total distance from all others
    outlier_idx = total_distances.index(max(total_distances))
    return ids[outlier_idx]


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

    result = solve(input_text)
    print(f"Result: {result}")

    output_file = os.path.join(script_dir, 'output.txt')
    with open(output_file, 'w') as f:
        f.write(result + '\n')
    print(f"Output written to: {output_file}")


if __name__ == '__main__':
    # Verify with sample
    sample = """>Rosalind_18
GACATGTTTGTTTGCCTTAAACTCGTGGCGGCCTAGCCGTAAGTTAAG
>Rosalind_23
ACTCATGTTTGTTTGCCTTAAACTCTTGGCGGCTTAGCCGTAACTTAAG
>Rosalind_51
TCCTATGTTTGTTTGCCTCAAACTCTTGGCGGCCTAGCCGTAAGGTAAG
>Rosalind_7
CACGTCTGTTCGCCTAAAACTTTGATTGCCGGCCTACGCTAGTTAGTTA
>Rosalind_28
GGGGTCATGGCTGTTTGCCTTAAACCCTTGGCGGCCTAGCCGTAATGTTT"""

    result = solve(sample)
    print(f"Sample result: {result} (expected: Rosalind_7)")
    print()
    main()
