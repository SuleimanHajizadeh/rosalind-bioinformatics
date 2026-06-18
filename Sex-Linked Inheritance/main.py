#!/usr/bin/env python3
import os

def solve_sexl(A):
    B = []
    for q in A:
        p = 1.0 - q
        carrier = 2.0 * p * q
        # Round to 3 decimal places to match sample format
        B.append(round(carrier, 3))
    return B

def main():
    input_path = "rosalind_sexl.txt"
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
    A = [float(p) for p in parts]
    print(f"Read {len(A)} probabilities from input.")
    
    B = solve_sexl(A)
    
    output_str = " ".join(str(b) for b in B)
    print("Computed carrier probabilities:", output_str)
    
    with open(output_path, 'w') as f:
        f.write(output_str + "\n")
    print(f"Result written to {output_path}")

if __name__ == "__main__":
    main()
