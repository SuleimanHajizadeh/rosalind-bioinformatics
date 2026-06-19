import os
import itertools

# Müxtəlif uzunluqlu sətirləri leksikoqrafik ardıcıllıqla generasiya edirik
# Generate all strings of length up to n from an alphabet lexicographically


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_lexv.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        lines = f.read().splitlines()

    alphabet = lines[0].split()
    n = int(lines[1].strip())

    results = []

    # Leksikoqrafik sıranı müəyyən etmək üçün reytinq funksiyası yazırıq
    # Recursively generate strings to match the lexicographical order of the given alphabet
    def generate(curr):
        if len(curr) > 0:
            results.append("".join(curr))
        if len(curr) == n:
            return
        for char in alphabet:
            generate(curr + [char])

    generate([])

    with open(output_path, "w") as f:
        for item in results:
            f.write(item + "\n")

    print(f"Generated {len(results)} strings.")


if __name__ == "__main__":
    main()
