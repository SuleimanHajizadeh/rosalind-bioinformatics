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
    profile = {base: [0.0]*k for base in ['A', 'C', 'G', 'T']}
    for i in range(k):
        col = [motifs[j][i] for j in range(t)]
        for base in ['A', 'C', 'G', 'T']:
            profile[base][i] = (col.count(base) + 1) / (t + 4)
    return profile

def kmer_probability(kmer, profile):
    prob = 1.0
    for i, base in enumerate(kmer):
        prob *= profile[base][i]
    return prob

# Ehtimal paylanmasına əsasən k-mer seçirik
# Select a k-mer from a sequence based on profile-determined probability distribution
def profile_random_kmer(seq, k, profile):
    probs = []
    kmers = []
    for i in range(len(seq) - k + 1):
        kmer = seq[i:i+k]
        kmers.append(kmer)
        probs.append(kmer_probability(kmer, profile))
    total = sum(probs)
    if total == 0:
        return random.choice(kmers)
    norm_probs = [p / total for p in probs]
    r = random.random()
    cumulative = 0.0
    for kmer, p in zip(kmers, norm_probs):
        cumulative += p
        if r <= cumulative:
            return kmer
    return kmers[-1]

def score_motifs(motifs):
    k = len(motifs[0])
    t = len(motifs)
    total_score = 0
    for i in range(k):
        col = [motifs[j][i] for j in range(t)]
        frequent_char = max(set(col), key=col.count)
        total_score += t - col.count(frequent_char)
    return total_score

# Gibbs Sampler-i bir dəfə işlədirik
# Run a single instance of GibbsSampler
def gibbs_sampler_once(dna, k, t, N):
    motifs = []
    for seq in dna:
        start = random.randint(0, len(seq) - k)
        motifs.append(seq[start:start+k])
    best_motifs = list(motifs)
    for _ in range(N):
        i = random.randint(0, t - 1)
        reduced_motifs = [motifs[j] for j in range(t) if j != i]
        profile = make_profile_pseudocounts(reduced_motifs)
        motifs[i] = profile_random_kmer(dna[i], k, profile)
        if score_motifs(motifs) < score_motifs(best_motifs):
            best_motifs = list(motifs)
    return best_motifs

# Çoxsaylı Gibbs Sampler işəsalması
# Gibbs Sampler with multiple starts
def gibbs_sampler(dna, k, t, N):
    best_motifs = gibbs_sampler_once(dna, k, t, N)
    for _ in range(50):
        motifs = gibbs_sampler_once(dna, k, t, N)
        if score_motifs(motifs) < score_motifs(best_motifs):
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

if __name__ == "__main__":
    main()
