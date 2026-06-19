import os
import glob
from Bio.Seq import Seq


def find_longest_orf_protein(dna: str) -> str:
    """
    Search all 6 reading frames (3 forward + 3 reverse complement)
    for ORFs. Return the longest translated protein string.
    An ORF starts at ATG and ends at a stop codon OR end of string.
    """
    seq = Seq(dna)
    strands = [seq, seq.reverse_complement()]
    longest = ""

    for strand in strands:
        for frame in range(3):
            i = frame
            while i < len(strand) - 2:
                codon = str(strand[i:i + 3])
                if codon == 'ATG':
                    # Found a start - translate until stop or end
                    protein = []
                    j = i
                    while j < len(strand) - 2:
                        c = str(strand[j:j + 3])
                        aa = str(Seq(c).translate())
                        if aa == '*':
                            break
                        protein.append(aa)
                        j += 3
                    protein_str = ''.join(protein)
                    if len(protein_str) > len(longest):
                        longest = protein_str
                i += 3

    return longest


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_files = glob.glob(os.path.join(script_dir, 'rosalind_*.txt'))

    if not dataset_files:
        print("Error: No rosalind_*.txt dataset file found.")
        return

    dataset_file = dataset_files[0]
    print(f"Using dataset: {dataset_file}")

    with open(dataset_file, 'r') as f:
        dna = f.read().strip()

    result = find_longest_orf_protein(dna)
    print(f"Result: {result}")

    output_file = os.path.join(script_dir, 'output.txt')
    with open(output_file, 'w') as f:
        f.write(result + '\n')
    print(f"Output written to: {output_file}")


if __name__ == '__main__':
    # Verify with sample
    sample = "AGCCATGTAGCTAACTCAGGTTACATGGGGATGACCCCGCGACTTGGATTAGAGTCTCTTTTGGAATAAGCCTGAATGATCCGAGTAGCATCTCAG"
    result = find_longest_orf_protein(sample)
    print(f"Sample result: {result}")
    print(f"Expected:      MLLGSFRLIPKETLIQVAGSSPCNLS")
    print()
    main()
