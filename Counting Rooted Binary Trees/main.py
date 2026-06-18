#!/usr/bin/env python3
import os

def solve_root(n):
    if n < 2:
        return 1
    ans = 1
    for i in range(3, 2 * n - 1, 2):
        ans = (ans * i) % 1000000
    return ans

def main():
    input_path = "rosalind_root.txt"
    output_path = "output.txt"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return
        
    with open(input_path, 'r') as f:
        content = f.read().strip()
        
    if not content:
        print("Error: Input file is empty.")
        return
        
    n = int(content)
    print(f"Leaf count n: {n}")
    
    result = solve_root(n)
    print(f"Result (modulo 1,000,000): {result}")
    
    with open(output_path, 'w') as f:
        f.write(str(result) + "\n")
    print(f"Result written to {output_path}")

if __name__ == "__main__":
    main()
