# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba9l.txt")
    if not os.path.exists(input_file):
        return "", []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    bwt = lines[0]
    patterns = lines[1].split()
    return bwt, patterns

# BWMatching alqoritmi
# Implement BWMatching
def bw_matching(bwt, pattern):
    first_col = sorted(list(bwt))
    
    # First and Last column occurrences structures
    # Occurrences indices setup
    indexed_bwt = []
    counts = {}
    for char in bwt:
        counts[char] = counts.get(char, 0) + 1
        indexed_bwt.append((char, counts[char]))
        
    first_col_indexed = sorted(indexed_bwt, key=lambda x: x[0])
    
    # Last-to-First mapping lookup dict
    lookup = {item: idx for idx, item in enumerate(first_col_indexed)}
    mapping = {idx: lookup[item] for idx, item in enumerate(indexed_bwt)}
    
    top = 0
    bottom = len(bwt) - 1
    
    curr_pattern = list(pattern)
    while top <= bottom:
        if curr_pattern:
            symbol = curr_pattern.pop()
            
            # top və bottom arasında symbol-un olub olmadığını yoxlayırıq
            # Check if symbol occurs in BWT in range [top, bottom]
            found = False
            top_idx = -1
            bottom_idx = -1
            
            for idx in range(top, bottom + 1):
                if bwt[idx] == symbol:
                    if not found:
                        top_idx = idx
                        found = True
                    bottom_idx = idx
                    
            if found:
                top = mapping[top_idx]
                bottom = mapping[bottom_idx]
            else:
                return 0
        else:
            return bottom - top + 1
    return 0

def main():
    bwt, patterns = read_input()
    if not bwt:
        return
    results = [bw_matching(bwt, p) for p in patterns]
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(map(str, results)) + "\n")

if __name__ == "__main__":
    main()
