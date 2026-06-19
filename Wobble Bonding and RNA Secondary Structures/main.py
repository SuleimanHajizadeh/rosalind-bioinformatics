import os
import sys

# Vobbl cütləşməsini (wobble bonding) nəzərə alaraq mümkün ikincili strukturların sayını tapırıq
# Compute the number of RNA secondary structures with wobble bonding (A-U, C-G, G-U)


def solve_rnas(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        s = f.read().strip()

    print(f"RNA String length: {len(s)}")

    valid_pairs = {
        ("A", "U"),
        ("U", "A"),
        ("C", "G"),
        ("G", "C"),
        ("U", "G"),
        ("G", "U"),
    }

    memo = {}

    def count_structures(i, j):
        if i >= j - 3:
            return 1
        state = (i, j)
        if state in memo:
            return memo[state]

        # 1. Mövqe j cütləşmir
        # Option 1: s[j] is unpaired
        ans = count_structures(i, j - 1)

        # 2. Mövqe j, k ilə cütləşir
        # Option 2: s[j] is paired with s[k]
        for k in range(i, j - 3):
            if (s[k], s[j]) in valid_pairs:
                ans += count_structures(i, k - 1) * count_structures(
                    k + 1, j - 1
                )

        memo[state] = ans
        return ans

    ans = count_structures(0, len(s) - 1)
    print(f"Structures count: {ans}")

    with open(output_path, "w") as f:
        f.write(str(ans) + "\n")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_rnas.txt")
    output_file = os.path.join(script_dir, "output.txt")
    solve_rnas(input_file, output_file)
