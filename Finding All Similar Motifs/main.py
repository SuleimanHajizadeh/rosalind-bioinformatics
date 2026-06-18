import os

def ksim_dict(k, s, t):
    m = len(s)
    n = len(t)
    
    # prev_row[j] stores {start_pos: distance}
    prev_row = [None] * (n + 1)
    for j in range(n + 1):
        prev_row[j] = {j: 0}
        
    results = []
    
    for i in range(1, m + 1):
        curr_row = [None] * (n + 1)
        if i <= k:
            curr_row[0] = {0: i}
            
        for j in range(1, n + 1):
            d1 = prev_row[j-1] # diagonal
            d2 = prev_row[j]   # up
            d3 = curr_row[j-1] # left
            
            if d1 is None and d2 is None and d3 is None:
                continue
                
            cell = {}
            
            # Diagonal: match/mismatch
            if d1 is not None:
                char_match = (s[i-1] == t[j-1])
                cost = 0 if char_match else 1
                for start, dist in d1.items():
                    nd = dist + cost
                    if nd <= k:
                        cell[start] = nd
                        
            # Up: deletion (gap in t)
            if d2 is not None:
                for start, dist in d2.items():
                    nd = dist + 1
                    if nd <= k:
                        if start not in cell or nd < cell[start]:
                            cell[start] = nd
                            
            # Left: insertion (gap in s)
            if d3 is not None:
                for start, dist in d3.items():
                    nd = dist + 1
                    if nd <= k:
                        if start not in cell or nd < cell[start]:
                            cell[start] = nd
                            
            if cell:
                curr_row[j] = cell
                
        prev_row = curr_row
        
    # Collect results from the last row
    for j in range(1, n + 1):
        if prev_row[j] is not None:
            for start, dist in prev_row[j].items():
                if dist <= k:
                    length = j - start
                    if length > 0:
                        results.append((start + 1, length))
                        
    return sorted(results)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, "rosalind_ksim.txt")
    output_path = os.path.join(script_dir, "output.txt")
    
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found.")
        return
        
    with open(input_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
        
    if len(lines) < 3:
        print("Error: Input file must contain at least 3 non-empty lines (k, motif, genome).")
        return
        
    try:
        k = int(lines[0])
    except ValueError:
        print(f"Error: Invalid k value on the first line: {lines[0]}")
        return
        
    s = lines[1].upper()
    t = lines[2].upper()
    
    print(f"Solving KSIM with k={k}, motif length={len(s)}, genome length={len(t)}...")
    results = ksim_dict(k, s, t)
    
    with open(output_path, "w") as f:
        for start, length in results:
            f.write(f"{start} {length}\n")
            
    print(f"Successfully wrote {len(results)} matches to '{output_path}'.")

if __name__ == "__main__":
    main()