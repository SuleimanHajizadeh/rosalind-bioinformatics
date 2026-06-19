import os
from Bio.Seq import Seq

# DNT ardıcıllığındakı bütün mümkün translyasiya edilmiş proteinləri (ORF) tapırıq
# Search all reading frames of a DNA sequence for potential translated proteins (ORFs)


def get_reverse_complement(dna):
    # Komplementar zənciri tapırıq
    # Compute reverse complement
    comp = {"A": "T", "T": "A", "C": "G", "G": "C"}
    return "".join(comp[c] for c in reversed(dna))


def find_proteins_from_dna(dna):
    # DNT ardıcıllığından bütün mümkün ORF-ləri tapırıq
    # Find all open reading frames and translate them to proteins
    proteins = set()
    n = len(dna)

    # Hər iki zənciri yoxlayırıq (normal və komplementar)
    # Check both forward and reverse complement strands
    for seq in [dna, get_reverse_complement(dna)]:
        # 3 oxuma çərçivəsi (reading frame) üzrə yoxlayırıq
        # Check all 3 reading frames for the current strand
        for frame in range(3):
            # Kodonlara bölürük
            # Extract list of codons
            codons = []
            for i in range(frame, n - 2, 3):
                codons.append(seq[i : i + 3])

            # Start codon (ATG) tapıldıqda protein zəncirini qurmağa başlayırıq
            # Scan codons: start building candidate sequence when ATG is found
            for idx in range(len(codons)):
                if codons[idx] == "ATG":
                    protein_seq = []
                    found_stop = False
                    for j in range(idx, len(codons)):
                        codon_seq = Seq(codons[j])
                        aa = str(codon_seq.translate(table=1))
                        if aa == "*":
                            found_stop = True
                            break
                        protein_seq.append(aa)

                    if found_stop:
                        proteins.add("".join(protein_seq))
    return proteins


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_orf.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    # FASTA faylından DNT ardıcıllığını oxuyuruq
    # Parse the FASTA file
    dna_seq = ""
    with open(input_path, "r") as f:
        for line in f:
            if not line.startswith(">"):
                dna_seq += line.strip()

    proteins = find_proteins_from_dna(dna_seq)

    with open(output_path, "w") as f:
        for p in proteins:
            print(p)
            f.write(p + "\n")


if __name__ == "__main__":
    main()
