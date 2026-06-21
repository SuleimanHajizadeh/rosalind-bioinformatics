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

# Standard amin turşusu kütlələri cədvəli
# Standard amino acid masses and symbols mapping
MASS_TABLE = {
    57: 'G', 71: 'A', 87: 'S', 97: 'P', 99: 'V', 101: 'T', 103: 'C', 113: 'I', # or L
    114: 'N', 115: 'D', 128: 'K', # or Q
    129: 'E', 131: 'M', 137: 'H', 147: 'F', 156: 'R', 163: 'Y', 186: 'W'
}

CHAR_TO_MASS = {
    'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 'T': 101, 'C': 103, 'I': 113, 'L': 113,
    'N': 114, 'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131, 'H': 137, 'F': 147,
    'R': 156, 'Y': 163, 'W': 186
}

# Peptidin ideal spektrini tapırıq
# Compute the ideal spectrum of a peptide
def get_ideal_spectrum(peptide):
    p_masses = [0]
    curr = 0
    for aa in peptide:
        curr += CHAR_TO_MASS[aa]
        p_masses.append(curr)
        
    s_masses = [0]
    curr = 0
    for aa in reversed(peptide):
        curr += CHAR_TO_MASS[aa]
        s_masses.append(curr)
        
    return sorted(p_masses[:-1] + s_masses[1:])

# İdeal spektrdən peptidin bərpa edilməsi
# Implement DecodingIdealSpectrum (find peptide matching ideal spectrum)
def decoding_ideal_spectrum(spectrum):
    # Spektri 0 ilə birlikdə artan sıra ilə düzürük
    # Ensure 0 is in the set of nodes
    s = sorted(list(set([0] + spectrum)))
    n = len(s)
    target = max(s)
    
    # Qrafı qururuq
    # Build graph adjacency list
    adj = {node: [] for node in s}
    for i in range(n):
        for j in range(i + 1, n):
            diff = s[j] - s[i]
            if diff in MASS_TABLE:
                adj[s[i]].append((s[j], MASS_TABLE[diff]))
                
    # Yol axtarışı (DFS)
    # Search paths from 0 to target using DFS
    # Hər bir tam yol üçün ideal spektrini yoxlayırıq
    # For each complete path, verify if it explains the spectrum
    spec_with_zero = list(spectrum)
    if 0 not in spec_with_zero:
        spec_with_zero.append(0)
    sorted_spec = sorted(spec_with_zero)
    
    found_peptides = []
    
    def dfs(curr, path):
        # Əgər hədəfə çatdıqsa, spektri yoxlayırıq
        # If we reached the target, check if it explains the spectrum
        if curr == target:
            if get_ideal_spectrum(path) == sorted_spec:
                found_peptides.append(path)
            return
            
        for neighbor, aa in adj[curr]:
            # Buduqlamanı tətbiq edirik: target - neighbor mütləq spektrdə olmalıdır
            # Apply pruning: (target - neighbor) must be in the spectrum
            if (target - neighbor) in s:
                dfs(neighbor, path + aa)
                if found_peptides:
                    return
                    
    dfs(0, "")
    return found_peptides[0] if found_peptides else ""

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
