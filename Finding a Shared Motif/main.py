import os

# FASTA formatlı giriş faylını oxuyuruq
# Parse the FASTA file to load DNA sequences


def read_fasta(file_path):
    sequences = []
    current_seq = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if current_seq:
                    sequences.append("".join(current_seq))
                    current_seq = []
            else:
                current_seq.append(line)
        if current_seq:
            sequences.append("".join(current_seq))
    return sequences


def longest_common_substring(sequences):
    # Ən qısa ardıcıllığı seçib onun bütün alt sətirlərini yoxlayırıq
    # Select the shortest sequence as candidate to search for substrings
    shortest_seq = min(sequences, key=len)
    n = len(shortest_seq)
    lcs = ""

    # İkilik axtarış (binary search) ilə ən uzun ortaq alt sətri (LCS) tapırıq
    # Binary search on length of longest common substring
    low = 1
    high = n

    while low <= high:
        mid = (low + high) // 2
        found = False
        # mid uzunluğunda namizəd alt sətirləri yoxlayırıq
        # Check candidate substrings of length 'mid'
        for i in range(n - mid + 1):
            candidate = shortest_seq[i : i + mid]
            if all(candidate in s for s in sequences):
                lcs = candidate
                found = True
                break

        if found:
            low = mid + 1
        else:
            high = mid - 1
    return lcs


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_lcsm.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    seqs = read_fasta(input_path)
    result = longest_common_substring(seqs)

    print(f"LCS length: {len(result)}")

    with open(output_path, "w") as f:
        f.write(result + "\n")


if __name__ == "__main__":
    main()
