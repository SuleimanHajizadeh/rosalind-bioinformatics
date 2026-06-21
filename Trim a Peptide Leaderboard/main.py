# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba4l.txt")
    if not os.path.exists(input_file):
        return [], [], 0
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    leaderboard = [list(map(int, p.split("-"))) for p in lines[0].split()]
    spectrum = list(map(int, lines[1].split()))
    N = int(lines[2])
    return leaderboard, spectrum, N

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

# Leaderboard-u N namizəd saxlayacaq şəkildə kəsirik
# Trim a peptide leaderboard
def trim(leaderboard, spectrum, N):
    if len(leaderboard) <= N:
        return leaderboard
    scores = [(p, score_linear(p, spectrum)) for p in leaderboard]
    scores.sort(key=lambda x: x[1], reverse=True)
    cutoff = scores[N - 1][1]
    return [p for p, score in scores if score >= cutoff]

def main():
    leaderboard, spectrum, N = read_input()
    if not leaderboard:
        return
    trimmed = trim(leaderboard, spectrum, N)
    
    # Nəticələri formatlayırıq
    # Format trimmed peptides
    result = ["-".join(map(str, p)) for p in trimmed]
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(result) + "\n")

if __name__ == "__main__":
    main()
