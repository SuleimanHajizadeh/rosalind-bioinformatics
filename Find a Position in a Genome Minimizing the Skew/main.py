# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba1f.txt")
    if not os.path.exists(input_file):
        return ""
    with open(input_file, "r") as f:
        return f.read().strip()

# Genomda skew (C və G fərqi) dəyərini minimum edən mövqeləri tapırıq
# Find a position in a genome minimizing the skew
def minimize_skew(genome):
    skew = 0
    min_skew = 0
    positions = []
    
    # Skew massivini qururuq
    # Construct the skew array
    for i, base in enumerate(genome):
        if base == 'C':
            skew -= 1
        elif base == 'G':
            skew += 1
        
        if skew < min_skew:
            min_skew = skew
            positions = [i + 1]
        elif skew == min_skew:
            positions.append(i + 1)
            
    return positions

def main():
    genome = read_input()
    if not genome:
        return
    result = minimize_skew(genome)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(map(str, result)) + "\n")

if __name__ == "__main__":
    main()
