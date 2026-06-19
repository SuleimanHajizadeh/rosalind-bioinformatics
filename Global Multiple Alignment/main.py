import os
import glob
from Bio import SeqIO
from Bio.Align import PairwiseAligner
from io import StringIO

# Bütün cütlər arasında qlobal düzülüş məsafəsini hesablayaraq
# ən fərqli ardıcıllığı tapırıq
# Find the most different sequence by building a pairwise distance matrix


def pairwise_distance(seq1, seq2):
    # Needleman-Wunsch qlobal düzülüşü qururuq
    # Build a Needleman-Wunsch global alignment
    aligner = PairwiseAligner()
    aligner.mode = 'global'
    aligner.match_score = 1
    aligner.mismatch_score = -1
    aligner.open_gap_score = -1
    aligner.extend_gap_score = -0.5
    score = aligner.score(seq1, seq2)
    max_len = max(len(seq1), len(seq2))
    # Normallaşdırılmış məsafə: 0=eyni, 1=tamamilə fərqli
    # Normalized distance: 0=identical, 1=completely different
    return 1.0 - score / max_len


def solve(input_text):
    records = list(SeqIO.parse(StringIO(input_text), 'fasta'))
    n = len(records)
    ids = [r.id for r in records]
    seqs = [str(r.seq) for r in records]

    # Hər ardıcıllığın digərləri ilə ümumi məsafəsini hesablayırıq
    # Accumulate total distance of each sequence to all others
    total_dist = [0.0] * n

    for i in range(n):
        for j in range(i + 1, n):
            d = pairwise_distance(seqs[i], seqs[j])
            total_dist[i] += d
            total_dist[j] += d

    # Ən böyük məsafəyə sahib ardıcıllıq ən fərqlidir
    # The sequence with the highest total distance is the outlier
    outlier_idx = total_dist.index(max(total_dist))
    return ids[outlier_idx]


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_files = glob.glob(os.path.join(script_dir, 'rosalind_*.txt'))

    if not dataset_files:
        print("Xəta: fayl tapılmadı.")
        return

    with open(dataset_files[0], 'r') as f:
        input_text = f.read()

    result = solve(input_text)

    # Nəticəni output.txt-ə yazırıq
    # Write result to output.txt
    output_file = os.path.join(script_dir, 'output.txt')
    with open(output_file, 'w') as f:
        f.write(result + '\n')


if __name__ == '__main__':
    main()
