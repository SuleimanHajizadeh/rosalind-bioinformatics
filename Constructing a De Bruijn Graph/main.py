import os

# De Bruijn qrafı qurmaq üçün komplementar zənciri tapırıq
# Helper to get the reverse complement of a DNA sequence


def reverse_complement(s):
    rc_map = str.maketrans("ATCG", "TAGC")
    return s.translate(rc_map)[::-1]


def read_input(file_path):
    # Giriş faylından oxunuşları oxuyuruq
    # Read the reads from the input file
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_dbru.txt")
    raw_reads = read_input(input_path)

    # Oxunuşlar və onların komplementar zəncirlərinin birləşməsini tapırıq (U)
    # Compute the union of reads and their reverse complements (U)
    U = set()
    for read in raw_reads:
        U.add(read)
        U.add(reverse_complement(read))

    # De Bruijn qrafının tillərini qururuq
    # Build the de Bruijn graph edges
    edges = set()
    for mer in U:
        prefix = mer[:-1]
        suffix = mer[1:]
        edges.add((prefix, suffix))

    # Tilləri leksikoqrafik olaraq sıralayırıq
    # Sort the edges lexicographically
    sorted_edges = sorted(list(edges))

    # Nəticəni output.txt faylına yazırıq
    # Write the edges list to output.txt
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        for u, v in sorted_edges:
            out_file.write(f"({u}, {v})\n")

    print(f"Generated {len(sorted_edges)} edges.")


if __name__ == "__main__":
    main()
