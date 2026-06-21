# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba3d.txt")
    if not os.path.exists(input_file):
        return 0, ""
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return int(lines[0]), lines[1]

# Sətirdən De Bruijn qrafı qururuq
# Construct the De Bruijn graph of a string
def de_bruijn_from_string(k, text):
    adj = {}
    for i in range(len(text) - k + 1):
        kmer = text[i:i+k]
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
    k, text = read_input()
    if not text:
        return
    result = de_bruijn_from_string(k, text)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(result) + "\n")

if __name__ == "__main__":
    main()
