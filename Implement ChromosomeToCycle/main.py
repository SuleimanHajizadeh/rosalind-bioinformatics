# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba6f.txt")
    if not os.path.exists(input_file):
        return []
    with open(input_file, "r") as f:
        content = f.read().strip()
        content = content.replace("(", "").replace(")", "")
        return list(map(int, content.split()))

# Xromosom ardıcıllığını qraf dövrü (cycle) şəklində təqdim edirik
# Implement ChromosomeToCycle
def chromosome_to_cycle(chrom):
    nodes = []
    for val in chrom:
        if val > 0:
            nodes.extend([2*val - 1, 2*val])
        else:
            nodes.extend([-2*val, -2*val - 1])
    return nodes

def main():
    chrom = read_input()
    if not chrom:
        return
    result = chromosome_to_cycle(chrom)
    
    # Nəticəni formatlayırıq (mötərizədə boşluqla ayrılmış ədədlər)
    # Format the cycle output: (1 2 3 4)
    out_str = "(" + " ".join(map(str, result)) + ")"
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(out_str + "\n")

if __name__ == "__main__":
    main()
