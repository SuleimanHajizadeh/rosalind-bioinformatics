#!/usr/bin/env python3
import os
import math

def nCr(n, r):
    return math.comb(n, r)

def solve_wfmd(N, m, g, k):
    num_alleles = 2 * N
    
    # P[i] is the probability of having i dominant alleles
    P = [0.0] * (num_alleles + 1)
    P[m] = 1.0
    
    # Transition matrix T
    # T[i][j] is transition from i dominant alleles to j dominant alleles
    T = [[0.0] * (num_alleles + 1) for _ in range(num_alleles + 1)]
    for i in range(num_alleles + 1):
        p = i / num_alleles
        for j in range(num_alleles + 1):
            T[i][j] = nCr(num_alleles, j) * (p ** j) * ((1.0 - p) ** (num_alleles - j))
            
    # Evolve for g generations
    for _ in range(g):
        next_P = [0.0] * (num_alleles + 1)
        for j in range(num_alleles + 1):
            for i in range(num_alleles + 1):
                next_P[j] += P[i] * T[i][j]
        P = next_P
        
    # We want at least k recessive alleles, which means at most (2N - k) dominant alleles
    max_dom = num_alleles - k
    ans = sum(P[j] for j in range(max_dom + 1))
    return round(ans, 3)

def main():
    input_path = "rosalind_wfmd.txt"
    output_path = "output.txt"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return
        
    with open(input_path, 'r') as f:
        content = f.read().strip()
        
    if not content:
        print("Error: Input file is empty.")
        return
        
    parts = content.split()
    N = int(parts[0])
    m = int(parts[1])
    g = int(parts[2])
    k = int(parts[3])
    
    print(f"Parameters N={N}, m={m}, g={g}, k={k}")
    
    prob = solve_wfmd(N, m, g, k)
    print(f"Computed probability: {prob}")
    
    with open(output_path, 'w') as f:
        f.write(str(prob) + "\n")
    print(f"Result written to {output_path}")

if __name__ == "__main__":
    main()
