import os
import sys

def solve_cunr(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} not found.")
        return
        
    with open(input_path, 'r') as f:
        content = f.read().strip()
        
    if not content:
        print("Error: Empty input file.")
        return
        
    try:
        n = int(content)
    except ValueError:
        print(f"Error: Invalid integer n: '{content}'")
        return
        
    print(f"Number of leaves n: {n}")
    
    if n <= 2:
        ans = 1
    else:
        ans = 1
        # (2n - 5)!!
        # Product of all odd numbers up to 2n - 5
        for i in range(1, 2 * n - 4, 2):
            ans = (ans * i) % 1000000
            
    print(f"Total unrooted binary trees modulo 1,000,000: {ans}")
    
    with open(output_path, 'w') as f:
        f.write(str(ans) + '\n')
        
    print(f"Result written to {output_path}")

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_cunr.txt")
    output_file = os.path.join(script_dir, "output.txt")
    solve_cunr(input_file, output_file)
