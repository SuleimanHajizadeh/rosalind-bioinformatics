import os
import glob
from Bio import SeqIO
from io import StringIO

# Hər bir FASTA ardıcıllığının tərsinə çevrilmiş tamamlayıcısını tapıb
# öz-özünə tamamlayan ardıcıllıqları sayırıq
# Count DNA strings equal to their own reverse complement


def solve(input_text):
    count = 0
    # FASTA formatında ardıcıllıqları oxuyuruq
    # Parse FASTA sequences
    for record in SeqIO.parse(StringIO(input_text), 'fasta'):
        seq = record.seq
        # Tərsinə çevrilmiş tamamlayıcı özünə bərabərdirsə sayı artırırıq
        # If the sequence equals its own reverse complement, count it
        if seq == seq.reverse_complement():
            count += 1
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
