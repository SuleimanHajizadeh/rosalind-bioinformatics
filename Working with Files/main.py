import os
import sys

# Faylı oxuyuruq və yalnız cüt nömrəli sətirləri süzüb (filtr) yazırıq
# Filter even-numbered lines from the input file and write them to output


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_ini5.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        sys.exit(1)

    # Giriş faylını oxuyur, cüt sətirləri output.txt-ə yazırıq
    # Iterate lines and write even index lines (1-based index)
    with open(input_path, "r") as f_in, open(output_path, "w") as f_out:
        for idx, line in enumerate(f_in, start=1):
            if idx % 2 == 0:
                f_out.write(line)

    print("Cüt nömrəli sətirlər uğurla yazıldı.")


if __name__ == "__main__":
    main()
