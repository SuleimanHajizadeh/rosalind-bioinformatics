# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba11e.txt")
    if not os.path.exists(input_file):
        return []
    with open(input_file, "r") as f:
        return list(map(int, f.read().split()))

MASS_TABLE = {
    57: 'G', 71: 'A', 87: 'S', 97: 'P', 99: 'V', 101: 'T', 103: 'C', 113: 'I',
    114: 'N', 115: 'D', 128: 'K', 129: 'E', 131: 'M', 137: 'H', 147: 'F',
    156: 'R', 163: 'Y', 186: 'W'
}

# Spektrə əsasən ən yüksək xallı peptidi tapırıq (Peptid ardıcıllığının müəyyən edilməsi)
# Sequence a Peptide by finding a path in the spectrum graph that maximizes total weight/score
def sequence_peptide(spectrum_vector):
    n = len(spectrum_vector)
    # DP və geriyə izləmə massivlərini təyin edirik
    # DP arrays to track max scores and backtrack pointers
    dp = [-float('inf')] * (n + 1)
    dp[0] = 0
    backtrack = [None] * (n + 1)
    
    for i in range(1, n + 1):
        # Hər bir standart kütlə keçidi üçün xalı hesablayırıq
        # Calculate transition scores for each amino acid mass
        for mass in MASS_TABLE:
            if i - mass >= 0:
                score = dp[i - mass] + spectrum_vector[i - 1]
                if score > dp[i]:
                    dp[i] = score
                    backtrack[i] = i - mass
                    
    # Geriyə izləmə vasitəsilə ən yaxşı yolu bərpa edirik
    # Backtrack path
    path = []
    curr = n
    while curr > 0:
        prev = backtrack[curr]
        if prev is None:
            break
        path.append(curr - prev)
        curr = prev
    path.reverse()
    
    # Kütlələri amin turşularına çeviririk
    # Convert masses to amino acid symbols
    peptide = "".join(MASS_TABLE[mass] for mass in path)
    return peptide

def main():
    spectrum_vector = read_input()
    if not spectrum_vector:
        return
    result = sequence_peptide(spectrum_vector)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(result + "\n")

if __name__ == "__main__":
    main()
