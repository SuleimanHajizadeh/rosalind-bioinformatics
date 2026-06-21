# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba6a.txt")
    if not os.path.exists(input_file):
        return []
    with open(input_file, "r") as f:
        content = f.read().strip()
        # mötərizələri təmizləyirik (e.g. (+1 -2 +3))
        # remove parentheses
        content = content.replace("(", "").replace(")", "")
        return list(map(int, content.split()))

# Tərs çevirmə (reversal) əməliyyatını simvolu da dəyişərək tətbiq edirik
# Apply reversal operation to a subsegment, flipping signs
def reverse_segment(p, i, j):
    sub = p[i:j+1]
    sub.reverse()
    p[i:j+1] = [-x for x in sub]

# Permutasiyanı formatlayıb sətir kimi təqdim edirik
# Format permutation as string: e.g. (+1 -2 +3)
def format_permutation(p):
    items = []
    for x in p:
        if x > 0:
            items.append(f"+{x}")
        else:
            items.append(str(x))
    return "(" + " ".join(items) + ")"

# Greedy Sorting alqoritmi
# Implement GreedySorting to sort a permutation by reversals
def greedy_sorting(p):
    n = len(p)
    steps = []
    
    for i in range(n):
        target = i + 1
        # target mövqeyində artıq düzgün ədəd yoxdursa, onu axtarırıq
        # If target element is not at index i
        if p[i] != target:
            # tapırıq (ya müsbət ya da mənfi versiyasını)
            # Find index of target or -target
            j = i
            while j < n:
                if abs(p[j]) == target:
                    break
                j += 1
            # Seçilmiş seqmenti tərs çeviririk
            # Reverse segment
            reverse_segment(p, i, j)
            steps.append(format_permutation(p))
            
            # İşarə mənfi qalıbsa, onu müsbət etmək üçün təkrardan i-ci elementi tək çeviririk
            # If sign is negative, flip the sign
            if p[i] == -target:
                p[i] = target
                steps.append(format_permutation(p))
    return steps

def main():
    p = read_input()
    if not p:
        return
    result = greedy_sorting(p)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write("\n".join(result) + "\n")

if __name__ == "__main__":
    main()
