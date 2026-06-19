import os
import glob

# DNT-dəki nukleotidləri (A, C, G, T) sayırıq
# Count the occurrences of each nucleotide (A, C, G, T) in the DNA string


def solve(dna):
    # Hər bir nukleotidin sayını hesablayırıq
    # Calculate the frequency of each nucleotide
    a = dna.count("A")
    c = dna.count("C")
    g = dna.count("G")
    t = dna.count("T")
    return f"{a} {c} {g} {t}"


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Dataset faylını tapırıq
    # Find the dataset file automatically
    dataset_files = glob.glob(os.path.join(script_dir, "rosalind_*.txt"))

    if not dataset_files:
        print("Xəta: rosalind_*.txt faylı tapılmadı.")
        return

    with open(dataset_files[0], "r") as f:
        dna = f.read().strip()

    result = solve(dna)
    print(result)

    # Nəticəni output.txt faylına yazırıq
    # Write the result to output.txt
    output_file = os.path.join(script_dir, "output.txt")
    with open(output_file, "w") as f:
        f.write(result + "\n")


if __name__ == "__main__":
    main()