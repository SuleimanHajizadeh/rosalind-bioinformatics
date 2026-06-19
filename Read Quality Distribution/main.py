import os
import sys
import io
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
    
    with open(input_path, 'r') as f:
        first_line = f.readline().strip()
        threshold = int(first_line)
        # Read the rest of the file content
        rest_content = f.read()
        
    print(f"Threshold: {threshold}")
    
    # Parse the rest as FASTQ
    records = SeqIO.parse(io.StringIO(rest_content), "fastq")
    below_threshold_count = 0
    total_records = 0
    
    for r in records:
        total_records += 1
        scores = r.letter_annotations["phred_quality"]
        avg = sum(scores) / len(scores)
        if avg < threshold:
            below_threshold_count += 1
            
    print(f"Total reads: {total_records}")
    print(f"Reads with average quality score below {threshold}: {below_threshold_count}")
    
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out:
        out.write(f"{below_threshold_count}\n")
        
    print(f"Successfully wrote count to {output_path}")

if __name__ == '__main__':
    main()
