import os
from collections import Counter

def read_input(file_path):
    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    if len(lines) < 2:
        raise ValueError("Input file must contain at least two non-empty lines.")
    S1 = [float(x) for x in lines[0].split()]
    S2 = [float(x) for x in lines[1].split()]
    return S1, S2

def solve_spectral_convolution(S1, S2):
    diffs = []
    for s1 in S1:
        for s2 in S2:
            # Minkowski difference: s1 - s2
            # Rounding to 5 decimal places to handle floating-point precision issues
            diff = round(s1 - s2, 5)
            diffs.append(diff)
            
    counter = Counter(diffs)
    # Find the element(s) with the maximum multiplicity
    most_common = counter.most_common()
    
    if not most_common:
        return 0, 0.0
        
    best_x, max_mult = most_common[0]
    
    # We return the multiplicity and the absolute value of the shift value x
    return max_mult, abs(best_x)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_conv.txt")
    
    print(f"Reading input from: {input_path}")
    S1, S2 = read_input(input_path)
    print(f"Multiset S1 size: {len(S1)}")
    print(f"Multiset S2 size: {len(S2)}")
    
    max_mult, abs_x = solve_spectral_convolution(S1, S2)
    
    print(f"Result:")
    print(f"Max multiplicity: {max_mult}")
    print(f"Absolute shift value |x|: {abs_x:.5f}")
    
    output_path = os.path.join(script_dir, "output.txt")
    with open(output_path, "w") as out_file:
        out_file.write(f"{max_mult}\n")
        out_file.write(f"{abs_x:.5f}\n")
    print(f"Output written to: {output_path}")

if __name__ == "__main__":
    main()
