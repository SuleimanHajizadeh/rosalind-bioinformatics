# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba3e.txt")
    if not os.path.exists(input_file):
        return []
    with open(input_file, "r") as f:
        return [line.strip() for line in f if line.strip()]

# K-merlər toplusundan De Bruijn qrafı qururuq
# Construct the De Bruijn graph of a collection of k-mers
def de_bruijn_from_kmers(kmers):
    adj = {}
    for kmer in kmers:
        prefix = kmer[:-1]
        suffix = kmer[1:]
        if prefix not in adj:
            adj[prefix] = []
        adj[prefix].append(suffix)
        
    result_lines = []
    for node in sorted(adj.keys()):
        neighbors = ",".join(sorted(adj[node]))
        result_lines.append(f"{node} -> {neighbors}")
    return result_lines

def main():
    kmers = read_input()
    if not kmers:
        return
    result = de_bruijn_from_kmers(kmers)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(result) + "\n")

if __name__ == "__main__":
    main()
