#!/usr/bin/env python3
import os
import math

# Verilmiş başlanğıc dominant allel saylarına görə təsisçi effekti ehtimallarının loqarifmini tapırıq
# Compute the probability distribution of alleles using transition matrices for the founder effect


def solve_foun(N, m, A):
    two_N = 2 * N
    comb = [math.comb(two_N, j) for j in range(two_N + 1)]

    # Keçid matrisini (Transition matrix) T qururuq
    # Populate the Wright-Fisher transition matrix
    T = [[0.0] * (two_N + 1) for _ in range(two_N + 1)]
    for i in range(two_N + 1):
        p = i / two_N
        for j in range(two_N + 1):
            if p == 0:
                T[j][i] = 1.0 if j == 0 else 0.0
            elif p == 1:
                T[j][i] = 1.0 if j == two_N else 0.0
            else:
                T[j][i] = comb[j] * (p**j) * ((1.0 - p) ** (two_N - j))

    results = []
    # Hər bir başlanğıc dominant allel sayı üçün nəsillər üzrə ehtimalı izləyirik
    # Track the propagation of probabilities for each initial count in A
    for k in range(len(A)):
        v = [0.0] * (two_N + 1)
        v[A[k]] = 1.0

        col_res = []
        for gen in range(1, m + 1):
            # Matrisi vektora vururuq: T * v
            # Multiply transition matrix by current probability vector
            v_next = [0.0] * (two_N + 1)
            for j in range(two_N + 1):
                v_next[j] = sum(T[j][i] * v[i] for i in range(two_N + 1))
            v = v_next

            # Allelin itirilməsi ehtimalı v[0]-dır (recessive phenotype fixated)
            # Probability of allele loss is v[0]
            p_zero = v[0]
            if p_zero > 0:
                col_res.append(math.log10(p_zero))
            else:
                col_res.append(-float("inf"))
        results.append(col_res)

    # Matrisi sətir-sətir generasiya etmək üçün translyasiya edirik
    # Transpose the result matrix to match generation rows
    matrix = []
    for i in range(m):
        row = [results[j][i] for j in range(len(A))]
        matrix.append(row)

    return matrix


def main():
    input_path = "rosalind_foun.txt"
    output_path = "output.txt"

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    first_line_parts = lines[0].split()
    N = int(first_line_parts[0])
    m = int(first_line_parts[1])

    A = [int(x) for x in lines[1].split()]

    matrix = solve_foun(N, m, A)

    with open(output_path, "w") as f:
        for row in matrix:
            row_str = " ".join(
                f"{val:.12f}" if val != -float("inf") else "-inf"
                for val in row
            )
            f.write(row_str + "\n")

    print("Founder effect simulation complete.")


if __name__ == "__main__":
    main()
