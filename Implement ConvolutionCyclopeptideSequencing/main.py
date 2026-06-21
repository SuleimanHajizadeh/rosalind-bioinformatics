# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba4i.txt")
    if not os.path.exists(input_file):
        return 0, 0, []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    M = int(lines[0])
    N = int(lines[1])
    spectrum = list(map(int, lines[2].split()))
    return M, N, spectrum

# Spektr konvolusiyasını hesablayırıq
# Compute spectral convolution
def spectral_convolution(spectrum):
    spectrum.sort()
    convolution = []
    n = len(spectrum)
    for i in range(n):
        for j in range(i):
            diff = spectrum[i] - spectrum[j]
            if 57 <= diff <= 200:
                convolution.append(diff)
    return convolution

# Ən populyar kütlələri tapırıq
# Find the top M most frequent masses in the convolution
def get_frequent_masses(spectrum, M):
    conv = spectral_convolution(spectrum)
    counts = {}
    for val in conv:
        counts[val] = counts.get(val, 0) + 1
        
    sorted_masses = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    if len(sorted_masses) <= M:
        return [item[0] for item in sorted_masses]
        
    cutoff = sorted_masses[M-1][1]
    return [item[0] for item in sorted_masses if item[1] >= cutoff]

def linear_spectrum(peptide):
    n = len(peptide)
    prefix_mass = [0] * (n + 1)
    for i in range(n):
        prefix_mass[i+1] = prefix_mass[i] + peptide[i]
    spectrum = [0]
    for length in range(1, n + 1):
        for start in range(n - length + 1):
            spectrum.append(prefix_mass[start+length] - prefix_mass[start])
    spectrum.sort()
    return spectrum

def score_linear(peptide, spectrum):
    theoretical = linear_spectrum(peptide)
    t_counts = {}
    for val in theoretical:
        t_counts[val] = t_counts.get(val, 0) + 1
    s_counts = {}
    for val in spectrum:
        s_counts[val] = s_counts.get(val, 0) + 1
    score = 0
    for val in t_counts:
        if val in s_counts:
            score += min(t_counts[val], s_counts[val])
    return score

def cyclic_spectrum(peptide):
    n = len(peptide)
    prefix_mass = [0] * (n + 1)
    for i in range(n):
        prefix_mass[i+1] = prefix_mass[i] + peptide[i]
    total_mass = prefix_mass[n]
    spectrum = [0, total_mass]
    for length in range(1, n):
        for start in range(n):
            if start + length <= n:
                spectrum.append(prefix_mass[start+length] - prefix_mass[start])
            else:
                spectrum.append(total_mass - (prefix_mass[start] - prefix_mass[start + length - n]))
    spectrum.sort()
    return spectrum

def score_cyclic(peptide, spectrum):
    theoretical = cyclic_spectrum(peptide)
    t_counts = {}
    for val in theoretical:
        t_counts[val] = t_counts.get(val, 0) + 1
    s_counts = {}
    for val in spectrum:
        s_counts[val] = s_counts.get(val, 0) + 1
    score = 0
    for val in t_counts:
        if val in s_counts:
            score += min(t_counts[val], s_counts[val])
    return score

def trim(leaderboard, spectrum, N):
    if len(leaderboard) <= N:
        return leaderboard
    scores = [(p, score_linear(p, spectrum)) for p in leaderboard]
    scores.sort(key=lambda x: x[1], reverse=True)
    cutoff = scores[N - 1][1]
    return [p for p, score in scores if score >= cutoff]

# Konvolusiya əsaslı Cyclopeptide Sequencing alqoritmi
# Implement ConvolutionCyclopeptideSequencing
def convolution_cyclopeptide_sequencing(spectrum, M, N):
    parent_mass = max(spectrum)
    frequent_masses = get_frequent_masses(spectrum, M)
    leaderboard = [[]]
    leader_peptide = []
    leader_score = -1
    
    while leaderboard:
        # Expand
        next_candidates = []
        for p in leaderboard:
            for m in frequent_masses:
                next_candidates.append(p + [m])
                
        leaderboard = []
        for p in next_candidates:
            p_mass = sum(p)
            if p_mass == parent_mass:
                p_score = score_cyclic(p, spectrum)
                if p_score > leader_score:
                    leader_peptide = p
                    leader_score = p_score
            elif p_mass < parent_mass:
                leaderboard.append(p)
                
        leaderboard = trim(leaderboard, spectrum, N)
        
    return "-".join(map(str, leader_peptide))

def main():
    M, N, spectrum = read_input()
    if not spectrum:
        return
    result = convolution_cyclopeptide_sequencing(spectrum, M, N)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(result + "\n")

if __name__ == "__main__":
    main()
