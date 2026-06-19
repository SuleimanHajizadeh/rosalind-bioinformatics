#!/usr/bin/env python3
import os
import math

# Rayt-Fişer (Wright-Fisher) genetik drift modelini populyasiya ehtimalları üzrə hesablayırıq
# Compute Wright-Fisher model of genetic drift using transition probability matrix


def solve_wfmd(N, m, g, k):
    num_alleles = 2 * N

    # P[i] dominant allellərin sayının i olması ehtimalını saxlayır
    # P[i] is the probability of having i dominant alleles in the population
    P = [0.0] * (num_alleles + 1)
    P[m] = 1.0

    # Nəsil addımları boyunca ehtimalları yeniləyirik
    # Step through generation steps to update allele distribution
    for gen in range(g):
        next_P = [0.0] * (num_alleles + 1)
        for next_i in range(num_alleles + 1):
            prob_sum = 0.0
            # Növbəti nəsil üçün binomial keçid ehtimalını tapırıq
            # Apply transition probability based on binomial distribution
            for curr_i in range(num_alleles + 1):
                p = curr_i / num_alleles
                # nCr(total, next_i) * p^next_i * (1-p)^(total-next_i)
                transition = (
                    math.comb(num_alleles, next_i)
                    * (p**next_i)
                    * ((1.0 - p) ** (num_alleles - next_i))
                )
                prob_sum += P[curr_i] * transition
            next_P[next_i] = prob_sum
        P = next_P

    # Ən azı k dominant allel olmaması ehtimalı
    # Probability of having <= k dominant alleles in the g-th generation
    ans = sum(P[: k + 1])
    return ans


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_wfmd.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        line = f.read().strip()

    parts = line.split()
    N = int(parts[0])
    m = int(parts[1])
    g = int(parts[2])
    k = int(parts[3])

    ans = solve_wfmd(N, m, g, k)
    result = f"{ans:.3f}"
    print(result)

    with open(output_path, "w") as f:
        f.write(result + "\n")


if __name__ == "__main__":
    main()
