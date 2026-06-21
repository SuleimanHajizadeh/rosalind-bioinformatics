# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba1h.txt")
    if not os.path.exists(input_file):
        return "", "", 0
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0], lines[1], int(lines[2])

# İki ardıcıllıq arasındakı Hamming məsafəsini hesablayırıq
# Compute Hamming distance
def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

# Pattern-in mətndə ən çoxu d fərqlə göründüyü mövqeləri tapırıq
# Find all approximate occurrences of a pattern in a string with mismatch limit d
def approximate_pattern_matching(pattern, text, d):
    positions = []
    k = len(pattern)
    for i in range(len(text) - k + 1):
        if hamming_distance(text[i:i+k], pattern) <= d:
            positions.append(i)
    return positions

def main():
    pattern, text, d = read_input()
    if not pattern:
        return
    result = approximate_pattern_matching(pattern, text, d)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(map(str, result)) + "\n")

if __name__ == "__main__":
    main()
