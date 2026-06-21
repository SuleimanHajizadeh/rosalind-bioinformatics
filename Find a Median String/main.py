# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba2b.txt")
    if not os.path.exists(input_file):
        return 0, []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    k = int(lines[0])
    dna = lines[1:]
    return k, dna

def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

# Bir pattern ilə bir neçə DNT zənciri arasındakı minimum Hamming məsafələrinin cəmini tapırıq
# Compute distance between a pattern and a set of DNA strings
def distance_between_pattern_and_strings(pattern, dna):
    k = len(pattern)
    total_dist = 0
    for seq in dna:
        min_dist = float('inf')
        for i in range(len(seq) - k + 1):
            dist = hamming_distance(pattern, seq[i:i+k])
            if dist < min_dist:
                min_dist = dist
        total_dist += min_dist
    return total_dist

# Bütün mümkün k-merlər üçün ən kiçik məsafəni verən median ardıcıllığı tapırıq
# Find a median string
def find_median_string(dna, k):
    # K-merlər generatoru
    # Generator for all 4^k kmers
    def all_kmers(length):
        if length == 1:
            return ['A', 'C', 'G', 'T']
        kmers = []
        for suffix in all_kmers(length - 1):
            for base in ['A', 'C', 'G', 'T']:
                kmers.append(base + suffix)
        return kmers
        
    best_pattern = ""
    min_dist = float('inf')
    for pattern in all_kmers(k):
        dist = distance_between_pattern_and_strings(pattern, dna)
        if dist < min_dist:
            min_dist = dist
            best_pattern = pattern
    return best_pattern

def main():
    k, dna = read_input()
    if not dna:
        return
    result = find_median_string(dna, k)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(result + "\n")

if __name__ == "__main__":
    main()
