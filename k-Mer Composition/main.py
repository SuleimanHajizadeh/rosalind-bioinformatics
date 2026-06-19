import os
import itertools

# DNT ardıcıllığındakı bütün mümkün 4-merlərin tezlik massivini tapırıq
# Compute the 4-mer composition of a DNA sequence in lexicographical order


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_kmer.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    # FASTA faylını oxuyuruq
    # Read the DNA sequence from FASTA format
    dna_seq = ""
    with open(input_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line.startswith(">"):
                dna_seq += line

    # 4-merləri leksikoqrafik olaraq generasiya edirik
    # Generate all 256 4-mers lexicographically
    bases = ["A", "C", "G", "T"]
    kmers = ["".join(p) for p in itertools.product(bases, repeat=4)]

    kmer_counts = {kmer: 0 for kmer in kmers}

    # Sürüşən pəncərə (sliding window) ilə sayırıq
    # Slide window of size 4 across DNA sequence to count occurrences
    k = 4
    for i in range(len(dna_seq) - k + 1):
        current_kmer = dna_seq[i : i + k]
        if current_kmer in kmer_counts:
            kmer_counts[current_kmer] += 1

    counts = [kmer_counts[kmer] for kmer in kmers]
    result_str = " ".join(map(str, counts))

    with open(output_path, "w") as f:
        f.write(result_str + "\n")

    print("Computed 4-mer composition.")


if __name__ == "__main__":
    main()
