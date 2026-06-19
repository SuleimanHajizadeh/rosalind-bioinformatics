import os
import sys

# Mətni müəyyən edilmiş koordinatlar üzrə kəsib birləşdiririk
# Read input file and slice sequence string based on given indices


def main():
    input_path = "rosalind_ini3.txt"
    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        sys.exit(1)

    with open(input_path, "r") as f:
        lines = f.readlines()

    if len(lines) < 2:
        print("Xəta: Giriş faylında ən azı 2 sətir olmalıdır.")
        sys.exit(1)

    s = lines[0].strip()
    nums = list(map(int, lines[1].strip().split()))

    a, b, c, d = nums

    # Göstərilən indekslər üzrə kəsikləri birləşdiririk
    # Slice strings inclusively using coordinates (a, b) and (c, d)
    slice1 = s[a : b + 1]
    slice2 = s[c : d + 1]

    result = f"{slice1} {slice2}"
    print(result)

    output_path = "output.txt"
    with open(output_path, "w") as out:
        out.write(result + "\n")


if __name__ == "__main__":
    main()
