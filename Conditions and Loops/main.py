import os
import sys

def main():
    input_path = "rosalind_ini4.txt"
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
    
    total = sum(i for i in range(a, b + 1) if i % 2 != 0)
    
    output_path = "output.txt"
    with open(output_path, "w") as out:
        out.write(f"{total}\n")
        
    print(f"Sum of odd integers from {a} to {b} is: {total}")
    print(f"Written to {output_path}")

if __name__ == '__main__':
    main()
