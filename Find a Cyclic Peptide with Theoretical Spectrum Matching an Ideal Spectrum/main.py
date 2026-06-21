# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba4e.txt")
    if not os.path.exists(input_file):
        return []
    with open(input_file, "r") as f:
        return list(map(int, f.read().split()))

# 18 unikal amin turşusu kütləsi (L və I, K və Q kütlələri eyni olduğu üçün cəmi 18 unikal kütlə var)
# 18 unique amino acid masses
MASSES = [57, 71, 87, 97, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]

# Xətti peptidin spektrini tapırıq
# Generate linear spectrum of a peptide
def linear_spectrum(peptide):
    n = len(peptide)
    prefix_mass = [0] * (n + 1)
    for i in range(n):
        prefix_mass[i+1] = prefix_mass[i] + peptide[i]
    spectrum = [0]
    for length in range(1, n + 1):
        for start in range(n - length + 1):
            spectrum.append(prefix_mass[start+length] - prefix_mass[start])
    spectrum.sort()
    return spectrum

# Spektrin tutarlılığını yoxlayırıq
# Check if a linear spectrum is consistent with the ideal spectrum
def is_consistent(peptide, ideal_spectrum):
    spec = linear_spectrum(peptide)
    temp = list(ideal_spectrum)
    for val in spec:
        if val not in temp:
            return False
        temp.remove(val)
    return True

def cyclic_spectrum(peptide):
    n = len(peptide)
    prefix_mass = [0] * (n + 1)
    for i in range(n):
        prefix_mass[i+1] = prefix_mass[i] + peptide[i]
    total_mass = prefix_mass[n]
    spectrum = [0, total_mass]
    for length in range(1, n):
        for start in range(n):
            if start + length <= n:
                spectrum.append(prefix_mass[start+length] - prefix_mass[start])
            else:
                spectrum.append(total_mass - (prefix_mass[start] - prefix_mass[start + length - n]))
    spectrum.sort()
    return spectrum

# Cyclopeptide Sequencing alqoritmini tətbiq edirik
# Implement CyclopeptideSequencing
def cyclopeptide_sequencing(ideal_spectrum):
    parent_mass = max(ideal_spectrum)
    candidate_peptides = [[]]
    final_peptides = []
    
    while candidate_peptides:
        # Hər bir namizəd peptidə yeni kütlələr əlavə edirik (expand)
        # Expand candidates
        next_candidates = []
        for p in candidate_peptides:
            for m in MASSES:
                next_candidates.append(p + [m])
                
        candidate_peptides = []
        for p in next_candidates:
            p_mass = sum(p)
            if p_mass == parent_mass:
                if cyclic_spectrum(p) == ideal_spectrum:
                    final_peptides.append(p)
            elif p_mass < parent_mass:
                if is_consistent(p, ideal_spectrum):
                    candidate_peptides.append(p)
                    
    # Peptidləri formatlayırıq (tire ilə kütlələr şəklində)
    # Format peptides as string
    results = []
    for p in final_peptides:
        results.append("-".join(map(str, p)))
    return list(set(results))

def main():
    ideal_spectrum = read_input()
    if not ideal_spectrum:
        return
    result = cyclopeptide_sequencing(ideal_spectrum)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(result) + "\n")

if __name__ == "__main__":
    main()
