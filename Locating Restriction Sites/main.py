import os

# FASTA formatlı giriş faylını oxuyuruq
# Parse the FASTA file to obtain the sequence string


def read_fasta(file_path):
    seq = ""
    with open(file_path, "r") as f:
        for line in f:
            if not line.startswith(">"):
                seq += line.strip()
    return seq


def reverse_complement(s):
    # Komplementar zənciri tapırıq
    # Compute reverse complement of a DNA sequence
    comp = {"A": "T", "T": "A", "C": "G", "G": "C"}
    return "".join(comp[c] for c in reversed(s))


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_revp.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    seq = read_fasta(input_path)
    n = len(seq)
    results = []

    # 4-dən 12-yə qədər olan uzunluqlarda tərs palindromları (reverse palindromes) tapırıq
    # Search for reverse palindromes of length 4 to 12
    for length in range(4, 13):
        for i in range(n - length + 1):
            sub = seq[i : i + length]
            if sub == reverse_complement(sub):
                results.append((i + 1, length))

    # Mövqe indeksinə görə sıralayırıq
    # Sort results by position
    results.sort(key=lambda x: x[0])

    # Nəticələri output.txt-yə yazırıq
    # Output position and length to output.txt
    with open(output_path, "w") as f:
        for pos, length in results:
            line = f"{pos} {length}"
            print(line)
            f.write(line + "\n")


if __name__ == "__main__":
    main()
