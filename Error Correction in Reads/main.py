import os

# FASTA formatlı giriş faylını oxuyuruq
# Parse the FASTA file and load read sequences


def read_fasta(file_path):
    seqs = []
    curr = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if curr:
                    seqs.append("".join(curr))
                    curr = []
            else:
                curr.append(line)
        if curr:
            seqs.append("".join(curr))
    return seqs


def reverse_complement(s):
    # Komplementar zənciri tapırıq
    # Compute the reverse complement of DNA sequence
    comp = {"A": "T", "T": "A", "C": "G", "G": "C"}
    return "".join(comp[c] for c in reversed(s))


def hamming_distance(s1, s2):
    # Hemminq məsafəsini (Hamming distance) hesablayırıq
    # Calculate Hamming distance between two strings
    return sum(1 for x, y in zip(s1, s2) if x != y)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_corr.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    reads = read_fasta(input_path)

    # Tezlikləri hesablamaq üçün bütün oxunuşları və onların komplementlərini yoxlayırıq
    # Count frequencies of each read including its reverse complement
    counts = {}
    for r in reads:
        rc = reverse_complement(r)
        # Hər bir oxunuş üçün normal və komplementar versiyasını eyni açara yığırıq
        # Map read and its reverse complement to a canonical form (alphabetically smaller)
        canonical = min(r, rc)
        counts[canonical] = counts.get(canonical, 0) + 1

    # Düzgün və səhv oxunuşları ayırırıq
    # Categorise reads into correct (freq >= 2) and incorrect (freq == 1)
    correct_reads = set()
    for r in reads:
        rc = reverse_complement(r)
        canonical = min(r, rc)
        if counts[canonical] >= 2:
            correct_reads.add(r)
            correct_reads.add(rc)

    incorrect_reads = []
    for r in reads:
        if r not in correct_reads:
            incorrect_reads.append(r)

    corrections = []
    # Hər bir səhv oxunuş üçün düzgün olanlar arasından 1 Hemminq məsafəsində olanı tapırıq
    # For each incorrect read, find a matching correct read at Hamming distance == 1
    for r in incorrect_reads:
        for corr in correct_reads:
            if hamming_distance(r, corr) == 1:
                corrections.append(f"{r}->{corr}")
                break

    with open(output_path, "w") as f:
        for c in corrections:
            f.write(c + "\n")

    print(f"Total corrections: {len(corrections)}")


if __name__ == "__main__":
    main()
