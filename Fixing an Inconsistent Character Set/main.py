#!/usr/bin/env python3
import os

def is_compatible(c1, c2, n):
    # Check if two character splits (represented as sets of 1-indices) are compatible
    if not (c1 & c2):
        return True
    if c1.issubset(c2):
        return True
    if c2.issubset(c1):
        return True
    if len(c1 | c2) == n:
        return True
    return False

def check_consistency(char_sets, n):
    num = len(char_sets)
    for i in range(num):
        for j in range(i + 1, num):
            if not is_compatible(char_sets[i], char_sets[j], n):
                return False, i, j
    return True, -1, -1

def main():
    input_path = "rosalind_cset.txt"
    output_path = "output.txt"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return
        
    with open(input_path, "r") as f:
        rows = [line.strip() for line in f if line.strip()]
        
    if not rows:
        print("Error: Empty character table.")
        return
        
    n = len(rows[0])
    num_rows = len(rows)
    print(f"Read {num_rows} characters on {n} taxa.")
    
    # Represent each character as a set of indices where the state is '1'
    char_sets = []
    for row in rows:
        c_set = {i for i, val in enumerate(row) if val == '1'}
        char_sets.append(c_set)
        
    deleted_row_idx = -1
    for r in range(num_rows):
        sub_sets = [char_sets[i] for i in range(num_rows) if i != r]
        consistent, _, _ = check_consistency(sub_sets, n)
        if consistent:
            deleted_row_idx = r
            break
            
    if deleted_row_idx != -1:
        print(f"Found row to delete: index {deleted_row_idx} (content: {rows[deleted_row_idx]})")
        output_rows = [rows[i] for i in range(num_rows) if i != deleted_row_idx]
        with open(output_path, "w") as f:
            for row in output_rows:
                f.write(row + "\n")
        print(f"Output successfully written to {output_path}")
    else:
        print("Error: No single row deletion makes the table consistent.")

if __name__ == "__main__":
    main()
