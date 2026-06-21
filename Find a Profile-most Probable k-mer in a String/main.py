# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba2c.txt")
    if not os.path.exists(input_file):
        return "", 0, {}
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    text = lines[0]
    k = int(lines[1])
    
    # Profil matrisini oxuyuruq
    # Parse profile matrix
    profile = {}
    nucleotides = ['A', 'C', 'G', 'T']
    for i, base in enumerate(nucleotides):
        profile[base] = list(map(float, lines[2+i].split()))
    return text, k, profile

# Profil matrisinə əsasən k-merin ehtimalını tapırıq
# Calculate probability of a kmer given a profile matrix
def kmer_probability(kmer, profile):
    prob = 1.0
    for i, base in enumerate(kmer):
        prob *= profile[base][i]
    return prob

# Ən yüksək ehtimallı k-mer-i tapırıq
# Find a profile-most probable k-mer in a string
def profile_most_probable_kmer(text, k, profile):
    best_kmer = text[0:k]
    max_prob = -1.0
    for i in range(len(text) - k + 1):
        kmer = text[i:i+k]
        prob = kmer_probability(kmer, profile)
        if prob > max_prob:
            max_prob = prob
            best_kmer = kmer
    return best_kmer

def main():
    text, k, profile = read_input()
    if not text:
        return
    result = profile_most_probable_kmer(text, k, profile)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(result + "\n")

if __name__ == "__main__":
    main()
