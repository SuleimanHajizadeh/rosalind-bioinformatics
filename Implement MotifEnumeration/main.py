# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba2a.txt")
    if not os.path.exists(input_file):
        return 0, 0, []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    k, d = map(int, lines[0].split())
    dna = lines[1:]
    return k, d, dna

def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

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

# Motif Enumeration alqoritmi
# Implement MotifEnumeration
def motif_enumeration(dna, k, d):
    patterns = set()
    first_seq = dna[0]
    for i in range(len(first_seq) - k + 1):
        kmer = first_seq[i:i+k]
        for neighbor in neighbors(kmer, d):
            # Qonşunun bütün digər DNT zəncirlərində d məsafədə olub olmadığını yoxlayırıq
            # Check if this neighbor exists in all other DNA strings with at most d mismatches
            in_all = True
            for seq in dna[1:]:
                found = False
                for j in range(len(seq) - k + 1):
                    if hamming_distance(seq[j:j+k], neighbor) <= d:
                        found = True
                        break
                if not found:
                    in_all = False
                    break
            if in_all:
                patterns.add(neighbor)
    return list(patterns)

def main():
    k, d, dna = read_input()
    if not dna:
        return
    result = motif_enumeration(dna, k, d)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(result) + "\n")

if __name__ == "__main__":
    main()
