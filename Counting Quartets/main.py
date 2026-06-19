import os
import math

# Verilmiş sayda takson üçün mümkün olan kvartetlərin sayını hesablayırıq
# Calculate the number of quartets for a given number of taxa


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, "rosalind_cntq.txt")
    output_path = os.path.join(base_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        lines = f.read().splitlines()

    n = int(lines[0].strip())

    # Kvartetlərin sayını n-dən 4-lü kombinasiya olaraq tapırıq və 1,000,000-a bölürük
    # Find the quartet count using n choose 4 combination modulo 1,000,000
    ans = math.comb(n, 4) % 1000000

    print(f"Taxa count: {n}, Quartets modulo 1M: {ans}")

    with open(output_path, "w") as f:
        f.write(str(ans) + "\n")


if __name__ == "__main__":
    main()
