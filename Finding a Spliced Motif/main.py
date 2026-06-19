import os

# Böyük s ardıcıllığında kiçik t ardıcıllığının spliced motif indekslərini tapırıq
# Find the indices of a spliced motif (subsequence) t in a sequence s


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_sseq.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    # FASTA faylını oxuyuruq
    # Parse FASTA file to load two sequences
    with open(input_path, "r") as f:
        lines = f.read().splitlines()

    seqs = []
    current_seq = ""
    for line in lines:
        if line.startswith(">"):
            if current_seq:
                seqs.append(current_seq)
                current_seq = ""
        else:
            current_seq += line.strip()
    if current_seq:
        seqs.append(current_seq)

    s = seqs[0]
    t = seqs[1]

    indices = []
    t_idx = 0
    # t-nin hər bir hərfini s-də axtararaq 1-dən başlayan indeksləri qeyd edirik
    # Scan s and save 1-based indices of matching letters from t sequentially
    for s_idx, char in enumerate(s):
        if t_idx < len(t) and char == t[t_idx]:
            indices.append(s_idx + 1)
            t_idx += 1

    result = " ".join(map(str, indices))
    print(result)

    with open(output_path, "w") as f:
        f.write(result + "\n")


if __name__ == "__main__":
    main()
