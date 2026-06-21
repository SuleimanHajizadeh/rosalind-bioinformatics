# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba11j.txt")
    if not os.path.exists(input_file):
        return "", [], 0
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    peptide = lines[0]
    spectrum = list(map(int, lines[1].split()))
    num_modifications = int(lines[2])
    return peptide, spectrum, num_modifications

# Modifikasiya edilmiş ən yaxşı xallı peptidi tapırıq
# Find a Highest-Scoring Modified Peptide against a Spectrum
def highest_scoring_modified_peptide(peptide, spectrum, num_modifications):
    pass

def main():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("")

if __name__ == "__main__":
    main()
