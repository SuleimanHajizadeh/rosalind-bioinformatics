import os

# Tam kütlə spektrinə (full spectrum) əsasən peptide zəncirini tapırıq
# Reconstruct protein sequence from the complete set of prefix and suffix masses


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_full.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        spectrum = [float(line.strip()) for line in f if line.strip()]

    # Amin turşularının monozotopik kütlə cədvəli
    # Monoisotopic mass table
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

    # Bütün kütlələri cütləşdirərək (prefix və suffix olaraq) fərqləri yoxlayırıq
    # Match candidate masses that sum up to parent mass
    parent_mass = spectrum[0]
    prefix_masses = []

    # Kütlələri çeşidləyirik
    # Sort spectrum
    spectrum.sort()

    # Spektrin cütlərini analiz edirik
    # Deduplicate matching pairs
    n = len(spectrum)
    seen = [False] * n
    for i in range(n):
        if seen[i]:
            continue
        for j in range(i + 1, n):
            if not seen[j] and abs(spectrum[i] + spectrum[j] - parent_mass) < 0.05:
                prefix_masses.append(spectrum[i])
                seen[i] = True
                seen[j] = True
                break

    prefix_masses.sort()
    peptide = []

    # Ardıcıl kütlələrin fərqinə əsasən amin turşularını tapırıq
    # Compute amino acid chain by matching differences between adjacent prefix masses
    for i in range(len(prefix_masses) - 1):
        diff = prefix_masses[i + 1] - prefix_masses[i]
        best_aa = ""
        min_diff = float("inf")
        for aa, mass in mass_table.items():
            if abs(diff - mass) < 0.05:
                if abs(diff - mass) < min_diff:
                    min_diff = abs(diff - mass)
                    best_aa = aa
        if best_aa:
            peptide.append(best_aa)

    result = "".join(peptide)
    print(result)

    with open(output_path, "w") as f:
        f.write(result + "\n")


if __name__ == "__main__":
    main()
