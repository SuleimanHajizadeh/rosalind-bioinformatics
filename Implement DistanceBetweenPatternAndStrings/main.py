# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba2h.txt")
    if not os.path.exists(input_file):
        return "", []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    pattern = lines[0]
    dna = lines[1].split()
    return pattern, dna

def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

# Bir pattern ilə DNT zəncirlər toplusu arasındakı məsafəni hesablayırıq
# Implement DistanceBetweenPatternAndStrings
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

def main():
    pattern, dna = read_input()
    if not pattern:
        return
    result = distance_between_pattern_and_strings(pattern, dna)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(str(result) + "\n")

if __name__ == "__main__":
    main()
