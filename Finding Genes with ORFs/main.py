import os
import glob
from Bio.Seq import Seq

# Bütün 6 oxuma çərçivəsini yoxlayıb ən uzun ORF-i tapırıq
# Search all 6 reading frames and find the longest ORF protein


def find_longest_orf(dna):
    seq = Seq(dna)
    # Hər iki zənciri yoxlayırıq: birbaşa və tamamlayıcı tərsinə
    # Check both strands: forward and reverse complement
    strands = [seq, seq.reverse_complement()]
    longest = ""

    for strand in strands:
        # 3 oxuma çərçivəsini yoxlayırıq (0, 1, 2 mövqelərindən başlayaraq)
        # Try 3 reading frames starting at positions 0, 1, 2
        for frame in range(3):
            i = frame
            while i < len(strand) - 2:
                codon = str(strand[i:i + 3])
                # ATG başlanğıc kodonu tapırıq
                # Look for ATG start codon
                if codon == 'ATG':
                    protein = []
                    j = i
                    while j < len(strand) - 2:
                        c = str(strand[j:j + 3])
                        aa = str(Seq(c).translate())
                        # Stop kodona çatdıqda dayanırıq
                        # Stop when we hit a stop codon
                        if aa == '*':
                            break
                        protein.append(aa)
                        j += 3
                    protein_str = ''.join(protein)
                    # Ən uzun zülalı saxlayırıq
                    # Keep the longest protein found so far
                    if len(protein_str) > len(longest):
                        longest = protein_str
                i += 3

    return longest


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_files = glob.glob(os.path.join(script_dir, 'rosalind_*.txt'))

    if not dataset_files:
        print("Xəta: fayl tapılmadı.")
        return

    with open(dataset_files[0], 'r') as f:
        dna = f.read().strip()

    result = find_longest_orf(dna)

    # Nəticəni output.txt-ə yazırıq
    # Write the result to output.txt
    output_file = os.path.join(script_dir, 'output.txt')
    with open(output_file, 'w') as f:
        f.write(result + '\n')


if __name__ == '__main__':
    main()
