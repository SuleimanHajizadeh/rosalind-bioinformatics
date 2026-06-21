# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba1b.txt")
    if not os.path.exists(input_file):
        return "", 0
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0], int(lines[1])

# Ən tez-tez təkrarlanan k-merləri tapırıq
# Find the most frequent k-mers in a string
def most_frequent_kmers(text, k):
    counts = {}
    for i in range(len(text) - k + 1):
        kmer = text[i:i+k]
        counts[kmer] = counts.get(kmer, 0) + 1
    max_count = max(counts.values())
    return [kmer for kmer, count in counts.items() if count == max_count]

def main():
    text, k = read_input()
    if not text:
        return
    result = most_frequent_kmers(text, k)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(result) + "\n")

if __name__ == "__main__":
    main()
