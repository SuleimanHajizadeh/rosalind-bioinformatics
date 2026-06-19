import os
import sys

# Genetik sətirlərdən (splits) simvol cədvəlini (character table) qururuq
# Build character table representing nontrivial splits from a group of DNA sequences


def solve_cstr(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        strings = [line.strip() for line in f if line.strip()]

    n = len(strings)
    L = len(strings[0])

    splits = []
    # Hər mövqe üzrə hərfləri analiz edərək uyğun bölünmələri tapırıq
    # Group sequences by character at each position: check for nontrivial splits
    for col in range(L):
        chars = [strings[row][col] for row in range(n)]
        unique_chars = list(set(chars))

        if len(unique_chars) == 2:
            c0, c1 = unique_chars[0], unique_chars[1]
            count0 = chars.count(c0)
            count1 = chars.count(c1)

            # Əgər hər iki qrupda ən azı 2 ardıcıllıq varsa (nontrivial split)
            # Only keep splits with at least 2 sequences in each group
            if count0 >= 2 and count1 >= 2:
                split_row = []
                # Birinci simvola '1', ikinciyə '0' verərək kodu qururuq
                # Reconstruct split configuration using '1' and '0'
                for val in chars:
                    split_row.append("1" if val == c0 else "0")
                splits.append("".join(split_row))

    with open(output_path, "w") as f:
        for split in splits:
            f.write(split + "\n")

    print(f"Nontrivial splits generated: {len(splits)}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_cstr.txt")
    output_file = os.path.join(script_dir, "output.txt")
    solve_cstr(input_file, output_file)
