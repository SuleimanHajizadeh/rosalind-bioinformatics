# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba11d.txt")
    if not os.path.exists(input_file):
        return []
    with open(input_file, "r") as f:
        return list(map(int, f.read().split()))

# Kütlələrin amin turşularına qarşılığı (K/Q və I/L üçün hər hansı birini götürə bilərik)
# Reverse mass mapping (defaulting to G, A, S, etc.)
MASS_TABLE = {
    57: 'G', 71: 'A', 87: 'S', 97: 'P', 101: 'V', 103: 'C', 113: 'I',
    114: 'N', 115: 'D', 128: 'K', 129: 'E', 131: 'M', 137: 'H', 147: 'F',
    156: 'R', 163: 'Y', 186: 'W'
}

# Peptid vektorunu peptidə çeviririk
# Convert a Peptide Vector into a Peptide
def vector_to_peptide(vector):
    # 1 olan indeksləri (kütlə mövqelərini) tapırıq
    # Identify indices where vector has value 1
    positions = [i + 1 for i, val in enumerate(vector) if val == 1]
    
    # 0 başlanğıcından etibarən fərqləri amin turşusu kimi bərpa edirik
    # Restore amino acid characters based on differences
    curr = 0
    peptide = []
    for pos in positions:
        diff = pos - curr
        if diff in MASS_TABLE:
            peptide.append(MASS_TABLE[diff])
        curr = pos
    return "".join(peptide)

def main():
    vector = read_input()
    if not vector:
        return
    result = vector_to_peptide(vector)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(result + "\n")

if __name__ == "__main__":
    main()
