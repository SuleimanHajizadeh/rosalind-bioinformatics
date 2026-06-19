import os

# Verilmiş protein ardıcıllığı üçün translyasiya edilə biləcək mümkün RNT sayını modul 1,000,000-da tapırıq
# Compute the number of different mRNA sequences that can translate to a given protein sequence modulo 1,000,000


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_mrna.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as file:
        protein = file.read().strip()

    # Amin turşularını kodlaşdıran kodon sayları cədvəli
    # Frequencies of codons for each amino acid
    codon_freq = {
        "F": 2,
        "L": 6,
        "S": 6,
        "Y": 2,
        "C": 2,
        "W": 1,
        "P": 4,
        "H": 2,
        "Q": 2,
        "R": 6,
        "I": 3,
        "M": 1,
        "T": 4,
        "N": 2,
        "K": 2,
        "V": 4,
        "A": 4,
        "D": 2,
        "E": 2,
        "G": 4,
    }

    # Stop kodonların sayı 3-dür
    # There are 3 stop codons
    ans = 3

    # Proteindəki hər bir amin turşusunun kodon saylarını vururuq
    # Multiply frequencies of codons for each amino acid in the protein modulo 1,000,000
    for aa in protein:
        if aa in codon_freq:
            ans = (ans * codon_freq[aa]) % 1000000

    print(ans)

    with open(output_path, "w") as out_file:
        out_file.write(str(ans) + "\n")


if __name__ == "__main__":
    main()
