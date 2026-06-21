# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba1g.txt")
    if not os.path.exists(input_file):
        return "", ""
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0], lines[1]

# İki ardıcıllıq arasındakı Hamming məsafəsini hesablayırıq
# Compute the Hamming distance between two strings
def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def main():
    s1, s2 = read_input()
    if not s1:
        return
    result = hamming_distance(s1, s2)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(str(result) + "\n")

if __name__ == "__main__":
    main()
