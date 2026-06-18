#!/usr/bin/env python3
import os

def calculate_nxx(lengths, total_len, xx):
    threshold = total_len * (xx / 100.0)
    current_sum = 0
    for length in lengths:
        current_sum += length
        if current_sum >= threshold:
            return length
    return 0

def main():
    input_path = "rosalind_asmq.txt"
    output_path = "output.txt"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return
        
    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
        
    lengths = sorted([len(s) for s in lines], reverse=True)
    total_len = sum(lengths)
    
    n50 = calculate_nxx(lengths, total_len, 50)
    n75 = calculate_nxx(lengths, total_len, 75)
    
    print(f"Total sequences: {len(lengths)}")
    print(f"Total length: {total_len}")
    print(f"N50: {n50}")
    print(f"N75: {n75}")
    
    with open(output_path, "w") as f:
        f.write(f"{n50} {n75}\n")
        
    print(f"Results written to {output_path}")

if __name__ == "__main__":
    main()
