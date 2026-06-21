# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba6g.txt")
    if not os.path.exists(input_file):
        return []
    with open(input_file, "r") as f:
        content = f.read().strip()
        content = content.replace("(", "").replace(")", "")
        return list(map(int, content.split()))

# Qraf dövrünü xromosom ardıcıllığına çeviririk
# Implement CycleToChromosome
def cycle_to_chromosome(nodes):
    chrom = []
    for i in range(0, len(nodes), 2):
        u, v = nodes[i], nodes[i+1]
        if u < v:
            chrom.append(v // 2)
        else:
            chrom.append(-u // 2)
    return chrom

def main():
    nodes = read_input()
    if not nodes:
        return
    result = cycle_to_chromosome(nodes)
    
    # İşarələri formatlayırıq
    # Format chromosome representation with signs
    out_str = "(" + " ".join(f"+{x}" if x > 0 else str(x) for x in result) + ")"
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(out_str + "\n")

if __name__ == "__main__":
    main()
