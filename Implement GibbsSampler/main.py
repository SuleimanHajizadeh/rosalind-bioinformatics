# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba2g.txt")
    if not os.path.exists(input_file):
        return 0, 0, 0, []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    k, t, N = map(int, lines[0].split())
    dna = lines[1:]
    return k, t, N, dna

import random

def make_profile_pseudocounts(motifs):
    k = len(motifs[0])
    t = len(motifs)
    profile = {base: [1.0] * k for base in ['A', 'C', 'G', 'T']}
    for j in range(t):
        motif = motifs[j]
        for i in range(k):
            profile[motif[i]][i] += 1.0
    denom = t + 4
    for base in ['A', 'C', 'G', 'T']:
        for i in range(k):
            profile[base][i] /= denom
    return profile

# Ehtimal paylanmasına əsasən k-mer seçirik (Optimizasiya olunmuş)
# Select a k-mer from a sequence based on profile-determined probability distribution
def profile_random_kmer(seq, k, profile):
    n = len(seq) - k + 1
    probs = [0.0] * n
    for start in range(n):
        prob = 1.0
        for i in range(k):
            prob *= profile[seq[start + i]][i]
        probs[start] = prob
    
    total = sum(probs)
    if total == 0:
        start = random.randint(0, n - 1)
    else:
        start = random.choices(range(n), weights=probs)[0]
    return seq[start:start+k]

def score_motifs(motifs):
    k = len(motifs[0])
    t = len(motifs)
    total_score = 0
    for i in range(k):
        counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
        for j in range(t):
            counts[motifs[j][i]] += 1
        max_val = max(counts.values())
        total_score += t - max_val
    return total_score

# Gibbs Sampler-i bir dəfə işlədirik
# Run a single instance of GibbsSampler
def gibbs_sampler_once(dna, k, t, N):
    motifs = []
    for seq in dna:
        start = random.randint(0, len(seq) - k)
        motifs.append(seq[start:start+k])
    best_motifs = list(motifs)
    best_score = score_motifs(best_motifs)
    for _ in range(N):
        i = random.randint(0, t - 1)
        reduced_motifs = [motifs[j] for j in range(t) if j != i]
        profile = make_profile_pseudocounts(reduced_motifs)
        motifs[i] = profile_random_kmer(dna[i], k, profile)
        
        curr_score = score_motifs(motifs)
        if curr_score < best_score:
            best_score = curr_score
            best_motifs = list(motifs)
    return best_motifs

# 20 təsadüfi başlanğıc ilə Gibbs Sampler (20 random starts)
# Gibbs Sampler with 20 random starts
def gibbs_sampler(dna, k, t, N):
    best_motifs = gibbs_sampler_once(dna, k, t, N)
    best_score = score_motifs(best_motifs)
    for _ in range(19):  # 20 starts total
        motifs = gibbs_sampler_once(dna, k, t, N)
        curr_score = score_motifs(motifs)
        if curr_score < best_score:
            best_score = curr_score
            best_motifs = motifs
    return best_motifs

def main():
    k, t, N, dna = read_input()
    if not dna:
        return
    result = gibbs_sampler(dna, k, t, N)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(result) + "\n")
    print("Best score found:", score_motifs(result))

if __name__ == "__main__":
    main()
