import os
import urllib.request
from Bio import SeqIO
from io import StringIO

# UniProt-dan FASTA ardıcıllığını yükləyirik
# Fetch FASTA sequence for a UniProt ID from the web database
def get_fasta_sequence(uniprot_id):
    # Bəzi UniProt ID-lərdə alt zəncir verilə bilər (məs. B5ZC00_CLIOC), onları təmizləyirik
    # Handle accessions with trailing descriptions (e.g. B5ZC00_CLIOC -> B5ZC00)
    clean_id = uniprot_id.split('_')[0]
    url = f"https://rest.uniprot.org/uniprotkb/{clean_id}.fasta"
    try:
        with urllib.request.urlopen(url) as response:
            fasta_data = response.read().decode('utf-8')
            # SeqIO ilə faylı oxuyuruq
            # Parse record using Biopython
            record = SeqIO.read(StringIO(fasta_data), "fasta")
            return str(record.seq)
    except Exception as e:
        print(f"Xəta: ID {uniprot_id} yüklənə bilmədi. {e}")
        return ""

# N-glycosylation motif mövqelərini tapırıq: N{P}[ST]{P}
# Find occurrences of the N-glycosylation motif: N{P}[ST]{P}
def find_motif_positions(sequence):
    positions = []
    # N-glycosylation motif şablonu: N, sonra P olmayan, sonra S və ya T, sonra P olmayan
    # Check regular expression constraints manually
    for i in range(len(sequence) - 3):
        if sequence[i] == 'N':
            if sequence[i+1] != 'P':
                if sequence[i+2] in ['S', 'T']:
                    if sequence[i+3] != 'P':
                        positions.append(i + 1)
    return positions

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_mprt.txt")
    output_path = os.path.join(script_dir, "output.txt")
    
    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return
        
    with open(input_path, 'r') as f:
        uniprot_ids = [line.strip() for line in f if line.strip()]
        
    output_lines = []
    # Hər bir protein üçün axtarış edirik
    # Process each protein ID
    for uid in uniprot_ids:
        seq = get_fasta_sequence(uid)
        if seq:
            pos = find_motif_positions(seq)
            if pos:
                output_lines.append(uid)
                output_lines.append(" ".join(map(str, pos)))
                
    # Nəticələri yazdırırıq və fayla yazırıq
    # Output and save the results
    with open(output_path, "w") as out:
        for line in output_lines:
            print(line)
            out.write(line + "\n")

if __name__ == '__main__':
    main()
