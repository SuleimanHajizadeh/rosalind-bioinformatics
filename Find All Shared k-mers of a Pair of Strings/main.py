# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba6e.txt")
    if not os.path.exists(input_file):
        return 0, "", ""
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return int(lines[0]), lines[1], lines[2]

# DNT-nin tərs komplementini tapırıq
# Reverse complement
def reverse_complement(dna):
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return "".join(complement[base] for base in reversed(dna))

# İki zəncir arasındakı ortaq k-merləri tapırıq
# Find all shared k-mers of a pair of strings (taking reverse complements into account)
def find_shared_kmers(k, s1, s2):
    # s2-nin bütün k-merlərini sürətli tapmaq üçün lüğət hazırlayırıq
    # Map kmers of s2 to their indices
    s2_kmers = {}
    for j in range(len(s2) - k + 1):
        kmer = s2[j:j+k]
        if kmer not in s2_kmers:
            s2_kmers[kmer] = []
        s2_kmers[kmer].append(j)
        
    shared_positions = []
    
    # s1 k-merlərini yoxlayırıq
    # Check kmers of s1
    for i in range(len(s1) - k + 1):
        kmer = s1[i:i+k]
        rc = reverse_complement(kmer)
        
        # Standart uyğunluq
        # Normal match
        if kmer in s2_kmers:
            for j in s2_kmers[kmer]:
                shared_positions.append((i, j))
        # Tərs komplement uyğunluğu
        # Reverse complement match
        if rc in s2_kmers:
            for j in s2_kmers[rc]:
                shared_positions.append((i, j))
                
    return shared_positions

def main():
    k, s1, s2 = read_input()
    if not s1:
        return
    result = find_shared_kmers(k, s1, s2)
    
    # Mövqeləri formatlayırıq
    # Format coordinate pairs
    output_lines = [f"({i}, {j})" for i, j in result]
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(output_lines) + "\n")

if __name__ == "__main__":
    main()
