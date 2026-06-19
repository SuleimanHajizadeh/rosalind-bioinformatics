import os

# KMP alqoritminin prefix-failure massivini (failure array) hesablayırıq
# Calculate the Knuth-Morris-Pratt failure array for a DNA sequence


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_kmp.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    # FASTA-dan DNT ardıcıllığını oxuyuruq
    # Read the DNA sequence from FASTA format
    dna_seq = ""
    with open(input_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line.startswith(">"):
                dna_seq += line

    n = len(dna_seq)
    pi = [0] * n

    # KMP failure array (pi massivi) hesablanması
    # Construct KMP failure array values
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and dna_seq[i] != dna_seq[j]:
            j = pi[j - 1]
        if dna_seq[i] == dna_seq[j]:
            j += 1
        pi[i] = j

    result_str = " ".join(map(str, pi))

    # Nəticəni output.txt faylına yazırıq
    # Write space-separated failure array to output.txt
    with open(output_path, "w") as f:
        f.write(result_str + "\n")

    print(f"Failure array computed for sequence length: {n}")


if __name__ == "__main__":
    main()
