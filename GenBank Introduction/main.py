import os
import sys
import urllib.request
import urllib.parse
import json

def query_genbank(genus, date_from, date_to):
    """
    Query NCBI Entrez to count Nucleotide entries for a given genus
    published between date_from and date_to (YYYY/M/D format).
    """
    # Convert dates to YYYY/MM/DD format for Entrez
    def format_date(d):
        parts = d.split('/')
        return f"{parts[0]}/{int(parts[1]):02d}/{int(parts[2]):02d}"
    
    from_date = format_date(date_from)
    to_date = format_date(date_to)
    
    query = f"{genus}[Organism] AND {from_date}[PDAT]:{to_date}[PDAT]"
    
    params = urllib.parse.urlencode({
        'db': 'nucleotide',
        'term': query,
        'rettype': 'count',
        'retmode': 'json',
        'tool': 'rosalind_solver',
        'email': 'example@email.com'
    })
    
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?{params}"
    
    print(f"Querying: {url}")
    
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        
    count = int(data['esearchresult']['count'])
    return count

def main():
    # Check for input file
    input_path = None
    for fname in os.listdir('.'):
        if fname.startswith('rosalind_') and fname.endswith('.txt'):
            input_path = fname
            break
    
    if input_path is None:
        print("Error: No rosalind_*.txt dataset file found in the current directory.")
        print("Please download the dataset from Rosalind and place it in this directory.")
        sys.exit(1)
        
    with open(input_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        
    if len(lines) < 3:
        print("Error: Input file must contain a genus name followed by two dates.")
        sys.exit(1)
        
    genus = lines[0]
    date_from = lines[1]
    date_to = lines[2]
    
    print(f"Searching for genus: {genus}")
    print(f"Date range: {date_from} to {date_to}")
    
    count = query_genbank(genus, date_from, date_to)
    
    output_path = "output.txt"
    with open(output_path, "w") as out:
        out.write(f"{count}\n")
        
    print(f"Count: {count}")
    print(f"Written to {output_path}")

if __name__ == '__main__':
    main()
