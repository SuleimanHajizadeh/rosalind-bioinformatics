#!/usr/bin/env python3
import os

def main():
    input_path = "rosalind_ebin.txt"
    output_path = "output.txt"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return
        
    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
        
    if len(lines) < 2:
        print("Error: Input file must contain at least two non-empty lines.")
        return
        
    n = int(lines[0])
    p_values = [float(x) for x in lines[1].split()]
    
    print(f"n = {n}")
    print(f"P-values: {p_values}")
    
    expected_values = [n * p for p in p_values]
    
    # Format floats: we can use a standard format or convert to string.
    # The sample shows 1.7 3.4 5.1, so simple space separation of floats is fine.
    output_str = " ".join(f"{val:.3f}" if int(val) != val else f"{int(val)}" for val in expected_values)
    # Actually, let's just write them as standard floats or formatted to a reasonable precision,
    # or just convert to string since python's str() handles floats well (e.g. 1.7, 3.4).
    # Wait, the sample dataset output was "1.7 3.4 5.1", and not "1.700 3.400 5.100".
    # Let's just use a clean float representation or standard format.
    # Let's format to something like 3 or 4 decimal places if it's not an integer,
    # or just use str(x) or round.
    # Let's see: `0.0702814659019 * 986448 = 69326.66113645396`
    # Let's format to 3 decimal places for non-integers, or just print with a high precision or str.
    # Wait, Rosalind usually accepts float outputs with standard format or up to 3-4 decimal places.
    # Let's use `"{:.3f}".format(val)` or similar, but drop trailing zeros, or just use `"{:.3f}"` or even standard `str()`.
    # Let's check other solved problems in the repo for how floats were handled.
    # Usually, simple float representation or `round(val, 3)` works.
    # Let's use `round(val, 3)` or standard formatting.
    # Let's just output space-separated float strings with a clean representation.
    
    formatted_vals = []
    for val in expected_values:
        # If it has a fractional part, format to 3 decimal places (or just standard float if it fits)
        # To match the sample 1.7, we can just use round(val, 3) or format to 3 decimal places.
        formatted_vals.append(str(round(val, 3)))
        
    output_str = " ".join(formatted_vals)
    print(f"Expected: {output_str}")
    
    with open(output_path, "w") as f:
        f.write(output_str + "\n")
        
    print(f"Results written to {output_path}")

if __name__ == "__main__":
    main()
