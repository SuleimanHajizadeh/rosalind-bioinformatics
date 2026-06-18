import os
import math

def read_fasta(file_path):
    seq = ""
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line.startswith(">"):
                seq += line
    return seq

def perm(n, k):
    return math.factorial(n) // math.factorial(n - k)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_mmch.txt")
    
    seq = read_fasta(input_path)
    
    n_A = seq.count('A')
    n_U = seq.count('U')
    n_G = seq.count('G')
    n_C = seq.count('C')
    
    print(f"Dizinin uzunluğu: {len(seq)}")
    print(f"Sayğaclar: A={n_A}, U={n_U}, G={n_G}, C={n_C}")
    
    au_ways = perm(max(n_A, n_U), min(n_A, n_U))
    gc_ways = perm(max(n_G, n_C), min(n_G, n_C))
    
    total_ways = au_ways * gc_ways
    
    print(f"Maksimal AU cütləşmə yollarının sayı: {au_ways}")
    print(f"Maksimal GC cütləşmə yollarının sayı: {gc_ways}")
    print(f"Ümumi maksimal cütləşmə (maximum matchings): {total_ways}")
    
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        out_file.write(str(total_ways) + "\n")

if __name__ == "__main__":
    main()
