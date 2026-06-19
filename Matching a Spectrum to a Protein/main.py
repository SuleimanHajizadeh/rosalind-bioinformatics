import os
from collections import Counter

# Proteinin kütlə spektrinə əsasən ən yaxın uyğunluğu tapırıq
# Match a protein sequence to a spectrum using prefix/suffix mass multiplicity


def complete_spectrum(protein):
    # Monoisotopic kütlə cədvəlinə əsasən tam spektr hesablayırıq
    # Return prefix and suffix masses for the protein sequence
    mass_table = {
        "A": 71.03711,
        "C": 103.00919,
        "D": 115.02694,
        "E": 129.04259,
        "F": 147.06841,
        "G": 57.02146,
        "H": 137.05891,
        "I": 113.08406,
        "K": 128.09496,
        "L": 113.08406,
        "M": 131.04049,
        "N": 114.04293,
        "P": 97.05276,
        "Q": 128.05858,
        "R": 156.10111,
        "S": 87.03203,
        "T": 101.04768,
        "V": 99.06841,
        "W": 186.07931,
        "Y": 163.06333,
    }
    n = len(protein)
    prefix_mass = 0.0
    masses = []
    for i in range(n):
        prefix_mass += mass_table[protein[i]]
        masses.append(prefix_mass)
    return masses


def max_multiplicity(protein_seq, spectrum):
    # Nəzəri spektr ilə eksperimental spektr arasındakı fərqlərin ən böyük sayını (multiplicity) tapırıq
    # Calculate maximum multiplicity of mass differences between candidate and experimental spectrum
    theo = complete_spectrum(protein_seq)
    diffs = []
    for t in theo:
        for s in spectrum:
            diffs.append(round(t - s, 5))
    counts = Counter(diffs)
    if not counts:
        return 0, 0.0
    best_diff, mult = counts.most_common(1)[0]
    return mult, best_diff


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_prsm.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    n = int(lines[0])
    protein_seq = lines[1]
    spectrum = [float(val) for val in lines[2:]]

    mult, diff = max_multiplicity(protein_seq, spectrum)
    print(f"Multiplicity: {mult}")

    with open(output_path, "w") as f:
        f.write(f"{mult}\n")


if __name__ == "__main__":
    main()
