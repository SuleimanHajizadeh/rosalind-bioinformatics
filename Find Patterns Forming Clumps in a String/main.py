# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba1e.txt")
    if not os.path.exists(input_file):
        return "", 0, 0, 0
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    genome = lines[0]
    k, L, t = map(int, lines[1].split())
    return genome, k, L, t

# Müəyyən bir pəncərədə t dəfə təkrarlanan k-merləri tapırıq
# Find patterns forming (L, t)-clumps in genome
def find_clumps(genome, k, L, t):
    clumps = set()
    for i in range(len(genome) - L + 1):
        window = genome[i:i+L]
        counts = {}
        for j in range(L - k + 1):
            kmer = window[j:j+k]
            counts[kmer] = counts.get(kmer, 0) + 1
            if counts[kmer] >= t:
                clumps.add(kmer)
    return list(clumps)

def main():
    genome, k, L, t = read_input()
    if not genome:
        return
    result = find_clumps(genome, k, L, t)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(result) + "\n")

if __name__ == "__main__":
    main()
