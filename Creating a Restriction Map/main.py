#!/usr/bin/env python3
import os
import math
from collections import Counter

def solve(L_list):
    counter = Counter(L_list)
    unique_sorted = sorted(counter.keys())
    
    num_diffs = len(L_list)
    n = int((1 + math.sqrt(1 + 8 * num_diffs)) / 2)
    
    M = unique_sorted[-1]
    X = {0, M}
    counter[M] -= 1
    
    def can_place(y, X, counter):
        needed = Counter()
        for x in X:
            diff = abs(y - x)
            needed[diff] += 1
            if counter[diff] < needed[diff]:
                return False
        return True

    def place_point(y, X, counter):
        for x in X:
            diff = abs(y - x)
            counter[diff] -= 1
        X.add(y)

    def remove_point(y, X, counter):
        X.remove(y)
        for x in X:
            diff = abs(y - x)
            counter[diff] += 1

    def backtrack(max_idx, X, counter):
        while max_idx >= 0 and counter[unique_sorted[max_idx]] == 0:
            max_idx -= 1
            
        if max_idx < 0:
            return sorted(list(X))
            
        y = unique_sorted[max_idx]
        
        # Option 1: place at y
        if can_place(y, X, counter):
            place_point(y, X, counter)
            res = backtrack(max_idx, X, counter)
            if res is not None:
                return res
            remove_point(y, X, counter)
            
        # Option 2: place at M - y
        alt_y = M - y
        if can_place(alt_y, X, counter):
            place_point(alt_y, X, counter)
            res = backtrack(max_idx, X, counter)
            if res is not None:
                return res
            remove_point(alt_y, X, counter)
            
        return None

    return backtrack(len(unique_sorted) - 1, X, counter)

def main():
    input_path = "rosalind_pdpl.txt"
    output_path = "output.txt"
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return
        
    with open(input_path, 'r') as f:
        # Split on spaces and newlines
        parts = f.read().strip().split()
        
    if not parts:
        print("Error: Input file is empty.")
        return
        
    L_list = [int(p) for p in parts]
    print(f"Read {len(L_list)} differences from input file.")
    
    X = solve(L_list)
    if X is None:
        print("Error: No solution found!")
        return
        
    print(f"Found solution X of size {len(X)}")
    
    output_str = " ".join(str(x) for x in X)
    with open(output_path, 'w') as f:
        f.write(output_str + "\n")
    print(f"Results written to {output_path}")

if __name__ == "__main__":
    main()
