import os
import glob
from Bio import SeqIO
from io import StringIO

# Oxunan hər bir FASTQ oxunuşunu hər iki ucundan keyfiyyətsiz bazaları kəsirik
# We trim low-quality bases from both ends of each FASTQ read


def trim_read(seq, qual_str, q):
    # Phred33 keyfiyyət skorlarını hesablayırıq: ASCII kodu - 33
    # Convert ASCII quality characters to Phred33 scores: ord(char) - 33
    quals = [ord(c) - 33 for c in qual_str]

    # Soldan başlayaraq keyfiyyəti q-dan az olan bazaları atlayırıq
    # Scan from the left: skip bases with quality below q
    start = 0
    while start < len(quals) and quals[start] < q:
        start += 1

    # Sağdan başlayaraq keyfiyyəti q-dan az olan bazaları atlayırıq
    # Scan from the right: skip bases with quality below q
    end = len(quals) - 1
    while end >= 0 and quals[end] < q:
        end -= 1

    # Əgər bütün bazalar keyfiyyətsizdirsə, None qaytarırıq
    # If all bases are below threshold, return None (drop this read)
    if start > end:
        return None, None

    # Kəsilmiş ardıcıllığı və keyfiyyət sətirini qaytarırıq
    # Return the trimmed sequence and quality string
    return seq[start:end + 1], qual_str[start:end + 1]


def solve(input_text):
    lines = input_text.strip().split('\n')

    # İlk sətir keyfiyyət həddidir
    # First line is the quality threshold
    q = int(lines[0].strip())

    # Qalan hissəni FASTQ formatında oxuyuruq
    # Parse the rest as FASTQ records
    fastq_text = '\n'.join(lines[1:])
    records = list(SeqIO.parse(StringIO(fastq_text), 'fastq'))

    output_lines = []
    for record in records:
        seq = str(record.seq)
        # Keyfiyyət skorlarını ASCII simvollarına çeviririk
        # Convert Phred quality scores back to ASCII characters
        qual_str = ''.join(chr(v + 33) for v in record.letter_annotations['phred_quality'])

        trimmed_seq, trimmed_qual = trim_read(seq, qual_str, q)

        # Keyfiyyətsiz oxunuşları nəticəyə əlavə etmirik
        # Skip reads that are entirely below quality threshold
        if trimmed_seq is not None:
            output_lines.append(f"@{record.id}")
            output_lines.append(trimmed_seq)
            output_lines.append('+')
            output_lines.append(trimmed_qual)

    return '\n'.join(output_lines)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Dataset faylını tapırıq
    # Find the dataset file automatically
    dataset_files = glob.glob(os.path.join(script_dir, 'rosalind_*.txt'))

    if not dataset_files:
        print("Xəta: rosalind_*.txt faylı tapılmadı.")
        return

    with open(dataset_files[0], 'r') as f:
        input_text = f.read()

    result = solve(input_text)

    # Nəticəni output.txt faylına yazırıq
    # Write result to output.txt
    output_file = os.path.join(script_dir, 'output.txt')
    with open(output_file, 'w') as f:
        f.write(result + '\n')


if __name__ == '__main__':
    main()
