# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba9j.txt")
    if not os.path.exists(input_file):
        return ""
    with open(input_file, "r") as f:
        return f.read().strip()

# BWT-dən sətiri bərpa edirik (Last-to-First mapping ilə)
# Reconstruct a string from its Burrows-Wheeler Transform
def reconstruct_bwt(bwt):
    # Simvolların indeksləri ilə sayını tapırıq
    # Build count arrays for First/Last column tracking
    indexed_bwt = []
    counts = {}
    for char in bwt:
        counts[char] = counts.get(char, 0) + 1
        indexed_bwt.append((char, counts[char]))
        
    first_col = sorted(indexed_bwt, key=lambda x: x[0])
    
    # Last-to-First xəritəsini qururuq
    # Map index in Last column to index in First column
    mapping = {}
    for idx, item in enumerate(indexed_bwt):
        # first_col-da həmin cütü tapırıq
        # Locate corresponding pair in first_col
        # Sürətli olması üçün lookup istifadə edilə bilər
        pass
        
    # Lookup üçün cəld lüğət quraq
    # Lookup dict
    lookup = {item: idx for idx, item in enumerate(first_col)}
    mapping = {idx: lookup[item] for idx, item in enumerate(indexed_bwt)}
    
    # $ işarəsindən başlayaraq geriyə doğru sətiri bərpa edirik
    # Trace backward starting from the terminal character '$'
    curr = bwt.index('$')
    chars = []
    for _ in range(len(bwt)):
        chars.append(indexed_bwt[curr][0])
        curr = mapping[curr]
        
    chars.reverse()
    return "".join(chars)

def main():
    bwt = read_input()
    if not bwt:
        return
    result = reconstruct_bwt(bwt)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(result + "\n")

if __name__ == "__main__":
    main()
