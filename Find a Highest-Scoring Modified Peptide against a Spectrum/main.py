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
    n = len(peptide)
    M = len(spectrum)
    k = num_modifications

    # Standard amino acid masses + sample ones (X, Z)
    aa_mass_map = {
        'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 'T': 101, 'C': 103,
        'I': 113, 'L': 113, 'N': 114, 'D': 115, 'K': 128, 'Q': 128,
        'E': 129, 'M': 131, 'H': 137, 'F': 147, 'R': 156, 'Y': 163, 'W': 186,
        'X': 4, 'Z': 5
    }

    orig_masses = [aa_mass_map[aa] for aa in peptide]

    # DP table: dp[i][j][t] = max score for prefix i at position j with t modifications
    # parent[i][j][t] = (prev_j, prev_t)
    dp = [[[float('-inf')] * (k + 1) for _ in range(M + 1)] for _ in range(n + 1)]
    parent = [[[None] * (k + 1) for _ in range(M + 1)] for _ in range(n + 1)]

    dp[0][0][0] = 0

    for i in range(1, n + 1):
        mass_i = orig_masses[i - 1]

        # best1[t_prev] = (val, index)
        # best2[t_prev] = (val, index)
        best1 = [(float('-inf'), -1) for _ in range(k + 1)]
        best2 = [(float('-inf'), -1) for _ in range(k + 1)]

        # Initialize with j' = 0
        for t_prev in range(k + 1):
            val = dp[i-1][0][t_prev]
            best1[t_prev] = (val, 0)

        for j in range(1, M + 1):
            score_contrib = spectrum[j - 1]

            for t in range(k + 1):
                # Candidate 1: No modification
                prev_j_no_mod = j - mass_i
                if prev_j_no_mod >= 0:
                    val = dp[i - 1][prev_j_no_mod][t] + score_contrib
                    if val > dp[i][j][t]:
                        dp[i][j][t] = val
                        parent[i][j][t] = (prev_j_no_mod, t)

                # Candidate 2: Modification
                if t > 0:
                    t_prev = t - 1
                    b1_val, b1_idx = best1[t_prev]
                    b2_val, b2_idx = best2[t_prev]

                    excluded_idx = j - mass_i
                    best_mod_val = float('-inf')
                    best_mod_idx = -1

                    if b1_idx != excluded_idx:
                        best_mod_val = b1_val
                        best_mod_idx = b1_idx
                    else:
                        best_mod_val = b2_val
                        best_mod_idx = b2_idx

                    if best_mod_val != float('-inf'):
                        val = best_mod_val + score_contrib
                        if val > dp[i][j][t]:
                            dp[i][j][t] = val
                            parent[i][j][t] = (best_mod_idx, t_prev)

            # Update running best1 and best2 with values at j' = j
            for t_prev in range(k + 1):
                val = dp[i-1][j][t_prev]
                b1_val, b1_idx = best1[t_prev]
                b2_val, b2_idx = best2[t_prev]

                if val > b1_val:
                    best2[t_prev] = (b1_val, b1_idx)
                    best1[t_prev] = (val, j)
                elif val > b2_val:
                    best2[t_prev] = (val, j)

    # Find the best score at dp[n][M][t] for t in 0..k
    best_score = float('-inf')
    best_t = -1
    for t in range(k + 1):
        if dp[n][M][t] > best_score:
            best_score = dp[n][M][t]
            best_t = t

    if best_t == -1 or best_score == float('-inf'):
        return "No solution found"

    # Backtrack to find the prefix masses
    curr_j = M
    curr_t = best_t
    path_w = []
    for i in range(n, 0, -1):
        prev_j, prev_t = parent[i][curr_j][curr_t]
        path_w.append(curr_j)
        curr_j = prev_j
        curr_t = prev_t
    path_w.reverse()

    # Reconstruct the modified peptide
    result_parts = []
    prev_w = 0
    for i in range(n):
        w_i = path_w[i]
        delta = (w_i - prev_w) - orig_masses[i]
        aa = peptide[i]
        if delta > 0:
            result_parts.append(f"{aa}(+{delta})")
        elif delta < 0:
            result_parts.append(f"{aa}({delta})")
        else:
            result_parts.append(aa)
        prev_w = w_i

    return "".join(result_parts)

def main():
    import os
    peptide, spectrum, num_modifications = read_input()
    if not peptide:
        return

    result = highest_scoring_modified_peptide(peptide, spectrum, num_modifications)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(result + "\n")
    print("Reconstructed peptide:", result)

if __name__ == "__main__":
    main()

