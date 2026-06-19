import os
from Bio.Seq import Seq

# İntronları çıxarıb ekzonları birləşdirərək RNT-ni proteinə translyasiya edirik
# Excise introns from DNA sequence and translate the joined exons to protein


def translate(seq):
    # DNT-ni proteinə çeviririk (Stop kodonları silirik)
    # Translate DNA sequence to protein sequence
    dna = Seq(seq)
    prot = str(dna.translate(to_stop=True))
    return prot


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_splc.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    # FASTA formatlı faylı oxuyuruq (ilk ardıcıllıq DNT-dir, qalanları intronlardır)
    # Parse FASTA: first record is sequence, remaining are introns to remove
    with open(input_path, "r") as f:
        lines = f.read().splitlines()

    seqs = []
    current_seq = []
    for line in lines:
        line = line.strip()
        if line.startswith(">"):
            if current_seq:
                seqs.append("".join(current_seq))
                current_seq = []
        else:
            current_seq.append(line)
    if current_seq:
        seqs.append("".join(current_seq))

    dna = seqs[0]
    introns = seqs[1:]

    # İntronları DNT-dən kəsib çıxarırıq
    # Remove all introns from the DNA sequence
    for intron in introns:
        dna = dna.replace(intron, "")

    result = translate(dna)
    print(result)

    with open(output_path, "w") as f:
        f.write(result + "\n")


if __name__ == "__main__":
    main()
