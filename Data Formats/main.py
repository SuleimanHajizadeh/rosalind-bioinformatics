import os
import sys
import urllib.request
import urllib.parse
from Bio import SeqIO
from io import StringIO

# NCBI GenBank bazasından ən qısa ardıcıllığı axtarıb tapırıq
# Query NCBI database to fetch records and identify the shortest sequence


def query_ncbi_fasta(ids):
    id_list = ",".join(ids)
    params = urllib.parse.urlencode(
        {
            "db": "nucleotide",
            "id": id_list,
            "rettype": "fasta",
            "retmode": "text",
            "tool": "rosalind_solver",
            "email": "example@email.com",
        }
    )
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?{params}"
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode("utf-8")
    except Exception as e:
        print(f"NCBI sorğu xətası: {e}")
        return None


def get_shortest_record(fasta_text):
    # Ən qısa ardıcıllığı tapırıq
    # Parse records and return the record with the shortest sequence
    records = list(SeqIO.parse(StringIO(fasta_text), "fasta"))
    if not records:
        return None
    shortest = min(records, key=lambda r: len(r.seq))
    return shortest


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_frmt.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        sys.exit(1)

    with open(input_path, "r") as f:
        ids = f.read().strip().split()

    print(f"NCBI-dan {len(ids)} ID üçün məlumat yüklənir...")
    fasta_text = query_ncbi_fasta(ids)
    if not fasta_text:
        print("Xəta: NCBI-dan məlumat alınmadı.")
        sys.exit(1)

    shortest = get_shortest_record(fasta_text)

    # Nəticəni yazırıq
    # Output and save shortest record details
    header = f">{shortest.description}"
    sequence = str(shortest.seq)

    print(header)
    print(sequence[:60] + "...")

    with open(output_path, "w") as out:
        out.write(f"{header}\n{sequence}\n")


if __name__ == "__main__":
    main()
