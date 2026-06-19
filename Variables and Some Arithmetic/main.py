import os
import sys

def main():
    input_path = "rosalind_ini2.txt"
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        sys.exit(1)
        
    with open(input_path, 'r') as f:
        line = f.read().strip()
        
    parts = line.split()
    if len(parts) < 2:
        print("Error: Input file must contain two numbers.")
        sys.exit(1)
        
    a = int(parts[0])
    b = int(parts[1])
    
    result = a**2 + b**2
    
    output_path = "output.txt"
    with open(output_path, "w") as out:
        out.write(f"{result}\n")
        
    print(f"Computed a^2 + b^2 = {result} for a={a}, b={b}.")
    print(f"Written to {output_path}")

if __name__ == '__main__':
    main()
