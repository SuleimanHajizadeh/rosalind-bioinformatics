# Giriş verilənlərini oxumaq
# Read input data
def read_input():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, "rosalind_ba9h.txt")
    if not os.path.exists(input_file):
        return "", []
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines[0], lines[1:]

def construct_suffix_array(text):
    suffixes = []
    for i in range(len(text)):
        suffixes.append((text[i:], i))
    suffixes.sort(key=lambda x: x[0])
    return [idx for suf, idx in suffixes]

# Suffix Array-dən istifadə edərək ikili axtarış (binary search) ilə naxışları (patterns) axtarırıq
# Pattern Matching with the Suffix Array using binary search
def pattern_matching_suffix_array(text, patterns):
    sa = construct_suffix_array(text)
    n = len(text)
    matching_positions = []
    
    for pattern in patterns:
        k = len(pattern)
        # İkili axtarışla sol sərhədi tapırıq
        # Binary search for left boundary
        low, high = 0, n - 1
        start_idx = -1
        while low <= high:
            mid = (low + high) // 2
            suffix = text[sa[mid]:sa[mid]+k]
            if suffix >= pattern:
                if suffix == pattern:
                    start_idx = mid
                high = mid - 1
            else:
                low = mid + 1
                
        if start_idx == -1:
            continue
            
        # Sağ sərhədi tapırıq
        # Binary search for right boundary
        low, high = 0, n - 1
        end_idx = -1
        while low <= high:
            mid = (low + high) // 2
            suffix = text[sa[mid]:sa[mid]+k]
            if suffix <= pattern:
                if suffix == pattern:
                    end_idx = mid
                low = mid + 1
            else:
                high = mid - 1
                
        # Bütün tapılan mövqeləri əlavə edirik
        # Collect positions from suffix array range
        for idx in range(start_idx, end_idx + 1):
            matching_positions.append(sa[idx])
            
    matching_positions = sorted(list(set(matching_positions)))
    return matching_positions

def main():
    text, patterns = read_input()
    if not text:
        return
    result = pattern_matching_suffix_array(text, patterns)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "output.txt"), "w") as f:
        f.write(" ".join(map(str, result)) + "\n")

if __name__ == "__main__":
    main()
