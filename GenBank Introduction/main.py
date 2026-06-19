import os
import sys
import urllib.request
import urllib.parse
import json

# NCBI GenBank bazasında verilmiş tarixlər arasında növə uyğun neçə qeyd olduğunu tapırıq
# Query NCBI database to count records of a species published between two dates


def query_genbank(species, date_start, date_end):
    # Sorğu tarix formatını ncbi uyğunlaşdırırıq: YYYY/MM/DD
    # Query string for GenBank search
    query = f'"{species}"[Organism] AND ("{date_start}"[PDAT] : "{date_end}"[PDAT])'
    params = urllib.parse.urlencode(
        {
            "db": "nucleotide",
            "term": query,
            "rettype": "count",
            "retmode": "json",
            "tool": "rosalind_solver",
            "email": "example@email.com",
        }
    )
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?{params}"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode("utf-8"))
            return int(data["esearchresult"]["count"])
    except Exception as e:
        print(f"NCBI GenBank sorğu xətası: {e}")
        return 0


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_gbk.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        sys.exit(1)

    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    species = lines[0]
    date_start = lines[1]
    date_end = lines[2]

    count = query_genbank(species, date_start, date_end)
    print(f"Records found: {count}")

    with open(output_path, "w") as out:
        out.write(str(count) + "\n")


if __name__ == "__main__":
    main()
