import os
import glob
from Bio import SeqIO
from io import StringIO


def trim_read(seq: str, qual_str: str, q: int):
    """
    Trim leading and trailing bases whose Phred33 quality < q.
    Returns (trimmed_seq, trimmed_qual) or (None, None) if all bases are low quality.
    """
    quals = [ord(c) - 33 for c in qual_str]

    # Find first position from left with quality >= q
    start = 0
    while start < len(quals) and quals[start] < q:
        start += 1

    # Find last position from right with quality >= q
    end = len(quals) - 1
    while end >= 0 and quals[end] < q:
        end -= 1

    if start > end:
        return None, None  # Entire read is below threshold

    return seq[start:end + 1], qual_str[start:end + 1]


def solve(input_text: str) -> str:
    lines = input_text.strip().split('\n')

    # First line is the quality threshold
    q = int(lines[0].strip())

    # Parse FASTQ records
    fastq_text = '\n'.join(lines[1:])
    records = list(SeqIO.parse(StringIO(fastq_text), 'fastq'))

    output_lines = []
    for record in records:
        seq = str(record.seq)
        qual_str = ''.join(chr(q_val + 33) for q_val in record.letter_annotations['phred_quality'])

        trimmed_seq, trimmed_qual = trim_read(seq, qual_str, q)

        if trimmed_seq is not None:
            output_lines.append(f"@{record.id}")
            output_lines.append(trimmed_seq)
            output_lines.append('+')
            output_lines.append(trimmed_qual)

    return '\n'.join(output_lines)


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

    output_file = os.path.join(script_dir, 'output.txt')
    with open(output_file, 'w') as f:
        f.write(result + '\n')
    print(f"Output written to: {output_file}")
    print("First few lines of output:")
    for line in result.split('\n')[:8]:
        print(line)


if __name__ == '__main__':
    # Verify with sample
    sample = """20
@Rosalind_0049
GCAGAGACCAGTAGATGTGTTTGCGGACGGTCGGGCTCCATGTGACACAG
+
FD@@;C<AI?4BA:=>C<G=:AE=><A??>764A8B797@A:58:527+,
@Rosalind_0049
AATGGGGGGGGGAGACAAAATACGGCTAAGGCAGGGGTCCTTGATGTCAT
+
1<<65:793967<4:92568-34:.>1;2752)24')*15;1,.3*3+*!
@Rosalind_0049
ACCCCATACGGCGAGCGTCAGCATCTGATATCCTCTTTCAATCCTAGCTA
+
B:EI>JDB5=>DA?E6B@@CA?C;=;@@C:6D:3=@49;@87;::;;?8+"""

    print("Sample output:")
    print(solve(sample))
    print()
    print("Expected:")
    print("""@Rosalind_0049
GCAGAGACCAGTAGATGTGTTTGCGGACGGTCGGGCTCCATGTGACAC
+
FD@@;C<AI?4BA:=>C<G=:AE=><A??>764A8B797@A:58:527
@Rosalind_0049
ATGGGGGGGGGAGACAAAATACGGCTAAGGCAGGGGTCCT
+
<<65:793967<4:92568-34:.>1;2752)24')*15;
@Rosalind_0049
ACCCCATACGGCGAGCGTCAGCATCTGATATCCTCTTTCAATCCTAGCT
+
B:EI>JDB5=>DA?E6B@@CA?C;=;@@C:6D:3=@49;@87;::;;?8""")
    print()
    main()
