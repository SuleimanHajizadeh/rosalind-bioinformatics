import os
import sys
import urllib.request
import urllib.parse
from Bio.Align import PairwiseAligner

# NCBI-dan cüt ardıcıllıqları yükləyib cüt-cüt qlobal düzülüşünü tapırıq
# Fetch pairwise sequences from NCBI and calculate the global alignment score


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


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    import glob

    files = glob.glob(os.path.join(script_dir, "rosalind_*.txt"))
    if not files:
        print("Xəta: Dataset tapılmadı.")
        return
    input_path = files[0]

    with open(input_path, "r") as f:
        ids = f.read().strip().split()

    print(f"NCBI-dan {len(ids)} ID üçün ardıcıllıq yüklənir...")
    fasta_text = query_ncbi_fasta(ids)
    if not fasta_text:
        return

    # FASTA faylını oxuyuruq
    # Parse records
    from Bio import SeqIO
    from io import StringIO

    records = list(SeqIO.parse(StringIO(fasta_text), "fasta"))
    s = str(records[0].seq)
    t = str(records[1].seq)

    # Qlobal düzülüş xalını hesablayırıq
    # Calculate global alignment score
    aligner = PairwiseAligner()
    aligner.mode = "global"
    aligner.match_score = 1
    aligner.mismatch_score = -1
    aligner.open_gap_score = -2
    aligner.extend_gap_score = -2

    score = aligner.score(s, t)
    print(f"Alignment Score: {score}")

    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as f:
        f.write(f"{int(score)}\n")


if __name__ == "__main__":
    main()
