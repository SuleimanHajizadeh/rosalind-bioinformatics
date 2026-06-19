import os

# FASTA formatını parçalayırıq
# Parse sequence strings from the FASTA file


def parse_fasta(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    seqs = []
    curr = []
    for line in lines:
        if line.startswith(">"):
            if curr:
                seqs.append("".join(curr))
                curr = []
        else:
            curr.append(line)
    if curr:
        seqs.append("".join(curr))
    return seqs


def find_overlap(s1, s2):
    # İki sətir arasındakı üst-üstə düşməni (overlap) tapırıq (ən azı uzunluğun yarısı qədər)
    # Find the overlap size between suffix of s1 and prefix of s2 (minimum overlap > len / 2)
    min_overlap = max(len(s1), len(s2)) // 2
    for overlap in range(len(s1), min_overlap - 1, -1):
        if s2.startswith(s1[-overlap:]):
            return overlap
    return 0


def solve_long(input_path, output_path):
    reads = parse_fasta(input_path)

    # Oxunuşları birləşdirərək ən qısa super sətiri (Shortest Common Superstring) tapırıq
    # Iteratively merge reads with maximum overlap to reconstruct the genome
    while len(reads) > 1:
        max_overlap = -1
        best_pair = (-1, -1)
        merged_str = ""

        # Hər bir cütü yoxlayırıq
        # Test overlaps for all pairs of reads
        for i in range(len(reads)):
            for j in range(len(reads)):
                if i == j:
                    continue
                overlap = find_overlap(reads[i], reads[j])
                if overlap > max_overlap:
                    max_overlap = overlap
                    best_pair = (i, j)
                    merged_str = reads[i] + reads[j][overlap:]

        i, j = best_pair
        # Birləşən cütü çıxarıb yeni birləşmiş sətri əlavə edirik
        # Update reads list by removing merged pair and adding the superstring
        if i > j:
            reads.pop(i)
            reads.pop(j)
        else:
            reads.pop(j)
            reads.pop(i)
        reads.append(merged_str)

    result = reads[0]

    with open(output_path, "w") as f:
        f.write(result + "\n")

    print(f"Superstring length: {len(result)}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_long.txt")
    output_file = os.path.join(script_dir, "output.txt")
    solve_long(input_file, output_file)
