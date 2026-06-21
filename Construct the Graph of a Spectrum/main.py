# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba11a.txt")
    if not os.path.exists(input_file):
        return []
    with open(input_file, "r") as f:
        return list(map(int, f.read().split()))

# Standard amin turşusu kütlələri cədvəli
# Standard amino acid masses and symbols mapping
MASS_TABLE = {
    57: 'G', 71: 'A', 87: 'S', 97: 'P', 99: 'V', 101: 'T', 103: 'C', 113: 'I', # or L
    114: 'N', 115: 'D', 128: 'K', # or Q
    129: 'E', 131: 'M', 137: 'H', 147: 'F', 156: 'R', 163: 'Y', 186: 'W'
}

# Spektr qrafını (Spectrum Graph) qururuq
# Construct the Graph of a Spectrum
def construct_spectrum_graph(spectrum):
    # Spektri 0 ilə birlikdə artan sıra ilə düzürük
    # Ensure 0 is included and spectrum is sorted
    s = sorted(list(set([0] + spectrum)))
    n = len(s)
    
    adj = []
    for i in range(n):
        for j in range(i + 1, n):
            diff = s[j] - s[i]
            # Əgər kütlə fərqi hər hansı standart amin turşusunun kütləsinə bərabərdirsə
            # If the mass difference equals a standard amino acid mass
            if diff in MASS_TABLE:
                adj.append(f"{s[i]}->{s[j]}:{MASS_TABLE[diff]}")
    return adj

def main():
    spectrum = read_input()
    if not spectrum:
        return
    result = construct_spectrum_graph(spectrum)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(result) + "\n")

if __name__ == "__main__":
    main()
