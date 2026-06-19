import os
import glob
from Bio import SeqIO
from io import StringIO

# Hər mövqe üçün orta Phred keyfiyyət skorunu hesablayırıq
# Compute mean Phred quality per position across all reads


def solve(input_text):
    lines = input_text.strip().split('\n')

    # İlk sətir keyfiyyət həddidir
    # First line is the quality threshold
    q = int(lines[0].strip())

    # Qalan hissəni FASTQ formatında oxuyuruq
    # Parse remaining lines as FASTQ
    fastq_text = '\n'.join(lines[1:])
    records = list(SeqIO.parse(StringIO(fastq_text), 'fastq'))

    if not records:
        return "0"

    # Bütün oxunuşların eyni uzunluqda olduğunu fərz edirik
    # Assume all reads have the same length
    read_len = len(records[0].seq)

    # Hər mövqe üçün keyfiyyət skorlarının cəmini saxlayırıq
    # Accumulate quality scores at each position
    quality_sums = [0] * read_len
    count = 0

    for record in records:
        quals = record.letter_annotations['phred_quality']
        if len(quals) == read_len:
            for i, score in enumerate(quals):
                quality_sums[i] += score
            count += 1

    # Orta keyfiyyəti hesablayıb həddən aşağı olan mövqeləri sayırıq
    # Count positions where mean quality falls below threshold q
    below = sum(1 for total in quality_sums if (total / count) < q)

    return str(below)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_files = glob.glob(os.path.join(script_dir, 'rosalind_*.txt'))

    if not dataset_files:
        print("Xəta: fayl tapılmadı.")
        return

    with open(dataset_files[0], 'r') as f:
        input_text = f.read()

    result = solve(input_text)

    # Nəticəni output.txt faylına yazırıq
    # Write the result to output.txt
    output_file = os.path.join(script_dir, 'output.txt')
    with open(output_file, 'w') as f:
        f.write(result + '\n')


if __name__ == '__main__':
    main()
