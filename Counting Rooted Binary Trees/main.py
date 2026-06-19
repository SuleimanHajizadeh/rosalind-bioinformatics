import os

# Verilmiş n yarpaqlı köklü binar ağacların sayını modul 1,000,000-da tapırıq
# Compute the number of rooted binary trees for n leaves modulo 1,000,000


def solve_root(n):
    if n < 2:
        return 1
    ans = 1
    # Köklü ağacların sayı (2n-3)!! düsturu ilə tapılır
    # Rooted tree counts are calculated as (2n-3)!! double factorial
    for i in range(3, 2 * n - 1, 2):
        ans = (ans * i) % 1000000
    return ans


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_root.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        n = int(f.read().strip())

    ans = solve_root(n)
    print(ans)

    with open(output_path, "w") as f:
        f.write(str(ans) + "\n")


if __name__ == "__main__":
    main()
