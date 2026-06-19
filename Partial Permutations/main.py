import os

# Hissəvi permutasiyaların sayını P(n, k) modul 1,000,000 ilə hesablayırıq
# Compute the number of partial permutations P(n, k) modulo 1,000,000


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_pper.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as file:
        n, k = map(int, file.read().split())

    # P(n, k) = n * (n - 1) * ... * (n - k + 1)
    # Multiply numbers iteratively and apply modulo at each step
    result = 1
    for i in range(k):
        result = (result * (n - i)) % 1000000

    print(f"Result: {result}")

    with open(output_path, "w") as out_file:
        out_file.write(str(result) + "\n")


if __name__ == "__main__":
    main()
