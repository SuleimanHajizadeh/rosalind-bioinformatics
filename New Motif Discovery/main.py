import os
import sys
import collections

# FASTA formatını oxumaq üçün köməkçi funksiya
# Helper function to read and parse FASTA records


def parse_fasta(filepath):
    seqs = []
    curr = []
    with open(filepath) as f:
        for line in f:
            if line.startswith(">"):
                if curr:
                    seqs.append("".join(curr))
                    curr = []
            else:
                curr.append(line.strip())
    if curr:
        seqs.append("".join(curr))
    return seqs


def mismatch_dist(s1, s2):
    # İki ardıcıllıq arasındakı fərqli mövqeləri (mismatch) sayırıq
    # Count mismatch count between two sequences of equal length
    return sum(1 for x, y in zip(s1, s2) if x != y)


def best_match_index(kmer, seq):
    # Ən uyğun (ən az fərqlə) düzülüşün indeksini tapırıq
    # Find the index of the start of the best match of kmer in seq
    best_dist = float("inf")
    best_idx = -1
    for i in range(len(seq) - len(kmer) + 1):
        d = mismatch_dist(kmer, seq[i : i + len(kmer)])
        if d < best_dist:
            best_dist = d
            best_idx = i
    return best_idx, best_dist


def find_seed_20mer(seqs):
    # Digər ardıcıllıqlarda ən az fərqlə tapılan 20-lik motifi axtarırıq
    # Find a 20-mer seed from sequence 1 that matches others with minimal mismatches
    seq0 = seqs[0]
    best_overall_dist = float("inf")
    best_kmer = None

    for i in range(len(seq0) - 19):
        kmer = seq0[i : i + 20]
        total_dist = 0
        for s in seqs[1:]:
            _, d = best_match_index(kmer, s)
            total_dist += d
        if total_dist < best_overall_dist:
            best_overall_dist = total_dist
            best_kmer = kmer
    return best_kmer


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_motz.txt")
    output_path = os.path.join(script_dir, "output.txt")

    # Əgər mövcuddursa, real dataseti oxuyuruq, əks halda rosalind_*.txt faylını axtarırıq
    # Use fallback file if input file isn't present
    import glob

    files = glob.glob(os.path.join(script_dir, "rosalind_*.txt"))
    if not files:
        print("Xəta: Dataset tapılmadı.")
        return
    input_path = files[0]

    seqs = parse_fasta(input_path)
    if not seqs:
        return

    # Ən uyğun motifi tapırıq
    # Find the best 20-mer seed motif
    motif = find_seed_20mer(seqs)

    with open(output_path, "w") as f:
        f.write(motif + "\n")

    print(f"Motif found: {motif}")


if __name__ == "__main__":
    main()
