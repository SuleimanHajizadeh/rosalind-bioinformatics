import os
import glob
from Bio import SeqIO
from io import StringIO

# FASTQ oxunuşlarından keyfiyyəti az olanları filtirləyirik
# Filter FASTQ reads: keep only reads where >= p% of bases have quality >= q


def solve(input_text):
    lines = input_text.strip().split('\n')

    # İlk sətirdə q (keyfiyyət hədd) və p (faiz hədd) verilir
    # First line contains quality threshold q and percentage threshold p
    q, p = map(int, lines[0].split())

    count = 0
    i = 1
    while i < len(lines):
        # Hər FASTQ qeydi 4 sətirdən ibarətdir: başlıq, ardıcıllıq, +, keyfiyyət
        # Each FASTQ record is 4 lines: header, sequence, +, quality
        if lines[i].startswith('@'):
            quality_str = lines[i + 3]
            # Phred33 keyfiyyət skorlarını hesablayırıq
            # Decode Phred33 quality scores
            quality_scores = [ord(c) - 33 for c in quality_str]
            total = len(quality_scores)
            if total == 0:
                i += 4
                continue
            # q-dan böyük və ya bərabər olan bazaların faizini hesablayırıq
            # Calculate percentage of bases meeting the quality threshold
            high_q = sum(1 for s in quality_scores if s >= q)
            if (high_q / total) * 100 >= p:
                count += 1
            i += 4
        else:
            i += 1

    return str(count)


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
