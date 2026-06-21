# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba2e.txt")
    if not os.path.exists(input_file):
        return 0, 0, []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    k, t = map(int, lines[0].split())
    dna = lines[1:]
    return k, t, dna

# Laplas ardıcıllığı (pseudocounts) ilə profil matrisi qururuq
# Create a profile matrix with pseudocounts from a set of motifs
def make_profile_pseudocounts(motifs):
    k = len(motifs[0])
    t = len(motifs)
    profile = {base: [0.0]*k for base in ['A', 'C', 'G', 'T']}
    for i in range(k):
        col = [motifs[j][i] for j in range(t)]
        for base in ['A', 'C', 'G', 'T']:
            # Pseudocount olaraq hər vəziyyətə 1 əlavə edirik, məxrəcə isə 4
            # Add 1 to count, 4 to denominator
            profile[base][i] = (col.count(base) + 1) / (t + 4)
    return profile

def kmer_probability(kmer, profile):
    prob = 1.0
    for i, base in enumerate(kmer):
        prob *= profile[base][i]
    return prob

def profile_most_probable(text, k, profile):
    best_kmer = text[0:k]
    max_prob = -1.0
    for i in range(len(text) - k + 1):
        kmer = text[i:i+k]
        prob = kmer_probability(kmer, profile)
        if prob > max_prob:
            max_prob = prob
            best_kmer = kmer
    return best_kmer

def score_motifs(motifs):
    k = len(motifs[0])
    t = len(motifs)
    total_score = 0
    for i in range(k):
        col = [motifs[j][i] for j in range(t)]
        frequent_char = max(set(col), key=col.count)
        total_score += t - col.count(frequent_char)
    return total_score

# Pseudocounts ilə Greedy Motif Search alqoritmi
# Implement GreedyMotifSearch with pseudocounts
def greedy_motif_search_pseudocounts(dna, k, t):
    best_motifs = [seq[0:k] for seq in dna]
    first_seq = dna[0]
    for i in range(len(first_seq) - k + 1):
        motifs = [first_seq[i:i+k]]
        for j in range(1, t):
            profile = make_profile_pseudocounts(motifs)
            motifs.append(profile_most_probable(dna[j], k, profile))
        if score_motifs(motifs) < score_motifs(best_motifs):
            best_motifs = motifs
    return best_motifs

def main():
    k, t, dna = read_input()
    if not dna:
        return
    result = greedy_motif_search_pseudocounts(dna, k, t)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(result) + "\n")

if __name__ == "__main__":
    main()
