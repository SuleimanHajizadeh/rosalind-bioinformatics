import os
import sys

def main():
    input_path = "rosalind_ini.txt"
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        sys.exit(1)
        
    with open(input_path, 'r') as f:
        seq = f.read().strip()
        
    a_count = seq.count('A')
    c_count = seq.count('C')
    g_count = seq.count('G')
    t_count = seq.count('T')
    
    result = f"{a_count} {c_count} {g_count} {t_count}"
    
    output_path = "output.txt"
    with open(output_path, "w") as out:
        out.write(result + "\n")
        
    print(f"Nucleotide counts: {result}")
    print(f"Written to {output_path}")

if __name__ == '__main__':
    main()
