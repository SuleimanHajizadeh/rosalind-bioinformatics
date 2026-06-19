import os
import sys
from Bio import SeqIO
from io import StringIO

# FASTQ formatlı oxunuşları FASTA formatına çeviririk
# Parse a FASTQ file and convert records to standard FASTA format


def solve(input_text):
    # FASTQ ardıcıllıqlarını oxuyub FASTA formatında formatlayırıq
    # Convert FASTQ records to FASTA representation
    records = list(SeqIO.parse(StringIO(input_text), "fastq"))
    output = []
    for record in records:
        output.append(f">{record.description}")
        output.append(str(record.seq))
    return "\n".join(output)


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

    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as f:
        f.write(result + "\n")

    print(f"FASTQ to FASTA conversion complete. Records count: {result.count('>')}")


if __name__ == "__main__":
    main()
