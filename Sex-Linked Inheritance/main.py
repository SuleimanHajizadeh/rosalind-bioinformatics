#!/usr/bin/env python3
import os

# Cinsi bağlı keçən xəstəlik daşıyıcılıq tezliyini hesablayırıq
# Compute the probability of heterozygous female carriers under Hardy-Weinberg for sex-linked inheritance


def solve_sexl(A):
    B = []
    for q in A:
        p = 1.0 - q
        # Daşıyıcı qadın tezliyi: 2pq
        # Female carrier frequency is calculated as 2pq
        carrier = 2.0 * p * q
        B.append(round(carrier, 3))
    return B


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_sexl.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        content = f.read().strip()

    A = list(map(float, content.split()))
    B = solve_sexl(A)

    result_str = " ".join(map(str, B))
    print(result_str)

    with open(output_path, "w") as f:
        f.write(result_str + "\n")


if __name__ == "__main__":
    main()
