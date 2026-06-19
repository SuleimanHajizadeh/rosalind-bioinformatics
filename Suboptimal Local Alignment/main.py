import os
import glob
from Bio import SeqIO
from io import StringIO

# İki ardıcıllıqda paylaşılan qısa təkrarlanan motifin sayını tapırıq
# Find the count of a shared inexact repeat (32-40 bp) in two sequences


def count_approx(query, text, max_dist=3):
    # q-dan fərqlənən mövqelərin sayını tapırıq (Hamming məsafəsi)
    # Count windows in text matching query with at most max_dist substitutions
    k = len(query)
    if k > len(text):
        return 0
    count = 0
    for i in range(len(text) - k + 1):
        d = 0
        for j in range(k):
            if query[j] != text[i + j]:
                d += 1
                if d > max_dist:
                    break
        if d <= max_dist:
            count += 1
    return count


def find_repeat(s, t, min_len=32, max_len=40, max_dist=3):
    # Hər uzunluqdakı s-dən götürülmüş k-merləri yoxlayırıq
    # Try all k-mers from s and find the one appearing most in both strings
    best_r = None
    best_cs = 0
    best_ct = 0
    best_total = 0

    for k in range(min_len, max_len + 1):
        for i in range(len(s) - k + 1):
            kmer = s[i:i + k]
            # Əvvəlcə t-də görünüb-görünmədiyini yoxlayırıq
            # Quick check: does this kmer appear at all in t?
            found = False
            for j in range(len(t) - k + 1):
                d = sum(kmer[c] != t[j + c] for c in range(k))
                if d <= max_dist:
                    found = True
                    break
            if not found:
                continue
            cs = count_approx(kmer, s, max_dist)
            ct = count_approx(kmer, t, max_dist)
            if cs >= 2 and ct >= 2:
                total = cs + ct
                if total > best_total:
                    best_total = total
                    best_cs = cs
                    best_ct = ct
                    best_r = kmer

    return best_r, best_cs, best_ct


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_files = glob.glob(os.path.join(script_dir, 'rosalind_*.txt'))

    if not dataset_files:
        print("Xəta: fayl tapılmadı.")
        return

    with open(dataset_files[0], 'r') as f:
        records = list(SeqIO.parse(f, 'fasta'))

    s = str(records[0].seq)
    t = str(records[1].seq)

    # Ən çox təkrarlanan motifi tapırıq
    # Find the most frequently repeated motif in both sequences
    r, cs, ct = find_repeat(s, t)

    result = f"{cs} {ct}"

    # Nəticəni output.txt-ə yazırıq
    # Write result to output.txt
    output_file = os.path.join(script_dir, 'output.txt')
    with open(output_file, 'w') as f:
        f.write(result + '\n')


if __name__ == '__main__':
    main()
