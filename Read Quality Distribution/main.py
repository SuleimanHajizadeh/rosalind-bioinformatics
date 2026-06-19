import os
import sys
from Bio import SeqIO
from io import StringIO

# FASTQ oxunuşlarının orta keyfiyyət paylanmasını hesablayırıq
# Compute the number of reads whose average Phred quality score is below threshold q


def solve(input_text):
    lines = input_text.strip().split("\n")
    # Həddi (threshold) oxuyuruq
    # Read the threshold quality value q
    q = int(lines[0].strip())

    fastq_text = "\n".join(lines[1:])
    records = list(SeqIO.parse(StringIO(fastq_text), "fastq"))

    low_quality_count = 0
    # Hər bir oxunuş üçün orta keyfiyyəti hesablayırıq
    # Check average Phred quality for each read record
    for record in records:
        quals = record.letter_annotations["phred_quality"]
        avg = sum(quals) / len(quals)
        if avg < q:
            low_quality_count += 1

    return str(low_quality_count)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    import glob

    files = glob.glob(os.path.join(script_dir, "rosalind_*.txt"))
    if not files:
        print("Xəta: Dataset tapılmadı.")
        return
    input_path = files[0]

    with open(input_path, "r") as f:
        input_text = f.read()

    result = solve(input_text)
    print(f"Reads below threshold: {result}")

    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as f:
        f.write(result + "\n")


if __name__ == "__main__":
    main()
