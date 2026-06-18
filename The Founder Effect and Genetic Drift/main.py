#!/usr/bin/env python3
import os
import math

def solve_foun(N, m, A):
    two_N = 2 * N
    
    # Precompute binomial coefficients
    comb = [math.comb(two_N, j) for j in range(two_N + 1)]
    
    # Transition matrix T of size (2N+1) x (2N+1)
    # T[j][i] is probability of transitioning from i copies to j copies
    T = [[0.0] * (two_N + 1) for _ in range(two_N + 1)]
    for i in range(two_N + 1):
        p = i / two_N
        for j in range(two_N + 1):
            if p == 0:
                T[j][i] = 1.0 if j == 0 else 0.0
            elif p == 1:
                T[j][i] = 1.0 if j == two_N else 0.0
            else:
                T[j][i] = comb[j] * (p ** j) * ((1.0 - p) ** (two_N - j))
                
    # We want to trace each A[k] separately
    results = []
    for k in range(len(A)):
        # Initial probability vector at gen 0
        v = [0.0] * (two_N + 1)
        v[A[k]] = 1.0
        
        col_res = []
        for gen in range(1, m + 1):
            # Multiply T by v: v_next[j] = sum_i T[j][i] * v[i]
            v_next = [0.0] * (two_N + 1)
            for j in range(two_N + 1):
                v_next[j] = sum(T[j][i] * v[i] for i in range(two_N + 1))
            v = v_next
            
            p_zero = v[0]
            if p_zero > 0:
                col_res.append(math.log10(p_zero))
            else:
                col_res.append(-float('inf'))
        results.append(col_res)
        
    # Transpose results to get m rows of k columns
    matrix = []
    for i in range(m):
        row = [results[j][i] for j in range(len(A))]
        matrix.append(row)
        
    return matrix

def main():
    input_path = "rosalind_foun.txt"
    output_path = "output.txt"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return
        
    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
        
    if len(lines) < 2:
        print("Error: Input file must contain at least two non-empty lines.")
        return
        
    # Parse N and m
    first_line_parts = lines[0].split()
    N = int(first_line_parts[0])
    m = int(first_line_parts[1])
    
    # Parse A
    A = [int(x) for x in lines[1].split()]
    
    print(f"N = {N}, m = {m}")
    print(f"A = {A}")
    
    matrix = solve_foun(N, m, A)
    
    with open(output_path, "w") as f:
        for row in matrix:
            # Output floating point numbers formatted cleanly
            row_str = " ".join(f"{val:.12f}" if val != -float('inf') else "-inf" for val in row)
            f.write(row_str + "\n")
            
    print(f"Results successfully written to {output_path}")

if __name__ == "__main__":
    main()
