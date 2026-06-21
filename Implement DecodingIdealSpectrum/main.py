# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba11b.txt")
    if not os.path.exists(input_file):
        return []
    with open(input_file, "r") as f:
        return list(map(int, f.read().split()))

MASS_TABLE = {
    57: 'G', 71: 'A', 87: 'S', 97: 'P', 101: 'V', 103: 'C', 113: 'I', # or L
    114: 'N', 115: 'D', 128: 'K', # or Q
    129: 'E', 131: 'M', 137: 'H', 147: 'F', 156: 'R', 163: 'Y', 186: 'W'
}

# İdeal spektrdən peptidin bərpa edilməsi
# Implement DecodingIdealSpectrum (find peptide matching ideal spectrum)
def decoding_ideal_spectrum(spectrum):
    s = sorted(list(set([0] + spectrum)))
    n = len(s)
    
    # Qrafı qururuq
    # Build graph adjacency list
    adj = {node: [] for node in s}
    for i in range(n):
        for j in range(i + 1, n):
            diff = s[j] - s[i]
            if diff in MASS_TABLE:
                adj[s[i]].append((s[j], MASS_TABLE[diff]))
                
    # 0-dan max_mass-a qədər yolları axtarırıq (DFS)
    # Search paths from 0 to max_mass using DFS
    target = max(s)
    paths = []
    
    def dfs(curr, path):
        if curr == target:
            paths.append(path)
            return
        for neighbor, aa in adj[curr]:
            dfs(neighbor, path + aa)
            
    dfs(0, "")
    # Ən uyğun olan ilk yolu qaytarırıq (idealı tapırıq)
    # Return first successful peptide string
    return paths[0] if paths else ""

def main():
    spectrum = read_input()
    if not spectrum:
        return
    result = decoding_ideal_spectrum(spectrum)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(result + "\n")

if __name__ == "__main__":
    main()
