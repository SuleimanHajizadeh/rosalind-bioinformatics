# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba1j.txt")
    if not os.path.exists(input_file):
        return "", 0, 0
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    text = lines[0]
    k, d = map(int, lines[1].split())
    return text, k, d

def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

# DNT zəncirinin tərs komplementini tapırıq
# Get reverse complement of a DNA string
def reverse_complement(dna):
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return "".join(complement[base] for base in reversed(dna))

def neighbors(pattern, d):
    if d == 0:
        return {pattern}
    if len(pattern) == 1:
        return {'A', 'C', 'G', 'T'}
    neighborhood = set()
    suffix_neighbors = neighbors(pattern[1:], d)
    for suffix in suffix_neighbors:
        if hamming_distance(pattern[1:], suffix) < d:
            for nucleotide in ['A', 'C', 'G', 'T']:
                neighborhood.add(nucleotide + suffix)
        else:
            neighborhood.add(pattern[0] + suffix)
    return neighborhood

# Mismatches və tərs komplement ilə ən çox rast gəlinən k-merləri tapırıq
# Find frequent words with mismatches and reverse complements
def frequent_words_mismatches_reverse(text, k, d):
    counts = {}
    for i in range(len(text) - k + 1):
        kmer = text[i:i+k]
        for neighbor in neighbors(kmer, d):
            counts[neighbor] = counts.get(neighbor, 0) + 1
            
    # Tərs komplementləri də əlavə edirik
    # Add count for reverse complements
    total_counts = {}
    for kmer in counts:
        rc = reverse_complement(kmer)
        total_counts[kmer] = counts[kmer] + counts.get(rc, 0)
        
    max_count = max(total_counts.values())
    return [kmer for kmer, count in total_counts.items() if count == max_count]

def main():
    text, k, d = read_input()
    if not text:
        return
    result = frequent_words_mismatches_reverse(text, k, d)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(result) + "\n")

if __name__ == "__main__":
    main()
