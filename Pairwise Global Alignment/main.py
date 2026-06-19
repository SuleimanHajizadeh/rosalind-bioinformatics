import os
import sys
import urllib.request
import urllib.parse
from Bio.Align import PairwiseAligner, substitution_matrices

def query_ncbi_fasta(ids):
    id_list = ",".join(ids)
    params = urllib.parse.urlencode({
        'db': 'nucleotide',
        'id': id_list,
        'rettype': 'fasta',
        'retmode': 'text',
        'tool': 'rosalind_solver',
        'email': 'example@email.com'
    })
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?{params}"
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req) as response:
        return response.read().decode('utf-8')

def parse_fasta(fasta_text):
    records = []
    current_seq = []
    for line in fasta_text.strip().split('\n'):
        if line.startswith('>'):
            if current_seq:
                records.append("".join(current_seq))
                current_seq = []
        else:
            current_seq.append(line.strip())
    if current_seq:
        records.append("".join(current_seq))
    return records

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
        content = f.read().strip()
        
    ids = [token.strip() for token in content.split() if token.strip()]
    if len(ids) != 2:
        print(f"Error: Expected exactly 2 accession IDs in {input_path}, found {len(ids)}")
        sys.exit(1)
        
    print(f"IDs to align: {ids}")
    
    try:
        fasta_text = query_ncbi_fasta(ids)
    except Exception as e:
        print(f"Error querying NCBI: {e}")
        sys.exit(1)
        
    sequences = parse_fasta(fasta_text)
    if len(sequences) != 2:
        print(f"Error: Expected 2 sequences from NCBI, got {len(sequences)}")
        sys.exit(1)
        
    print(f"Sequence 1 length: {len(sequences[0])}")
    print(f"Sequence 2 length: {len(sequences[1])}")
    
    aligner = PairwiseAligner()
    aligner.mode = 'global'
    aligner.substitution_matrix = substitution_matrices.load("NUC.4.4")
    aligner.open_gap_score = -10
    aligner.extend_gap_score = -1
    
    score = aligner.score(sequences[0], sequences[1])
    int_score = int(round(score))
    print(f"Global Alignment Score: {int_score}")
    
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out:
        out.write(f"{int_score}\n")
        
    print(f"Successfully wrote score to {output_path}")

if __name__ == '__main__':
    main()
