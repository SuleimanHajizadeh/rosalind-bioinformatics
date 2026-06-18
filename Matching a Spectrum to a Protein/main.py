import os
from collections import Counter

# Monoisotopic masses of amino acids
MASS = {
    'A': 71.03711, 'C': 103.00919, 'D': 115.02694, 'E': 129.04259,
    'F': 147.06841, 'G':  57.02146, 'H': 137.05891, 'I': 113.08406,
    'K': 128.09496, 'L': 113.08406, 'M': 131.04049, 'N': 114.04293,
    'P':  97.05276, 'Q': 128.05858, 'R': 156.10111, 'S':  87.03203,
    'T': 101.04768, 'V':  99.06841, 'W': 186.07931, 'Y': 163.06333,
}


def complete_spectrum(protein):
    """Return the complete spectrum (list of all prefix and suffix masses)."""
    n = len(protein)
    prefix = [0.0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + MASS[protein[i]]

    suffix = [0.0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix[n - i] = suffix[n - i - 1] + MASS[protein[i]]

    return prefix + suffix   # includes 0 and full mass from both ends


def max_multiplicity(spectrum_protein, spectrum_R):
    """
    Return the maximum multiplicity of (spectrum_R ⊖ spectrum_protein).
    That is, the largest number of pairs (r, s) sharing the same difference r-s.
    Uses rounding to 5 decimal places to handle floating-point noise.
    """
    counts = Counter()
    for r in spectrum_R:
        for s in spectrum_protein:
            diff = round(r - s, 5)
            counts[diff] += 1
    return max(counts.values()) if counts else 0


def solve_prsm(input_path, output_path):
    with open(input_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    n = int(lines[0])
    proteins = lines[1: n + 1]
    spectrum_R = [float(x) for x in lines[n + 1:]]

    best_mult = -1
    best_protein = ''

    for protein in proteins:
        sp = complete_spectrum(protein)
        mult = max_multiplicity(sp, spectrum_R)
        if mult > best_mult:
            best_mult = mult
            best_protein = protein

    result = f"{best_mult}\n{best_protein}"
    with open(output_path, 'w') as f:
        f.write(result + '\n')

    print(result)


if __name__ == '__main__':
    base = os.path.dirname(os.path.abspath(__file__))
    solve_prsm(
        os.path.join(base, 'rosalind_prsm.txt'),
        os.path.join(base, 'output.txt'),
    )
