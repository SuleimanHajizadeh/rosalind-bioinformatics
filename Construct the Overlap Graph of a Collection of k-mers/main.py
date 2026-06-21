# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba3c.txt")
    if not os.path.exists(input_file):
        return []
    with open(input_file, "r") as f:
        return [line.strip() for line in f if line.strip()]

# K-merlər toplusunun üst-üstə düşmə qrafını (overlap graph) qururuq
# Construct the overlap graph of a collection of k-mers
def overlap_graph(kmers):
    adj_list = []
    for kmer1 in kmers:
        suffix = kmer1[1:]
        for kmer2 in kmers:
            if kmer2.startswith(suffix):
                adj_list.append(f"{kmer1} -> {kmer2}")
    return adj_list

def main():
    kmers = read_input()
    if not kmers:
        return
    result = overlap_graph(kmers)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(result) + "\n")

if __name__ == "__main__":
    main()
