# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba1d.txt")
    if not os.path.exists(input_file):
        return "", ""
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0], lines[1]

# Pattern-in mətndəki bütün başlanğıc indekslərini tapırıq
# Find all starting positions where Pattern appears as a substring of Genome
def find_occurrences(pattern, genome):
    positions = []
    k = len(pattern)
    for i in range(len(genome) - k + 1):
        if genome[i:i+k] == pattern:
            positions.append(i)
    return positions

def main():
    pattern, genome = read_input()
    if not pattern:
        return
    result = find_occurrences(pattern, genome)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(map(str, result)) + "\n")

if __name__ == "__main__":
    main()
