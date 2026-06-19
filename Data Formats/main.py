import os
import sys
import urllib.request
import urllib.parse

def query_ncbi_fasta(ids):
    """
    Fetch FASTA records from NCBI Nucleotide database for a list of accession IDs.
    """
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
    print(f"Fetching: {url}")
    
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    
    with urllib.request.urlopen(req) as response:
        return response.read().decode('utf-8')

def get_shortest_record(fasta_text):
    """
    Parses a FASTA multi-record string and returns the record with the shortest sequence.
    """
    parts = fasta_text.split('>')
    shortest_record = None
    shortest_len = float('inf')
    
    for part in parts:
        if not part.strip():
            continue
        lines = part.strip().split('\n')
        # Sequence lines are everything after the header line
        seq = "".join(lines[1:]).replace(" ", "").replace("\r", "")
        if len(seq) < shortest_len:
            shortest_len = len(seq)
            shortest_record = ">" + part.strip()
            
    return shortest_record

def main():
    # Discover input file
    input_path = None
    for fname in os.listdir('.'):
        if fname.startswith('rosalind_') and fname.endswith('.txt'):
            input_path = fname
            break
            
    if input_path is None:
        print("Error: No rosalind_*.txt dataset file found in the current directory.")
        sys.exit(1)
        
    print(f"Reading from {input_path}")
    with open(input_path, 'r') as f:
        content = f.read()
        
    # Get all space-separated tokens/IDs
    ids = [token.strip() for token in content.split() if token.strip()]
    if not ids:
        print("Error: No IDs found in the input file.")
        sys.exit(1)
        
    print(f"Found {len(ids)} IDs: {ids}")
    
    # Query NCBI
    try:
        fasta_text = query_ncbi_fasta(ids)
    except Exception as e:
        print(f"Error querying NCBI: {e}")
        sys.exit(1)
        
    # Find shortest record
    shortest = get_shortest_record(fasta_text)
    if shortest is None:
        print("Error: Could not parse any valid records from NCBI response.")
        sys.exit(1)
        
    # Write output
    output_path = "output.txt"
    with open(output_path, "w") as out:
        out.write(shortest + "\n")
        
    print(f"Successfully wrote the shortest record to {output_path}")

if __name__ == '__main__':
    main()
