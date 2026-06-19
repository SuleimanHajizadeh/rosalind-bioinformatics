import os
import sys
from Bio import SeqIO

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Discover input file starting with rosalind_ and ending with .txt
    input_path = None
    for fname in os.listdir(script_dir):
        if fname.startswith('rosalind_') and fname.endswith('.txt'):
            input_path = os.path.join(script_dir, fname)
            break
            
    if input_path is None:
        print("Error: No rosalind_*.txt dataset file found in the script directory.")
        sys.exit(1)
        
    print(f"Reading from {input_path}")
    
    output_path = os.path.join(script_dir, "output.txt")
    
    try:
        count = 0
        with open(input_path, "r") as in_f, open(output_path, "w") as out_f:
            records = SeqIO.parse(in_f, "fastq")
            count = SeqIO.write(records, out_f, "fasta")
            
        print(f"Successfully converted {count} records to {output_path}")
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
