import os

# Verilmiş n elementi olan çoxluğun alt çoxluqlarının sayını modul 1,000,000-da tapırıq
# Compute the number of subsets for a set of size n modulo 1,000,000


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_sset.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        n = int(f.read().strip())

    # Alt çoxluqların sayı 2^n düsturu ilə tapılır
    # Total subsets count is computed as 2^n modulo 1,000,000
    ans = pow(2, n, 1000000)

    print(f"n = {n}, Subsets: {ans}")

    with open(output_path, "w") as out_file:
        out_file.write(str(ans) + "\n")


if __name__ == "__main__":
    main()
