import os
import sys

def main():
    input_path = "rosalind_ini3.txt"
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        sys.exit(1)
        
    with open(input_path, 'r') as f:
        lines = f.readlines()
        
    if len(lines) < 2:
        print("Error: Input file must contain at least two lines.")
        sys.exit(1)
        
    s = lines[0].strip()
    nums = list(map(int, lines[1].strip().split()))
    if len(nums) < 4:
        print("Error: Line 2 must contain four integers.")
        sys.exit(1)
        
    a, b, c, d = nums
    
    # Slice inclusively
    slice1 = s[a : b + 1]
    slice2 = s[c : d + 1]
    
    result = f"{slice1} {slice2}"
    
    output_path = "output.txt"
    with open(output_path, "w") as out:
        out.write(result + "\n")
        
    print(f"Processed slices: '{slice1}' and '{slice2}'.")
    print(f"Written to {output_path}")

if __name__ == '__main__':
    main()
