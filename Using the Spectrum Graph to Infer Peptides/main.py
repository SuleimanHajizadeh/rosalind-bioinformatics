import os

# Monoisotopic masses of amino acids
MASS = {
    'A':  71.03711, 'C': 103.00919, 'D': 115.02694, 'E': 129.04259,
    'F': 147.06841, 'G':  57.02146, 'H': 137.05891, 'I': 113.08406,
    'K': 128.09496, 'L': 113.08406, 'M': 131.04049, 'N': 114.04293,
    'P':  97.05276, 'Q': 128.05858, 'R': 156.10111, 'S':  87.03203,
    'T': 101.04768, 'V':  99.06841, 'W': 186.07931, 'Y': 163.06333,
}

TOLERANCE = 0.02   # Da; tight enough to distinguish close masses (e.g. N=114.04 vs D=115.03)

# Pre-sort amino acids by mass for quick lookup
_MASS_LIST = sorted(MASS.items(), key=lambda x: x[1])


def diff_to_aa(diff):
    """Return the amino acid character if diff ≈ its monoisotopic mass, else None."""
    for aa, mass in _MASS_LIST:
        if diff < mass - TOLERANCE:
            break            # masses sorted: no point continuing
        if abs(diff - mass) <= TOLERANCE:
            return aa
    return None


def solve_sgra(input_path, output_path):
    with open(input_path, 'r') as f:
        masses = sorted(float(line.strip()) for line in f if line.strip())

    n = len(masses)
    MAX_AA_MASS = 186.08 + TOLERANCE   # W is the heaviest

    # dp[i] = (path_length, path_string) for longest path ending at node i
    dp = [(0, '') for _ in range(n)]

    for j in range(n):
        for i in range(j - 1, -1, -1):
            diff = masses[j] - masses[i]
            if diff > MAX_AA_MASS:
                break          # masses sorted → all further i give larger diff
            aa = diff_to_aa(diff)
            if aa:
                new_len = dp[i][0] + 1
                if new_len > dp[j][0]:
                    dp[j] = (new_len, dp[i][1] + aa)

    best_len, best_path = max(dp, key=lambda x: x[0])
    result = best_path

    with open(output_path, 'w') as f:
        f.write(result + '\n')

    print(result)


if __name__ == '__main__':
    base = os.path.dirname(os.path.abspath(__file__))
    solve_sgra(
        os.path.join(base, 'rosalind_sgra.txt'),
        os.path.join(base, 'output.txt'),
    )
