# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba3a.txt")
    if not os.path.exists(input_file):
        return 0, ""
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return int(lines[0]), lines[1]

# K-mer tərkibini tapıb əlifba sırası ilə düzürük
# Generate the k-mer composition of a string (sorted lexicographically)
def kmer_composition(k, text):
    kmers = []
    for i in range(len(text) - k + 1):
        kmers.append(text[i:i+k])
    kmers.sort()
    return kmers

def main():
    k, text = read_input()
    if not text:
        return
    result = kmer_composition(k, text)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(result) + "\n")

if __name__ == "__main__":
    main()
