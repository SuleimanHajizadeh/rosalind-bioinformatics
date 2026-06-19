import os
import glob
from Bio.SeqIO import parse
from Bio.Seq import Seq


def solve(input_text: str) -> str:
    from io import StringIO
    count = 0
    for record in parse(StringIO(input_text), 'fasta'):
        seq = record.seq
        if seq == seq.reverse_complement():
            count += 1
    return str(count)


def main():
    dataset_files = glob.glob(os.path.join(os.path.dirname(__file__), 'rosalind_*.txt'))

    if not dataset_files:
        print("Error: No rosalind_*.txt dataset file found in the current directory.")
        return

    dataset_file = dataset_files[0]
    print(f"Using dataset: {dataset_file}")

    with open(dataset_file, 'r') as f:
        input_text = f.read()

    result = solve(input_text)
    print(f"Result: {result}")

    output_file = os.path.join(os.path.dirname(__file__), 'output.txt')
    with open(output_file, 'w') as f:
        f.write(result + '\n')
    print(f"Output written to: {output_file}")


if __name__ == '__main__':
    # Verify with sample
    sample = """>Rosalind_64
ATAT
>Rosalind_48
GCATA"""
    print(f"Sample result: {solve(sample)} (expected: 1)")

    main()
