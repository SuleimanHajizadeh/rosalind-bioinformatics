#!/usr/bin/env python3
import os
import math

# Müstəqil segregasiyaya əsasən ən azı k xromosomun dominant getməsi ehtimalını tapırıq
# Compute the probability of having at least k dominant alleles during independent segregation


def solve_ind(n):
    # Xromosomların ümumi sayı: 2n
    # Total number of chromosomes is 2n
    total = 2 * n
    results = []

    # k = 1-dən 2n-ə qədər ehtimalları hesablayırıq
    # Calculate probabilities for k from 1 to 2n
    for k in range(1, total + 1):
        # 1 - (k-dan az dominant olması ehtimalı)
        # Probability(at least k) = 1 - sum(C(2n, i) * 0.5^(2n) for i in range(k))
        prob_less_than_k = 0.0
        for i in range(k):
            prob_less_than_k += math.comb(total, i) * (0.5**total)
        prob_at_least_k = 1.0 - prob_less_than_k
        results.append(f"{math.log10(prob_at_least_k):.3f}")

    return " ".join(results)


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_indz.txt")
    output_path = os.path.join(script_dir, "output.txt")

    if not os.path.exists(input_path):
        print(f"Xəta: {input_path} tapılmadı.")
        return

    with open(input_path, "r") as f:
        n = int(f.read().strip())

    result = solve_ind(n)
    print(result)

    with open(output_path, "w") as f:
        f.write(result + "\n")


if __name__ == "__main__":
    main()
