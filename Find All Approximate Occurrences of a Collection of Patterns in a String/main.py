# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba9o.txt")
    if not os.path.exists(input_file):
        return "", [], 0
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    text = lines[0]
    patterns = lines[1].split()
    d = int(lines[2])
    return text, patterns, d

def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

# Təxmini naxış axtarışı (approximate pattern matching)
# Find all approximate occurrences of a collection of patterns in a string
def approximate_pattern_matching_all(text, patterns, d):
    positions = []
    for pattern in patterns:
        k = len(pattern)
        for i in range(len(text) - k + 1):
            if hamming_distance(text[i:i+k], pattern) <= d:
                positions.append(i)
    return sorted(list(set(positions)))

def main():
    text, patterns, d = read_input()
    if not text:
        return
    result = approximate_pattern_matching_all(text, patterns, d)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(map(str, result)) + "\n")

if __name__ == "__main__":
    main()
