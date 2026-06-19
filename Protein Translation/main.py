import os
import sys
import warnings
from Bio.Seq import translate
from Bio.Seq import BiopythonWarning

# Suppress Biopython warnings about codons coding for both STOP and an amino acid
warnings.simplefilter('ignore', BiopythonWarning)

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
        lines = [line.strip() for line in f if line.strip()]
        
    if len(lines) < 2:
        print("Error: Expected at least 2 lines (DNA and Protein sequences)")
        sys.exit(1)
        
    dna = lines[0]
    expected_protein = lines[1]
    
    print(f"DNA length: {len(dna)}")
    print(f"Protein length: {len(expected_protein)}")
    
    # Test NCBI translation tables 1 to 33
    matched_table = None
    for table_id in range(1, 34):
        try:
            # translate the DNA sequence (to_stop=False to see all codons)
            translated = str(translate(dna, table=table_id, to_stop=False))
            
            # Strategy 1: strip ALL stop codons and compare
            if translated.replace("*", "") == expected_protein:
                matched_table = table_id
                break
            
            # Strategy 2: strip only TRAILING stop codons and compare
            if translated.rstrip("*") == expected_protein:
                matched_table = table_id
                break
            
            # Strategy 3: compare only the first len(expected_protein) characters
            # This handles the case where the last codon is recoded but others
            # within the sequence are treated as amino acids by this table
            if translated[:len(expected_protein)] == expected_protein:
                matched_table = table_id
                break
                
        except Exception:
            pass
            
    if matched_table is None:
        print("Error: No codon table matches the translated protein.")
        sys.exit(1)
        
    print(f"Found matching codon table ID: {matched_table}")
    
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out:
        out.write(f"{matched_table}\n")
        
    print(f"Successfully wrote table ID to {output_path}")

if __name__ == '__main__':
    main()
