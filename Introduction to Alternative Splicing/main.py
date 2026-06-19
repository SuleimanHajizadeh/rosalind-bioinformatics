import os
import math

# Alternativ splaysinq zamanı kombinasiyaların sayını hesablayırıq
# Calculate the sum of combinations C(n, k) for m <= k <= n modulo 1,000,000


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_aspc.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        line = f.read().strip()

    parts = line.split()
    n = int(parts[0])
    m = int(parts[1])

    # Kombinasiyaların cəmini tapırıq
    # Accumulate combinations modulo 1,000,000
    ans = sum(math.comb(n, k) for k in range(m, n + 1)) % 1000000

    print(f"n = {n}, m = {m}, Result: {ans}")

    with open(output_path, "w") as out_file:
        out_file.write(str(ans) + "\n")


if __name__ == "__main__":
    main()
