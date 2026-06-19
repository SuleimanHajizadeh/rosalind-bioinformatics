import os
import glob
from Bio import SeqIO
from io import StringIO


def solve(input_text: str) -> str:
    lines = input_text.strip().split('\n')

    # First line is the quality threshold
    q = int(lines[0].strip())

    # Parse FASTQ records from the rest
    fastq_text = '\n'.join(lines[1:])
    records = list(SeqIO.parse(StringIO(fastq_text), 'fastq'))

    if not records:
        return "0"

    read_len = len(records[0].seq)

    # Sum quality scores at each position across all reads
    quality_sums = [0] * read_len
    count = 0

    for record in records:
        quals = record.letter_annotations['phred_quality']
        if len(quals) == read_len:
            for i, score in enumerate(quals):
                quality_sums[i] += score
            count += 1

    # Count positions where mean quality < q
    below_threshold = sum(
        1 for total in quality_sums
        if (total / count) < q
    )

    return str(below_threshold)


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
    sample = """26
@Rosalind_0029
GCCCCAGGGAACCCTCCGACCGAGGATCGT
+
>?F?@6<C<HF?<85486B;85:8488/2/
@Rosalind_0029
TGTGATGGCTCTCTGAATGGTTCAGGCAGT
+
@J@H@>B9:B;<D==:<;:,<::?463-,,
@Rosalind_0029
CACTCTTACTCCCTAGCCGAACTCCTTTTT
+
=88;99637@5,4664-65)/?4-2+)$)$
@Rosalind_0029
GATTATGATATCAGTTGGCTCCGAGAGCGT
+
<@BGE@8C9=B9:B<>>>7?B>7:02+33."""

    print(f"Sample result: {solve(sample)} (expected: 17)")
    print()
    main()
