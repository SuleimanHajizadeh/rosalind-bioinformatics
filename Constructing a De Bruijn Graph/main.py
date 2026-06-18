import os

def reverse_complement(s):
    rc_map = str.maketrans('ATCG', 'TAGC')
    return s.translate(rc_map)[::-1]

def read_input(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_dbru.txt")
    
    print(f"Reading input from: {input_path}")
    raw_reads = read_input(input_path)
    print(f"Loaded {len(raw_reads)} raw reads.")
    
    # Compute the union of reads and their reverse complements
    U = set()
    for read in raw_reads:
        U.add(read)
        U.add(reverse_complement(read))
        
    print(f"Unique (k+1)-mers in U: {len(U)}")
    
    # Build the de Bruijn graph edges
    edges = set()
    for mer in U:
        prefix = mer[:-1]
        suffix = mer[1:]
        edges.add((prefix, suffix))
        
    # Sort the edges lexicographically
    sorted_edges = sorted(list(edges))
    print(f"Generated {len(sorted_edges)} edges.")
    
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        for u, v in sorted_edges:
            out_file.write(f"({u}, {v})\n")
            
    print(f"De Bruijn graph adjacency list written to: {output_path}")

if __name__ == "__main__":
    main()
